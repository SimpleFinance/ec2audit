from os.path import join
from ec2audit.utils import *

def to_stdout(data, fmt):
    if fmt.startswith('j'):
        import json
        print json.dumps(data, indent=4)
    elif fmt.startswith('y'):
        from ec2audit import yamlout
        print yamlout.dump(data)
    elif fmt.startswith('p'):
        from pprint import pprint
        pprint(data)

def to_dir(data, fmt, output):
    if fmt.startswith('j'):
        import json
        ext = 'json'
        dump = lambda data, f: json.dump(data, f, indent=4)
    elif fmt.startswith('y'):
        from ec2audit import yamlout
        ext = 'yaml'
        dump = lambda data, f: yamlout.dump(data, f)
    elif fmt.startswith('p'):
        from pprint import pprint
        ext = 'py'
        dump = lambda data, f: pprint(data, f)

    mkdirp(output)
    for dtype, items in data.items():
        base = join(output, dtype)
        mkdirp(base)
        for name, item in items.items():
            with open(join(base, name.replace('/', ':') + '.' + ext), 'w') as f:
                dump({name:item}, f)
