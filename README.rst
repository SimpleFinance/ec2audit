ec2audit
========

Dump all EC2 information to a folder suitable for version control

ec2audit can output either to ``stdout`` or to a directory, and can
output in ``json`` and ``yaml`` formats. Identical data should produce
identical output (suitable for ``diff``-ing).

Types
-----

Currently ``ec2audit`` can dump:

-  instances
-  security groups
-  volumes.

Usage
-----

The most basic usage is:

::

    ec2audit <region>

However the recommended usage is to output to a directory with one item
per file.

::

    ec2audit <region> -o <output_dir>

This will create ``instances``, ``security_groups``, and ``volumes``
folders under the ``<output_dir>`` directory, with each instance,
security group and volume represented in its own file.

You can change the output format using ``-f json`` or ``-f yaml``. For
convenience you can also do ``-fj`` or ``-fy``.

For reference, the complete usage information is represented below:

::

    Usage:
      ec2audit [options] <region>
      ec2audit -h | --help
      ec2audit -v | --version

    Options:
      -h --help                               Show this screen.
      -v --version                            Show the version.

      -o --output=OUTPUT                      The output directory, stdout otherwise
      -f --format=FORMAT                      The output format: json or yaml [default: yaml]

      -I --access-key-id=ACCESS_KEY_ID        AWS access key to use (default: $AWS_ACCESS_KEY_ID)[.
      -S --secret-key=SECRET_KEY              AWS secret key to use (default: $AWS_SECRET_ACCESS_KEY).
      -K --secret-key-file=SECRET_KEY_FILE    File containing AWS secret key to use.

