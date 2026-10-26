[English](README.md) | [简体中文](README.zh-CN.md)

# WenHeng · 文衡

A Chinese writing assessment and improvement application combining image intake, OCR proofreading, independent model reviews and evidence-linked feedback. The repository name remains `multi_model_essay`; the current frontend identifies the product as **文衡**.

This is an application/source snapshot, not a promise of a currently available public service. It is separate from the historical [妙笔智改 (智笔 / ZhiBi)](https://github.com/pasariga/ProjectZhiBi) writing assistant. [OpenEssayScore](https://github.com/pasariga/OpenEssayScore) is a separately packaged scoring research toolkit with a different score scale and evidence boundary, not this application's three-provider review engine.

## The workflow

1. Register or sign in, then submit typed text or ordered page images with writing context.
2. Inspect image quality, run OCR, and correct text while keeping links to the original image regions.
3. Request independent DeepSeek, Qwen and Doubao reviews using a shared structured rubric.
4. Compare scores and evidence, examine disagreement, optionally request cross-review, and read or export the persisted report.
5. Reopen personal history, add teacher reference assessments, and use revision/training features for further writing practice.

The code supports these paths; remote providers still require valid accounts, configuration and model access. Reports are learning aids, not validated replacements for teacher assessment.

## Implementation and completed work

| Area | Evidence in the repository |
| --- | --- |
| Account isolation | Bearer sessions, essay ownership and access checks in `backend/app/api/` and `backend/app/modules/auth/`. |
| Image/OCR pipeline | OpenCV preprocessing retains originals and geometric mappings; Baidu handwriting OCR is the default, with PaddleOCR as an explicitly enabled local alternative. Corrections are stored separately from recognition output. |
| Review orchestration | Provider adapters, structured contracts, parallel attempts, retry/error records and a quorum/grace policy in `backend/app/modules/reviews/`. One slow service need not keep a qualifying batch waiting indefinitely. |
| Score interpretation | A normalized 100-point rubric with four 25-point dimensions, disagreement detection, evidence offsets and separate recheck records. Historical teacher samples enable reliability weights only when the configured sample threshold is met. |
| Writing improvement | Dedicated training, polishing and deeper-analysis code, with report/history interfaces in the Vue application. |
| Verification boundaries | `backend/TESTING.md` separates offline tests from opt-in live-service smoke tests. A successful mock test does not demonstrate usable paid APIs or OCR accounts. |

History records work on materials, mock-exam workflows and annotation feedback. These are implementation changes, not quantified improvements in educational outcomes. Detailed historical configuration and API notes are retained in [the previous implementation guide](docs/IMPLEMENTATION.zh-CN.md); some sections describe earlier stages, so current source takes precedence.

## Architecture

- **Frontend:** Vue 3, TypeScript and Vite, with the product workflow in `frontend/src/App.vue`.
- **Backend:** FastAPI, SQLAlchemy/asyncpg, Alembic and PostgreSQL.
- **External services:** Baidu OCR and independently configured review providers. API credentials remain server-side.
- **Operations:** local and production Compose files, deployment documentation and service readiness checks.

Unlike a wholly local application, enabled OCR and review providers receive submitted content. Use authorized material and evaluate provider/data-handling requirements before deployment.

## Local setup

Requirements documented by the project: Python 3.11+, Node.js 20+ and PostgreSQL 16+. Configure your own credentials; real `.env`, databases and uploads do not belong in Git.

```powershell
git clone https://github.com/pasariga/multi_model_essay.git
cd multi_model_essay
Copy-Item .env.example .env
docker compose up -d postgres
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
# Set DATABASE_URL to your local PostgreSQL database before migrating.
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe app.py
```

In a second terminal, run `npm install`, copy `.env.example` to `.env`, and run `npm run dev` from `frontend/`. The development frontend is at `http://localhost:5173`; backend health is `/api/health` on port 8000. Configure provider keys and model identifiers in `backend/.env` for the corresponding live features. PaddleOCR requires explicit worker configuration and is not silently started as a fallback.

[Deployment notes](DEPLOYMENT.md) · [Offline and live testing](backend/TESTING.md) · [Historical implementation details](docs/IMPLEMENTATION.zh-CN.md)

[Contributing and PR checks](CONTRIBUTING.md) · [Release authorization and ECS prerequisites](docs/RELEASE_SECURITY.zh-CN.md). Merging a PR does not deploy production.

## Status, provenance and license

This documentation review did not deploy the application, run paid services or establish new performance/accuracy results. Hosting availability and continued maintenance are not established by a restored source repository.

The repository has no top-level license file at this revision. No new license or third-party rights are granted by this README. Provider services and dependencies retain their own terms. The legacy project is formally 妙笔智改, abbreviated 智笔 (ZhiBi). WenHeng is its later, independently developed application line; features and results remain attributed to their own repositories.
