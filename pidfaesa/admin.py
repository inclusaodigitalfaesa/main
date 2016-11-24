from django.contrib import admin

from .models import *

#admin.site.register(Alun_Resp_Perg_Ques)

class QuestionarioAdmin(admin.ModelAdmin):
    ordering = ['id']
admin.site.register(Questionario, QuestionarioAdmin)

class CursoAdmin(admin.ModelAdmin):
    list_display = ('ds_nome', 'is_ativo')
admin.site.register(Curso, CursoAdmin)

class TurmaAdmin(admin.ModelAdmin):
    list_display = ('ds_nome', 'curso', 'is_ativo')
    list_filter = ('curso',)
admin.site.register(Turma, TurmaAdmin)

class AlunoAdmin(admin.ModelAdmin):
    list_display = ('ds_nome', 'ds_telefone', 'ds_email')
    list_filter = ('turma', )
admin.site.register(Aluno, AlunoAdmin)

class VoluntarioAdmin(admin.ModelAdmin):
    list_display = ('ds_nome', 'ds_telefone', 'ds_email')
    list_filter = ('turma', 'escola', 'curso')
admin.site.register(Voluntario, VoluntarioAdmin)

class EscolaVoluntarioAdmin(admin.ModelAdmin):
    list_display = ('ds_nome', 'is_ativo')
admin.site.register(EscolaVoluntario, EscolaVoluntarioAdmin)

class CursoVoluntarioAdmin(admin.ModelAdmin):
    list_display = ('ds_nome', 'is_ativo')
admin.site.register(CursoVoluntario, CursoVoluntarioAdmin)

class RespostaInline(admin.StackedInline):
    model = Resposta
    extra = 5

class PerguntaAdmin(admin.ModelAdmin):
    list_display = ('ds_descricao', 'no_ordem')
    list_filter = ('questionario', )

    ordering = ['questionario', 'no_ordem']

    fieldsets = [
        ('Questionario', 
            {'fields': ['questionario']}
        ),
        ('Pergunta',
            {'fields': ['no_ordem','ds_descricao']}
        ),
    ]

    inlines = [RespostaInline]
admin.site.register(Pergunta, PerguntaAdmin)

class RespostaAdmin(admin.ModelAdmin):
    list_display = ('ds_descricao', 'no_ordem')
    list_filter = ('pergunta', )
    ordering = ['pergunta', 'no_ordem']
admin.site.register(Resposta, RespostaAdmin)

class Alun_Resp_Perg_QuesAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'dthr_criacao')
    list_filter = ('aluno', 'dthr_criacao', )
admin.site.register(Alun_Resp_Perg_Ques, Alun_Resp_Perg_QuesAdmin)

class PresencaAlunoAdmin(admin.ModelAdmin):
    #list_display = ('__str__', 'no_hora_aula')
    list_display = ('aluno', 'dt_presenca', 'no_hora_aula')
    list_filter = ('dt_presenca', 'aluno', )
admin.site.register(PresencaAluno, PresencaAlunoAdmin)

class PresencaVoluntarioAdmin(admin.ModelAdmin):
    #list_display = ('__str__', 'no_hora_aula')
    list_display = ('voluntario', 'dt_presenca', 'no_hora_aula')
    list_filter = ('dt_presenca', 'voluntario', )
admin.site.register(PresencaVoluntario, PresencaVoluntarioAdmin)

class CertificadoAdmin(admin.ModelAdmin):
    list_filter = ('turma', )
admin.site.register(Certificado, CertificadoAdmin)
