from django.http import HttpResponse
from django.shortcuts import render
from smartadmin.models import AdminInfo
import re

# Create your views here.


def admin(request):
    return render(request, '/login')


def login(request):
    if request.session.has_key('adminid'):
        userid = request.session['adminid']
        if request.session.session_key == AdminInfo.objects.get(adminid=userid).session_key:
            response = HttpResponse(render(request, 'adminindex.html', {"userid": userid}))
            _add_to_header(response, 'Cache-Control', 'no-store')
            _add_to_header(response, 'Cache-Control', 'no-cache')
            _add_to_header(response, 'Pragma', 'no-store')
            return response
        else:
            return render(request, 'login.html', {'Message' : 'Session terminated!'})
    else:
        return render(request, 'login.html')


def _add_to_header(response, key, value):
    if response.has_header(key):
        values = re.split(r'\s*,\s*', response[key])
        if not value in values:
            response[key] = ', '.join(values + [value])
    else:
        response[key] = value


def register(request):
    return render(request, 'register.html')


def logout(request):
    try:
        del request.session['adminid']
        return render(request, 'login.html', {'Message':'You have been logged out successfully!!!'})
    except:
        pass
        return render(request, 'login.html', {'Message':'You cannot logout without logging in!'})


def update(request):
    first_name = request.POST['name1']
    last_name = request.POST['name2']
    sex = request.POST['sex']
    aadhaar = request.POST['aadhaar']
    mobile = request.POST['mobile']
    ad1 = request.POST['ad1']
    ad2 = request.POST['ad2']
    city = request.POST['city']
    pin = request.POST['pin']
    pass1 = request.POST['pass1']

    Admin_info_object = AdminInfo()
    Admin_info_object.first_name = first_name
    Admin_info_object.last_name = last_name
    Admin_info_object.sex = sex
    Admin_info_object.adhaar = aadhaar
    Admin_info_object.mobile_no = mobile
    Admin_info_object.address_l1 = ad1
    Admin_info_object.address_l2 = ad2
    Admin_info_object.city = city
    Admin_info_object.pin_code = pin
    Admin_info_object.password = pass1

    Admin_info_object.save()

    return render(request, 'adminindex.html', {'Message': 'Admin Registered Successfully!!!'})
