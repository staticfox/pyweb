import pysrvx.srvx
import sys
import traceback

from flask import g
from functools import wraps
from gamesurge.utils import get_services

""" Return 401 if the user does not have access """
def access(a):
    def decorator(func):
        @wraps(func)
        def modified_func(*args, **kwargs):
            """ TODO: Check ACL """
            if True: #current_user.access < a:
                return "You do not have access to view this page"
            return func(*args, **kwargs)
        return modified_func
    return decorator

""" Catch SrvX exceptions """
def requiresrvx(app):
    def decorator(func):
        @wraps(func)
        def modified_func(*args, **kwargs):
            try:
                get_services(app).test_srvx()
                return func(*args, **kwargs)
            except (pysrvx.srvx.AuthenticationError,
                    pysrvx.srvx.ConnectionError,
                    pysrvx.srvx.NotConnected,
                    pysrvx.srvx.QServerSecurityViolation):
                return("Services are currently unavailable")
            except Exception as e:
                print("Error processing {}: <pre>{}</pre>".format(func.__name__, traceback.format_exc()), file=sys.stderr, flush=True)
                return("An error has occured, please try again later")
        return modified_func
    return decorator
