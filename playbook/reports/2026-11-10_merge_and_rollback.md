# Proposed merge and rollback procedure (pro-system → main)

A record, not instructions. Nothing here is done without the user's approval.

**Recovery baseline:** commit `fb25e5933dc52d27c7b7be6c05c1d19258a52616` (`fb25e59`), the tip of `main` on GitHub, verified 2026-11-10 with `git ls-remote origin refs/heads/main`. A local tag `pre-pro-system` points at it; this session cannot push tags (HTTP 403). The user can add the tag on GitHub (Releases → Draft a new release → tag `pre-pro-system`, target `fb25e59`), or the hash is used directly.

## Proposed merge method: a merge commit (not squash, not rebase)
1. Open a pull request from `pro-system` into `main` on GitHub.
2. Before merging, confirm:
   - `main` is still at `fb25e59`. If it has moved (e.g. a GS 5/6 or 6/6 delivery commit), merge `main` into `pro-system` first and re-run `pipeline/qc/tests/run_tests.py` and `check_rules.py`.
   - The PR's file list matches the delivery report.
3. Merge with **"Create a merge commit"**. That keeps the branch history and gives one commit to revert.
4. Timing: after GS 6/6 is delivered (Sat Nov 14), so no Short switches system mid-season.

## Rollback, by merge method (each rehearsed in a scratch clone on 2026-11-10; the tree afterwards matched `fb25e59` exactly)
| Merge method | Rollback | Rehearsal result |
|---|---|---|
| **Merge commit** (proposed) | `git revert -m 1 <merge-commit-sha>`, then push to `main` | 0 files differ from `fb25e59` |
| Squash merge | `git revert <squash-commit-sha>`, a plain revert: a squash commit has one parent, so `-m 1` doesn't apply | 0 files differ from `fb25e59` |
| Rebase merge | `git revert --no-edit fb25e59..<last-rebased-sha>` (reverts each rebased commit, newest first) | Not rehearsed; not proposed |

Last resort only, never routine: reset `main` to `fb25e59` and force-push. This discards anything merged after it, and only the user may authorise it.

## What a rollback affects
Phase 2A and 2B change only Markdown, `setup.sh` (the `.m4a` line) and the new `pipeline/qc/` folder. No renderer, style, Remotion effect, music, sound or voice file changes, so a rollback never affects a past or current video build.
