#helper script for automated publishing
from os import remove, mkdir
from shutil import rmtree, copy
copy('./for_publishing/pyproject.toml','./_t.txt')
rmtree('./for_publishing')
mkdir('./for_publishing')
copy('./_t.txt','./for_publishing/pyproject.toml')
remove('./_t.txt')