#!/usr/bin/env python3
"""Transcribe audio to word-level timestamps."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def format_timestamp(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, rem = divmod(ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1_000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def build_markdown(segments: list[dict]) -> str:
    lines = ["# Transcript", "", "| 开始 | 结束 | 字幕 |", "|---|---|---|"]
    for seg in segments:
        lines.append(f"| {seg['start']:.2f} | {seg['end']:.2f} | {seg['text'].strip()} |")
    return "\n".join(lines) + "\n"


def build_srt(segments: list[dict]) -> str:
    blocks = []
    for i, seg in enumerate(segments, 1):
        blocks.append(
            f"{i}\n{format_timestamp(seg['start'])} --> {format_timestamp(seg['end'])}\n"
            f"{seg['text'].strip()}\n"
        )
    return "\n".join(blocks)


def serialize_segments(raw_segments) -> list[dict]:
    out = []
    for seg in raw_segments:
        out.append(
            {
                "start": round(seg.start, 3),
                "end": round(seg.end, 3),
                "text": seg.text.strip(),
                "words": [
                    {
                        "start": round(w.start, 3),
                        "end": round(w.end, 3),
                        "word": w.word,
                        "probability": round(w.probability, 4),
                    }
                    for w in (seg.words or [])
                ],
            }
        )
    return out


def transcribe(audio: Path, model_name: str, language: str, device: str, compute_type: str, vad_filter: bool):
    from faster_whisper import WhisperModel

    model = WhisperModel(model_name, device=device, compute_type=compute_type)
    segments, info = model.transcribe(
        str(audio),
        language=language,
        vad_filter=vad_filter,
        word_timestamps=True,
    )
    return serialize_segments(segments), info


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Word-level transcription with faster-whisper")
    ap.add_argument("audio", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--model", default="small")
    ap.add_argument("--language", default="zh")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--compute-type", default="int8")
    ap.add_argument("--no-vad", action="store_true")
    ap.add_argument("--srt", action="store_true")
    args = ap.parse_args(argv)

    if not args.audio.is_file():
        print(f"Audio not found: {args.audio}", file=sys.stderr)
        return 2

    try:
        segments, info = transcribe(
            args.audio,
            args.model,
            args.language,
            args.device,
            args.compute_type,
            vad_filter=not args.no_vad,
        )
    except Exception as exc:
        print(f"Transcription failed: {exc}", file=sys.stderr)
        return 2

    args.out.mkdir(parents=True, exist_ok=True)
    payload = {
        "language": getattr(info, "language", args.language),
        "duration": getattr(info, "duration", None),
        "segments": segments,
    }
    (args.out / "transcript.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (args.out / "TRANSCRIPT.md").write_text(build_markdown(segments), encoding="utf-8")
    if args.srt:
        (args.out / "captions.srt").write_text(build_srt(segments), encoding="utf-8")

    print(f"Wrote {args.out}/transcript.json, TRANSCRIPT.md" + (", captions.srt" if args.srt else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
