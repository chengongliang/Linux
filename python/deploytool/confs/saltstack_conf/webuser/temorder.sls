/home/webuser/tem-order/:
  file.recurse:
    - source: salt://files/tem-order/
    - makedir: True
    - include_empty: True
    - clean: True
/home/webuser/tem-order/bin/:
  file.directory:
    - dir_mode: 755
    - file_mode: 755
    - recurse:
      - mode
stop:
  cmd.run:
    - name: /home/webuser/tem-order/bin/shutdown.sh
    - user: root
start:
  cmd.run:
    - name: /home/webuser/tem-order/bin/startup.sh
    - user: root
