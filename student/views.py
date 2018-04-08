from django.shortcuts import render, redirect

from smartadmin.models import AdminInfo
from .models import Studentinfo, message, Notice, ContactUsMessage
from manager.models import EmployeeInfo
from payfees.models import Fees
from Room.models import Room
from django.http import HttpResponse
import re
from datetime import datetime
import json
from transactions.models import Transaction_Details
# from payfees.models import TransactionDetails

# Create your views here.


#def accountlogs(request, stu_id):
#    if checkstdnt(request):
#        if checkstdntsession(request):
#            return render(request, 'accountlogs.html',{'student_transaction': Transaction_Details.objects.filter(sid=stu_id)})
#        else:
#            return render(request, 'error.html')
#    else:
#            return render(request, 'error.html')


#def view_balance_fee(request, stu_id):
#    if checkstdnt(request):
#        if checkstdntsession(request):
#            stu = Studentinfo.objects.filter(sid=stu_id)
#            if not stu.exists():
#                return HttpResponse("<h3>Student ID not found</h3>")
#            b = Studentinfo.objects.get(sid=stu_id)
#            # print(b.sid + " " + str(b.room))
#            room_number = b.room
#            room_type = Room.objects.get(room_number=room_number).roomType
#            room = Fees.objects.filter(room_type=room_type).values()
#            for rt in room:
#                rent_per_installment = rt['fees'] / rt['parts_per_year']
#                # if (b.balance > installment):
#                #     b1 = 1
#                #     total = installment + b.running_fine
#                # else:
#                #     b1 = 0
#                #     total = b.balance + b.running_fine
#                minimum_pay = b.total_dues
#                # maximum_pay=b.balance
#            l1 = [b.sid, b.first_name + " " + b.last_name]
#            # l = {'running_dues':b.running_dues, 'running_fine':b.running_fine, 'total_dues': b.total_dues,'balance': b.balance, 'installment': installment, 'b1':b1}
#            l = [b.next_installment, b.running_fine, minimum_pay, b.balance, rent_per_installment, b.next_due_date]
#            context = {'attr': l, 'attr1': l1}
#            return render(request, 'show_student_dues.html', context)
#        else:
#            return render(request, 'error.html')
#    else:
#            return render(request, 'error.html')


def messageroom(request):
    if checkstdnt(request):
        if checkstdntsession(request):
            return render(request, 'messageroom.html')
        else:
            return render(request, 'error.html')
    else:
            return render(request, 'error.html')


def studentinfo(request):
    if checkuser(request):
        if checkusersession(request):
            return render(request, 'studentinfo/studentinfo.html', {'context':Studentinfo.objects.all()})
        else:
            return render(request, 'error.html')
    elif checkadmin(request):
        if checkadminsession(request):
            return render(request, 'studentinfo/studentinfo.html', {'context': Studentinfo.objects.all()})
        else:
            return render(request, 'error.html')
    else:
        return render(request, 'error.html')


def form(request):
    if checkuser(request):
        if checkusersession(request):
            return render(request, 'registration/form1.html', {'context': Room.objects.filter(vacancy__gt=0)})
        else:
            return render(request, 'error.html')
    else:
        return render(request, 'error.html')


def change_info(request):
    if checkuser(request):
        if checkusersession(request):
            sid = request.POST['student_id']
            [context] = Studentinfo.objects.filter(sid=sid)
            return render(request, 'registration/change_details.html', {'student': context, 'rooms': Room.objects.filter(vacancy__gt=0)})
        else:
            return render(request, 'error.html')
    return render(request, 'error.html')


