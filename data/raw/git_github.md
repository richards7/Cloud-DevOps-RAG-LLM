# Git and GitHub

## Core concepts
- **Repository**: a folder tracked by Git, containing your project's full history.
- **Commit**: a saved snapshot of changes, with a message describing what changed.
- **Branch**: an independent line of development — lets you work on a feature without
  affecting `main`.
- **Remote**: a version of the repo hosted elsewhere (e.g. GitHub) — `origin` is the
  conventional name for the primary remote.

## Everyday commands
```bash
git init                          # start tracking a new repo
git clone <url>                    # copy a remote repo locally
git status                         # what's changed
git add file.py                    # stage a change
git add .                          # stage everything
git commit -m "message"            # save a snapshot
git push origin main                # send commits to the remote
git pull origin main                # fetch + merge remote changes

git branch feature/login            # create a branch
git checkout feature/login          # switch to it
git checkout -b feature/login       # create and switch in one step
git switch feature/login            # modern equivalent of checkout for branches

git log --oneline --graph           # compact visual history
git diff                            # see unstaged changes
git diff --staged                   # see staged changes
```

## Merge vs rebase
- **Merge**: combines two branches, creating a merge commit that preserves both
  histories exactly as they happened.
- **Rebase**: replays your branch's commits on top of another branch, producing a
  linear history — cleaner, but rewrites commit hashes, so never rebase a branch
  others are already working from (a shared/public branch).

```bash
git merge feature/login             # merge feature into current branch
git rebase main                     # replay current branch's commits onto main
```

## Resolving conflicts
When Git can't auto-merge changes to the same lines, it marks the file with conflict
markers (`<<<<<<<`, `=======`, `>>>>>>>`). Edit the file to keep the correct content,
remove the markers, then:
```bash
git add <resolved-file>
git commit          # (or `git rebase --continue` if resolving during a rebase)
```

## Undoing changes
```bash
git restore file.py                 # discard unstaged changes to a file
git reset --soft HEAD~1             # undo last commit, keep changes staged
git reset --hard HEAD~1             # undo last commit, DISCARD changes (destructive)
git revert <commit-hash>            # create a new commit that undoes a previous one
                                     # (safe for shared branches, unlike reset)
```

## GitHub-specific workflow
- **Pull Request (PR)**: proposes merging one branch into another, with a space for
  review, comments, and CI checks before merging.
- **Fork**: your own copy of someone else's repo, used for contributing to projects
  you don't have direct write access to.
- **GitHub Actions**: GitHub's built-in CI/CD, defined in `.github/workflows/*.yml`.

## Common errors & fixes
- **"failed to push some refs" (rejected, non-fast-forward)**: the remote has commits
  you don't have locally — run `git pull` (or `git pull --rebase`) first, then push.
- **Merge conflict during pull**: resolve conflicts as above, then commit.
- **Accidentally committed a secret**: change/revoke the secret immediately (removing
  it from history alone isn't enough once pushed) — then use `git filter-repo` or the
  BFG Repo-Cleaner to scrub it from history, and force-push (coordinate with your team
  first, since this rewrites history).
- **Detached HEAD state**: you checked out a specific commit instead of a branch —
  create a branch from here if you want to keep the work: `git checkout -b new-branch`.
- **Large file rejected by GitHub**: GitHub blocks files over 100MB — use Git LFS
  (Large File Storage) for large binary assets.
