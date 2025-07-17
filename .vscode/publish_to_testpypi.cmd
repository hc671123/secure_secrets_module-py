pip install build twine
python .//publishing_script1.py
cd .//for_publishing
CLS
python -m build
python -m twine upload -r testpypi dist/* --verbose
cd ..//
python .//publishing_script2.py