def update(request,sid = None):
    flag=0
    first_name = request.POST['name1']
    last_name = request.POST['name2']
    blood_grp = request.POST['blood_grp']
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

    initial_bal=0
    p_mode=""
    particulars=""
    cheque_no=""
    yearlyfees=0
    security_money=0
    if sid is  None:
        initial_bal = float(request.POST['initial_balance'])
        p_mode = (request.POST['payment_mode'])
        particulars = request.POST['particulars']
        cheque_no = request.POST['cheque_no']
        yearlyfees=float(request.POST['yearlyfees'])
        security_money=float(request.POST['security_money'])

    # hname = request.POST['hname']
    # hmobile = request.POST['hmobile']
    # if sid is None:
    room_number = request.POST['vacant_room_list'].split()[0]

    room_type = Room.objects.get(room_number=room_number).roomType
    room = Fees.objects.filter(room_type=room_type).values()

    bal=yearlyfees+security_money-initial_bal
    for rt in room:
        next_installment_amount = 0.0
        fee_per_installment = rt['fees'] / rt['parts_per_year']
        # bal = (rt['fees'])+rt['security_money']-initial_bal
        fee_paid = initial_bal - rt['security_money']
        print(fee_paid)
        no_of_installments_cleared = int(fee_paid / fee_per_installment)
        print(no_of_installments_cleared)
        if (bal > 0):
            next_installment_amount_cleared = fee_paid - no_of_installments_cleared * fee_per_installment
            print(next_installment_amount_cleared)
            next_installment_amount = fee_per_installment - next_installment_amount_cleared
            print(next_installment_amount)
        duration_bw_succ_installments = 12 / rt['parts_per_year']
        today = datetime.now()
        month = today.month
        next_installment_month = int(month + no_of_installments_cleared * duration_bw_succ_installments)
        if (next_installment_month > 12):
            next_installment_month = next_installment_month - 12
            next_due_date = str((today.year) + 1) + "-" + str(next_installment_month) + "-05"
        else:
            next_due_date = str(today.year) + "-" + str(next_installment_month) + "-05"
        d = datetime.strptime(next_due_date, "%Y-%m-%d").date()
    # fee = Fees.objects.filter(room_type=room_type).values()
    # init_bal=0
    # total=0
    # for f in fee:
    #     init_bal=f['fees']+f['security_money']
    #     total = (f['fees'] / f['parts_per_year']) + f['security_money']
    # print(room_number)
    # print(room_type)
            #print(first_name, last_name)
    if sid is None:
        flag=1
        student_info_object = Studentinfo()
        student_info_object.balance = bal
        student_info_object.running_dues = 0.0
        student_info_object.running_fine = 0.0
        student_info_object.refundable_security = 0.0
        student_info_object.total_dues = next_installment_amount
        student_info_object.next_due_date = d
        student_info_object.next_installment = next_installment_amount


        # sid=increment_id()


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

    # student_info_object.hod_name = hname
    # student_info_object.hod_mobile = hmobile
    if room_number != 'None':
        [new_room] = Room.objects.filter(room_number=room_number)

        # in case there is room change request increase the vacancy of old room by one
        try:
            old_room = student_info_object.room
            old_room.vacancy = str(int(old_room.vacancy) + 1)
            old_room.save()
        except:
            pass

        student_info_object.room = new_room
        new_room.vacancy = str(int(new_room.vacancy)-1)
        new_room.save()
    elif int(student_info_object.room.vacancy) < 1 and room_number != 'None':
        return redirect('/student/register')
    student_info_object.save()

    if flag==1:
        last_booking = Studentinfo.objects.all().order_by('sid').last()
        sid=""
        sid=last_booking.sid
        print(sid)
        transaction = Transaction_Details()
        [transaction.sid]=Studentinfo.objects.filter(sid=sid)
        transaction.transaction_date = datetime.now()
        transaction.payment_mode = p_mode
        transaction.fees_paid = initial_bal
        transaction.fine_paid = 0.0
        transaction.remaining_fees = 0.0
        transaction.remaining_fine = 0.0
        transaction.remaining_total = bal
        transaction.particulars = particulars
        transaction.cheque_dd_no = cheque_no
        transID = transaction.transaction_id
        print("Latest transaction id= " + transID)
        transaction.save()

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
        if flag==1:
            return render(request, 'tempacc.html', {'Message': 'Student Registered Successfully!!!', 'trans_id': transID})
        return render(request, 'tempacc.html', {'Message': 'Student Registered Successfully!!!', 'trans_id': ""})

    # l={}
    # last_booking = Studentinfo.objects.all().order_by('sid').last()
    # fee = Fees.objects.filter(room_type = room_type).values()
    # max_pay=0
    # for f in fee:
    #     total = (f['fees']/f['parts_per_year']) + f['security_money']
    #     max_pay=f['fees']+f['security_money']
    #     # l = [f['security_money'],f['fees'],total]
    #     l=[f['fees'], f['security_money'], total, max_pay]
    #     l1=[last_booking.sid, room_number, room_type, f['parts_per_year'] ]
    # context = {'attr': l, "attr1":l1}
    # # fee = Fees.objects.get(room_type = room_type).values()
    return render(request, 'tempacc.html', {'Message': 'Student Registered Successfully!!!', 'trans_id': transID})


