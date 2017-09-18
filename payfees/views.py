from django.http import HttpResponse
from django.shortcuts import render
from .models import Dues
from datetime import datetime
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
            dues = Dues.objects.filter(sid = stu_id).values()
            stu = Studentinfo.objects.filter(sid = stu_id).values()
            for due in dues:
                attr = {
                    'Student id': due['sid'],
                    'Room Fees': due['roomfees'],
                    'Mess Fees': due['messfees'],
                    'Total': due['totaldue'],
                }
                l = [due['sid'], due['roomfees'], due['messfees'], due['totaldue']]
                counter = 1
            for b in stu:
                l.append(b['balance'])
            context = {'attr': l}
            return render(request, 'payfees/show_individual_dues.html', context)
    else:
        return render(request, 'error.html')


def update_dues(request):
    stu_id = request.POST['student_id']
    room_fees = request.POST['room_fees']
    mess_fees = request.POST['mess_fees']

    if stu_id:
        dues = Dues.objects.filter(sid = stu_id).values()
        dues1 = Dues.objects.filter(sid = stu_id).values()
        stu = Studentinfo.objects.filter(sid = stu_id).values()
        stu1 = Studentinfo.objects.filter(sid = stu_id).values()
        for s in stu:
            remaining_bal = s['balance'] - (float(room_fees) + float(mess_fees))
        for due in dues:
            room_fees = due['roomfees'] - float(room_fees)
            mess_fees = due['messfees'] - float(mess_fees)

        dues1.update(roomfees = room_fees, messfees = mess_fees, totaldue = (room_fees + mess_fees))
        stu1.update(balance = remaining_bal)
        return HttpResponse("<h3>Fees paid Successfully<h3>")


def account(request):
    if request.session.has_key('userid'):
        return render(request, 'payfees/account.html')
    else:
        return render(request, 'error.html')


def info(request):
    if request.session.has_key('userid'):
        return render(request, 'payfees/displayreports.html', {'FeesDetails': Dues.objects.all()})
    else:
        return render(request, 'error.html')