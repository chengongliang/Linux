from fabric.api import run
from fabric.api import env

env.user = 'test'
env.password = 'test'
env.hosts = ['localhost']

def host_type():
    run('uname -s:echo $USER')

def check_var():
    run("""LIVE_VER=`curl -s http://192.168.11.110/deploy/livever`
           LIVE_WP=/var/www/deploy/wordpress-$LIVE_VER
           test -d $LIVE_WP && echo "$LIVE_WP is exists"
        """)
