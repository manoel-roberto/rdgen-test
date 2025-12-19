# admin.py - Configuração da interface administrativa do Django para o app rdgenerator
# Este arquivo registra os modelos do app no Django Admin, criando uma interface web
# para gerenciar dados do banco sem precisar de código customizado
# Para mais informações: https://docs.djangoproject.com/pt-br/5.0/ref/contrib/admin/

# Importação do módulo admin do Django
# Fornece a classe admin e funções para registrar modelos
from django.contrib import admin

# Registro de modelos no Django Admin
# Aqui você registra os modelos que deseja gerenciar via interface web
# Exemplo: admin.site.register(MeuModelo)
# Isso cria automaticamente páginas para listar, criar, editar e excluir registros

# Para o app rdgenerator, podemos registrar o modelo GithubRun:
# from .models import GithubRun
# admin.site.register(GithubRun)

# O registro permite:
# - Visualizar lista de execuções do GitHub
# - Ver detalhes de cada execução (UUID, status)
# - Filtrar e buscar execuções
# - Editar status manualmente se necessário
# - Excluir registros antigos

# Exemplo de registro com personalização:
# @admin.register(GithubRun)
# class GithubRunAdmin(admin.ModelAdmin):
#     list_display = ['id', 'uuid', 'status']  # Campos mostrados na lista
#     list_filter = ['status']  # Filtros laterais
#     search_fields = ['uuid']  # Campo de busca
#     readonly_fields = ['id', 'uuid']  # Campos somente leitura

# Registre seus modelos aqui quando precisar de interface administrativa.
