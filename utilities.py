# -*- coding: utf-8 -*-
import logging
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import logout


def groups_required(login_url='/', *names):
    """
    Decorator for views that require user to be a member of a group, redirecting to login_url page.
    """
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            if "no_permission" in request.session:
                del request.session["no_permission"]
            if not request.user.is_authenticated():
                messages.error(request, u'Please login')
                return HttpResponseRedirect(login_url)
            user = request.user
            if user.groups.filter(name__in=names).exists():
                return view(request, *args, **kwargs)
            else:
                logout(request)
                messages.error(request, u'You do not have permission')
                request.session["no_permission"] = True
                return HttpResponseRedirect(login_url)
        return wrapper
    return decorator

