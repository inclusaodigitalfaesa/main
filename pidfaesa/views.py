from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django import forms
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import logout
from easy_pdf.views import PDFTemplateView

from .models import *
from .forms import *

def index(request):
	cursos_ativos = Curso.objects.filter(is_ativo=True)
	turmas_ativas = Turma.objects.filter(is_ativo=True)

	context = {'cursos_ativos': cursos_ativos, 'turmas_ativas': turmas_ativas}
	return render(request, 'pidfaesa/index.html', context)

def inscricao_aluno(request, curso_id, turma_id):
	curso = Curso.objects.get(pk=curso_id)
	turma = Turma.objects.get(pk=turma_id)

	if request.method == 'POST':
		form = AlunoForm(request.POST)
		if form.is_valid():
			ds_nome = form.cleaned_data['ds_nome'].upper()
			dt_nasc = form.cleaned_data['dt_nasc']
			ds_telefone = form.cleaned_data['ds_telefone']
			ds_email = form.cleaned_data['ds_email'].lower()

			aluno = Aluno(ds_nome=ds_nome, dt_nasc=dt_nasc, ds_telefone=ds_telefone, ds_email=ds_email)
			aluno.turma = turma
			aluno.save()

			questionario = Questionario.objects.get(pk=curso.questionario.id)

			return redirect('questionario', questionario_id=questionario.id, aluno_id=aluno.id)
	else:
		form = AlunoForm()

	context = {'curso': curso, 'turma': turma, 'form': form}
	return render(request, 'pidfaesa/inscricao_aluno.html', context)

def questionario(request, questionario_id, aluno_id):
	questionario = Questionario.objects.get(pk=questionario_id)
	aluno = Aluno.objects.get(pk=aluno_id)

	ja_tem_respostas = Alun_Resp_Perg_Ques.objects.filter(aluno__id=aluno_id)

	if ja_tem_respostas.count() > 0:
		return redirect('sucesso')

	if request.method == 'POST':
		form = QuestionarioForm(request.POST)
		if form.is_valid():
			lista_respostas = form.cleaned_data['lista_respostas']

			if len(lista_respostas) > 0:
				respostas = lista_respostas[:-1].split(';')

				for index in range(len(respostas)):
					resposta_pergunta = respostas[index].split('-')
					pergunta = Pergunta.objects.get(pk=resposta_pergunta[0])
					resposta = Resposta.objects.get(pk=resposta_pergunta[1])

					r = Alun_Resp_Perg_Ques()
					r.aluno = aluno
					r.resposta = resposta
					r.pergunta = pergunta
					r.questionario = questionario
					r.save()

				return redirect('sucesso')
	else:
		form = QuestionarioForm()

	context = {'questionario': questionario, 'aluno': aluno, 'form': form}
	return render(request, 'pidfaesa/questionario.html', context)

def inscricao_voluntario(request, curso_id, turma_id):
	curso = Curso.objects.get(pk=curso_id)
	turma = Turma.objects.get(pk=turma_id)

	if request.method == 'POST':
		form = VoluntarioForm(request.POST)
		if form.is_valid():
			ds_nome = form.cleaned_data['ds_nome'].upper()
			ds_email = form.cleaned_data['ds_email'].lower()
			escola = form.cleaned_data['escola']
			curso = form.cleaned_data['curso']
			ds_telefone = form.cleaned_data['ds_telefone']

			turma  = Turma.objects.get(pk=turma_id)
			v = Voluntario(ds_nome=ds_nome, ds_email=ds_email, escola=escola, curso=curso, ds_telefone=ds_telefone)
			v.turma = turma
			v.save()

			return redirect('sucesso')
	else:
		form = VoluntarioForm()

	context = {'curso': curso, 'turma': turma, 'form': form}
	return render(request, 'pidfaesa/inscricao_voluntario.html', context)

def sucesso(request):
	return render(request, 'pidfaesa/sucesso.html')

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
@permission_required('pidfaesa.add_presencaaluno', raise_exception=True)
def presenca(request):
	return render(request, 'pidfaesa/presenca.html')

@login_required
@permission_required('pidfaesa.add_presencaaluno', raise_exception=True)
def presenca_aluno(request):
	turmas_ativas = Turma.objects.filter(is_ativo=True)

	context = {'turmas_ativas': turmas_ativas}
	return render(request, 'pidfaesa/presenca_aluno.html', context)

