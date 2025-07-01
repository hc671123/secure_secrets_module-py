from secure_secrets_module import *
secmod = secrets()
print(secmod.get_secret('Version'))
secmod.add_secret('example','Hello World')
print(secmod.get_secret('example'))
secmod.add_secret('example2',['Hello','World',2])
print(secmod.get_secret('example2'))
#secmod.password_change()