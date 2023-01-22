from django import forms

from .models import Echeance, Formation

class CalculatriceCpfForm(forms.Form):
    formation = forms.ModelChoiceField(queryset=Formation.objects.all())
    echeance = forms.ModelChoiceField(queryset=Echeance.objects.all())
    solde_cpf = forms.DecimalField(min_value=500)

