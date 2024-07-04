from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['complaint_against', 'content']
        widgets = {
            'complaint_against': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'form-control'}),
        }


