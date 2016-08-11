/home/webuser/:
  file.recurse:
    - source: salt://files/temorder/
    - file_mode: 644
    - dir_mode: 755
    - makedir: True
    - include_empty: True
    - clean: True
