# settings.py - Arquivo de configurações do projeto Django RDGen
# Este arquivo contém todas as configurações essenciais para o funcionamento da aplicação Django.
# Ele é gerado automaticamente pelo comando 'django-admin startproject' e personalizado para o projeto RDGen.
# Para mais informações sobre configurações do Django, consulte: https://docs.djangoproject.com/pt-br/5.0/topics/settings/

"""
Configurações do Django para o projeto rdgen.

Gerado pelo 'django-admin startproject' usando Django 5.0.3.

Para mais informações sobre este arquivo, consulte
https://docs.djangoproject.com/pt-br/5.0/topics/settings/

Para a lista completa de configurações e seus valores, consulte
https://docs.djangoproject.com/pt-br/5.0/ref/settings/
"""

# Importações necessárias para as configurações
# 'os' - Módulo para interagir com o sistema operacional (acesso a variáveis de ambiente, caminhos, etc.)
# 'Path' - Classe para manipulação de caminhos de arquivos de forma segura e cross-platform
import os
from pathlib import Path

# Construção de caminhos dentro do projeto de forma segura
# BASE_DIR aponta para o diretório pai do arquivo settings.py (raiz do projeto)
# Exemplo: se settings.py estiver em /home/user/project/rdgen/settings.py, BASE_DIR será /home/user/project
# Uso: BASE_DIR / 'subdir' cria caminhos como Path('/home/user/project/subdir')
BASE_DIR = Path(__file__).resolve().parent.parent

# Configurações de desenvolvimento e produção
# IMPORTANTE: Mantenha a SECRET_KEY em segredo em produção!
# A SECRET_KEY é usada para criptografia de sessões, cookies e outras funcionalidades de segurança
# Em produção, defina via variável de ambiente: export SECRET_KEY='sua-chave-secreta-aqui'
# Para gerar uma chave segura, use: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY = os.environ.get('SECRET_KEY','django-insecure-!(t-!f#6g#sr%yfded9(xha)g+=!6craeez^cp+*&bz_7vdk61')

# Credenciais para integração com GitHub API
# GHUSER: Nome de usuário do GitHub (ex: 'meuusuario')
# GHBEARER: Token de acesso pessoal do GitHub com permissões para Actions
# Como obter: https://github.com/settings/tokens (crie um token classic ou fine-grained)
# Permissões necessárias: repo (para acesso ao repositório) e workflow (para disparar workflows)
GHUSER = os.environ.get("GHUSER", '')
GHBEARER = os.environ.get("GHBEARER", '')

# URL de callback para workflows do GitHub Actions
# Deve ser a URL pública onde o servidor RDGen está rodando (ex: 'https://meu-dominio.com')
# Usada pelos workflows para enviar atualizações de status de volta para a aplicação
GENURL = os.environ.get("GENURL", '')

# Protocolo para URLs (http ou https)
# Padrão: 'https' para produção, 'http' para desenvolvimento local
PROTOCOL = os.environ.get("PROTOCOL", 'https')

# Nome do repositório GitHub onde os workflows estão hospedados
# Exemplo: 'rdgen' - deve corresponder ao repositório forkado do usuário
REPONAME = os.environ.get("REPONAME", 'rdgen')

# Configurações de mídia (uploads de arquivos)
# MEDIA_URL: URL base para acessar arquivos de mídia via web (ex: '/media/')
# MEDIA_ROOT: Caminho absoluto no servidor onde os arquivos são armazenados fisicamente
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Configuração de modo de depuração
# DEBUG = True: Mostra páginas de erro detalhadas e ativa ferramentas de desenvolvimento
# DEBUG = False: Oculta informações sensíveis em produção
# IMPORTANTE: Sempre defina DEBUG = False em produção para evitar vazamento de informações
DEBUG = False

# Lista de hosts permitidos para acessar a aplicação
# Em desenvolvimento: ['localhost', '127.0.0.1']
# Em produção: ['meu-dominio.com', 'www.meu-dominio.com']
# ALLOWED_HOSTS = ['*'] permite qualquer host (útil para desenvolvimento, mas inseguro para produção)
ALLOWED_HOSTS = ['*']

# Configuração opcional para CSRF (Cross-Site Request Forgery) em produção
# Descomentado quando necessário: CSRF_TRUSTED_ORIGINS = ['https://meu-dominio.com']
#CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', '').split()

