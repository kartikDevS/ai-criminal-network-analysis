# Contributing & Git Collaboration Guidelines

To maintain code quality, avoid merge conflicts, and ensure a smooth hackathon workflow, all team members must adhere to these 11 collaboration rules.

---

## The 11 Golden Rules

1. **Never directly push to `main`:**  
   The `main` branch is protected and represents the stable, working version of the system.
2. **Work exclusively on your assigned branch:**  
   - `data` for dataset and ETL pipeline work
   - `ml` for AI/ML models, training, and evaluation
   - `architect` for graph algorithms and system design
   - `security` for cybersecurity, authentication, and RBAC
   - `research` for documentation, papers, and benchmarks
   - `integration` for frontend, backend API, and end-to-end testing
3. **Pull the latest `main` before starting work:**  
   Always run `git checkout <your-branch> && git pull origin main` to ensure your working branch is up to date.
4. **Test your changes locally:**  
   Run `pytest tests/` and verify that your scripts run cleanly before committing.
5. **Commit meaningful, atomic changes:**  
   Use descriptive commit messages (e.g., `feat(ml): implement isolation forest baseline`, `docs(schema): update event fields`).
6. **Push your branch to GitHub:**  
   Push changes using `git push origin <your-branch>`.
7. **Create a Pull Request (PR):**  
   Open a PR targeting `main` with a clear description of what changed and how it was tested.
8. **Review before merging:**  
   At least one team member or the Project Architect must review and approve the PR before merging.
9. **Never commit passwords, API keys, or secrets:**  
   Always use `.env` (which is git-ignored) and keep `.env.example` updated with placeholders.
10. **Never commit huge generated datasets:**  
    Store only small sample data in `data/sample/`. Large raw/generated files are git-ignored.
11. **Document important architectural decisions:**  
    Update the corresponding markdown file in `docs/` whenever you introduce a new feature or change an interface.
