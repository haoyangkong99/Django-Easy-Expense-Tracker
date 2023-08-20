from uuid import UUID
from django.shortcuts import render,redirect
from expense_tracker.models import Category


def addCategory (request):
    return render (request,'add-category.html')
def processAddCategory (request):
    name=request.POST.get("name")
    category=Category.objects.create(name=name)
    category.save()
    return redirect(getAllCategory)
def getAllCategory (request):
    category=Category.objects.all()
    for x in category:
        x.id = str(x.id)
    category=category.order_by('name')
    return render (request,'manage-category.html',{'data':category})
def processDeleteCategory (request):
    id=request.POST.get("id")
    category=Category.objects.get(id=id)
    category.delete()
    return redirect(getAllCategory)

def updateCategory (request):
    id=request.GET.get("id")
    category=Category.objects.filter(id=id).first()
    return render(request,'update-category.html',{'data':category})

def processUpdateCategory (request):
    id=request.POST.get("id")
    name=request.POST.get("name")
    category=Category.objects.filter(id=id).update(name=name)
    return redirect(getAllCategory)