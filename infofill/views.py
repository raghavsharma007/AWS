from django.shortcuts import render,redirect
from .forms import FillupForm
from django.contrib.auth import settings
from .models import Fillup, LoggedIn, Link
from django.contrib.auth import logout
from django.db.models import Q
from django.core.mail import send_mail
from django.utils import timezone
from datetime import datetime
import time

link = Link.objects.get(id=1).link


def home(request):
    settings.LOGIN_REDIRECT_URL = '/for/creator/1/'
    return render(request, 'infofill/home.html')

def forcreator1(request):
    data = Fillup.objects.all().exclude(action="Live").exclude(action='Stop').order_by('-id')
    for i in data:
        target_date = i.target_launch_date
        date_today = datetime.now().date()
        if target_date > date_today:
            i.ontime_status = 'On Time'
        else:
            i.ontime_status = 'Late'
    return render(request, 'infofill/forcreator.html', {'data': data})

def form(request):
    if request.method == 'POST':
        client_type = request.POST.get('clientSelect')
        active_clients = request.POST.get('activeclients')
        new_client = request.POST.get('newclient')
        textarea = request.POST.get('textarea')
        date = request.POST.get('date')

        if active_clients == '':
            obj = Fillup.objects.create(client_type=client_type, client_name=new_client, request_synopsis=textarea, target_launch_date=date)
            obj.save()
            salesapprover = LoggedIn.objects.filter(role='Sales Approver')
            # link = Link.objects.get(id=1).link
            send_mail(f'{new_client + " - " + textarea} - Request for approval',
                      f'login to give approval action: {link}/app/home/',
                      settings.EMAIL_HOST_USER, [i.email for i in salesapprover])  # give sales approver email
        else:
            obj = Fillup.objects.create(client_type=client_type, client_name=active_clients, request_synopsis=textarea, target_launch_date=date)
            obj.save()
            salesapprover = LoggedIn.objects.filter(role='Sales Approver')
            # link = Link.objects.get(id=1).link
            send_mail(f'{active_clients + " - " + textarea} - Request for approval',
                      f'login to give approval action: {link}/sales/app/home/',
                      settings.EMAIL_HOST_USER, [i.email for i in salesapprover])  # give sales approver email

        obj = Fillup.objects.order_by('-pk')[0]
        obj.current_status = 'Pending by Sales Approver'
        obj.save()
        return redirect('infofill:form')

    return render(request, 'infofill/form.html', {'form': form})
    #     form = FillupForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         client_name = request.POST.get('client_name')
    #         request_synopsis = request.POST.get('request_synopsis')
    #         obj = Fillup.objects.order_by('-pk')[0]
    #         obj.current_status = 'Pending by Sales Approver'
    #         obj.save()
    #         send_mail(f'{client_name +" - "+ request_synopsis}-Request for approval', 'login to give approval action: http://127.0.0.1:8000/sales/app/home/',
    #                   settings.EMAIL_HOST_USER, ['rsharma2@dataflowgroup.com', ])#give sales approver email
    #         return redirect('infofill:form')
    # form = FillupForm()
    # return render(request, 'infofill/form.html', {'form': form})

def logout_creator(request):
    logout(request)
    return redirect('infofill:home')

def golive(request, id):
    obj = Fillup.objects.get(pk=id)
    if request.method == 'POST':
        if '_live' in request.POST:
            Fillup.objects.filter(pk=id).update(action='Live')
            Fillup.objects.filter(pk=id).update(actual_live_date=timezone.now())

            return redirect('infofill:forcreator1')
        if '_hold' in request.POST:
            if obj.action == "Hold":
                Fillup.objects.filter(pk=id).update(action='')
                Fillup.objects.filter(pk=id).update(current_status='WIP')
                return redirect('infofill:forcreator1')
            else:
                Fillup.objects.filter(pk=id).update(current_status='Hold')
                Fillup.objects.filter(pk=id).update(action='Hold')
                return redirect('infofill:forcreator1')
        if '_stop' in request.POST:
            Fillup.objects.filter(pk=id).update(action='Stop')
            return redirect('infofill:forcreator1')


