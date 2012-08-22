import os, sys, errno

def mkdirp(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else: raise

class NaturalOrderDict(dict):
    def keys(self):
        return sorted(super(NaturalOrderDict, self).keys())

    def items(self):
        return sorted(super(NaturalOrderDict, self).items())

    def iterkeys(self):
        return iter(self.keys())

    def iteritems(self):
        return iter(self.items())

    def __iter__(self):
        return iter(sorted(super(NaturalOrderDict, self).__iter__()))

def exit_with_error(error):
    sys.stderr.write(error)
    sys.exit(1)

def get_aws_credentials(params):
    access_key=params.get('--access-key-id') or os.environ.get('AWS_ACCESS_KEY_ID')
    if params.get('--secret-key-file'):
        with open(params.get('--secret-key-file')) as f:
            secret_key = f.read().strip()
    else:
        secret_key = params.get('--secret-key') or os.environ.get('AWS_SECRET_ACCESS_KEY')
    if not (access_key and secret_key):
        exit_with_error('ERROR: Invalid AWS credentials supplied.')
    return access_key, secret_key
