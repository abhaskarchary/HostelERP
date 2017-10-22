import re
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.http import HttpResponse
from .models import EmployeeInfo
from payfees.views import deduct_fees
from Inventory.views import *
from student.models import Studentinfo, message, Notice
import datetime
# from payfees.models import TransactionDetails
from Room.models import Room
from payfees.models import Fees
from transactions.models import Transaction_Details
# Create your views here.


def manager(request):
    return redirect('/login/')


def login(request):
    if request.session.has_key('userid'):
        userid = request.session['userid']
        if request.session.session_key == EmployeeInfo.objects.get(empid=userid).session_key:
            response = HttpResponse(render(request, 'index.html', {"userid": userid}))
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
    if request.session.has_key('userid'):
        userid = request.session['userid']
        if request.session.session_key == EmployeeInfo.objects.get(empid=userid).session_key:
            return render(request, 'registration1/register.html')
        else:
            return render(request, 'login.html', {'Message': 'Session terminated!'})
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

# """ No longer needed: Made Combined Login """
# def startsession(request):
#     userid = request.POST['userid']
#     userpass = request.POST['userpass']
#     try:
#         [object] = EmployeeInfo.objects.filter(empid = userid, password = userpass)
#         if object.first_name != "" and object.employee_type == "manager":
#             request.session['userid'] = userid
#             attr = {'userid': userid}
#             context = {'attr': attr}
#             if not request.session.session_key:
#                 request.session.save()
#             EmployeeInfo.objects.filter(empid=userid, password=userpass).update(session_key = request.session.session_key)
#             return redirect('/manager/login/')
#         else: return render(request, 'login.html', {'Message': 'Error Code 1.1 : Invalid Userid or password!!!'})
#     except:
#         pass
#     return render(request, 'login.html', {'Message':'Error Code 1.2 : Invalid Userid or password!!!'})


def viewempdata(request):
    if request.session.has_key('userid'):
        userid = request.session['userid']
        if request.session.session_key == EmployeeInfo.objects.get(empid=userid).session_key:
            return render(request, 'displayaccounts.html', {'Employee': EmployeeInfo.objects.all()})
        else:
            return render(request, 'login.html', {'Message': 'Session terminated!'})
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

    return render(request, 'index.html', {'Message': 'Employee Registered Successfully!!!'})


def pay_init_fees(request, stu_id):
    last_booking = Studentinfo.objects.all().order_by('sid').last()

    stu = Studentinfo.objects.filter(sid = stu_id).values()
    stu1 = Studentinfo.objects.filter(sid = stu_id).values()
    initial_bal = float(request.POST['initial_balance'])
    #stu['balance'] = stu['balance'] + initial_bal
    #stu.update(balance = (stu['balance'] + initial_bal))
    for s in stu:
        #s.update(balance = (s['balance'] + initial_bal))
        room_number = Studentinfo.objects.get(sid = stu_id).room
        room_type = Room.objects.get(room_number = room_number).roomType
        room = Fees.objects.filter(room_type = room_type).values()
        for rt in room:
            bal = (rt['fees'])+rt['security_money']-initial_bal
        # bal = s['balance'] + initial_bal
        #s['balance'] = s['balance'] + initial_bal
    stu1.update(balance = bal)

    #return HttpResponse("<h1>" +"Fee paid successfully"+ "<h1>")

    #return render(request, 'registration/registration_complete.html')
    return render(request, 'index.html', {'Message': 'Student Registered Successfully!!!'})
    # return redirect('/manager/login/', {'Message': 'Student Registered Successfully'})
    #return HttpResponse("<h1>"+stu.sid+"<h1>")
    #return

