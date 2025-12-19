#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

Este script é o ponto de entrada para todos os comandos administrativos do Django no projeto RDGen.
Ele configura o ambiente Django e executa comandos como runserver, migrate, makemigrations, etc.

Comandos comuns:
- python manage.py runserver: Inicia servidor de desenvolvimento
- python manage.py migrate: Aplica migrações do banco de dados
- python manage.py makemigrations: Cria novas migrações baseadas em mudanças nos modelos
- python manage.py createsuperuser: Cria usuário administrador
- python manage.py test: Executa testes automatizados
- python manage.py shell: Abre shell interativo do Django

Para mais informações: https://docs.djangoproject.com/pt-br/5.0/ref/django-admin/
"""

# Importações necessárias
import os  # Para manipulação de variáveis de ambiente e sistema operacional
import sys  # Para acesso aos argumentos da linha de comando


def main():
    """
    Função principal que executa tarefas administrativas do Django.

    Esta função:
    1. Define o módulo de settings do Django
    2. Tenta importar o executor de comandos do Django
    3. Executa o comando passado via linha de comando

    Args:
        Nenhum (usa sys.argv para argumentos da linha de comando)

    Raises:
        ImportError: Se Django não estiver instalado ou não for encontrado
    """
    # Define qual arquivo settings.py usar
    # IMPORTANTE: Deve corresponder ao nome do seu projeto Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rdgen.settings')

    # Tenta importar o executor de comandos do Django
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Erro se Django não estiver instalado ou acessível
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Executa o comando passado via linha de comando
    # sys.argv contém todos os argumentos passados ao script
    # Exemplo: ['manage.py', 'runserver', '8000']
    execute_from_command_line(sys.argv)


# Executa a função main se o script for chamado diretamente
# Padrão Python: if __name__ == '__main__':
if __name__ == '__main__':
    main()