def completed(request):
    data = Fillup.objects.filter(Q(action='Live') | Q(action='Stop')).order_by('-id')
    for i in data:
        target_date = i.target_launch_date
        date_today = datetime.now().date()
        if target_date > date_today:
            i.ontime_status = 'On Time'
        else:
            i.ontime_status = 'Late'
    return render(request, 'infofill/completed.html', {'data':data})



#######

def salesapphome(request):
    # settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '582896860190-rntgt5tc2hsf3it77gn3f955771t6re6.apps.googleusercontent.com'
    # settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'qhIwKDYR5FVLSVDuWdDn2YoL'
    # settings.SOCIAL_AUTH__KEY = 'ID'
    # settings.SOCIAL_AUTH__SECRET = 'SECRET'
    settings.LOGIN_REDIRECT_URL = '/sales/app/action/'
    return render(request, 'infofill/home.html')

def salesappaction(request):
    data = Fillup.objects.filter(approval='Pending').exclude(client_name='').order_by('-id')
    action = Fillup.objects.filter(Q(approval='Approved') | Q(approval='Reject')).exclude(client_name='').order_by('-id')
    for i in data:
        target_date = i.target_launch_date
        date_today = datetime.now().date()
        if target_date > date_today:
            i.ontime_status = 'On Time'
        else:
            i.ontime_status = 'Late'
    return render(request, 'infofill/forsalesapp.html', {'data': data, 'action':action})

def logout_salesapp(request):
    logout(request)
    return redirect('infofill:salesapphome')

def approvalaction(request, id):
    if request.method == 'POST':
        if '_approve' in request.POST:
            obj = Fillup.objects.filter(pk=id).update(approval='Approved')
            obj = Fillup.objects.filter(pk=id).update(current_status='Pending By IT Approver')
            remark = request.POST.get('_textarea')
            Fillup.objects.filter(pk=id).update(remarks=remark)
            info = Fillup.objects.get(pk=id)
            sales = LoggedIn.objects.filter(role='Sales')
            itapprover = LoggedIn.objects.filter(role='IT Approver')
            send_mail(f'{info.client_name +" - "+ info.request_synopsis} - Request for Estimated Date', f'login to give Estimated Date : {link}/it/app/home/',
                      settings.EMAIL_HOST_USER, [i.email for i in itapprover]) #give IT approver email
            send_mail(f'Notification: {info.client_name +" - " + info.request_synopsis} -  Approved', f'login : {link}/home/login/via/google/',
                      settings.EMAIL_HOST_USER, [i.email for i in sales]) # give creator email
            return redirect('infofill:salesappaction')
        elif '_reject' in request.POST:
            obj = Fillup.objects.filter(pk=id).update(approval='Reject')
            remark = request.POST.get('_textarea')
            Fillup.objects.filter(pk=id).update(remarks=remark)
            info = Fillup.objects.get(pk=id)
            sales = LoggedIn.objects.filter(role='Sales')
            send_mail(f'Notification: {info.client_name +" - " + info.request_synopsis} - Rejected!', f'kindly login to view: {link}/home/login/via/google/',
                      settings.EMAIL_HOST_USER, [i.email for i in sales])#creator email
            return redirect('infofill:salesappaction')

####
def itapphome(request):
    settings.LOGIN_REDIRECT_URL = '/it/app/action/'
    return render(request, 'infofill/home.html')
def itappaction(request):
    data = Fillup.objects.filter(approval='Approved').exclude(close='close').order_by('-id')
    for i in data:
        target_date = i.target_launch_date
        date_today = datetime.now().date()
        if target_date > date_today:
            i.ontime_status = 'On Time'
        else:
            i.ontime_status = 'Late'
    return render(request, 'infofill/foritapp.html', {'data': data})

def afterclose(request):
    data = Fillup.objects.filter(approval='Approved').exclude(close='close').order_by('-id')
    for i in data:
        target_date = i.target_launch_date
        date_today = datetime.now().date()
        if target_date > date_today:
            i.ontime_status = 'On Time'
        else:
            i.ontime_status = 'Late'
    return render(request, 'infofill/foritapp.html', {'data': data})


def logout_itapp(request):
    logout(request)
    return redirect('infofill:itapphome')

