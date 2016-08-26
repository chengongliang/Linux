from fabric.api import run
from fabric.api import env

env.user = 'test'
env.password = 'test'

env.hosts = ['localhost','192.168.1.6']

def host_type():
    run('uname -s')
    run('date')
