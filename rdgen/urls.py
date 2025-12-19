# urls.py - Configuração de URLs para o projeto Django RDGen
# Este arquivo define as rotas (URLs) da aplicação e mapeia-as para as views correspondentes
# Cada URL pattern conecta uma requisição HTTP a uma função view que processa a requisição
# Para mais informações: https://docs.djangoproject.com/pt-br/5.0/topics/http/urls/

"""
Configuração de URLs para o projeto rdgen.

A lista `urlpatterns` roteia URLs para views. Para mais informações consulte:
    https://docs.djangoproject.com/pt-br/5.0/topics/http/urls/

Exemplos:
Funções view
    1. Adicione uma importação: from my_app import views
    2. Adicione uma URL a urlpatterns: path('', views.home, name='home')
Views baseadas em classe
    1. Adicione uma importação: from other_app.views import Home
    2. Adicione uma URL a urlpatterns: path('', Home.as_view(), name='home')
Incluindo outro URLconf
    1. Importe a função include: from django.urls import include, path
    2. Adicione uma URL a urlpatterns: path('blog/', include('blog.urls'))
"""

# Importação do módulo django para verificar a versão
# Necessário para compatibilidade entre versões do Django
import django

# Importação das views do app rdgenerator
# 'as views' evita conflitos de nome com outros módulos
from rdgenerator import views as views

# Lógica condicional para compatibilidade entre versões do Django
# Django 4.0+ usa 're_path' em vez de 'url' para expressões regulares
# Django < 4.0 usa 'url' do django.conf.urls
# Isso garante que o código funcione em diferentes versões do Django
if django.__version__.split('.')[0] >= '4':
    # Django 4.0+: importa re_path como url
    from django.urls import re_path as url
else:
    # Django < 4.0: importa url do django.conf.urls
    from django.conf.urls import url, include

# Lista de padrões de URL (urlpatterns)
# Cada entrada mapeia uma URL para uma view usando expressões regulares
# Sintaxe: url(padrão_regex, view_function, name='nome_opcional')
urlpatterns = [
    # URL raiz: exibe o formulário de geração de cliente
    # GET: mostra formulário HTML para configuração do cliente
    # POST: processa formulário e inicia geração via GitHub Actions
    # Template: generator.html
    url(r'^$', views.generator_view),

    # URL /generator: formulário de geração (alternativa à raiz)
    # Mesmo comportamento da URL raiz, para compatibilidade
    url(r'^generator', views.generator_view),

    # URL /check_for_file: verifica status do build via polling AJAX
    # GET: retorna JSON com status atual da execução (UUID via query param)
    # Usado pelo JavaScript frontend para atualizar status em tempo real
    # Respostas: {"status": "Building..."} ou {"file": "download_url"} quando pronto
    url(r'^check_for_file', views.check_for_file),

    # URL /download: serve o arquivo executável gerado para download
    # GET: serve arquivo binário do cliente personalizado
    # Parâmetros: uuid (identifica qual execução), filename (nome do arquivo)
    # Headers: Content-Disposition para forçar download
    url(r'^download', views.download),

    # URL /creategh: cria registro de execução no banco (usado internamente)
    # POST: cria novo registro GithubRun com UUID e status inicial
    # Chamado automaticamente quando uma geração é iniciada
    url(r'^creategh', views.create_github_run),

    # URL /updategh: atualiza status da execução (chamado pelos workflows)
    # POST: atualiza status de uma execução existente
    # Parâmetros: uuid, status (ex: "5% complete", "Success", "Failed")
    # Chamado pelos workflows do GitHub Actions via webhook/callback
    url(r'^updategh', views.update_github_run),

    # URL /startgh: endpoint para iniciar geração via API externa
    # POST: aceita dados JSON para iniciar geração programaticamente
    # Usado por integrações externas ou APIs de terceiros
    url(r'^startgh', views.startgh),

    # URL /get_png: serve arquivos PNG (ícones/logos) para download
    # GET: serve arquivos de imagem armazenados localmente
    # Parâmetros: filename (nome do arquivo), uuid (diretório da execução)
    # Usado pelos workflows para baixar ícones customizados
    url(r'^get_png', views.get_png),

    # URL /save_custom_client: salva cliente customizado enviado externamente
    # POST: recebe arquivo binário e o salva no servidor
    # Usado para armazenar clientes gerados externamente
    url(r'^save_custom_client', views.save_custom_client),
]
