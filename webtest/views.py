from django.shortcuts import render
import requests
import sys
from django.core.files.storage import FileSystemStorage
from subprocess import run,PIPE

def button(request):
    return render(request,'index.html')


def external(request):
 inp= request.POST.get('param')
 out= run([sys.executable,'//Users//rohan//Downloads//Django1//webtest//test.py',inp],shell=False,stdout=PIPE)
 print(out)
 return render(request,'index.html',{'data1':out.stdout})

def upload(request):
    if request.method=='POST':
        context = {}
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save("newsimg.jpg", uploaded_file)
        context['name'] = uploaded_file.name
        
    return render(request,'index.html',context)

def checking(request):
    if request.method=='POST':
     out= run([sys.executable,'//Users//rohan//Downloads//Django1//webtest//ocrtest.py'],shell=False,stdout=PIPE)
     print(out)
    return render(request,'index.html',{'data2':out.stdout})