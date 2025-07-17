from shutil import copytree, copy
copy('./README.md','./for_publishing/README.md')
copytree('./secure_secrets_module','./for_publishing/secure_secrets_module')
