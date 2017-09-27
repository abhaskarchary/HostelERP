from django.http import HttpResponse
from django.shortcuts import render
import datetime
from student.models import Studentinfo
from . models import TransactionDetails
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


def update_dues(request, stu_id):
    #stu_id = request.POST['student_id']
    amount = float(request.POST['amount'])
   #mess_fees = request.POST['mess_fees']

    if stu_id:
        stu = Studentinfo.objects.filter(sid = stu_id).values()
        stu1 = Studentinfo.objects.filter(sid = stu_id).values()
        for s in stu:
            total = s['total_dues']
            bal = s['balance']
            fine = s['running_fine']
            due = s['running_dues']
            if total<amount:
                remaining_dues=0.0
                remaining_fine=0.0
                remaining_amount=amount-total
            elif amount<total and amount<due:
                remaining_dues=due-amount
                remaining_fine=fine
                remaining_amount=0.0
            elif amount<total and amount>due:
                remaining_dues=0.0
                remaining_amount=amount-due
                remaining_fine=fine-remaining_amount
                remaining_amount=0.0

            remaining_total_dues = remaining_dues + remaining_fine
            remaining_bal = bal + remaining_amount

            stu1.update(running_dues=remaining_dues, running_fine=remaining_fine,
                        balance=remaining_bal, total_dues=remaining_total_dues)

            credit_transaction = TransactionDetails()
            [credit_transaction.sid] = Studentinfo.objects.filter(sid = stu_id)
            credit_transaction.debit = 0.0
            credit_transaction.remarks = 'Deposited amount'
            credit_transaction.credit = amount
            credit_transaction.balance = bal+amount
            credit_transaction.transaction_type = 'Credit'
            credit_transaction.save()

            debit_transaction = TransactionDetails()
            [debit_transaction.sid] = Studentinfo.objects.filter(sid=stu_id)
            debit_transaction.debit = bal + amount - remaining_bal
            debit_transaction.remarks = 'Dues deduction'
            debit_transaction.credit = 0.0
            debit_transaction.balance = remaining_bal
            debit_transaction.transaction_type = 'Debit'
            debit_transaction.save()




        return HttpResponse("<h3>Existing Dues deducted according to amount and balance successfully updated<h3>")


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
    if d>1:
        for s in stu:
            total = s['total_dues']
            bal = s['balance']
            fine = s['running_fine']
            due = s['running_dues']
            remaining_dues=due
            remaining_fine=fine
            remaining_total_dues=total
            remaining_bal=bal
            stu1 = Studentinfo.objects.filter(sid = s['sid']).values()
            if((due>0.0 or fine>0.0) and bal>0.0):
                if total<=bal:
                    remaining_dues = 0.0
                    remaining_fine = 0.0
                    remaining_bal = bal - total
                elif(total>bal):
                    if(due>bal):
                        remaining_dues=due-bal
                        remaining_fine=fine
                        remaining_bal=0.0
                    else:
                        remaining_dues=0.0
                        remaining_bal=bal-due
                        remaining_fine=fine-remaining_bal
                        remaining_bal=0.0
                remaining_total_dues = remaining_dues + remaining_fine

                debit_transaction = TransactionDetails()
                [debit_transaction.sid] = Studentinfo.objects.filter(sid = s['sid'])
                debit_transaction.debit = bal-remaining_bal
                debit_transaction.remarks = 'Dues and Fee deduction'
                debit_transaction.credit = 0.0
                debit_transaction.balance = remaining_bal
                debit_transaction.transaction_type = 'Debit'
                debit_transaction.save()

            stu1.update(running_dues = remaining_dues, running_fine = remaining_fine ,
                    balance = remaining_bal, total_dues = remaining_total_dues)
    return HttpResponse("<h1>Fees paid successfully<h1")