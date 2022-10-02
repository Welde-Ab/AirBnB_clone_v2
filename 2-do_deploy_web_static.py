#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

import os
from fabric.api import *


env.hosts = ['44.192.52.135', '44.192.246.111']
env.user = 'ubuntu'
def do_deploy(archive_path):
    '''
        Deploys an archive to the web servers
    '''
    name = archive_path.split("/")[1]
    if not os.path.exists(archive_path):
        return False

    result = put(archive_path, "/tmp/")
    if result.failed:
        return False

    run("mkdir -p /data/web_static/releases/{}".format(name[:-4]))

    cmd = "tar -xzf /tmp/{} -C /data/web_static/releases/{}".format(name,
                                                                    name[:-4])
    result = run(cmd)
    if result.failed:
        return False

    result = run("rm /tmp/{}".format(name))
    if result.failed:
        return False

    run("cp -rp /data/web_static/releases/{}/web_static/*\
        /data/web_static/releases/{}/".format(name[:-4], name[:-4]))

    run("rm -rf /data/web_static/releases/{}/web_static/".format(name[:-4]))
    result = run("rm /data/web_static/current")
    if result.failed:
        return False

    path = "/data/web_static/releases/{}".format(name[:-4])
    cmd = "ln -sf {} /data/web_static/current".format(path)
    result = run(cmd)
    if result.failed:
        return False
    return True
       
   
