import re
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.http import HttpResponse
from .models import EmployeeInfo
from payfees.views import deduct_fees
from student.models import Studentinfo
import datetime
from payfees.models import TransactionDetails
# Create your views here.


def manager(request):
    return redirect('/manager/login/')


def login(request):
    if request.session.has_key('userid'):
        userid = request.session['userid']
        response = HttpResponse(render(request, 'loggedin.html', {"userid": userid}))
        _add_to_header(response, 'Cache-Control', 'no-store')
        _add_to_header(response, 'Cache-Control', 'no-cache')
        _add_to_header(response, 'Pragma', 'no-store')
        return response
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
    if request.session.has_key('userid'):
        return render(request, 'registration1/register.html')
    else:
        return render(request, 'error.html')


def logout(request):
    try:
        del request.session['userid']
        return render(request, 'login.html', {'Message': 'You have been logged out successfully!'})
    except:
        pass
        return render(request, 'login.html', {'Message': 'You cannot logout without logging in!'})
    #return render(request, 'login.html', {'Message': 'You have been logged out successfully!'})


def startsession(request):
    userid = request.POST['userid']
    userpass = request.POST['userpass']
    try:
        object = EmployeeInfo.objects.get(empid = userid, password = userpass)
        if object.first_name != "" and object.employee_type == "manager":
            request.session['userid'] = userid
            attr = {'userid': userid}
            context = {'attr': attr}
            return redirect('/manager/login/')
        else: return render(request, 'login.html', {})
    except:
        pass
    return render(request, 'login.html', {'Message':'Error Code 1 : Invalid Userid or password!!!'})


def viewempdata(request):
    if request.session.has_key('userid'):
        return render(request, 'displayaccounts.html', {'Employee':EmployeeInfo.objects.all()})
    else:
        return render(request, 'error.html')


def update(request):
    first_name = request.POST['name1']
    last_name = request.POST['name2']
    sex = request.POST['sex']
    aadhaar = request.POST['aadhaar']
    mobile = request.POST['mobile']
    pname = request.POST['pname']
    pmobile = request.POST['pmobile']
    ad1 = request.POST['ad1']
    ad2 = request.POST['ad2']
    city = request.POST['city']
    pin = request.POST['pin']
    pass1 = request.POST['pass1']

    Manager_info_object = EmployeeInfo()
    Manager_info_object.first_name = first_name
    Manager_info_object.last_name = last_name
    Manager_info_object.sex = sex
    Manager_info_object.adhaar = aadhaar
    Manager_info_object.mobile_no = mobile
    Manager_info_object.parent_name = pname
    Manager_info_object.parent_mobile = pmobile
    Manager_info_object.address_l1 = ad1
    Manager_info_object.address_l2 = ad2
    Manager_info_object.city = city
    Manager_info_object.pin_code = pin
    Manager_info_object.password = pass1

    Manager_info_object.save()

    return HttpResponse("<H1>Registered successfully</H1>")

def deduct_fees(request):
    stu = Studentinfo.objects.all().values()
    y = datetime.date.today().year
    m = datetime.date.today().month
    d = datetime.date.today().month
    if d>1 and d<5:
        for s in stu:
            # total = s['total_dues']
            # bal = s['balance']
            # fine = s['running_fine']
            # due = s['running_dues']
            remaining_dues=s['running_dues']
            remaining_fine=s['running_fine']
            remaining_total_dues=s['total_dues']
            remaining_bal=s['balance']
            stu1 = Studentinfo.objects.filter(sid = s['sid']).values()
            if((s['running_dues']>0.0 or s['running_fine']>0.0) and s['balance']>0.0):
                if s['total_dues']<=s['balance']:
                    remaining_dues = 0.0
                    remaining_fine = 0.0
                    remaining_bal = s['balance'] - s['total_dues']
                elif(s['total_dues']>s['balance']):
                    if(s['running_dues']>s['balance']):
                        remaining_dues=s['running_dues']-s['balance']
                        remaining_fine=s['running_fine']
                        remaining_bal=0.0
                    else:
                        remaining_dues=0.0
                        remaining_bal=s['balance']-s['running_dues']
                        remaining_fine=s['running_fine']-remaining_bal
                        remaining_bal=0.0
                remaining_total_dues = remaining_dues + remaining_fine
            stu1.update(running_dues = remaining_dues, running_fine = remaining_fine ,
                    balance = remaining_bal, total_dues = remaining_total_dues)
    return HttpResponse("<h1>Fees paid successfully<h1")


def all_transactions(request):
    return render(request, 'display_transactions.html', {'all_transactions':TransactionDetails.objects.all()})