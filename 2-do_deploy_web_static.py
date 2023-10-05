#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from fabric.api import env, put, run
from os.path import exists

env.hosts = ['100.25.180.140', '54.82.156.0']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""

    if not exists(archive_path):
        return False

    # Upload the archive to the /tmp/ directory of the web server
    put(archive_path, '/tmp/')

    archive_filename = archive_path.split('/')[-1]
    folder_name = archive_filename.split('.')[0]
    release_path = '/data/web_static/releases/{}'.format(folder_name)
    run('mkdir -p {}'.format(release_path))
    run('tar -xzf /tmp/{} -C {}'.format(archive_filename, release_path))

    # Delete the archive from the web server
    run('rm /tmp/{}'.format(archive_filename))

    run('mv {}/web_static/* {}/'.format(release_path, release_path))

    # Remove the web_static directory
    run('rm -rf {}/web_static'.format(release_path))

    # Remove the symbolic link /data/web_static/current
    run('rm -rf /data/web_static/current')

    # Create a new symbolic link /data/web_static/current
    run('ln -s {} /data/web_static/current'.format(release_path))

    print('New version deployed!')
    return True
