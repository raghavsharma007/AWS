from django import forms
from.models import Fillup

class FillupForm(forms.ModelForm):
    # client_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'enter client name'}))
    # request_synopsis = forms.Textarea(widget=forms.TextInput(attrs={'placeholder':'Enter'}))
    # contract_received_date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control'}))
    # client_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'enter client name'}))
    # current_status= forms.CharField(widget=forms.D(attrs={'class':'bootstrap-select'}))

    class Meta:
        model = Fillup
        fields = [
            'client_type',
            'client_name',
            'request_synopsis',
            'target_launch_date',
        ]

        widgets = {
            'target_launch_date': forms.DateInput(attrs={'type': 'date'}),
            # 'current_status': forms.CharField(attrs={'class' : 'bootstrap-select'}),
        }

