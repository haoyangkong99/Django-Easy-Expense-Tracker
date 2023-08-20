from uuid import UUID
from django.shortcuts import render,redirect
from expense_tracker.models import Mode


def addMode (request):
    return render (request,'add-mode.html')
def processAddMode (request):
    name=request.POST.get("name")
    mode=Mode.objects.create(name=name)
    mode.save()
    return redirect(getAllMode)
def getAllMode (request):
    mode=Mode.objects.all()
    for x in mode:
        x.id = str(x.id)

    return render (request,'manage-mode.html',{'data':mode})
def processDeleteMode (request):
    id=request.POST.get("id")
    mode=Mode.objects.get(id=id)
    mode.delete()
    return redirect(getAllMode)

def updateMode (request):
    id=request.GET.get("id")
    mode=Mode.objects.filter(id=id).first()
    return render(request,'update-mode.html',{'data':mode})

def processUpdateMode (request):
    id=request.POST.get("id")
    name=request.POST.get("name")
    mode=Mode.objects.filter(id=id).update(name=name)
    return redirect(getAllMode)