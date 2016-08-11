/home/wwwroot/:
  file.recurse:
    - source: salt://files/order/
    - file_mode: 644
    - dir_mode: 755
    - makedir: True
    - include_empty: True
    - clean: True
