from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime, timezone
from student.models import Studentinfo
from Room.models import Room
from .models import Fees
from transactions.models import Transaction_Details
from manager.models import EmployeeInfo
from .utils import render_to_pdf
from django.template.loader import get_template
import json
from django.http import HttpResponseRedirect
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
                    rent_per_installment = rt['fees'] / rt['parts_per_year']
                    # if (b.balance > installment):
                    #     b1 = 1
                    #     total = installment + b.running_fine
                    # else:
                    #     b1 = 0
                    #     total = b.balance + b.running_fine
                    minimum_pay=b.total_dues
                    #maximum_pay=b.balance
                l1 = [b.sid, b.first_name + " " + b.last_name]

                # l = {'running_dues':b.running_dues, 'running_fine':b.running_fine, 'total_dues': b.total_dues,'balance': b.balance, 'installment': installment, 'b1':b1}
                l = [b.next_installment , b.running_fine, minimum_pay, b.balance, rent_per_installment]
                next=[b.next_due_date]
                context = {'attr': l, 'attr1': l1, 'next': next}
                return render(request, 'payfees/show_student_dues.html', context)
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
                stu = Studentinfo.objects.filter(sid = stu_id)
                stu1 = Studentinfo.objects.filter(sid = stu_id).values()
                for s in stu:
                    total = s.total_dues
                    bal = s.balance
                    fine = s.running_fine
                    #due = s.running_dues
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
                    total_fee = amount - fine
                    #remaining_fine = 0.0
                    s.running_fine=0.0
                    remaining_amount=total_fee-s.next_installment
                    rem_bal=bal-total_fee
                    room_number = Studentinfo.objects.get(sid=stu_id).room
                    room_type = Room.objects.get(room_number=room_number).roomType
                    room = Fees.objects.filter(room_type=room_type).values()
                    for rt in room:
                        next_installment_amount = 0.0
                        next_installment_year=s.next_due_date.year
                        fee_per_installment = rt['fees'] / rt['parts_per_year']
                        next_installment_month=s.next_due_date.month+int(12/rt['parts_per_year'])
                        if (next_installment_month > 12):
                            next_installment_month = next_installment_month - 12
                            next_installment_year=s.next_due_date.year+1
                        #rem_bal = bal - remaining_amount
                        #fee_paid = initial_bal - rt['security_money']
                        no_of_installments_cleared = int(remaining_amount / fee_per_installment)
                        if (rem_bal > 0):
                            next_installment_amount_cleared = remaining_amount - no_of_installments_cleared * fee_per_installment
                            next_installment_amount = fee_per_installment - next_installment_amount_cleared
                        duration_bw_succ_installments = 12 / rt['parts_per_year']
                        next_installment_month = int(next_installment_month + no_of_installments_cleared * duration_bw_succ_installments)
                        if (next_installment_month > 12):
                            next_installment_month = next_installment_month - 12
                            next_installment_year=next_installment_year+1
                        next_due_date = str(next_installment_year) + "-" + str(next_installment_month) + "-05"
                        d = datetime.strptime(next_due_date, "%Y-%m-%d").date()
                        # bal = s['balance'] + initial_bal
                        # s['balance'] = s['balance'] + initial_bal
                    s.balance=rem_bal
                    s.next_due_date=d
                    s.next_installment=next_installment_amount
                    s.total_dues=s.next_installment+s.running_fine
                    s.save()
                #stu1.update(balance=bal, next_due_date=d, next_installment=next_installment_amount)

                # remaining_bal = bal-remaining_amount
                # remaining_total = remaining_fine + remaining_bal
                # stu1.update(balance=remaining_bal, running_fine = remaining_fine, total_dues = remaining_total)

                # fine_paid = fine
                # fees_paid = remaining_amount
                # remaining_fees = remaining_bal

                transaction = Transaction_Details()
                [transaction.sid] = Studentinfo.objects.filter(sid=stu_id)
                transaction.transaction_date=datetime.now()
                transaction.payment_mode = p_mode
                transaction.fees_paid = total_fee
                transaction.fine_paid = fine
                transaction.remaining_fees = rem_bal
                transaction.remaining_fine = 0.0
                transaction.remaining_total = rem_bal
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



                # template = get_template('receipt.html')
                # context = {
                #     "sid": stu_id,
                #     "trans_id": transaction.transaction_id,
                #     "trans_date": transaction.transaction_date,
                #     "pmode": p_mode,
                #     "fees_paid": transaction.fees_paid,
                #     "fine": transaction.fine_paid,
                #     "balance": transaction.remaining_total,
                #     "total": transaction.remaining_total,
                #     "particulars": particulars,
                #     "next_due_date": d
                # }
                # html = template.render(context)
                # pdf = render_to_pdf('receipt.html', context)
                # return HttpResponse(pdf, content_type="application/pdf")
                #return HttpResponse("<h3>Existing Dues deducted according to amount and balance successfully updated<h3>"
                return render(request, 'index.html', {'Message': 'Fee paid successfully', 'trans_id':transaction.transaction_id })
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
