

---

```shell
cd git/repos/OpenStudioLandscapes-Test

git clone https://github.com/michimussato/OpenStudioLandscapes-filebrowser
```

```shell
cd OpenStudioLandscapes-filebrowser
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install --force-reinstall --editable ".[dev]"
```