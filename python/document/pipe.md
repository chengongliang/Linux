###管道
```
    #!/usr/bin/python
    from subprocess import Popen, PIPE
    
    p1 = Popen(['ps','ef'],stdout=PIPE)
    p2 = Popen(['grep','SCREEN'],stdin=p1.stdout,stdout=PIPE,stderr=PIPE)
    result = p2.stdout
    for i in result:
        print i
```
