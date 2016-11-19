from django import forms
from .models import Aluno, Voluntario

import datetime

class AlunoForm(forms.ModelForm):
	class Meta:
		model = Aluno
		fields = ['ds_nome', 'dt_nasc', 'ds_telefone', 'ds_email']
		fields_names = {
			'ds_nome': 'Nome completo',
			'ds_email': 'Email (opcional)',
		}
		widgets = {	'ds_telefone': forms.NumberInput, }

class VoluntarioForm(forms.ModelForm):
	class Meta:
		model = Voluntario
		fields = ['ds_nome', 'ds_email', 'ds_telefone', 'escola', 'curso']
		widgets = {	'ds_telefone': forms.NumberInput, }

class PresencaAlunoForm(forms.Form):
	dt_presenca = forms.DateField(label='Data', initial=datetime.date.today())
	no_hora_aula = forms.IntegerField(label='Hora aula', min_value=1, initial=4)
	lista_presentes = forms.CharField(max_length=300, widget=forms.HiddenInput, required=False)

class PresencaVoluntarioForm(forms.Form):
	dt_presenca = forms.DateField(label='Data', initial=datetime.date.today())
	no_hora_aula = forms.IntegerField(label='Hora aula', min_value=1, initial=4)
	lista_presentes = forms.CharField(max_length=300, widget=forms.HiddenInput, required=False)

class QuestionarioForm(forms.Form):
	lista_respostas = forms.CharField(max_length=500, widget=forms.HiddenInput, required=False)