@login_required
@permission_required('pidfaesa.add_presencaaluno', raise_exception=True)
def presenca_aluno_turma(request, turma_id):
	turma = Turma.objects.get(pk=turma_id)
	alunos = Aluno.objects.filter(turma__id=turma_id).order_by('ds_nome')

	if request.method == 'POST':
		form = PresencaAlunoForm(request.POST)
		if form.is_valid():
			dt_presenca = form.cleaned_data['dt_presenca']
			no_hora_aula = form.cleaned_data['no_hora_aula']

			lista_presentes = form.cleaned_data['lista_presentes']
			if len(lista_presentes) > 0:
				presentes = lista_presentes[:-1].split(';')

				for p in presentes:
					presenca = PresencaAluno(dt_presenca=dt_presenca, no_hora_aula=no_hora_aula, is_presente=True)
					aluno = Aluno.objects.get(pk=p)
					presenca.aluno = aluno
					presenca.save()

				return HttpResponse('<h4>Registrado com sucesso!<br><a href="../../../">Retornar</a></h4>')
	else:
		form = PresencaAlunoForm()

	context = {'turma': turma, 'alunos': alunos, 'form': form}
	return render(request, 'pidfaesa/presenca_aluno_turma.html', context)

@login_required
@permission_required('pidfaesa.add_presencavoluntario', raise_exception=True)
def presenca_voluntario(request):
	turmas_ativas = Turma.objects.filter(is_ativo=True)

	context = {'turmas_ativas': turmas_ativas}
	return render(request, 'pidfaesa/presenca_voluntario.html', context)

@login_required
@permission_required('pidfaesa.add_presencavoluntario', raise_exception=True)
def presenca_voluntario_turma(request, turma_id):
	turma = Turma.objects.get(pk=turma_id)
	voluntarios = Voluntario.objects.filter(turma__id=turma_id).order_by('ds_nome')

	if request.method == 'POST':
		form = PresencaVoluntarioForm(request.POST)
		if form.is_valid():
			dt_presenca = form.cleaned_data['dt_presenca']
			no_hora_aula = form.cleaned_data['no_hora_aula']

			lista_presentes = form.cleaned_data['lista_presentes']
			if len(lista_presentes) > 0:
				presentes = lista_presentes[:-1].split(';')

				for p in presentes:
					presenca = PresencaVoluntario(dt_presenca=dt_presenca, no_hora_aula=no_hora_aula, is_presente=True)
					voluntario = Voluntario.objects.get(pk=p)
					presenca.voluntario = voluntario
					presenca.save()

				return HttpResponse('<h4>Registrado com sucesso!<br><a href="../../../">Retornar</a></h4>')
	else:
		form = PresencaVoluntarioForm()

	context = {'turma': turma, 'voluntarios': voluntarios, 'form': form}
	return render(request, 'pidfaesa/presenca_voluntario_turma.html', context)

def sobre(request):
	cursos_ativos = Curso.objects.filter(is_ativo=True)

	context = {'cursos_ativos': cursos_ativos}
	return render(request, 'pidfaesa/sobre.html', context)

@login_required
@permission_required('pidfaesa.add_presencavoluntario', raise_exception=True)
def relatorio(request):
	turmas_ativas = Turma.objects.filter(is_ativo=True)

	context = {'turmas_ativas': turmas_ativas}
	return render(request, 'pidfaesa/relatorio.html', context)

@login_required
@permission_required('pidfaesa.add_presencavoluntario', raise_exception=True)
def relatorio_turma(request, turma_id):
	turma = Turma.objects.get(pk=turma_id)
	alunos = Aluno.objects.filter(turma__id=turma_id)
	arpqs = Alun_Resp_Perg_Ques.objects.filter(aluno__in=alunos, pergunta__id=1)

	curso = Curso.objects.get(pk=turma.curso.id)
	questionario = Questionario.objects.get(pk=curso.questionario.id)
	pergunta_questionario = Pergunta.objects.filter(questionario__id=questionario.id).order_by('no_ordem')
	quant_perguntas = pergunta_questionario.count()

	dados = list()
	for p in pergunta_questionario:
		a = list()
		a.append(p)
		respostas = Resposta.objects.filter(pergunta__id=p.id).order_by('no_ordem')		
		b = list()				
		for r in respostas:
			c = list()
			count = Alun_Resp_Perg_Ques.objects.filter(pergunta__id=p.id, resposta__id=r.id).count()
			if count > 0:								
				c.append(r.ds_descricao)
				c.append(count)
				b.append(c)
		a.append(b)
		dados.append(a)

	context = {'turma': turma, 'arpqs': arpqs, 'dados': dados, 'quant_perguntas': quant_perguntas}
	return render(request, 'pidfaesa/relatorio_turma.html', context)

