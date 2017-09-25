from django.shortcuts import render, redirect
from .models import Studentinfo
from payfees.models import Fees
from Room.models import Room


# Create your views here.


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

def change_info(request, sid):
    if request.session.has_key('userid'):
        [context] = Studentinfo.objects.filter(sid=sid)
        return render(request, 'registration/form1.html', {'context': context})
    return render(request, 'error.html')


def update(request):
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

    student_info_object = Studentinfo()
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
    student_info_object.balance = 0.0
    student_info_object.running_dues = 0.0
    student_info_object.running_fine = 0.0
    student_info_object.refundable_security = 0.0
    student_info_object.total_dues = 0.0
    [student_info_object.room] = Room.objects.filter(room_number=room_number)
    if int(student_info_object.room.vacancy) < 1:
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