# Instructions for developers of ezdevice-python

The setup file was developed using instructions from https://realpython.com/pypi-publish-python-package/.

## Releasing a new version to pypi

```
python setup.py sdist bdist_wheel
twine check dist/*
# test the upload
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# view the upload at https://test.pypi.org/ it it looks good upload for real
twine upload dist/*
```
