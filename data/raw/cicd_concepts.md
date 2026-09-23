# CI/CD Concepts

CI/CD (Continuous Integration / Continuous Deployment) automates the
process of building, testing, and releasing software so changes reach
production quickly and reliably.

## Continuous Integration (CI)
Developers merge code changes frequently. Each change triggers an
automated pipeline that builds the project and runs tests, catching
integration problems early instead of at release time.

## Continuous Deployment/Delivery (CD)
Continuous Delivery means every change that passes CI is automatically
prepared for release (but a human may approve the final deploy).
Continuous Deployment goes further and deploys automatically with no
manual step, once all checks pass.

## A typical pipeline
1. **Trigger**: a push or pull request to a branch (e.g. `main`).
2. **Build**: install dependencies, build the Docker image.
3. **Test**: run unit/integration tests.
4. **Push**: push the built image to a registry (e.g. Google Artifact
   Registry, Docker Hub).
5. **Deploy**: deploy the new image (e.g. `gcloud run deploy`).

## GitHub Actions example
```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker image
        run: docker build -t my-app .
      - name: Run tests
        run: pytest
      - name: Deploy to Cloud Run
        run: gcloud run deploy my-app --image my-app --region asia-south1
```

## Git fundamentals often tested alongside CI/CD
- **Branching**: isolating work (e.g. `feature/xyz`) from `main`.
- **Merge vs rebase**: merge creates a merge commit preserving both
  histories; rebase replays your commits on top of another branch for a
  linear history. Rebase is often preferred for feature branches before
  merging into `main`, but should be avoided on shared/public branches.
- **Pull requests**: a way to review changes before merging, often
  gated by required CI checks passing.
