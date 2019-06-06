#import configparser
import appdirs
import os.path
import yaml
try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader

def load_config(path=None):
    if path is None:
        path=os.path.join(appdirs.user_config_dir("etcbackup","SunnySeaside"),"config.yaml")
    try:
        file=open(path,"r")
    except FileNotFoundError:
        sys.exit("Error: no configuration file found at "+path)
    config=yaml.load(file,Loader=SafeLoader)
    file.close()
    return config

def get_yaml_list(obj,name,allow_dict=False):
    data=obj.get(name)
    if type(data) is list:
        return data
    elif type(data) is str:
        return [data]
    elif allow_dict and type(data) is dict:
        return [data]
    elif data is None:
        return []
    else:
        sys.exit("Error: "+name+" must be a list or string")

