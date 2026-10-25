# video-director-custom

Chen 的 `video-director` 定制分支，基于上游 1.0.0 快照（2026-10-25）。

- `main`：上游快照，标签 `upstream-2026-10-25`，不要直接改。
- `custom`：定制分支（案例库、21 风格、模式 B/C、交付脚本）。
- 使用路径：`~/.claude/skills/video-director-custom`（软链到本仓库）。

## 上游同步

```bash
# 把新版上游复制到 main（保留本仓库 README/.gitignore）
cd ~/code/video/skills/video-director-custom
git checkout main
rsync -a --exclude='.git' --exclude='README.md' --exclude='.gitignore' ~/.claude/skills/video-director/ ./
git add -A && git commit -m "upstream-sync-YYYY-MM-DD"
git checkout custom
git merge main
```

## 验证

```bash
~/.venvs/video/bin/python -m unittest discover -s tests -v
```
