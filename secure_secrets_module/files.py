import os
def backendpath(path:str) -> str:
    directory = __file__[:-9]
    paths = path.split('/')
    respath = directory
    for path in paths:
        respath = os.path.join(respath,path)
    return respath