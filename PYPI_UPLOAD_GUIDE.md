# PyPI Upload Guide for Codemni

## Prerequisites

1. Install build tools:
```powershell
pip install build twine
```

2. Create PyPI account:
   - Go to https://pypi.org/account/register/
   - Verify your email

3. Create API token:
   - Go to https://pypi.org/manage/account/token/
   - Create a new API token with "Entire account" scope
   - Save the token (starts with `pypi-`)

## Build the Package

1. Clean previous builds:
```powershell
if (Test-Path dist) { Remove-Item -Recurse -Force dist }
if (Test-Path build) { Remove-Item -Recurse -Force build }
if (Test-Path *.egg-info) { Remove-Item -Recurse -Force *.egg-info }
```

2. Build the distribution:
```powershell
python -m build
```

This will create:
- `dist/Codemni-1.1.0.tar.gz` (source distribution)
- `dist/Codemni-1.1.0-py3-none-any.whl` (wheel distribution)

## Test the Package Locally (Optional)

Install the package locally to test:
```powershell
pip install dist/Codemni-1.1.0-py3-none-any.whl
```

Test the import:
```python
from Codemni.llm import openai_llm
from Codemni.TOOL_CALLING_AGENT import Create_ToolCalling_Agent
from Codemni.memory import ConversationalBufferMemory
```

## Upload to TestPyPI (Recommended First)

1. Create TestPyPI account at https://test.pypi.org/

2. Upload to TestPyPI:
```powershell
python -m twine upload --repository testpypi dist/*
```

3. Test installation from TestPyPI:
```powershell
pip install --index-url https://test.pypi.org/simple/ Codemni
```

## Upload to PyPI (Production)

1. Upload to PyPI:
```powershell
python -m twine upload dist/*
```

2. Enter your credentials:
   - Username: `__token__`
   - Password: Your API token (including the `pypi-` prefix)

## Verify Upload

1. Check your package page: https://pypi.org/project/Codemni/

2. Test installation:
```powershell
pip install Codemni
```

## Update Package Version

When releasing a new version:

1. Update version in:
   - `pyproject.toml` (line 5)
   - `__init__.py` (line 18)
   - `llm/__init__.py`
   - `memory/__init__.py`
   - `TOOL_CALLING_AGENT/__init__.py`

2. Clean and rebuild:
```powershell
Remove-Item -Recurse -Force dist, build, *.egg-info
python -m build
python -m twine upload dist/*
```

## Troubleshooting

### "File already exists"
This means the version already exists on PyPI. Increment the version number.

### "Invalid distribution metadata"
Check that all fields in `pyproject.toml` are correct.

### Import errors after installation
Make sure all `__init__.py` files are present and properly configured.

### "Package not found"
Wait a few minutes after upload for PyPI to index your package.

## Files Created for PyPI

✅ `pyproject.toml` - Package metadata and build configuration
✅ `LICENSE` - MIT license
✅ `MANIFEST.in` - Include/exclude files in distribution
✅ `.gitignore` - Exclude build artifacts from git
✅ `__init__.py` files - Make directories Python packages
✅ `requirements.txt` - Dependencies documentation

## Next Steps

1. Build the package: `python -m build`
2. Upload to TestPyPI first (recommended)
3. Test installation from TestPyPI
4. Upload to PyPI: `python -m twine upload dist/*`
5. Share your package: `pip install Codemni`

---

**Package Name:** Codemni  
**Version:** 1.1.0  
**PyPI URL:** https://pypi.org/project/Codemni/  
**License:** MIT
