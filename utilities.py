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


def find_between( s, first, last ):
    """
    get the string between two characters
    """
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


def createThumbnail(user):
    """ Create a thumbnail of image and save it as user image """
    from io import StringIO
    from PIL import Image
    IMAGE_WIDTH = 300
    IMAGE_HEIGHT = 300
    try:
        if not user.image:
            return

        image = Image.open(user.image.file).convert('RGB')
        # If the image is smaller than 300 x 300, don't bother creating a thumbnail
        width, height = image.size
        if width < IMAGE_WIDTH and height < IMAGE_HEIGHT:
            return

        # Crop as little as possible to square, keeping the center.
        if width > height:
            aspect = height / float(width)
            width = IMAGE_WIDTH
            height = int(width * aspect)
        else:
            aspect = width / float(height)
            height = IMAGE_HEIGHT
            width = int(height * aspect)

        # overwrite image file
        resized = image.resize((width, height), Image.ANTIALIAS)
        try:
            save_path = user.image.path
            ar = save_path.split('.')
            if len(ar) == 2:
                save_path = ar[0] + 's.' + ar[1]
            resized.save(save_path, quality=90)
            user.image = save_path.replace(settings.MEDIA_ROOT + '/', '')
            user.save()
        except Exception as e:
            print("image save error")
            print(str(e))
        return
    except Exception as e:
        print(str(e))
        return
