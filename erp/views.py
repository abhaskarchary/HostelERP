from django.shortcuts import render, redirect
from manager.models import EmployeeInfo
from smartadmin.models import AdminInfo
from student.models import Studentinfo
# Create your views here.


def home(request):
    return render(request, 'home/home1.html')


def login(request):
    if request.session.has_key('stdntid'):
        return redirect('/student/login/')
    elif request.session.has_key('userid'):
        return redirect('/manager/login/')
    elif request.session.has_key('adminid'):
        return redirect('/smartadmin/login/')
    else:
        return render(request, 'login.html')


def start_session(request):
    userid = request.POST['userid']
    userpass = request.POST['userpass']

    if userid[:3] == 'EMP':
        #current_model = EmployeeInfo
        sess_name = 'userid' #variable to decide string for session dictionary
    elif userid[:3] == 'ETL':
        #current_model = Studentinfo
        sess_name = 'stdntid'
    else:
        sess_name = 'adminid'
    try:
        here = ""
        if sess_name == 'stdntid':
            [object] = Studentinfo.objects.filter(sid=userid, password=userpass)
        elif sess_name == 'userid':
            [object] = EmployeeInfo.objects.filter(empid=userid, password=userpass)
        else:
            [object] = AdminInfo.objects.filter(adminid=userid, password=userpass)
        if object.first_name != "":
            if sess_name == 'userid' and object.employee_type != "manager":
                return render(request, 'login.html', {'Message': 'Error Code 1.3 : Invalid Userid or password!!!'} )
            elif sess_name == 'stdntid' and not object.active:
                return render(request, 'login.html', {'Message': 'Error Code 1.4 : Your Account is no longer active!!!'} )

            request.session[sess_name] = userid

            if not request.session.session_key: #for removing 2 times login request error
                request.session.save()
            if sess_name == 'userid':
                EmployeeInfo.objects.filter(empid=userid, password=userpass).update(session_key=request.session.session_key)
                return redirect('/manager/login/')
            elif sess_name == 'stdntid':
                Studentinfo.objects.filter(sid=userid, password=userpass).update(
                    sessionkey=request.session.session_key)
                return redirect('/student/login/')
            else:
                AdminInfo.objects.filter(adminid=userid, password=userpass).update(
                    session_key=request.session.session_key)
                return redirect('/smartadmin/login/')

        else:
            return render(request, 'login.html', {'Message': 'Error Code 1.1 : Invalid Userid or password!!!'})
    except:
        return render(request, 'login.html', {'Message': 'Error Code 1.2 : Invalid Userid or password!!!'})