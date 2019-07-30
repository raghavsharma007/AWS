"""clientregister URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views

admin.site.site_header = 'DataFlow Client Management'
app_name = 'infofill'

urlpatterns = [
    path('home/login/via/google/', views.home, name='home'),
    #creater
    path('for/creator/1/', views.forcreator1, name='forcreator1'),
    # path('data/', views.forcreator2, name='forcreator2')
    path('form/', views.form, name='form'),
    path('logout_creator/', views.logout_creator, name='logout_creator'),
    path('go/live/<int:id>/', views.golive, name='golive'),
    path('completed/entry/', views.completed, name='completed'),
    #salesApprover
    # path('home2/login/via/google/', views.home2, name='home2'),
    path('sales/app/home/', views.salesapphome, name='salesapphome'),
    path('sales/app/action/', views.salesappaction, name='salesappaction'),
    path('logout_sales/app/', views.logout_salesapp, name='logout_salesapp'),
    path('approval/action/<int:id>/', views.approvalaction, name='approvalaction'),
    #ITApprover
    path('it/app/home/',views.itapphome, name='itapphome'),
    path('it/app/action/',views.itappaction, name='itappaction'),
    path('logout_it/app/',views.logout_itapp, name='logout_itapp'),
    path('est/date/<int:id>/', views.estdate, name='estdate'),
    path('after/close/', views.afterclose, name='afterclose'),
    path('est/date/given/', views.estdategiven, name='estdategiven'),
    #opsApprover
    path('ops/app/home/', views.opsapphome, name='opsapphome'),
    path('ops/app/action/', views.opsappaction, name='opsappaction'),
    path('logout_ops/app/', views.logout_opsapp, name='logout_opsapp'),
    path('uat/date/<int:id>/', views.uatdate, name='uatdate'),
    path('after/close/2/', views.afterclose2, name='afterclose2'),
    path('ops/date/given/', views.opsdategiven, name='opsdategiven'),
    ###creator action
    # path('action/home/', views.actionhome, name='actionhome'),
    # path('action/table/', views.actiontable, name='actiontable'),
    # path('logout_creator/action/', views.logout_creatoraction, name='logout_creatoraction'),

]