@login_required
@permission_required('pidfaesa.add_presencavoluntario', raise_exception=True)
def certificado(request):
	turmas_ativas = Turma.objects.filter(is_ativo=True)

	context = {'turmas_ativas': turmas_ativas}
	return render(request, 'pidfaesa/certificado.html', context)

@login_required
@permission_required('pidfaesa.add_presencavoluntario', raise_exception=True)
def certificado_turma(request, turma_id):
	turma = Turma.objects.get(pk=turma_id)
	alunos = Aluno.objects.filter(turma__id=turma_id).order_by('ds_nome')
	voluntarios = Voluntario.objects.filter(turma__id=turma_id).order_by('ds_nome')

	context = {'turma': turma, 'alunos': alunos, 'voluntarios': voluntarios}
	return render(request, 'pidfaesa/certificado_turma.html', context)

@login_required
@permission_required('pidfaesa.add_presencavoluntario', raise_exception=True)
def visquestionario(request):
	cursos_ativos = Curso.objects.filter(is_ativo=True)

	context = {'cursos_ativos': cursos_ativos}
	return render(request, 'pidfaesa/visquestionario.html', context)

@login_required
@permission_required('pidfaesa.add_presencavoluntario', raise_exception=True)
def visquestionario_curso(request, curso_id):
	curso = Curso.objects.get(pk=curso_id)
	questionario = Questionario.objects.get(pk=curso.questionario.id)

	context = {'curso': curso, 'questionario': questionario}
	return render(request, 'pidfaesa/visquestionario_curso.html', context)

class CertificadoAlunoView(PDFTemplateView):
	template_name = "pidfaesa/certificado_aluno.html"

	def get_context_data(self, **kwargs):
		context = super(CertificadoAlunoView, self).get_context_data(**kwargs)

		aluno_id = int(kwargs['aluno_id'])

		aluno = Aluno.objects.get(pk=aluno_id)
		turma = Turma.objects.get(pk=aluno.turma.id)
		curso = Curso.objects.get(pk=turma.curso.id)
		horas = aluno.get_total_horas

		context['aluno'] = aluno
		context['turma'] = turma
		context['curso'] = curso
		context['horas'] = horas
		context['pagesize'] = "A4"
		context['title'] = "Certificado"

		return context

	def render_to_response(self, context, **response_kwargs):
		response = super(CertificadoAlunoView, self).render_to_response(context, **response_kwargs)
		
		aluno = context['aluno']
		nome_aluno = aluno.ds_nome.upper()
		
		response_kwargs.setdefault('content_type', 'application/pdf')
		response['Content-Disposition'] = 'attachment; filename="CERTIFICADO - ' + nome_aluno +  '.pdf"'

		return response

class CertificadoVoluntarioView(PDFTemplateView):
	template_name = "pidfaesa/certificado_voluntario.html"

	def get_context_data(self, **kwargs):
		context = super(CertificadoVoluntarioView, self).get_context_data(**kwargs)

		voluntario_id = int(kwargs['voluntario_id'])

		voluntario = Voluntario.objects.get(pk=voluntario_id)
		turma = Turma.objects.get(pk=voluntario.turma.id)
		curso = Curso.objects.get(pk=turma.curso.id)
		horas = voluntario.get_total_horas

		context['voluntario'] = voluntario
		context['turma'] = turma
		context['curso'] = curso
		context['horas'] = horas
		context['pagesize'] = "A4"
		context['title'] = "Certificado"

		return context

	def render_to_response(self, context, **response_kwargs):
		response = super(CertificadoVoluntarioView, self).render_to_response(context, **response_kwargs)
		
		voluntario = context['voluntario']
		nome_voluntario = voluntario.ds_nome.upper()
		
		response_kwargs.setdefault('content_type', 'application/pdf')
		response['Content-Disposition'] = 'attachment; filename="CERTIFICADO - ' + nome_voluntario +  '.pdf"'

		return response