# Definição das aplicações instaladas no projeto
# Cada app Django precisa ser listado aqui para ser reconhecido pelo framework
# Apps padrão do Django + apps customizados do projeto
INSTALLED_APPS = [
    'django.contrib.admin',        # Interface administrativa do Django
    'django.contrib.auth',         # Sistema de autenticação de usuários
    'django.contrib.contenttypes', # Framework para tipos de conteúdo
    'django.contrib.sessions',     # Gerenciamento de sessões
    'django.contrib.messages',     # Sistema de mensagens para usuários
    'django.contrib.staticfiles',  # Gerenciamento de arquivos estáticos (CSS, JS, imagens)
    'rdgenerator',                 # App customizado para geração de clientes RustDesk
]

# Configuração do middleware
# Middleware são camadas que processam requisições/respostas HTTP
# Ordem importa: executados de cima para baixo na requisição, inverso na resposta
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',        # Adiciona headers de segurança
    'django.contrib.sessions.middleware.SessionMiddleware',  # Gerencia sessões
    'django.middleware.common.CommonMiddleware',            # Headers comuns e redirecionamentos
    #'django.middleware.csrf.CsrfViewMiddleware',           # Proteção CSRF (desabilitado neste projeto)
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Autenticação de usuários
    'django.contrib.messages.middleware.MessageMiddleware',  # Sistema de mensagens
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Proteção contra clickjacking
]

# Configuração das URLs principais
# Aponta para o arquivo urls.py que define as rotas da aplicação
ROOT_URLCONF = 'rdgen.urls'

# Configuração dos templates
# Define como o Django encontra e renderiza templates HTML
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Engine de templates
        'DIRS': [],                    # Diretórios adicionais para procurar templates (vazio = só em apps)
        'APP_DIRS': True,              # Procura templates nas pastas 'templates' dos apps
        'OPTIONS': {
            'context_processors': [    # Funções disponíveis em todos os templates
                'django.template.context_processors.debug',       # Debug info
                'django.template.context_processors.request',      # Objeto request
                'django.contrib.auth.context_processors.auth',     # Usuário autenticado
                'django.contrib.messages.context_processors.messages', # Mensagens do sistema
            ],
        },
    },
]

# Configuração do servidor WSGI
# Aponta para o arquivo wsgi.py para deployment
WSGI_APPLICATION = 'rdgen.wsgi.application'


# Configuração do banco de dados
# Define qual banco usar e suas configurações de conexão
# Padrão: SQLite (banco de arquivo, ideal para desenvolvimento)
# Para produção, considere PostgreSQL ou MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Driver do banco
        'NAME': BASE_DIR / 'db.sqlite3',          # Caminho para o arquivo do banco
    }
}

# Exemplo para PostgreSQL (descomente e configure se necessário):
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'nome_do_banco',
#         'USER': 'usuario',
#         'PASSWORD': 'senha',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }


# Validadores de senha para usuários
# Funções que verificam a força das senhas durante criação/alteração
# Melhoram a segurança exigindo senhas complexas
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        # Evita senhas similares ao nome/email do usuário
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        # Exige comprimento mínimo (padrão: 8 caracteres)
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        # Bloqueia senhas comuns como 'password', '123456', etc.
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        # Evita senhas compostas apenas por números
    },
]


# Configurações de internacionalização
# Controlam idioma, fuso horário e formatação de datas/números

# Idioma padrão da aplicação (códigos ISO: 'en-us', 'pt-br', 'es-es', etc.)
LANGUAGE_CODE = 'en-us'

# Fuso horário padrão (lista completa: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
TIME_ZONE = 'UTC'

# Habilita tradução de textos da interface
USE_I18N = True

# Habilita fuso horário (armazena datas como UTC, converte para TIME_ZONE na exibição)
USE_TZ = True


# Configurações de arquivos estáticos (CSS, JavaScript, imagens)
# Arquivos que não mudam frequentemente e podem ser servidos diretamente pelo servidor web

# URL base para acessar arquivos estáticos (ex: '/static/')
STATIC_URL = 'static/'

# Diretório onde os arquivos estáticos são coletados para produção
# Comando 'python manage.py collectstatic' copia arquivos aqui
# STATIC_ROOT = BASE_DIR / 'staticfiles'  # Descomente para produção

# Diretórios adicionais para procurar arquivos estáticos durante desenvolvimento
# STATICFILES_DIRS = [BASE_DIR / 'static']  # Descomente se necessário

# Tipo de campo padrão para chaves primárias automáticas
# 'BigAutoField' suporta valores maiores que 'AutoField' (útil para bancos grandes)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Tamanho máximo de upload de arquivos em memória (em bytes)
# Arquivos maiores que isso são armazenados temporariamente em disco
# None = sem limite (cuidado com ataques de DoS)
# Exemplo: 10MB = 10 * 1024 * 1024
DATA_UPLOAD_MAX_MEMORY_SIZE = None
