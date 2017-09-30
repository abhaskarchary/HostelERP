from django.shortcuts import render, redirect
from .models import Studentinfo
from payfees.models import Fees
from Room.models import Room
from django.http import HttpResponse
import re
from payfees.models import TransactionDetails

# Create your views here.


def accountlogs(request, stu_id):
    return render(request, 'accountlogs.html', {'student_transaction':TransactionDetails.objects.filter(sid = stu_id)})


def messageroom(request):
    return render(request, 'messageroom.html')


def studentinfo(request):
    if request.session.has_key('userid'):
        return render(request, 'studentinfo/studentinfo.html', {'context':Studentinfo.objects.all()})
    else:
        return render(request, 'error.html')


def form(request):
    if request.session.has_key('userid'):
        return render(request, 'registration/form1.html', {'context':Room.objects.filter(room_number__gt=0)})
    else:
        return render(request, 'error.html')


def change_info(request):
    if request.session.has_key('userid'):
        sid= request.POST['student_id']
        [context] = Studentinfo.objects.filter(sid=sid)
        return render(request, 'registration/change_details.html', {'student': context,'rooms':Room.objects.filter(vacancy__gt=0)})
    return render(request, 'error.html')


def update(request,sid = None):
    first_name = request.POST['name1']
    last_name = request.POST['name2']
    sex = request.POST['sex']
    adhaar = request.POST['adhaar']
    mobile = request.POST['mobile']
    pname = request.POST['pname']
    pmobile = request.POST['pmobile']
    ad1 = request.POST['ad1']
    ad2 = request.POST['ad2']
    city = request.POST['city']
    pin = request.POST['pin']
    gname = request.POST['gname']
    gmobile = request.POST['gmobile']
    iname = request.POST['iname']
    hname = request.POST['hname']
    hmobile = request.POST['hmobile']
    room_number = request.POST['room']
            #print(first_name, last_name)
    if sid is None:
        student_info_object = Studentinfo()
        student_info_object.balance = 0.0
        student_info_object.running_dues = 0.0
        student_info_object.running_fine = 0.0
        student_info_object.refundable_security = 0.0
        student_info_object.total_dues = 0.0
    else:
        [student_info_object] = Studentinfo.objects.filter(sid=sid)
    student_info_object.first_name = first_name
    student_info_object.last_name = last_name
    student_info_object.sex = sex
    student_info_object.adhaar = adhaar
    student_info_object.mobile_no = mobile
    student_info_object.parent_name = pname
    student_info_object.parent_mobile = pmobile
    student_info_object.address_l1 = ad1
    student_info_object.address_l2 = ad2
    student_info_object.city = city
    student_info_object.pin_code = pin
    student_info_object.guardian_name = gname
    student_info_object.guardian_mobile = gmobile
    student_info_object.institution_name = iname
    student_info_object.hod_name = hname
    student_info_object.hod_mobile = hmobile
    if room_number != 'None':
        [student_info_object.room] = Room.objects.filter(room_number=room_number)
    if int(student_info_object.room.vacancy) < 1 and room_number != 'None':
        return redirect('/student/register')
    student_info_object.save()

    """Changes discarded"""
    # due = Dues()
    #
    # last_booking = Studentinfo.objects.all().order_by('sid').last()
    #
    # due.sid = last_booking.sid
    # due.name = last_booking.first_name +" "+ last_booking.last_name
    # due.fees = 0.0
    # due.securitymoney = 0.0
    # due.fine = 0.0
    # due.totaldue = 0.0
    # due.save()
    #
    # attr = {
    #     'Student id': student_info_object.sid,
    #     'First name':student_info_object.first_name,
    #     'Last name':student_info_object.last_name,
    #     'Sex':student_info_object.sex,
    #     'Adhaar Card no.':student_info_object.adhaar,
    #     'Mobile':student_info_object.mobile_no,
    #     'Parent Name':student_info_object.parent_name,
    #     'Parent Mobile':student_info_object.parent_mobile,
    #     'Address line 1':student_info_object.address_l1,
    #     'Address line 2':student_info_object.address_l2,
    #     'City':student_info_object.city,
    #     'Pin Code':student_info_object.pin_code,
    #     'Guardian Name':student_info_object.guardian_name,
    #     'Guardian Mobile':student_info_object.guardian_mobile,
    #     'Registration Date':student_info_object.registration_date,
    #     'Institution Name':student_info_object.institution_name,
    #     'HOD Name':student_info_object.hod_name,
    #     'HOD Mobile':student_info_object.hod_mobile
    # }
    # context = {'attr':attr}

    if sid is not None:
        return render(request, 'registration/registration_complete.html')

    l=[]
    fee = Fees.objects.filter(id = 1).values()
    for f in fee:
        l = [f['security_money']]
    context = {'attr': l}
    return render(request, 'registration/pay_initial_fees.html',context)


