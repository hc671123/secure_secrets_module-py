import os
def backendpath(directory: str,path: str) -> str:
    paths = path.split('/')
    respath = directory
    for path in paths:
        respath = os.path.join(respath,path)
    return respath