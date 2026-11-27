# Contributing to ciscoaxl

Thank you for your interest in contributing! ciscoaxl wraps the Cisco AXL SOAP API and new
method coverage is always welcome.

## Getting started

1. **Fork** the repository on GitHub and clone your fork locally.

2. **Create a feature branch** off `master`:

   ```bash
   git checkout -b feat/my-new-feature
   ```

   Use a descriptive name — e.g. `feat/add-remote-destination` or `fix/list-hunt-groups`.

3. **Set up your environment** with [uv](https://github.com/astral-sh/uv):

   ```bash
   uv sync
   ```

4. **Make your changes.** A few guidelines:
   - Follow the existing method patterns in `ciscoaxl/axl.py` (see `get_line_group` as a reference).
   - Add or update the corresponding page under `docs/` using the `options:` mkdocstrings syntax.
   - Do not commit `.env` files or credentials.

5. **Run the tests:**

   ```bash
   uv run pytest tests/test_offline_requests.py
   ```

6. **Build the docs locally to verify:**

   ```bash
   uv run --with mkdocs --with mkdocs-material --with 'mkdocstrings[python]' mkdocs build
   ```

7. **Commit** with a [conventional commit](https://www.conventionalcommits.org/) message:

   ```bash
   git commit -m "feat: add remote destination CRUD methods"
   ```

8. **Push your branch** and **open a Pull Request** on GitHub against `master`.

## Pull request guidelines

- Describe **why** the change is needed, not just what it does.
- Reference any related GitHub Issue (e.g. `Closes #42`).
- Keep PRs focused — one feature or fix per PR makes review easier.
- If you are adding new AXL methods, include at least one offline test using the existing
  mock patterns in `tests/test_offline_requests.py`.

## Roadmap

Unimplemented features are tracked at:
[https://github.com/users/levensailor/projects/6](https://github.com/users/levensailor/projects/6)
