#!/usr/bin/python3
""" Fabric script that creates and distributes
an archive to your web servers """
from fabric.api import local, env, run, put
from os.path import exists
from datetime import datetime


env.hosts = ['44.192.52.135', '44.192.246.111']


def do_pack():
    """ Generate .tgz file """
    try:
        local('mkdir -p versions')
        date = str(datetime.now().strftime("%Y%m%d%H%M%S"))
        path = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(path))
        print(path)
        return path
    except Exception as e:
        print(e)
        return None


def do_deploy(archive_path):
    """ Distribute file to server """
    if not exists(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')

        file = archive_path.split('/')[-1].split('.')[0]
        run('mkdir -p /data/web_static/releases/{}/'.format(file))
        run('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}'
            .format(file, file))
        run('rm /tmp/{}.tgz'.format(file))
        run('mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}'.format(file, file))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(file))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}\
            /data/web_static/current'.format(file))
        return True

    except Exception as e:
        print(e)
        return False


def deploy():
    """ Creates and distributes an archive """
    archive_path = do_pack()
    if archive_path is None:
        return False

    return(do_deploy(archive_path))
