# CI/CD Concepts — Additional Common Errors & Fixes
(Supplements cicd_concepts.md already in the knowledge base.)

- **Pipeline passes locally but fails in CI**: almost always an environment difference
  — missing environment variables/secrets in the CI runner, a different OS/dependency
  version, or tests relying on local state (a file, a running service) that CI doesn't
  have.
- **Flaky tests failing intermittently in CI**: often timing/race conditions, or tests
  that aren't properly isolated from each other (shared state between test runs).
- **Secrets accidentally exposed in CI logs**: most CI systems auto-mask registered
  secrets in log output — but only if the secret is registered as a secret variable,
  not just hardcoded and echoed; never `echo $SECRET_VAR` in a pipeline step.