def get_init_pay(request):
    room_number = request.GET["room"]
    room_type = Room.objects.get(room_number=room_number).roomType
    fee = Fees.objects.filter(room_type=room_type).values()
    data={}
    for f in fee:
        total = (f['fees']/f['parts_per_year']) + f['security_money']
        max_pay=f['fees']+f['security_money']
        # l = [f['security_money'],f['fees'],total]
        l=[f['fees'], f['security_money'], total, max_pay, room_number, f['parts_per_year']]
        l1=[room_number, room_type, f['parts_per_year'] ]
        data['fees']=f['fees']
        data['security_money']=f['security_money']
        data['total']=total
        data['max_pay']=max_pay
        data['room_number']=room_number
        #data['room_type']=room_type
        data['parts_per_year']=f['parts_per_year']
        print(data)
    return HttpResponse(json.dumps(data), content_type="application/json")


def pay_init_fees(request, stu_id):
    last_booking = Studentinfo.objects.all().order_by('sid').last()

    stu = Studentinfo.objects.filter(sid = stu_id).values()
    stu1 = Studentinfo.objects.filter(sid = stu_id).values()
    initial_bal = float(request.POST['initial_balance'])
    #stu['balance'] = stu['balance'] + initial_bal
    #stu.update(balance = (stu['balance'] + initial_bal))
    for s in stu:
        #s.update(balance = (s['balance'] + initial_bal))

        bal = s['balance'] + initial_bal
        #s['balance'] = s['balance'] + initial_bal
    stu1.update(balance = bal)
    #return HttpResponse("<h1>" +"Fee paid successfully"+ "<h1>")

    #return render(request, 'registration/registration_complete.html')
    return render(request, 'manager/loggedin.html', {'Message': 'Student Registered Successfully'})
    #return HttpResponse("<h1>"+stu.sid+"<h1>")
    #return


def change_std_info(request):
    return render(request, 'studentinfo/changes.html')

# """ No Longer Needed: Made Combined Login"""
# def startsession(request):
#     stdntid = request.POST['userid']
#     userpass = request.POST['userpass']
#     try:
#         [object] = Studentinfo.objects.filter(sid = stdntid, password = userpass)
#         if object.first_name != "":
#             request.session['stdntid'] = stdntid
#             attr = {'stdntid': stdntid}
#             context = {'attr': attr}
#             if not request.session.session_key:
#                 request.session.save()
#             Studentinfo.objects.filter(sid = stdntid, password = userpass).
# update(sessionkey = request.session.session_key)
#             #object.sessionkey = request.session.session_key
#             #object.save()
#             return redirect('/student/login/')
#         else: return render(request, 'student_zone/login.html',
# {'Error':'Error Code 1.1 : Invalid Userid or password!!!'})
#     except:
#         pass
#     return render(request,'student_zone/login.html', {'Message':'Error Code 1.2 : Invalid Userid or password!!!'})


