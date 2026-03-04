# Deployment

## Publishing to PyPI

The package can be published to PyPI using the standard Python workflow.

### Build

```bash
pip install build
python -m build
```

### Upload to PyPI

```bash
pip install twine
twine upload dist/*
```

## GitHub Releases

1. Update version in `healthsites/__init__.py` and `pyproject.toml`
2. Create a git tag: `git tag v0.1.0`
3. Push the tag: `git push origin v0.1.0`
4. Create a GitHub release from the tag

## Documentation

Documentation is automatically deployed to GitHub Pages when pushing to `main`.

---

Made with love by [Kartoza](https://kartoza.com) | [Donate!](https://github.com/sponsors/kartoza) | [GitHub](https://github.com/kartoza/healthsites-api-client)
