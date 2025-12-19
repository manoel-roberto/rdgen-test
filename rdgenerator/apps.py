# apps.py - Configuração do app rdgenerator no Django
# Este arquivo define a configuração específica do app rdgenerator
# A classe AppConfig permite personalizar comportamento do app no Django
# Para mais informações: https://docs.djangoproject.com/pt-br/5.0/ref/applications/

# Importação da classe base AppConfig do Django
# Todas as configurações de app herdam desta classe
from django.apps import AppConfig


class RdgeneratorConfig(AppConfig):
    # Classe de configuração para o app 'rdgenerator'
    # Nome da classe segue convenção: NomeDoApp + Config

    # Tipo de campo padrão para chaves primárias automáticas neste app
    # BigAutoField suporta valores maiores que AutoField (até 9.2 quintilhões)
    # Útil para bancos de dados com muitos registros
    # Pode ser override por settings.DEFAULT_AUTO_FIELD
    default_auto_field = 'django.db.models.BigAutoField'

    # Nome do app (deve corresponder ao nome do diretório/pacote)
    # Usado pelo Django para identificar e referenciar este app
    # IMPORTANTE: Deve ser exatamente o nome do diretório do app
    name = 'rdgenerator'

    # Outras configurações opcionais que podem ser adicionadas:
    # verbose_name = 'Gerador de Clientes RD'  # Nome legível para o app
    # label = 'rdgenerator'  # Rótulo curto para o app
    # path = '/caminho/para/app'  # Caminho customizado (se necessário)