def login(request):
    if checkstdnt(request):
        if checkstdntsession(request):
            b = Studentinfo.objects.get(sid=request.session['stdntid'])

            room_number = b.room
            room_type = Room.objects.get(room_number=room_number).roomType
            room = Fees.objects.filter(room_type=room_type).values()
            for rt in room:
                rent_per_installment = rt['fees'] / rt['parts_per_year']
                minimum_pay = b.total_dues
            l1 = [b.sid, b.first_name + " " + b.last_name]
            l = [b.next_installment, b.running_fine, minimum_pay, b.balance, rent_per_installment, b.next_due_date]
            context = {'context': b,'student_transaction': Transaction_Details.objects.filter(sid=request.session['stdntid']),'attr': l, 'attr1': l1}

            response = HttpResponse(render(request, 'stutempindex.html', context))
            _add_to_header(response, 'Cache-Control', 'no-store')
            _add_to_header(response, 'Cache-Control', 'no-cache')
            _add_to_header(response, 'Pragma', 'no-store')
            return response
        else:
            return render(request, 'login.html', {'Message': 'Session terminated'})
    else:
        return render(request, 'login.html')


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
        return render(request, 'login.html', {'Message': 'You have been logged out successfully!'})
    except:
        pass
        return render(request, 'login.html', {'Message': 'You cannot logout without logging in!'})


def change_password(request, sid):
    if checkstdnt(request):
        if checkstdntsession(request):
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']
            student_object = Studentinfo.objects.get(sid=sid)
            if pass1 == pass2:
                student_object.password = pass1
                student_object.save()
            else:
                return render(request, 'student_zone/changepass.html', {'context': sid,'Error':'true','Message':'Error Code 2 : Passwords do not match'})
            return render(request, 'stutempindex.html', {'context':student_object,'Error':'false','Message':'Password changed successfully'})
        else:
            return render(request, 'error.html')
    return render(request, 'error.html')


def change_pass(request, sid):
    if checkstdnt(request):
        if checkstdntsession(request):
            return render(request, 'student_zone/changepass.html', {'context': sid})
        else:
            return render(request, 'error.html')
    return render(request, 'error.html')


def send_message(request):
    if checkstdnt(request):
        if checkstdntsession(request):
            student_object = Studentinfo.objects.get(sid=request.session['stdntid'])
            new_message = message()
            new_message.sender = Studentinfo.objects.get(sid=request.session['stdntid'])
            new_message.type_of_message = request.POST['subject']
            new_message.body_of_message = request.POST['body']
            new_message.save()
            return render(request, 'stutempindex.html', {'context': student_object,'Message': 'Message Sent Successfully!!!'})
        else:
            return render(request, 'error.html')
    return render(request, 'error.html')


def noticebox(request):
    if checkstdnt(request):
        if checkstdntsession(request):
            context = Notice.objects.all().order_by('-time_sent')
            return render(request, 'student_zone/all_notice.html', {'context': context})
        else:
            return render(request, 'error.html')
    return render(request, 'error.html')


def notice(request, nid):
    if checkstdnt(request):
        if checkstdntsession(request):
            context = Notice.objects.get(notice_id=nid)
            return render(request, 'student_zone/notice.html', {'context': context})
        else:
            return render(request, 'error.html')
    return render(request, 'error.html')


def profile(request):
    if checkstdnt(request):
        if checkstdntsession(request):
            context = Studentinfo.objects.get(sid=request.session['stdntid'])
            return render(request, 'studentprofile.html', {'context': context})
        else:
            return render(request, 'error.html')
    return render(request, 'error.html')


def send_contact_message(request):
    new_message = ContactUsMessage()
    new_message.sender_name = request.POST['contact_name']
    new_message.sender_email = request.POST['contact_email']
    new_message.body_of_message = request.POST['contact_message']
    new_message.save()
    return render(request, 'home/home1.html', {'Message': 'Message Sent Successfully!!'})


def checkstdnt(request):
    if request.session.has_key('stdntid'):
        return True
    else:
        return False


def checkstdntsession(request):
    if request.session.session_key == Studentinfo.objects.get(sid=request.session['stdntid']).sessionkey:
        return True
    else:
        return


def checkuser(request):
    if request.session.has_key('userid'):
        return True
    else:
        return False


def checkusersession(request):
    if request.session.session_key == EmployeeInfo.objects.get(empid=request.session['userid']).session_key:
        return True
    else:
        return False


def checkadmin(request):
    if request.session.has_key('adminid'):
        return True
    else:
        return False


def checkadminsession(request):
    if request.session.session_key == AdminInfo.objects.get(adminid=request.session['adminid']).session_key:
        return True
    else:
        return False


