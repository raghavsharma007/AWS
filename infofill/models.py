from django.db import models

class Fillup(models.Model):
    client_name = models.CharField(max_length=50, null=True, blank=True)
    client_type = models.CharField(choices=(('Existing Client Enhancement','Existing Client Enhancement'),('New Client Onboarding','New Client Onboarding')),max_length=50, default=None, null=True, blank=True)
    request_created_date = models.DateField(auto_now_add=True, editable=False)
    target_launch_date = models.DateField(null=True, default=None)
    request_synopsis = models.TextField(default='', null=True, blank=True)
    estimated_date = models.DateField(null=True, default=None, blank=True)
    actual_live_date = models.DateField(null=True, default=None, blank=True)
    current_status = models.CharField(max_length=100, blank=True, null=True)
    approval = models.CharField(choices=(('Pending','Pending'),('Approved','Approved'),('Reject','Reject')),max_length=20,default='Pending', blank=True)
    ontime_status = models.CharField(max_length=50, default='', null=True, blank=True)
    remarks = models.TextField(default='', null=True, blank=True)
    action = models.CharField(choices=(('Live','Live'),('Hold','Hold'),('Stop','Stop')),max_length=20, default='', blank=True,null=True)
    uat_date = models.DateField(null=True, default=None, blank=True)
    close = models.CharField(max_length=50, null=True, blank=True)
    close_2 = models.CharField(max_length=50, null=True, blank=True)



    def __str__(self):
        return '%s %s' %(self.client_name, self.approval)

class LoggedIn(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField()
    role = models.CharField(choices=(('Sales','Sales'),('Sales Approver','Sales Approver'),('IT Approver','IT Approver'),('OPS Approver','OPS Approver')),max_length=50)


    def __str__(self):
        return '%s %s' %(self.name, self.role)

class Link(models.Model):
    link = models.CharField(max_length=100)

    def __str__(self):
        return self.link