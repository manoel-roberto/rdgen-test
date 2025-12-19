# gunicorn.conf.py - Configuração do servidor WSGI Gunicorn para RDGen
# Gunicorn é um servidor WSGI HTTP para Python, usado em produção para servir aplicações Django

import os

# Configurações principais do Gunicorn
# Ajustar estes valores conforme necessário baseado nos recursos do sistema

# Endereço e porta onde o Gunicorn irá escutar conexões
# 0.0.0.0 permite conexões de qualquer interface de rede
bind = "0.0.0.0:8000"

# Número de processos worker para concorrência
# Mais workers = melhor performance, mas consome mais memória
# Regra geral: 2 * CPU cores + 1
workers = 3

# Ativar ambiente virtual (se aplicável)
# Define se deve ativar um virtualenv antes de iniciar os workers
activate_base = True

# Caminho para o módulo WSGI da aplicação Django
# Deve apontar para o objeto application no arquivo wsgi.py
wsgi_app = "rdgen.wsgi.application"