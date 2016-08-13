/home/webuser/tem-order/:
  file.recurse:
    - source: salt://files/tem-order/
    - file_mode: 744
    - dir_mode: 755
    - makedir: True
    - include_empty: True
    - clean: True
stop:
  cmd.run:
    - name: /home/webuser/tem-order/bin/shutdown.sh
    - user: root
start:
  cmd.run:
    - name: /home/webuser/tem-order/bin/startup.sh
    - user: root
