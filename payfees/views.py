from django.http import HttpResponse
from django.shortcuts import render
import datetime
from student.models import Studentinfo
from Room.models import Room
from .models import Fees
from transactions.models import Transaction_Details
from manager.models import EmployeeInfo
# Create your views here.


def search(request):
    if request.session.has_key('userid'):
        userid = request.session['userid']
        if request.session.session_key == EmployeeInfo.objects.get(empid=userid).session_key:
            return render(request, 'payfees/search.html')
        else:
            return render(request, 'login.html', {'Message': 'Session terminated!'})
    else:
        return render(request, 'error.html')

def show(request):
    if request.session.has_key('userid'):
        userid = request.session['userid']
        if request.session.session_key == EmployeeInfo.objects.get(empid=userid).session_key:
            stu_id = request.POST['student_id']
            dues = None
            #context = {}
            counter = 0
            l=[]
            if stu_id:
                # stu = Studentinfo.objects.filter(sid = stu_id).values()
                # for b in stu:
                #     print(b['sid']+""+b['room'])
                #     room_number = b['room']
                #     room_type = Room.objects.get(room_number = room_number).roomType
                #     room = Fees.objects.filter(room_type = room_type).values()
                #     for rt in room:
                #         installment = rt['fees']/rt['parts_per_year']
                #         if(b['balance']>installment):
                #             b=1
                #         else:
                #             b=0
                #     l1 = [b['sid'], b['first_name']+" "+b['last_name']]
                #     l = [b['running_dues'], b['running_fine'], b['total_dues'], b['balance'], installment, b]
                # context = {'attr': l,'attr1': l1}
                # return render(request, 'payfees/show_individual_dues.html', context)
                c=0
                stu = Studentinfo.objects.filter(sid=stu_id)
                if not stu.exists():
                    return HttpResponse("<h3>Student ID not found</h3>")
                b=Studentinfo.objects.get(sid = stu_id)
                print(b.sid + " " + str(b.room))
                room_number = b.room
                room_type = Room.objects.get(room_number=room_number).roomType
                room = Fees.objects.filter(room_type=room_type).values()
                for rt in room:
                    installment = rt['fees'] / rt['parts_per_year']
                    if (b.balance > installment):
                        b1 = 1
                        total = installment + b.running_fine
                    else:
                        b1 = 0
                        total = b.balance + b.running_fine
                l1 = [b.sid, b.first_name + " " + b.last_name]
                # l = {'running_dues':b.running_dues, 'running_fine':b.running_fine, 'total_dues': b.total_dues,'balance': b.balance, 'installment': installment, 'b1':b1}
                l = [b.running_dues, b.running_fine, b.balance, b.total_dues, installment]
                l2= [b1, total]
                context = {'attr': l, 'attr1': l1, 'attr2':l2}
                return render(request, 'payfees/show_individual_dues.html', context)
        else:
            return render(request, 'login.html', {'Message': 'Session terminated!'})
    else:
        return render(request, 'error.html')


def update_dues(request, stu_id):
    if request.session.has_key('userid'):
        userid = request.session['userid']
        if request.session.session_key == EmployeeInfo.objects.get(empid=userid).session_key:
            #stu_id = request.POST['student_id']
            amount = float(request.POST['amount'])
            p_mode = (request.POST['payment_mode'])
            particulars = request.POST['particulars']
           #mess_fees = request.POST['mess_fees']

            if stu_id:
                stu = Studentinfo.objects.filter(sid = stu_id).values()
                stu1 = Studentinfo.objects.filter(sid = stu_id).values()
                for s in stu:
                    total = s['total_dues']
                    bal = s['balance']
                    fine = s['running_fine']
                    due = s['running_dues']
                    # if total<amount:
                    #     remaining_dues=0.0
                    #     remaining_fine=0.0
                    #     remaining_amount=amount-total
                    # elif amount<total and amount<due:
                    #     remaining_dues=due-amount
                    #     remaining_fine=fine
                    #     remaining_amount=0.0
                    # elif amount<total and amount>due:
                    #     remaining_dues=0.0
                    #     remaining_amount=amount-due
                    #     remaining_fine=fine-remaining_amount
                    #     remaining_amount=0.0


                    # remaining_total_dues = remaining_dues + remaining_fine
                    # remaining_bal = bal + remaining_amount
                    remaining_amount = amount - fine
                    remaining_fine = 0.0
                    remaining_bal = s['balance']-remaining_amount
                    remaining_total = remaining_fine + remaining_bal
                    stu1.update(balance=remaining_bal, running_fine = remaining_fine, total_dues = remaining_total)

                    fine_paid = fine
                    fees_paid = remaining_amount
                    remaining_fees = remaining_bal

                    transaction = Transaction_Details()
                    [transaction.sid] = Studentinfo.objects.filter(sid=stu_id)
                    transaction.payment_mode = p_mode
                    transaction.fees_paid = fees_paid
                    transaction.fine_paid = fine_paid
                    transaction.remaining_fees = remaining_fees
                    transaction.remaining_fine = remaining_fine
                    transaction.remaining_total = remaining_total
                    transaction.particulars = particulars

                    transaction.save()



                    # credit_transaction = TransactionDetails()
                    # [credit_transaction.sid] = Studentinfo.objects.filter(sid = stu_id)
                    # credit_transaction.debit = 0.0
                    # credit_transaction.remarks = 'Deposited amount'
                    # credit_transaction.credit = amount
                    # credit_transaction.balance = bal+amount
                    # credit_transaction.transaction_type = 'Credit'
                    # credit_transaction.transaction_mode = p_mode
                    # credit_transaction.save()
                    #
                    # if total>0:
                    #     debit_transaction = TransactionDetails()
                    #     [debit_transaction.sid] = Studentinfo.objects.filter(sid=stu_id)
                    #     debit_transaction.debit = bal + amount - remaining_bal
                    #     debit_transaction.remarks = 'Dues deduction'
                    #     debit_transaction.credit = 0.0
                    #     debit_transaction.balance = remaining_bal
                    #     debit_transaction.transaction_type = 'Debit'
                    #     debit_transaction.save()




                return HttpResponse("<h3>Existing Dues deducted according to amount and balance successfully updated<h3>")
        else:
            return render(request, 'login.html', {'Message': 'Session terminated!'})
    else:
        return render(request, 'error.html')


def account(request):
    if request.session.has_key('userid'):
        userid = request.session['userid']
        if request.session.session_key == EmployeeInfo.objects.get(empid=userid).session_key:
            return render(request, 'payfees/account.html')
        else:
            return render(request, 'login.html', {'Message': 'Session terminated!'})
    else:
        return render(request, 'error.html')


def info(request):
    if request.session.has_key('userid'):
        userid = request.session['userid']
        if request.session.session_key == EmployeeInfo.objects.get(empid=userid).session_key:
            return render(request, 'payfees/displayreports.html', {'FeesDetails': Studentinfo.objects.all()})
        else:
            return render(request, 'login.html', {'Message': 'Session terminated!'})
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

                # debit_transaction = TransactionDetails()
                # [debit_transaction.sid] = Studentinfo.objects.filter(sid = s['sid'])
                # debit_transaction.debit = bal-remaining_bal
                # debit_transaction.remarks = 'Dues and Fee deduction'
                # debit_transaction.credit = 0.0
                # debit_transaction.balance = remaining_bal
                # debit_transaction.transaction_type = 'Debit'
                # debit_transaction.save()

            stu1.update(running_dues = remaining_dues, running_fine = remaining_fine ,
                    balance = remaining_bal, total_dues = remaining_total_dues)
    return HttpResponse("<h1>Fees paid successfully<h1")