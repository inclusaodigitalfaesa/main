from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^sobre/$', views.sobre, name='sobre'),
	url(r'^curso/(?P<curso_id>[0-9]+)/turma/(?P<turma_id>[0-9]+)/inscricao/aluno/$', views.inscricao_aluno, name='inscricao_aluno'),
	url(r'^curso/(?P<curso_id>[0-9]+)/turma/(?P<turma_id>[0-9]+)/inscricao/voluntario/$', views.inscricao_voluntario, name='inscricao_voluntario'),
	url(r'^sucesso/$', views.sucesso, name='sucesso'),
	url(r'^questionario/(?P<questionario_id>[0-9]+)/aluno/(?P<aluno_id>[0-9]+)/$', views.questionario, name='questionario'),
	url(r'^presenca/$', views.presenca, name='presenca'),
	url(r'^presenca/aluno/$', views.presenca_aluno, name='presenca_aluno'),
	url(r'^presenca/aluno/turma/(?P<turma_id>[0-9]+)/$', views.presenca_aluno_turma, name='presenca_aluno_turma'),
	url(r'^presenca/voluntario/$', views.presenca_voluntario, name='presenca_voluntario'),
	url(r'^presenca/voluntario/turma/(?P<turma_id>[0-9]+)/$', views.presenca_voluntario_turma, name='presenca_voluntario_turma'),
	url(r'^certificado/$', views.certificado, name='certificado'),
	url(r'^logout/$', views.logout_view, name='logout_view'),
] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)