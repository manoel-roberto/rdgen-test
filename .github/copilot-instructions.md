# Instruções do Copilot para RDGen

## Visão Geral do Projeto
RDGen é uma aplicação web Django que gera instaladores personalizados de clientes RustDesk. Os usuários enviam formulários com opções de personalização, o que aciona fluxos de trabalho do GitHub Actions para construir clientes específicos para plataformas (Windows, Linux, macOS, Android) usando o código-fonte do RustDesk.

## Arquitetura
- **Backend**: Django 5.0 com um único app `rdgenerator`
- **Sistema de Build**: Fluxos de trabalho do GitHub Actions despachados via chamadas de API
- **Armazenamento**: Banco de dados SQLite para rastreamento de execuções; armazenamento de arquivos em `png/` (ícones/logos) e `exe/` (clientes construídos)
- **Integração**: Usa API do GitHub para acionadores de fluxo de trabalho; suporta callbacks de servidor de API externo

## Componentes Principais
- `rdgenerator/views.py`: Lógica principal - processamento de formulários, chamadas de API do GitHub, serviço de arquivos
- `rdgenerator/forms.py`: Formulário extenso com opções de personalização do RustDesk (permissões, temas, servidores)
- `rdgenerator/models.py`: Modelo `GithubRun` rastreia status de build por UUID
- `.github/workflows/generator-*.yml`: Fluxos de trabalho de build específicos para plataformas
- Templates: `generator.html` (formulário), `waiting.html` (polling), `generated.html` (download)

## Fluxos de Trabalho Críticos
- **Geração de Cliente**: Formulário → Criação de UUID → Salvamento de PNG → Codificação Base64 de JSON personalizado → Despacho de fluxo de trabalho do GitHub → Polling de status → Download
- **Atualizações de Status**: Fluxos de trabalho chamam de volta o endpoint `/updategh` para atualizar `GithubRun.status`
- **Serviço de Arquivos**: Clientes armazenados em `exe/{uuid}/filename`, servidos via view `/download`

## Variáveis de Ambiente
- `GHUSER`/`GHBEARER`: Credenciais do GitHub para acesso à API
- `GENURL`: URL pública para callbacks de fluxo de trabalho
- `PROTOCOL`/`REPONAME`: Padrões para HTTPS e 'rdgen'

## Comandos de Desenvolvimento
- `python manage.py runserver 0.0.0.0:8000`: Iniciar servidor de desenvolvimento
- `python manage.py migrate`: Configurar banco de dados
- `docker compose up -d`: Implantação em produção
- `pip install -r requirements.txt`: Instalar dependências

## Padrões de Código
- **Uso de UUID**: Cada solicitação recebe `str(uuid.uuid4())` para organização e rastreamento de arquivos
- **Codificação Base64**: JSON de configurações personalizadas codificado para entradas de fluxo de trabalho (limites de entrada do GitHub)
- **Polling**: Frontend faz polling em `/check_for_file` para conclusão do build
- **Manipulação de Arquivos**: `save_png()` lida com arquivos enviados e strings base64
- **API do GitHub**: Usa `requests` para POST em `/actions/workflows/{workflow}/dispatches`

## Convenções
- Configurações personalizadas usam strings 'Y'/'N' para valores booleanos em JSON
- Servidor padrão do RustDesk: `rs-ny.rustdesk.com`
- Redimensionamento de ícone/logo para largura máxima de 200px
- Sanitização de nome de arquivo: Apenas ASCII, substituir caracteres especiais por underscores</content>
<parameter name="filePath">/home/manoel/Projects/rdgen-test/.github/copilot-instructions.md