#!/usr/local/bin/python
import logging
import subprocess


def use_logging(level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if level == "warn":
                logging.warn("%s is running" % func.__name__)
            elif level == "error":
                logging.error("%s is running" % func.__name__)
            return func(*args)
        return wrapper

    return decorator


@use_logging(level="error")
def foo(name='foo'):
    print("i am %s" % name)


foo()
subprocess.call('w', shell=True)
