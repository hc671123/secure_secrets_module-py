#deletes the pycache and deletes the data and key from the module for the next commit
from shutil import rmtree
rmtree('./secure_secrets_module/__pycache__')
from os import remove
remove('./secure_secrets_module/k.bin')
remove('./secure_secrets_module/s.bin')
remove('./secure_secrets_module/data.secrets')