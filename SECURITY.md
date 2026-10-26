# Reporting security issues

Do not publish credentials, student writing, personal data, or exploit details in
a public issue or pull request. Report a vulnerability privately to the repository
owner through a channel you already trust. If GitHub private vulnerability
reporting is enabled, use the repository Security tab.

Use synthetic test data. Never commit production `.env` files, SSH private keys,
API tokens, database backups, or private model archives. If a real credential is
committed, removing it in a later commit does not make it secret again: notify
the owner and revoke or rotate it.

Collaborator write access is not production access. Keep deployment secrets only
in the protected production environment, review workflow changes, and never
expose a production-connected self-hosted runner to repository writers. See
[the release trust boundary](docs/RELEASE_SECURITY.zh-CN.md), especially before
changing repository visibility or subscription plans.
