from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone

def get_60days_from_now():
    return datetime.date.today() + datetime.timedelta(days=60)

@python_2_unicode_compatible
class Questionario(models.Model):
    
    ds_titulo = models.CharField('Titulo', max_length=400)
    ds_descricao = models.TextField('Descricao', max_length=600)
    dthr_criacao = models.DateTimeField('Data de criacao', auto_now_add=True)

    class Meta:
        ordering = ["-pk"]

    def __str__(self):
        return self.ds_titulo

@python_2_unicode_compatible
class Curso(models.Model):
    ds_nome = models.CharField('Nome', max_length=400)  
    is_ativo = models.BooleanField('Ativo', default=True)  
    ds_descricao = models.TextField('Descricao', max_length=4000)
    ds_local = models.CharField('Local', max_length=300)    
    dthr_criacao = models.DateTimeField('Data de criacao', auto_now_add=True)

    questionario = models.ForeignKey(Questionario, models.SET_NULL, null=True)

    class Meta:
        ordering = ["-pk"]

    def __str__(self):
        return self.ds_nome

    def total_turmas_criadas(self):
        quant = Turma.objects.filter(curso__id=self.id).count()
        return (quant)

    def total_alunos_inscritos(self):
        turmas_criadas = self.turma_set.all()
        quant = 0
        for turma in turmas_criadas:
            quant += Aluno.objects.filter(turma__id=turma.id).count()
        return (quant)

    def total_voluntarios_inscritos(self):
        turmas_criadas = self.turma_set.all()
        quant = 0
        for turma in turmas_criadas:
            quant += Voluntario.objects.filter(turma__id=turma.id).count()
        return (quant)

    def get_turmas_ativas(self):
        return self.turma_set.filter(is_ativo=True)

@python_2_unicode_compatible
class Turma(models.Model):
    hora_ini_padrao = datetime.time(8,0,0)
    hora_fim_padrao = datetime.time(12,0,0)

    ds_nome = models.CharField('Nome', max_length=400)
    is_ativo = models.BooleanField('Ativo', default=True)
    ds_descricao = models.TextField('Descricao', max_length=2000)
    dt_ini = models.DateField('Data de inicio', default=datetime.date.today)
    dt_fim = models.DateField('Data de fim', default=get_60days_from_now)
    hr_ini = models.TimeField('Hora de inicio', default=hora_ini_padrao)
    hr_fim = models.TimeField('Hora de fim', default=hora_fim_padrao)
    no_carga_horaria = models.PositiveSmallIntegerField('Carga horaria')
    no_vagas = models.PositiveSmallIntegerField('Quantidade de vagas')
    no_vagas_extras = models.PositiveSmallIntegerField('Quantidade de vagas extras')    
    dthr_criacao = models.DateTimeField('Data de criacao', auto_now_add=True)

    curso = models.ForeignKey(Curso, models.CASCADE)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.ds_nome

    def imprime_data_turma(self):
        d1 = self.dt_ini.strftime('%d/%m/%y')
        d2 = self.dt_fim.strftime('%d/%m/%y')
        return str(d1) + " a " + str(d2)

    def no_vagas_preenchidas(self):
        qtde_alunos = Aluno.objects.filter(turma__id=self.id).count()
        return (qtde_alunos)

    def no_vagas_restantes(self):
        qtde_alunos = Aluno.objects.filter(turma__id=self.id).count()
        return (self.no_vagas - qtde_alunos)

    def no_vagas_restantes_com_extras(self):
        qtde_alunos = Aluno.objects.filter(turma__id=self.id).count()
        return (self.no_vagas + self.no_vagas_extras - qtde_alunos)

    def no_voluntarios(self):
        qtde_voluntarios = Voluntario.objects.filter(turma__id=self.id).count()
        return (qtde_voluntarios)

    def imprime_hora_turma(self):
        h1 = self.hr_ini.strftime('%H:%M')
        h2 = self.hr_fim.strftime('%H:%M')
        return str(h1) + " as " + str(h2) + "h"

@python_2_unicode_compatible
class Aluno(models.Model):
    
    ds_nome = models.CharField('Nome', max_length=400)
    dt_nasc = models.DateField('Data de nascimento')
    ds_telefone = models.CharField('Telefone', max_length=30)
    ds_email = models.EmailField('Email', max_length=200, blank=True)
    dthr_criacao = models.DateTimeField('Data de criacao', auto_now_add=True)

    turma = models.ForeignKey(Turma, models.CASCADE)

    class Meta:
        ordering = ["-pk"]

    def __str__(self):
        return self.ds_nome

    def get_total_horas(self):
        presencas = PresencaAluno.objects.filter(aluno__id=self.id)
        horas = 0
        for p in presencas:
            horas += p.no_hora_aula
        return horas

@python_2_unicode_compatible
class EscolaVoluntario(models.Model):
    
    ds_nome = models.CharField('Escola', max_length=400)
    is_ativo = models.BooleanField('Ativo', default=True)
    dthr_criacao = models.DateTimeField('Data de criacao', auto_now_add=True)

    class Meta:
        ordering = ["ds_nome"]
        verbose_name = 'Voluntario/Escola disponivel'
        verbose_name_plural = 'Voluntarios/Escolas disponiveis'

    def __str__(self):
        return self.ds_nome