def estdate(request, id):
    if request.method == 'POST':
        date = request.POST.get('_date', None)

        if '_dateSubmit' in request.POST:
            obj = Fillup.objects.filter(pk=id).update(estimated_date=date)
            return redirect('infofill:itappaction')
        if '_close' in request.POST:
            Fillup.objects.filter(pk=id).update(close='close')
            obj = Fillup.objects.filter(pk=id).update(current_status='Pending By OPS Approver')
            info = Fillup.objects.get(pk=id)
            opsapprover = LoggedIn.objects.filter(role='OPS Approver')
            sales = LoggedIn.objects.filter(role='Sales')
            send_mail(f'{info.client_name + " - " + info.request_synopsis} - Provide UAT Date',
                      f'kindly login to give UAT date: {link}/ops/app/home/',
                      settings.EMAIL_HOST_USER, [i.email for i in opsapprover])  # mail of ops approver
            send_mail(f'Notification: {info.client_name +" - " + info.request_synopsis} - Estimated Date provided',
                      f'login : {link}/home/login/via/google/',
                      settings.EMAIL_HOST_USER, [i.email for i in sales])  # give creator email
            return redirect('infofill:afterclose')

def estdategiven(request):
    comp = Fillup.objects.filter(close='close').exclude(estimated_date=None).order_by('-id')
    return render(request, 'infofill/estdategiven.html', {'comp':comp})


####
def opsapphome(request):
    settings.LOGIN_REDIRECT_URL = '/ops/app/action/'
    return render(request, 'infofill/home.html')
def opsappaction(request):
    data = Fillup.objects.filter(approval__exact='Approved').exclude(estimated_date=None).exclude(close_2='close').order_by('-id')
    for i in data:
        target_date = i.target_launch_date
        date_today = datetime.now().date()
        if target_date > date_today:
            i.ontime_status = 'On Time'
        else:
            i.ontime_status = 'Late'
    return render(request, 'infofill/uatdate.html', {'data':data})
def logout_opsapp(request):
    logout(request)
    return redirect('infofill:opsapphome')
def uatdate(request,id):
    if request.method == 'POST':
        date = request.POST.get('_date',None)

        if '_givedate' in request.POST:
            obj = Fillup.objects.filter(pk=id).update(uat_date=date)
            obj = Fillup.objects.filter(pk=id).update(current_status='WIP')
            return redirect('infofill:opsappaction')
        if '_close' in request.POST:
            Fillup.objects.filter(pk=id).update(close_2='close')
            info = Fillup.objects.get(pk=id)
            sales = LoggedIn.objects.filter(role='Sales')
            send_mail(f'{info.client_name + " - " + info.request_synopsis} - Provide action',
                      f'kindly login to give action: {link}/home/login/via/google/',
                      settings.EMAIL_HOST_USER, [i.email for i in sales])  # creator mail
            return redirect('infofill:afterclose2')
def afterclose2(request):
    data = Fillup.objects.filter(approval='Approved').exclude(close_2='close').exclude(estimated_date=None).order_by('-id')
    for i in data:
        target_date = i.target_launch_date
        date_today = datetime.now().date()
        if target_date > date_today:
            i.ontime_status = 'On Time'
        else:
            i.ontime_status = 'Late'

    return render(request, 'infofill/uatdate.html', {'data':data})
def opsdategiven(request):
    comp = Fillup.objects.filter(close_2='close').exclude(uat_date=None).order_by('-id')
    return render(request, 'infofill/opsdategiven.html', {'comp':comp})







######
# def actionhome(request):
#     settings.LOGIN_REDIRECT_URL = '/action/table/'
#     return render(request, 'infofill/home.html')
# def actiontable(request):
#     data = Fillup.objects.filter(approval='Approved').exclude(estimated_date=None).exclude(uat_date=None).order_by('-id')
#     for i in data:
#         target_date = i.target_launch_date
#         date_today = datetime.now().date()
#         if target_date > date_today:
#             i.ontime_status = 'On Time'
#         else:
#             i.ontime_status = 'Late'
#     return render(request, 'infofill/actiontable.html', {'data': data})
# def logout_creatoraction(request):
#     logout(request)
#     return redirect('infofill:actionhome')