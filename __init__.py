from pathlib import Path, PurePath
from sys import path

def add_path(newPath: str) -> str:
    # Taken from ExecUtil.
    strPath = str(newPath) if isinstance(newPath, PurePath) else newPath

    if strPath in path:
        print(f'path: {newPath} is already on sys.path. (No action taken.)')
        return path
    else:
        print(f'Adding new path: {strPath} to sys.path.')
        path.append(strPath)
    return path

parent = Path('..').resolve() # Must add the parent dir of Utilities.
add_path(parent)