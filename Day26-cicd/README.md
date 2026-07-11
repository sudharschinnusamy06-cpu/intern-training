# Day 26 - CI/CD with GitHub Actions

## What I learned
- CI = automatically test every push. CD = automatically build/ship if tests pass
- GitHub Actions workflows live in .github/workflows/ - and MUST sit at repo root, never inside a subfolder
- working-directory in a workflow step, for when your project isn't at repo root
- GitHub Secrets - encrypted values (API_KEY, DATABASE_PASSWORD) injected via env:, masked in logs
- CI runs on pull requests automatically, showing pass/fail directly on the PR page

## What I did
1. Copied Day25 app, wrote first ci.yml (run tests on push/PR to main)
2. Added API_KEY and DATABASE_PASSWORD as GitHub repository secrets
3. Fixed 2 real bugs: .github was inside Day26-cicd (moved to repo root), then missing working-directory caused "requirements.txt not found"
4. Added a Docker build step to the workflow - confirmed the image builds cleanly on GitHub's machine too
5. Deliberately broke a test on a new branch, opened a PR, watched CI go red, fixed it, watched it go green, merged

## Results
- CI workflow runs automatically on every push/PR to main
- Pipeline: checkout -> setup Python -> install deps -> run 18 tests -> build Docker image
- Proved CI actually catches broken code, not just passes silently

## Key commands
| Command | Purpose |
|---|---|
| git checkout -b <branch> | Create a branch for isolated testing |
| git push -u origin <branch> | Push new branch and set upstream |
| working-directory: Day26-cicd | Run a workflow step inside a specific subfolder |