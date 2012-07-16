from os import environ
from os.path import join
from boto import ec2, dynamodb

from ec2audit.utils import *


def instance_data(i):
    data = NaturalOrderDict()

    verbatim = ['id', 'image_id', 'architecture', 'instance_type',
                'launch_time', 'placement', 'private_ip_address', 'ip_address',
                'root_device_type', 'state']

    vpc_only = ['sourceDest', 'subnet_id', 'vpc_id']

    for key in verbatim:
        v = i.__dict__[key]
        if v == '' or v == None: # but not False
            continue
        data[key] = v

    if i.__dict__.get('vpc_id'):
        for key in vpc_only:
            data[key] = i.__dict__[key]

    data['security_groups'] = NaturalOrderDict()
    for group in i.groups:
        data['security_groups'][group.id] = group.name

    if i.block_device_mapping:
        data['devices'] = NaturalOrderDict()
        for dev, vol in i.block_device_mapping.items():
            data['devices'][dev] = vol.volume_id

    name = i.tags.get('Name') or i.id

    tags = i.tags.copy();
    tags.pop('Name')
    if tags:
        data['tags'] = NaturalOrderDict(tags)

    return name, data


def get_ec2_instances(econ):
    instances = NaturalOrderDict()
    for res in econ.get_all_instances():
        for i in res.instances:
            name, data = instance_data(i)
            instances[name] = data

    return instances

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

def to_dir(instances, fmt, output):
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
    for name, data in instances.items():
        with open(join(output, name + '.' + ext), 'w') as f:
            dump({name:data}, f)

def run(params):
    access_key, secret_key = get_aws_credentials(params)
    region = params['<region>']
    if params['--format'] not in ['j', 'y', 'p', 'json', 'yaml', 'pprint']:
        exit_with_error('Error: format must be one of json or yaml\n')

    con = ec2.connect_to_region(region,
                                 aws_access_key_id=access_key,
                                 aws_secret_access_key=secret_key)


    instances = get_ec2_instances(con)
    output = params['--output']
    if not output:
        to_stdout(instances, params['--format'])
    else:
        to_dir(instances, params['--format'], output)
