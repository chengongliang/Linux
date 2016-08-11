/home/wwwroot/www.iclassedu.com/:
  file.recurse:
    - source: salt://files/www.iclassedu.com/
    - file_mode: 644
    - dir_mode: 755
    - makedir: True
    - include_empty: True
    - clean: True
