from etcbackup.config import *
repotype="normal"
def get_paths(modarg):
    if type(modarg) is str:
        return [modarg]
    else:
        return modarg
