# GitHub Actions production deployment

Production deployments use this path:

`PR -> owner review + Web CI -> merge main -> successful main CI -> owner dispatches exact SHA -> production approval -> restricted SSH wrapper -> deploy/deploy.sh`

There is no push-triggered production deployment. Development branches and main
pushes run CI only. The production environment variable
`WENHENG_PRODUCTION_DEPLOY_ENABLED` is currently `false`; leave it disabled until
the existing ECS identity and deployment account privileges have been verified.
The GitHub workflow is prepared, but ECS access and actual least privilege have
not been verified in this setup. No production release was executed.

See [collaboration](../CONTRIBUTING.md) and
[release authorization, ECS checklist and private-repository fallback](../docs/RELEASE_SECURITY.zh-CN.md).

Historical deployment documentation records `/opt/wenheng-production`. Secrets remain
outside the checkout in `/opt/wenheng-secrets/production.env`; the server-only
Compose override remains in `/opt/wenheng-secrets/compose.server.yaml`.

## Required GitHub production secrets

Add these under **Settings -> Environments -> production -> Environment secrets**:

- `ALIYUN_HOST`: production server host or IP.
- `ALIYUN_SSH_PORT`: SSH port, normally `22`.
- `ALIYUN_SSH_USER`: restricted deployment user.
- `ALIYUN_SSH_PRIVATE_KEY`: complete private half of the dedicated Actions key.
- `ALIYUN_SSH_KNOWN_HOSTS`: verified OpenSSH known-hosts line for the server.

Do not add application API keys, database passwords, or `production.env` to
GitHub. They are read only from the production server.

## Deployment safety

- Only `pasariga` can use the production workflow on `main`.
- Dispatch requires an exact current main SHA with a successful main-push Web CI run.
- `validate-only` never uses production secrets or connects to ECS.
- `deploy` also requires production environment approval and the independently
  enabled readiness switch. A stale SHA is rejected after approval.
- The environment only accepts the `main` branch and only the owner is a reviewer.
- Repository-level secrets and production-connected self-hosted runners must not
  be added. Collaborators must not receive root or production SSH credentials.
- The credential-bearing job does not check out code, install dependencies, or
  execute repository scripts on the runner.
- The following server-side behavior is documented in existing scripts; the
  current server, restricted SSH wrapper and permissions still require inspection:
- A server lock prevents overlapping deployments.
- A dirty server checkout stops deployment instead of overwriting local files.
- Git updates are fast-forward only.
- Existing containers keep running while new images build.
- Docker layer caching avoids reinstalling unchanged Python and npm dependencies.
- Before backend migrations, a PostgreSQL custom-format backup is created and
  verified under `/opt/backups/wenheng/<timestamp>/`.
- If replacement containers fail their health checks, the previous application
  images are restored. Database migrations are not automatically downgraded;
  production migrations must remain backward compatible.
- `.env` and the server-only Compose override are outside the Git checkout.

## Verifying a deployment

The GitHub Actions run must finish successfully and contain a final line like:

`DEPLOYMENT_OK commit=<40-character commit SHA>`

Then verify both the public home page and `/api/health`. The deployed commit is
also recorded in `/opt/wenheng-secrets/last-deployed-commit`.
