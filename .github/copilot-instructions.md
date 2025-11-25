<!-- .github/copilot-instructions.md -->
# Copilot / AI Agent Instructions — TDE_agentes_zombie

Purpose: Quickly orient an AI coding agent to be productive in this repository. Keep edits small, runnable, and traceable. If this file already exists, merge carefully: preserve run/debug instructions and any project-specific notes.

- Repository snapshot
  - Single top-level script: `tde_zombie.py` (currently empty). No `requirements.txt`, no tests, no CI configured.
  - Platform: developer uses Windows (PowerShell); treat run/debug examples as PowerShell-friendly.

- Immediate goals for an agent
  - Make minimal, focused edits that are executable locally (create `main()` and a __main__ guard when adding logic).
  - When adding dependencies, create `requirements.txt` and document install/run steps in `README.md`.

- How to run & quick checks (PowerShell examples)
  - Run the script directly:

    ```powershell
    python tde_zombie.py
    ```

  - If adding packages, prefer a virtual environment and `requirements.txt`:

    ```powershell
    python -m venv .venv; .\\.venv\\Scripts\\Activate.ps1; pip install -r requirements.txt; python tde_zombie.py
    ```

- Project-specific conventions (discoverable patterns)
  - Keep the entrypoint named `main()` and guarded with `if __name__ == "__main__": main()` so CI/run scripts can import parts for tests.
  - File and module names: snake_case. Classes: PascalCase.
  - Tests (if added): use `pytest` style, files named `test_*.py` and placed at repo root or `tests/`.
  - If you introduce config or secrets, add a `.env.example` and load via `os.environ` or `python-dotenv`.

- Integration & external dependencies
  - There are no current external integrations. If you add one (HTTP service, DB, etc.), document connection steps in `README.md` and add a small smoke test script under `tests/`.

- Guidance for edits by AI agents
  - Prefer small, self-contained changes with a short commit message that explains intent.
  - Add or update `README.md` for any new feature or dependency.
  - Before finishing a change: run `python -m py_compile <file>` or simply run the script to catch syntax/runtime errors.

- Merge guidance (if this file exists already)
  - Preserve the “How to run” section and any documented commands. Append new project-specific notes below existing content and keep the file short (20–50 lines).

- When to ask the human
  - If behavior, expected inputs/outputs, or the intended agent architecture are unclear, ask: "What should an agent do in this repository? Provide a short example or expected output."  
  - If you plan to add major structure (packages, CI, tests), confirm before large refactors.

Reference files: `tde_zombie.py` (entrypoint), `README.md` (create/update when adding features).

If you'd like, I can now (a) create a minimal starter `tde_zombie.py` scaffold (main + logging), (b) add `README.md` with run instructions, or (c) modify this guidance after you tell me the intended agent behavior. Which should I do next?