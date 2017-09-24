from django.http import HttpResponse
from django.shortcuts import render
import datetime
from student.models import Studentinfo
# Create your views here.


def search(request):
    if request.session.has_key('userid'):
        return render(request, 'payfees/search.html')
    else:
        return render(request, 'error.html')

def show(request):
    if request.session.has_key('userid'):
        stu_id = request.POST['student_id']
        dues = None
        #context = {}
        counter = 0
        l=[]
        if stu_id:
            stu = Studentinfo.objects.filter(sid = stu_id).values()
            for b in stu:
                l = [b['sid'], b['running_dues'], b['running_fine'], b['total_dues'], b['balance']]
            context = {'attr': l}
            return render(request, 'payfees/show_individual_dues.html', context)
    else:
        return render(request, 'error.html')


def update_dues(request):
    stu_id = request.POST['student_id']
    fees = request.POST['room_fees']
   # mess_fees = request.POST['mess_fees']

    if stu_id:
        stu = Studentinfo.objects.filter(sid = stu_id).values()
        stu1 = Studentinfo.objects.filter(sid = stu_id).values()
        for s in stu:
            remaining_bal = s['balance'] - (float(fees))
            if(float(fees)<s['running_dues']):
                remaining_dues = s['running_dues'] - float(fees)
                remaining_fine = s['running_fine']
            elif(float(fees)>=s['running_dues'] and float(fees)<s['total_dues']):
                fees = float(fees) - s['running_dues']
                remaining_dues = 0.0
                remaining_fine = s['running_fine'] - fees;
            else:
                remaining_dues = 0.0
                remaining_fine = 0.0
        remaining_total_dues = s['total_dues'] - float(fees)
        stu1.update(running_dues = remaining_dues, running_fine = remaining_fine ,
                    balance = remaining_bal, total_dues = remaining_total_dues)
        return HttpResponse("<h3>Fees paid Successfully<h3>")


def account(request):
    if request.session.has_key('userid'):
        return render(request, 'payfees/account.html')
    else:
        return render(request, 'error.html')


def info(request):
    if request.session.has_key('userid'):
        return render(request, 'payfees/displayreports.html', {'FeesDetails': Studentinfo.objects.all()})
    else:
        return render(request, 'error.html')

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