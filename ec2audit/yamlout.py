import yaml

from ec2audit.utils import NaturalOrderDict

def unicode_representer(dumper, ustr):
    return dumper.represent_scalar("tag:yaml.org,2002:str", ustr)

def natural_order_dict_representer(dumper, dct):
    dumper.ignore_aliases = lambda data: True
    return dumper.represent_mapping('tag:yaml.org,2002:map', dct)

yaml.add_representer(unicode, unicode_representer)
yaml.add_representer(NaturalOrderDict, natural_order_dict_representer)

def dump(data, stream=None):
    return yaml.dump(data, stream=stream, default_flow_style=False)
