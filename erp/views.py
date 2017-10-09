from django.shortcuts import render, redirect
from manager.models import EmployeeInfo
from student.models import Studentinfo
# Create your views here.
def home(request):
    return render(request, 'home/home1.html')

def login(request):
    return render(request, 'login.html')

def start_session(request):
    userid = request.POST['userid']
    userpass = request.POST['userpass']

    if userid[:3] == 'EMP':
        #current_model = EmployeeInfo
        sess_name = 'userid' #variable to decide string for session dictionary
    else:
        #current_model = Studentinfo
        sess_name = 'stdntid'
    try:
        here = ""
        if sess_name == 'stdntid':
            [object] = Studentinfo.objects.filter(sid=userid, password=userpass)
        else:
            here = "tatti"

            [object] = EmployeeInfo.objects.filter(empid=userid, password=userpass)
        if object.first_name != "":
            if sess_name == 'userid' and object.employee_type != "manager":
                return render(request, 'login.html', {'Message': 'Error Code 1.3 : Invalid Userid or password!!!'} )

            request.session[sess_name] = userid

            if not request.session.session_key:
                request.session.save()
            if sess_name == 'userid':
                EmployeeInfo.objects.filter(empid=userid, password=userpass).update(session_key=request.session.session_key)
                return redirect('/manager/login/')
            else:
                Studentinfo.objects.filter(sid=userid, password=userpass).update(
                    sessionkey=request.session.session_key)

                return redirect('/student/login/')
        else:
            return render(request, 'login.html', {'Message': 'Error Code 1.1 : Invalid Userid or password!!!'})
    except:
        return render(request, 'login.html', {'Message': here + 'Error Code 1.2 : Invalid Userid or password!!!'})