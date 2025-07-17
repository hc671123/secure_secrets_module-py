#deletes the pycache and deletes the data and key from the module for the next commit
from shutil import rmtree
rmtree('./secure_secrets_module/__pycache__')
from os import remove
remove('./k.bin')
remove('./s.bin')
remove('./data.secrets')