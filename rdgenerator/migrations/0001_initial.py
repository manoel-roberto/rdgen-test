# 0001_initial.py - Migração inicial do app rdgenerator
# Este arquivo foi gerado automaticamente pelo Django em 26/09/2024 às 14:48
# Migrações são arquivos Python que descrevem mudanças no banco de dados
# Elas permitem versionar o schema do banco e aplicar mudanças de forma controlada
# Para mais informações: https://docs.djangoproject.com/pt-br/5.0/topics/migrations/

# Importações necessárias para criar migrações
# 'migrations' - Framework de migrações do Django
# 'models' - Tipos de campos de modelo disponíveis
from django.db import migrations, models


class Migration(migrations.Migration):
    # Classe que representa uma migração específica
    # Cada migração tem um número sequencial (0001, 0002, etc.)

    # Indica que esta é a primeira migração do app (cria tabelas do zero)
    initial = True

    # Lista de migrações das quais esta depende
    # Vazia para migrações iniciais, pois não há dependências anteriores
    dependencies = [
    ]

    # Lista de operações a serem executadas nesta migração
    # Cada operação representa uma mudança no banco de dados
    operations = [
        # Operação para criar o modelo GithubRun
        migrations.CreateModel(
            # Nome do modelo a ser criado
            name='GithubRun',
            # Campos do modelo (equivalentes aos campos em models.py)
            fields=[
                # Campo 'id': chave primária inteira
                # primary_key=True: identifica como chave primária
                # serialize=False: não incluir no JSON de serialização
                # verbose_name='ID': nome legível para interfaces admin
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='ID')),

                # Campo 'uuid': string para armazenar UUID único da execução
                # max_length=100: tamanho máximo da string
                # verbose_name='uuid': nome legível
                ('uuid', models.CharField(max_length=100, verbose_name='uuid')),

                # Campo 'status': string para armazenar status da execução
                # max_length=100: tamanho máximo da string
                # verbose_name='status': nome legível
                ('status', models.CharField(max_length=100, verbose_name='status')),
            ],
        ),
    ]
