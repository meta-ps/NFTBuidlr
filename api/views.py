from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from NFT_GEN.models import LayersModel,Image,ProjectDesc, ArchivedProject
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.serializer import LayersModelSerializer,ImageModelSerializer,ProjectModelSerializer,ArchivedProjectModelSerializer
from rest_framework.generics import ListAPIView
import json
from django.contrib.auth.hashers import make_password
# Create your views here.
from django.core import serializers
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from crm1.settings import BASE_DIR
from django.contrib import auth
import os
import shutil
from django.shortcuts import render, redirect 

auser = []

class LayersModelAPIGET(ListAPIView):
    queryset = LayersModel.objects.all()
    serializer_class = LayersModelSerializer


class ImagesModelAPIGET(ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageModelSerializer

class ProjectModelAPIGET(ListAPIView):
    queryset = ProjectDesc.objects.all()
    serializer_class = ProjectModelSerializer

class ArchivedProjectModelAPIGET(ListAPIView):
    queryset = ArchivedProject.objects.all()
    serializer_class = ArchivedProjectModelSerializer

@csrf_exempt 
def saveuser(request): 
    global auser
    auser.append(request.POST['id'])
    password = request.POST['id'][:4] + request.POST['id'][-4:]

    new_user = User.objects.create_user(username=request.POST['id'],password=password)
    #new_user.set_password(password)
    new_user.save()

    tuser = User.objects.get(username=request.POST['id'])

    dir = BASE_DIR + '/' + str(tuser.id)
    imgdir = dir + '/images'
    opdir = dir + '/output'

    try:
        os.mkdir(dir)
    except:
        pass
    try:
        os.mkdir(imgdir)
    except:
        pass 
    try: 
        os.mkdir(opdir)
    except:
        pass

    return HttpResponse("Saved")

@csrf_exempt     
def login(request):
    if request.method != 'POST':
        return HttpResponse('Only POSTs are allowed')
    print(request.POST['id'])
    password = request.POST['id'][:4] + request.POST['id'][-4:]
    user = auth.authenticate(username=request.POST['id'],password=password)
    print(user,user.username)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        return HttpResponse("Login Success!")
    else:
        # Show an error page
        return HttpResponse("Login Failed!")



@csrf_exempt 
def clear(request):
    LayersModel.objects.all().delete()
    ProjectDesc.objects.all().delete()
   
    tuser = User.objects.get(username=request.POST['id'])
    for obj in User.objects.all():
        if obj.is_superuser:
            pass
        else:
            obj.delete()
    print(tuser.id)
    dir = BASE_DIR + '/' + str(tuser.id)

    try:
        shutil.rmtree(dir)
    except:
        pass 

    return HttpResponse("Deleted")


    

def getuser():
    return auser[-1]


