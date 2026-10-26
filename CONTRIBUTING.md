# Contributing to the WenHeng web application

[简体中文操作说明](docs/COLLABORATION.zh-CN.md)

This repository contains the WenHeng web frontend and backend. It is independent
of the historical ZhiBi application and of OpenEssayScore, model training, DSW,
and private model archives. Keep contributions within this web application.

## Access and branches

Use your own GitHub account. The owner invites collaborators through repository
**Settings → Collaborators → Add people**. Share only the GitHub username; no
server account, shared login, production SSH key, or root access is needed.

Create one branch per change, such as `feature/username-report-layout`,
`fix/username-upload-error`, or `docs/username-setup`. Never force-push `main`.

```bash
git clone https://github.com/pasariga/multi_model_essay.git
cd multi_model_essay
git switch main
git pull --ff-only
git switch -c feature/yourname-short-description
# Make and verify your change.
git add frontend/path-you-changed backend/path-you-changed
git diff --cached
git commit -m "feat: describe the change"
git push -u origin feature/yourname-short-description
```

Stage only the files you intend to submit; the paths above are examples. Never
stage `.env`, credentials, student submissions, uploads, database dumps, or model
weights. Use your own development configuration and synthetic examples.

## Editors

- **VS Code:** clone the repository, create a branch using Source Control, edit,
  review the diff, commit, and publish that branch. Open a PR targeting `main`.
- **Codex:** open your local clone on that branch. State the intended change and
  web-only scope. Review its changes and test results before committing. Do not
  give an assistant production credentials or ask it to deploy automatically.
- **GitHub website:** edit a file and choose **Create a new branch for this
  commit and start a pull request**. For broader edits, press `.` to use github.dev.

## Automated checks and review

`Web CI` runs for PRs into `main`, for `main` pushes and named development
branches, and on manual request. Required checks are:

| Check | What it verifies |
| --- | --- |
| Frontend checks | Locked npm installation, Vue/TypeScript checks, Vite production build |
| Backend checks | Python syntax, migrations and existing web tests against a disposable PostgreSQL 16 database |
| Repository safety | Common accidental credential commits and deployment shell syntax |

The optional Paddle runtime is excluded from web-test installation. OCR and
model-service calls in the existing integration tests use test doubles; CI has
no production API keys. This does not validate real OCR models or real provider
availability. Frontend unit tests are not currently defined; build/type checks
are not a substitute for manual browser testing. The hygiene check is not an
exhaustive secret scanner.

Open a PR with its purpose, verification and release impact. `@pasariga` is the
code owner for all files, including workflows and CODEOWNERS. New commits dismiss
stale approvals. Resolve discussions and keep the branch current with `main`.
After the checks and owner review pass, use squash merge. The branch is deleted
after merging. Ordinary collaborators cannot directly update protected `main`.

The owner retains GitHub administrator bypass for repository recovery and initial
configuration; it is not a collaborator privilege. Use it only deliberately and
normally merge through the same PR checks. If the owner authors a PR, another
eligible reviewer is needed for normal approval; GitHub does not permit approving
your own PR. The initial setup may therefore use the owner's administrative merge
after successful CI, without authorizing a production deployment.

## Releasing

PRs and merges do **not** deploy the website. See
[release security and ECS prerequisites](docs/RELEASE_SECURITY.zh-CN.md).
Production is deliberately disabled until the owner verifies the existing ECS
identity, restricted SSH wrapper, and privileges. Do not approve deployment jobs
for unreviewed workflow changes.