def pay_init_fees(request):
    last_booking = Studentinfo.objects.all().order_by('sid').last()

    stu = Studentinfo.objects.filter(sid = last_booking.sid).values()
    stu1 = Studentinfo.objects.filter(sid = last_booking.sid).values()
    initial_bal = float(request.POST['initial_balance'])
    #stu['balance'] = stu['balance'] + initial_bal
    #stu.update(balance = (stu['balance'] + initial_bal))
    for s in stu:
        #s.update(balance = (s['balance'] + initial_bal))
        bal = s['balance'] + initial_bal
        #s['balance'] = s['balance'] + initial_bal
    stu1.update(balance = bal)
    #return HttpResponse("<h1>" +"Fee paid successfully"+ "<h1>")

    return render(request, 'registration/registration_complete.html')
    #return HttpResponse("<h1>"+stu.sid+"<h1>")
    #return


def change_std_info(request):
    return render(request, 'studentinfo/changes.html')

def startsession(request):
    stdntid = request.POST['userid']
    userpass = request.POST['userpass']
    try:
        [object] = Studentinfo.objects.filter(sid = stdntid, password = userpass)
        if object.first_name != "":
            request.session['stdntid'] = stdntid
            attr = {'stdntid': stdntid}
            context = {'attr': attr}
            return redirect('/student/login/')
        else: return render(request, 'student_zone/login.html', {'Error':'Error Code 1 : Invalid Userid or password!!!'})
    except:
        pass
    return render(request,'student_zone/login.html', {'Message':'Error Code 1 : Invalid Userid or password!!!'})


def login(request):
    if request.session.has_key('stdntid'):
        stdntid = request.session['stdntid']
        context = Studentinfo.objects.get(sid=stdntid)
        response = HttpResponse(render(request, 'student_zone/loggedin.html', {'context': context}))
        _add_to_header(response, 'Cache-Control', 'no-store')
        _add_to_header(response, 'Cache-Control', 'no-cache')
        _add_to_header(response, 'Pragma', 'no-store')
        return response
    else:
        return render(request, 'student_zone/login.html')


def _add_to_header(response, key, value):
    if response.has_header(key):
        values = re.split(r'\s*,\s*', response[key])
        if not value in values:
            response[key] = ', '.join(values + [value])
    else:
        response[key] = value


def logout(request):
    try:
        del request.session['stdntid']
        return render(request, 'student_zone/login.html', {'Message': 'You have been logged out successfully!'})
    except:
        pass
        return render(request, 'student_zone/login.html', {'Message': 'You cannot logout without logging in!'})


def change_password(request, sid):
    if request.session.has_key('stdntid'):
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        student_object = Studentinfo.objects.get(sid=sid)
        if pass1 == pass2:
            student_object.password = pass1
            student_object.save()
        else:
            #url = '<h1>Password Do no match </h1><br><a href="/student/changepass/'+str(sid)+'">Enter Again</a>'
            #return HttpResponse(url)
            return render(request, 'student_zone/changepass.html', {'context': sid,'Message':'Error Code 2 : Passwords do not match'})
        return render(request, 'student_zone/loggedin.html', {'context':student_object,'Message':'Password changed successfully'})
    return render(request, 'error.html')


def change_pass(request, sid):
    if request.session.has_key('stdntid'):
        return render(request, 'student_zone/changepass.html', {'context':sid,'Message':'Change Password'})
    return render(request, 'error.html')