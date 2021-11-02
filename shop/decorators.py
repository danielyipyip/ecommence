from django.shortcuts import redirect

def allowed_users(allowed_roles=[]):
    def decor(view_func):
        def inner(request, *args, **kwargs):
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name #only 1 role for now
                if group in allowed_roles:
                    return view_func(request, *args, **kwargs)
            else: #i.e. customers
                return redirect('shop:unauthorized')
        return inner
    return decor