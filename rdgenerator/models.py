# models.py - Definição dos modelos de dados da aplicação RDGen
# Este arquivo contém os modelos Django que representam as tabelas do banco de dados
# usados para armazenar informações sobre as execuções de geração de clientes.
# Para mais informações sobre modelos: https://docs.djangoproject.com/pt-br/5.0/topics/db/models/

# Importação do módulo models do Django
# Fornece classes base e tipos de campo para definir modelos de dados
from django.db import models


class GithubRun(models.Model):
    # Modelo Django que representa uma execução do GitHub Actions para geração de cliente
    # Cada registro nesta tabela corresponde a uma solicitação de build feita pelo usuário
    # Usado para rastrear o progresso e status das gerações de cliente RustDesk

    # Campo de chave primária personalizada (normalmente Django cria 'id' automaticamente)
    # IntegerField: armazena números inteiros (range: -2.147.483.648 a 2.147.483.647)
    # primary_key=True: identifica este campo como chave primária da tabela
    # verbose_name="ID": nome legível para interfaces admin e formulários
    # Exemplo: 1, 2, 3, 4... (sequencial, mas pode ser definido manualmente)
    id = models.IntegerField(verbose_name="ID", primary_key=True)

    # Campo para armazenar o UUID único da execução
    # CharField: string de tamanho fixo/variável
    # max_length=100: tamanho máximo da string (suficiente para UUID v4)
    # verbose_name="uuid": nome legível
    # UUID segue formato: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    # Exemplo: "550e8400-e29b-41d4-a716-446655440000"
    # Usado para identificar exclusivamente cada solicitação de geração
    uuid = models.CharField(verbose_name="uuid", max_length=100)

    # Campo para armazenar o status atual da execução
    # CharField: string de tamanho variável
    # max_length=100: tamanho máximo (suficiente para mensagens de status)
    # verbose_name="status": nome legível
    # Valores possíveis: "Starting generator...please wait", "Building...", "Success", "Failed", etc.
    # Atualizado via API calls dos workflows do GitHub Actions
    status = models.CharField(verbose_name="status", max_length=100)

    # Método __str__ poderia ser adicionado para representação legível:
    # def __str__(self):
    #     return f"Execução {self.uuid} - Status: {self.status}"

    # Meta class poderia ser adicionada para configurações avançadas:
    # class Meta:
    #     ordering = ['-id']  # Ordenar por ID decrescente
    #     verbose_name = 'Execução do GitHub'
    #     verbose_name_plural = 'Execuções do GitHub'