# def deduct_fees(request):
#     stu = Studentinfo.objects.all().values()
#     y = datetime.date.today().year
#     m = datetime.date.today().month
#     d = datetime.date.today().month
#     if d>1 and d<5:
#         for s in stu:
#             # total = s['total_dues']
#             # bal = s['balance']
#             # fine = s['running_fine']
#             # due = s['running_dues']
#             remaining_dues=s['running_dues']
#             remaining_fine=s['running_fine']
#             remaining_total_dues=s['total_dues']
#             remaining_bal=s['balance']
#             stu1 = Studentinfo.objects.filter(sid = s['sid']).values()
#             if((s['running_dues']>0.0 or s['running_fine']>0.0) and s['balance']>0.0):
#                 if s['total_dues']<=s['balance']:
#                     remaining_dues = 0.0
#                     remaining_fine = 0.0
#                     remaining_bal = s['balance'] - s['total_dues']
#                 elif(s['total_dues']>s['balance']):
#                     if(s['running_dues']>s['balance']):
#                         remaining_dues=s['running_dues']-s['balance']
#                         remaining_fine=s['running_fine']
#                         remaining_bal=0.0
#                     else:
#                         remaining_dues=0.0
#                         remaining_bal=s['balance']-s['running_dues']
#                         remaining_fine=s['running_fine']-remaining_bal
#                         remaining_bal=0.0
#                 remaining_total_dues = remaining_dues + remaining_fine
#             stu1.update(running_dues = remaining_dues, running_fine = remaining_fine ,
#                     balance = remaining_bal, total_dues = remaining_total_dues)
#     return HttpResponse("<h1>Fees paid successfully<h1")


def all_transactions(request):
    if request.session.has_key('userid'):
        userid = request.session['userid']
        if request.session.session_key == EmployeeInfo.objects.get(empid=userid).session_key:
            return render(request, 'display_transactions.html', {'all_transactions': Transaction_Details.objects.all()})
        else:
            return render(request, 'login.html', {'Message': 'Session terminated!'})
    else:
        return render(request, 'error.html')
    return render(request, 'display_transactions.html', {'all_transactions':Transaction_Details.objects.all().order_by('-transaction_id')})


def all_messages(request):
    if request.session.has_key('userid'):
        userid = request.session['userid']
        if request.session.session_key == EmployeeInfo.objects.get(empid=userid).session_key:
            return render(request, 'Inbox/inbox.html', {'context': message.objects.all().order_by('-time_sent')})
        else:
            return render(request, 'login.html', {'Message': 'Session terminated!'})
    else:
        return render(request, 'error.html')


def issue_notice(request):
    if request.session.has_key('userid'):
        userid = request.session['userid']
        if request.session.session_key == EmployeeInfo.objects.get(empid=userid).session_key:
            return render(request, 'Inbox/notice.html')
        else:
            return render(request, 'login.html', {'Message': 'Session terminated!'})
    else:
        return render(request, 'error.html')


def send_notice(request):
    if request.session.has_key('userid'):
        userid = request.session['userid']
        if request.session.session_key == EmployeeInfo.objects.get(empid=userid).session_key:
            new_notice = Notice()
            new_notice.type_of_notice = request.POST['subject']
            new_notice.body_of_notice = request.POST['body']
            new_notice.save()
            return render(request, 'index.html', {'userid': userid,'Message': 'Notice Sent Successfully!'} )
        else:
            return render(request, 'login.html', {'Message': 'Session terminated!'})
    else:
        return render(request, 'error.html')


def deactivate_student(request):
    if request.session.has_key('userid'):
        userid = request.session['userid']
        if request.session.session_key == EmployeeInfo.objects.get(empid=userid).session_key:
            return render(request, 'Inbox/deleteStudent.html', {'context': Studentinfo.objects.all(), 'rooms':Room.objects.filter(vacancy__gt=0)})
        else:
            return render(request, 'login.html', {'Message': 'Session terminated!'})
    else:
        return render(request, 'error.html')


def deactivate(request, sid, op):
    if request.session.has_key('userid'):
        userid = request.session['userid']
        if request.session.session_key == EmployeeInfo.objects.get(empid=userid).session_key:
            student = Studentinfo.objects.get(sid=sid)
            if op == 'd':
                student.active = False
                room = Room.objects.get(room_number=student.room.room_number)
                room.vacancy = str(int(room.vacancy)+1)
                room.save()
                # student.room = None
            else:
                student.active = True
                room_number = request.POST['room']
                student.room = Room.objects.get(room_number=room_number)
                student.room.vacancy = str(int(student.room.vacancy)-1)
                student.room.save()
            student.save()
            return redirect('/manager/deactivate_student/')
        else:
            return render(request, 'login.html', {'Message': 'Session terminated!'})
    else:
        return render(request, 'error.html')


def userpanel(request):
    return render(request, 'panel.html')


def account(request):
    return render(request, 'account.html')


def fees(request):
    return render(request, 'fees.html')


def room(request):
    return render(request, 'room.html')


def inventory(request):
    return render(request, 'inventory.html')