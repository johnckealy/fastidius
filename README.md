To develop:

```
python setup.py develop
```

To upload:


```bash
python setup.py sdist bdist_wheel

twine upload --repository testpypi --skip-existing dist/*
```

Use `__token__` as username and the token as the password.

Install with
```
pip install --index-url https://test.pypi.org/simple/my-test-cli-click-tool
```
