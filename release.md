# Release steps

- Update the version in `pyproject.toml`

  ```console
  # Bump the version string
  uv version --bump {major|minor|patch|alpha|beta|stable}
  # or specify the version directly
  uv version X.Y.Z
  ```

- Commit changes to `main`
- Tag the repo with the new version: `vX.Y.Z`
