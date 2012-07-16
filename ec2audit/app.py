from os import environ
from os.path import join
from boto import ec2, dynamodb

from ec2audit.utils import *
from ec2audit.output import to_dir, to_stdout

def name_and_tags(it):
    name = it.tags.get('Name') or it.id

    tags = it.tags.copy();
    tags.pop('Name')
    return name, NaturalOrderDict(tags)

def instance_data(i):
    data = NaturalOrderDict()

    data['zone'] = i.placement

    verbatim = ['id', 'image_id', 'architecture', 'instance_type',
                'launch_time', 'private_ip_address', 'ip_address',
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
        data['volumes'] = NaturalOrderDict()
        for dev, vol in i.block_device_mapping.items():
            data['volumes'][dev] = vol.volume_id

    name, tags = name_and_tags(i)
    if tags:
        data['tags'] = tags

    return name, data

def volume_data(vol):
    data = NaturalOrderDict()

    tags = vol.__dict__['tags']
    if tags:
        data['tags'] = NaturalOrderDict(tags)

    for key in ['id', 'create_time', 'size', 'status', 'snapshot_id']:
        data[key] = vol.__dict__[key]

    return vol.id, data

def get_ec2_instances(econ):
    instances = NaturalOrderDict()
    for res in econ.get_all_instances():
        for i in res.instances:
            name, data = instance_data(i)
            instances[name] = data

    return instances

def instance_relevant_volume(vol):
    return NaturalOrderDict(id=vol['id'], size=vol['size'])

def get_ec2_volumes(econ):
    return NaturalOrderDict(volume_data(vol) for vol in econ.get_all_volumes())

def run(params):
    access_key, secret_key = get_aws_credentials(params)
    region = params['<region>']
    if params['--format'] not in ['j', 'y', 'p', 'json', 'yaml', 'pprint']:
        exit_with_error('Error: format must be one of json or yaml\n')

    con = ec2.connect_to_region(region,
                                 aws_access_key_id=access_key,
                                 aws_secret_access_key=secret_key)


    volumes = get_ec2_volumes(con)
    instances = get_ec2_instances(con)

    for instance in instances.values():
        if 'volumes' in instance:
            for k, v in instance['volumes'].items():
                instance['volumes'][k] = instance_relevant_volume(volumes[v])

    output = params['--output']
    if not output:
        to_stdout(instances, params['--format'])
    else:
        to_dir(instances, params['--format'], output)
