from uuid import UUID
from django.shortcuts import render,redirect
from expense_tracker.models import Transaction,Mode,Category
from datetime import datetime

def addTransaction (request):
    categorys=Category.objects.all()
    modes=Mode.objects.all()
    categorys=categorys.order_by('name')
    modes=modes.order_by("name")
    return render (request,'add-transaction.html',{'category':categorys,'mode':modes})
def processAddTransaction (request):
    type=request.POST.get("type")
    amount=request.POST.get("amount")
    mode=request.POST.get("mode_id")
    category=request.POST.get("category_id")
    note=request.POST.get("note")
    date=request.POST.get("date")
    date = datetime.strptime(date, "%Y-%m-%d")
    transaction=Transaction.objects.create(type=type,amount=amount,mode_id=mode,category_id=category,date=date,note=note)
    transaction.save()
    return redirect(getAllTransaction)
def getAllTransaction (request):
    transaction=Transaction.objects.all()
    categorys=Category.objects.all()
    modes=Mode.objects.all()
    for x in transaction:
        x.id = str(x.id)
    transaction=transaction.order_by('-date')
    return render (request,'manage-transaction.html',{'data':transaction,'category':categorys,'mode':modes})
def processDeleteTransaction (request):
    id=request.POST.get("id")
    transaction=Transaction.objects.get(id=id)
    transaction.delete()
    return redirect(getAllTransaction)

def updateTransaction (request):
    id=request.GET.get("id")
    transaction=Transaction.objects.filter(id=id).first()
    categorys=Category.objects.all()
    modes=Mode.objects.all()
    return render(request,'update-transaction.html',{'data':transaction,'category':categorys,'mode':modes})

def processUpdateTransaction (request):
    id=request.POST.get("id")
    type=request.POST.get("type")
    amount=request.POST.get("amount")
    mode_id=request.POST.get("mode_id")
    category_id=request.POST.get("category_id")
    note=request.POST.get("note")
    date=request.POST.get("date")
    transaction=Transaction.objects.filter(id=id).update(type=type,amount=amount,mode_id=mode_id,category_id=category_id,date=date,note=note)
    return redirect(getAllTransaction)