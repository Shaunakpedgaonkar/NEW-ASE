from django import forms
from core_app.models import Incident


class IncidentStatusForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['status']  # Add other fields as needed