@python_2_unicode_compatible
class CursoVoluntario(models.Model):
    
    ds_nome = models.CharField('Curso', max_length=400)
    is_ativo = models.BooleanField('Ativo', default=True)
    dthr_criacao = models.DateTimeField('Data de criacao', auto_now_add=True)

    class Meta:
        ordering = ["ds_nome"]
        verbose_name = 'Voluntario/Curso disponivel'
        verbose_name_plural = 'Voluntarios/Cursos disponiveis'

    def __str__(self):
        return self.ds_nome

@python_2_unicode_compatible
class Voluntario(models.Model):
    
    ds_nome = models.CharField('Nome', max_length=400)
    ds_email = models.EmailField('Email', max_length=200)
    escola = models.ForeignKey(EscolaVoluntario, models.CASCADE)
    curso = models.ForeignKey(CursoVoluntario, models.CASCADE)
    ds_telefone = models.CharField('Telefone', max_length=30)
    dthr_criacao = models.DateTimeField('Data de criacao', auto_now_add=True)

    turma = models.ForeignKey(Turma, models.CASCADE)

    class Meta:
        ordering = ["-pk"]

    def __str__(self):
        return self.ds_nome

    def get_total_horas(self):
        presencas = PresencaVoluntario.objects.filter(voluntario__id=self.id)
        horas = 0
        for p in presencas:
            horas += p.no_hora_aula
        return horas

@python_2_unicode_compatible
class Pergunta(models.Model):
    
    no_ordem = models.PositiveSmallIntegerField('Ordem')
    ds_descricao = models.CharField('Descricao', max_length=500)    
    dthr_criacao = models.DateTimeField('Data de criacao', auto_now_add=True)

    questionario = models.ForeignKey(Questionario, models.CASCADE)

    class Meta:
        ordering = ["no_ordem"]

    def __str__(self):
        return self.ds_descricao

@python_2_unicode_compatible
class Resposta(models.Model):
    
    no_ordem = models.PositiveSmallIntegerField('Ordem')
    ds_descricao = models.CharField('Descricao', max_length=300)    
    dthr_criacao = models.DateTimeField('Data de criacao', auto_now_add=True)

    class Meta:
        ordering = ["no_ordem"]

    pergunta = models.ForeignKey(Pergunta, models.CASCADE)

    def __str__(self):
        return self.ds_descricao

@python_2_unicode_compatible
class Alun_Resp_Perg_Ques(models.Model):
    
    aluno = models.ForeignKey(Aluno, models.CASCADE)
    resposta = models.ForeignKey(Resposta, models.CASCADE)
    pergunta = models.ForeignKey(Pergunta, models.CASCADE)
    questionario = models.ForeignKey(Questionario, models.CASCADE)
    dthr_criacao = models.DateTimeField('Data de criacao', auto_now_add=True)

    class Meta:
        ordering = ['questionario', 'pergunta', 'resposta', 'aluno']
        verbose_name = 'Quest/Perg/Resp/Alun'
        verbose_name_plural = 'Questionario/Pergunta/Resposta/Aluno'

    def __str__(self):
        return str(self.questionario.id) + '/'+ str(self.pergunta.id) + '/'+ str(self.resposta.id) + '/'+ str(self.aluno.id)

@python_2_unicode_compatible
class PresencaAluno(models.Model):

    aluno = models.ForeignKey(Aluno, models.CASCADE)
    
    dt_presenca = models.DateField('Data da presenca')
    no_hora_aula = models.PositiveSmallIntegerField('Hora aula')
    is_presente = models.BooleanField('Presente', default=False)
    dthr_criacao = models.DateTimeField('Data de criacao', auto_now_add=True)    

    class Meta:
        ordering = ['-dt_presenca', 'aluno']
        verbose_name = 'Presenca de Aluno'
        verbose_name_plural = 'Presencas de Alunos'

    def __str__(self):
        return str(self.dt_presenca) + ' / id:' + str(self.aluno.id)

@python_2_unicode_compatible
class PresencaVoluntario(models.Model):

    voluntario = models.ForeignKey(Voluntario, models.CASCADE)
    
    dt_presenca = models.DateField('Data da presenca')
    no_hora_aula = models.PositiveSmallIntegerField('Hora aula')
    is_presente = models.BooleanField('Presente', default=False)
    dthr_criacao = models.DateTimeField('Data de criacao', auto_now_add=True)    

    class Meta:
        ordering = ['-dt_presenca', 'voluntario']
        verbose_name = 'Presenca de Voluntario'
        verbose_name_plural = 'Presencas de Voluntarios'

    def __str__(self):
        return str(self.dt_presenca) + ' / id:' + str(self.voluntario.id)

@python_2_unicode_compatible
class Certificado(models.Model):
    
    html_body = models.TextField('Html body', max_length=600)
    dthr_criacao = models.DateTimeField('Data de criacao', auto_now_add=True)

    turma = models.ForeignKey(Turma, models.SET_NULL, null=True)

    def __str__(self):
        return str(self.html_body)
