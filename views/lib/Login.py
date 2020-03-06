# -*- coding: UTF-8 -*-

from functools import wraps
from flask import session,url_for, redirect
from loghandle import *

def logincheck(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            if session.has_key('login'):
                if session['login'] == 'loginsuccess':
                    return f(*args, **kwargs)
                else:
                    return redirect(url_for('Login'))

            else:

                return redirect(url_for('Login'))
        except Exception, e:
            Log().exception("error")
            return redirect(url_for('Error'))

    return wrapper
