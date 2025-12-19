# views.py - Lógica principal da aplicação RDGen
# Este arquivo contém as views do Django que gerenciam a geração de clientes RustDesk personalizados.
# Inclui processamento de formulários, chamadas para API do GitHub e serviço de arquivos.

# Imports do Python/Django
import io  # Para manipulação de buffers de bytes (imagens)
from pathlib import Path  # Para operações com caminhos de arquivos
from django.http import HttpResponse, JsonResponse  # Respostas HTTP do Django
from django.shortcuts import render  # Função para renderizar templates
from django.core.files.base import ContentFile  # Classe para arquivos em memória
import os  # Operações do sistema operacional
import re  # Expressões regulares
import requests  # Cliente HTTP para chamadas de API
import base64  # Codificação/decodificação base64
import json  # Manipulação de dados JSON
import uuid  # Geração de identificadores únicos
from django.conf import settings as _settings  # Configurações do Django
from django.db.models import Q  # Consultas complexas no banco de dados

# Imports do projeto
from .forms import GenerateForm  # Formulário de geração de cliente
from .models import GithubRun  # Modelo para rastreamento de builds
from PIL import Image  # Biblioteca Pillow para processamento de imagens
from urllib.parse import quote

def generator_view(request):
    # View principal que processa o formulário de geração de cliente RustDesk
    # Recebe dados do formulário, valida, processa configurações e dispara workflow do GitHub
    if request.method == 'POST':
        form = GenerateForm(request.POST, request.FILES)
        if form.is_valid():
            # Extração dos dados do formulário
            platform = form.cleaned_data['platform']  # Plataforma alvo (windows, linux, etc.)
            version = form.cleaned_data['version']  # Versão do RustDesk
            delayFix = form.cleaned_data['delayFix']  # Correção de delay
            cycleMonitor = form.cleaned_data['cycleMonitor']  # Monitor de ciclo
            xOffline = form.cleaned_data['xOffline']  # Modo offline
            hidecm = form.cleaned_data['hidecm']  # Ocultar CM
            removeNewVersionNotif = form.cleaned_data['removeNewVersionNotif']  # Remover notificação de nova versão
            server = form.cleaned_data['serverIP']  # Servidor personalizado
            key = form.cleaned_data['key']  # Chave pública
            apiServer = form.cleaned_data['apiServer']  # Servidor API
            urlLink = form.cleaned_data['urlLink']  # Link personalizado
            downloadLink = form.cleaned_data['downloadLink']  # Link de download
            # Valores padrão se não fornecidos
            if not server:
                server = 'rs-ny.rustdesk.com' #default rustdesk server
            if not key:
                key = 'OeVuKk5nlHiXp+APNn0Y3pC1Iwpwn44JGqrQCsWqmBw=' #default rustdesk key
            if not apiServer:
                apiServer = server+":21114"
            if not urlLink:
                urlLink = "https://rustdesk.com"
            if not downloadLink:
                downloadLink = "https://rustdesk.com/download"
            # Extração de mais configurações do formulário
            direction = form.cleaned_data['direction']  # Direção da conexão
            installation = form.cleaned_data['installation']  # Desabilitar instalação
            settings = form.cleaned_data['settings']  # Desabilitar configurações
            appname = form.cleaned_data['appname']  # Nome personalizado do app
            filename = form.cleaned_data['exename']  # Nome do arquivo executável
            compname = form.cleaned_data['compname']  # Nome da empresa
            if not compname:
                compname = "Purslane Ltd"
            compname = compname.replace("&","\\&")  # Escapar & para uso em comandos
            permPass = form.cleaned_data['permanentPassword']  # Senha permanente
            theme = form.cleaned_data['theme']  # Tema
            themeDorO = form.cleaned_data['themeDorO']  # Default ou Override para tema
            runasadmin = form.cleaned_data['runasadmin']  # Executar como admin
            passApproveMode = form.cleaned_data['passApproveMode']  # Modo de aprovação
            denyLan = form.cleaned_data['denyLan']  # Negar LAN
            enableDirectIP = form.cleaned_data['enableDirectIP']  # Habilitar IP direto
            autoClose = form.cleaned_data['autoClose']  # Fechar automaticamente
            permissionsDorO = form.cleaned_data['permissionsDorO']  # Default ou Override para permissões
            permissionsType = form.cleaned_data['permissionsType']  # Tipo de permissões
            enableKeyboard = form.cleaned_data['enableKeyboard']  # Habilitar teclado
            enableClipboard = form.cleaned_data['enableClipboard']  # Habilitar clipboard
            enableFileTransfer = form.cleaned_data['enableFileTransfer']  # Habilitar transferência de arquivos
            enableAudio = form.cleaned_data['enableAudio']  # Habilitar áudio
            enableTCP = form.cleaned_data['enableTCP']  # Habilitar TCP
            enableRemoteRestart = form.cleaned_data['enableRemoteRestart']  # Habilitar reinício remoto
            enableRecording = form.cleaned_data['enableRecording']  # Habilitar gravação
            enableBlockingInput = form.cleaned_data['enableBlockingInput']  # Habilitar bloqueio de entrada
            enableRemoteModi = form.cleaned_data['enableRemoteModi']  # Habilitar modificação remota
            removeWallpaper = form.cleaned_data['removeWallpaper']  # Remover wallpaper
            defaultManual = form.cleaned_data['defaultManual']  # Configurações manuais padrão
            overrideManual = form.cleaned_data['overrideManual']  # Configurações manuais override

            # Sanitização do nome do arquivo
            if all(char.isascii() for char in filename):
                filename = re.sub(r'[^\w\s-]', '_', filename).strip()
                filename = filename.replace(" ","_")
            else:
                filename = "rustdesk"
            # Sanitização do nome do app
            if not all(char.isascii() for char in appname):
                appname = "rustdesk"
            # Geração de UUID único para esta solicitação
            myuuid = str(uuid.uuid4())
            # Construção da URL completa para callbacks
            protocol = _settings.PROTOCOL
            host = request.get_host()
            full_url = f"{protocol}://{host}"
            # Processamento do ícone personalizado
            try:
                iconfile = form.cleaned_data.get('iconfile')
                if not iconfile:
                    iconfile = form.cleaned_data.get('iconbase64')
                iconlink = save_png(iconfile,myuuid,full_url,"icon.png")
            except:
                print("failed to get icon, using default")
                iconlink = "false"
            # Processamento do logo personalizado
            try:
                logofile = form.cleaned_data.get('logofile')
                if not logofile:
                    logofile = form.cleaned_data.get('logobase64')
                logolink = save_png(logofile,myuuid,full_url,"logo.png")
            except:
                print("failed to get logo")
                logolink = "false"

            ### Criação do JSON de configurações personalizadas para o cliente RustDesk
            decodedCustom = {}
            # Configurações gerais
            if direction != "Both":
                decodedCustom['conn-type'] = direction
            if installation == "installationN":
                decodedCustom['disable-installation'] = 'Y'
            if settings == "settingsN":
                decodedCustom['disable-settings'] = 'Y'
            if appname.upper != "rustdesk".upper and appname != "":
                decodedCustom['app-name'] = appname
            # Inicialização de dicionários para configurações padrão e override
            decodedCustom['override-settings'] = {}
            decodedCustom['default-settings'] = {}
            # Senha permanente
            if permPass != "":
                decodedCustom['password'] = permPass
            # Tema
            if theme != "system":
                if themeDorO == "default":
                    decodedCustom['default-settings']['theme'] = theme
                elif themeDorO == "override":
                    decodedCustom['override-settings']['theme'] = theme
            # Configurações de segurança
            decodedCustom['enable-lan-discovery'] = 'N' if denyLan else 'Y'
            decodedCustom['allow-auto-disconnect'] = 'Y' if autoClose else 'N'
            decodedCustom['allow-remove-wallpaper'] = 'Y' if removeWallpaper else 'N'
            # Configurações de permissões - controlam o que o usuário remoto pode fazer
            if permissionsDorO == "default":
                # Configurações padrão: usuário pode alterar, mas estes são os valores iniciais
                decodedCustom['default-settings']['access-mode'] = permissionsType  # 'custom' (permite escolher), 'full' (acesso total), 'view' (só visualização)
                # Permissões específicas - controlam funcionalidades remotas
                decodedCustom['default-settings']['enable-keyboard'] = 'Y' if enableKeyboard else 'N'  # Permite controle remoto do teclado
                decodedCustom['default-settings']['enable-clipboard'] = 'Y' if enableClipboard else 'N'  # Sincroniza conteúdo da área de transferência
                decodedCustom['default-settings']['enable-file-transfer'] = 'Y' if enableFileTransfer else 'N'  # Permite envio/recebimento de arquivos
                decodedCustom['default-settings']['enable-audio'] = 'Y' if enableAudio else 'N'  # Habilita áudio bidirecional (voz/microfone)
                decodedCustom['default-settings']['enable-tunnel'] = 'Y' if enableTCP else 'N'  # Tunelamento TCP para jogos/redes locais
                decodedCustom['default-settings']['enable-remote-restart'] = 'Y' if enableRemoteRestart else 'N'  # Permite reiniciar o PC remotamente
                decodedCustom['default-settings']['enable-record-session'] = 'Y' if enableRecording else 'N'  # Grava a sessão para arquivo
                decodedCustom['default-settings']['enable-block-input'] = 'Y' if enableBlockingInput else 'N'  # Bloqueia entrada do usuário local
                decodedCustom['default-settings']['allow-remote-config-modification'] = 'Y' if enableRemoteModi else 'N'  # Permite alterar config remotamente
                decodedCustom['default-settings']['direct-server'] = 'Y' if enableDirectIP else 'N'  # Conexão direta por IP (pula servidor central)
                decodedCustom['default-settings']['hide-cm'] = 'Y' if hidecm else 'N'  # Oculta campo de senha permanente na interface
                # Método de verificação: usa senha permanente ou ambas (temporária + permanente)
                decodedCustom['default-settings']['verification-method'] = 'use-permanent-password' if hidecm else 'use-both-passwords'
                decodedCustom['default-settings']['approve-mode'] = passApproveMode  # Como aprovar conexões: 'password', 'click', 'password-click'
            else:
                # Configurações override: usuário NÃO pode alterar estas configurações no cliente
                decodedCustom['override-settings']['access-mode'] = permissionsType
                decodedCustom['override-settings']['enable-keyboard'] = 'Y' if enableKeyboard else 'N'
                decodedCustom['override-settings']['enable-clipboard'] = 'Y' if enableClipboard else 'N'
                decodedCustom['override-settings']['enable-file-transfer'] = 'Y' if enableFileTransfer else 'N'
                decodedCustom['override-settings']['enable-audio'] = 'Y' if enableAudio else 'N'
                decodedCustom['override-settings']['enable-tunnel'] = 'Y' if enableTCP else 'N'
                decodedCustom['override-settings']['enable-remote-restart'] = 'Y' if enableRemoteRestart else 'N'
                decodedCustom['override-settings']['enable-record-session'] = 'Y' if enableRecording else 'N'
                decodedCustom['override-settings']['enable-block-input'] = 'Y' if enableBlockingInput else 'N'
                decodedCustom['override-settings']['allow-remote-config-modification'] = 'Y' if enableRemoteModi else 'N'

            # Processamento de configurações manuais avançadas
            # Permite ao usuário adicionar configurações customizadas não disponíveis na interface
            # Formato: uma configuração por linha, no formato chave=valor
            # Exemplos:
            # custom-resolution=1920x1080
            # disable-hwcodec=Y
            # max-bitrate=2048
            # idle-timeout=300
            for line in defaultManual.splitlines():
                line = line.strip()  # Remove espaços em branco
                if line and '=' in line:  # Verificar se não está vazia e contém '='
                    k, value = line.split('=', 1)  # Split apenas na primeira ocorrência de '='
                    decodedCustom['default-settings'][k.strip()] = value.strip()

            # Mesmo processamento para configurações override manuais
            for line in overrideManual.splitlines():
                line = line.strip()
                if line and '=' in line:
                    k, value = line.split('=', 1)
                    decodedCustom['override-settings'][k.strip()] = value.strip()
            
            # Codificação do JSON customizado em base64
            # Necessário porque o GitHub Actions tem limite de caracteres nos inputs
            # Base64 aumenta o tamanho em ~33%, mas permite transmissão segura de dados complexos
            # Processo: JSON → string UTF-8 → bytes → base64 → string ASCII
            decodedCustomJson = json.dumps(decodedCustom)  # Converte dicionário para string JSON
            string_bytes = decodedCustomJson.encode("ascii")  # Converte string para bytes ASCII
            base64_bytes = base64.b64encode(string_bytes)  # Codifica em base64
            encodedCustom = base64_bytes.decode("ascii")  # Converte bytes base64 para string ASCII

            # Criação do dicionário de extras (limite de 10 inputs no GitHub)
            extras = {}
            extras['genurl'] = _settings.GENURL  # URL para callbacks
            extras['runasadmin'] = runasadmin  # Executar como admin
            extras['urlLink'] = urlLink  # Link personalizado
            extras['downloadLink'] = downloadLink  # Link de download
            extras['delayFix'] = 'true' if delayFix else 'false'  # Correção de delay
            extras['version'] = version  # Versão
            extras['rdgen'] = 'true'  # Flag RDGen
            extras['cycleMonitor'] = 'true' if cycleMonitor else 'false'  # Monitor de ciclo
            extras['xOffline'] = 'true' if xOffline else 'false'  # Modo offline
            extras['hidecm'] = 'true' if hidecm else 'false'  # Ocultar CM
            extras['removeNewVersionNotif'] = 'true' if removeNewVersionNotif else 'false'  # Remover notificação
            extras['compname'] = compname  # Nome da empresa
            extra_input = json.dumps(extras)

            #### Disparo do workflow do GitHub Actions para build do cliente
            # Cada plataforma tem seu próprio workflow específico
            # URLs seguem o padrão: /repos/{owner}/{repo}/actions/workflows/generator-{platform}.yml/dispatches
            if platform == 'windows':
                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-windows.yml/dispatches' 
            elif platform == 'linux':
                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-linux.yml/dispatches'  
            elif platform == 'android':
                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-android.yml/dispatches'
            elif platform == 'macos':
                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-macos.yml/dispatches'
            else:
                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-windows.yml/dispatches'

            # Preparação dos dados para o POST na API do GitHub
            # Método POST com autenticação Bearer token
            # Headers incluem Accept para versão da API e Content-Type
            # Payload JSON com ref (branch) e inputs customizados
            data = {
                "ref":"master",
                "inputs":{
                    "server":server,
                    "key":key,
                    "apiServer":apiServer,
                    "custom":encodedCustom,
                    "uuid":myuuid,
                    "iconlink":iconlink,
                    "logolink":logolink,
                    "appname":appname,
                    "extras":extra_input,
                    "filename":filename,
                    "upload-tag": "Claude Haiku 4.5"  # Tag para upload, habilitando Claude Haiku 4.5
                }
            } 
            # Configuração dos headers para autenticação
            headers = {
                'Accept':  'application/vnd.github+json',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer '+_settings.GHBEARER,
                'X-GitHub-Api-Version': '2022-11-28'
            }
            # Criação do registro no banco de dados
            # Salva o UUID e status inicial para rastreamento do build
            # Permite polling posterior para verificar conclusão
            create_github_run(myuuid)
            # Envio da requisição para disparar o workflow
            # Status 204 indica sucesso (No Content)
            # Qualquer outro status indica erro na API
            response = requests.post(url, json=data, headers=headers)
            print(response)
            if response.status_code == 204:
                return render(request, 'waiting.html', {'filename':filename, 'uuid':myuuid, 'status':"Starting generator...please wait", 'platform':platform})
            else:
                return JsonResponse({"error": "Something went wrong"})
    else:
        # Método GET: exibir formulário vazio
        form = GenerateForm()
    #return render(request, 'maintenance.html')
    return render(request, 'generator.html', {'form': form})


def check_for_file(request):
    # View para verificar o status do build via polling
    # Frontend faz chamadas AJAX periódicas para esta view
    # Recebe filename, uuid e platform via parâmetros GET
    filename = request.GET['filename']
    uuid = request.GET['uuid']
    platform = request.GET['platform']
    # Consulta o status no banco de dados usando o UUID
    # GithubRun model armazena status atualizado pelos workflows
    gh_run = GithubRun.objects.filter(Q(uuid=uuid)).first()
    status = gh_run.status

    # Se o status for "Success", o build foi concluído com sucesso
    # Redirecionar para página de download com link para o arquivo
    if status == "Success":
        return render(request, 'generated.html', {'filename': filename, 'uuid':uuid, 'platform':platform})
    else:
        # Caso contrário, continuar mostrando página de espera
        # Status pode ser "Running", "Failed", etc.
        return render(request, 'waiting.html', {'filename':filename, 'uuid':uuid, 'status':status, 'platform':platform})

def download(request):
    # View para servir o arquivo executável gerado
    # Chamada quando usuário clica em "Download" na página generated.html
    # Recebe filename e uuid via parâmetros GET
    filename = request.GET['filename']
    uuid = request.GET['uuid']
    #filename = filename+".exe"
    # Construção do caminho absoluto do arquivo
    # Arquivos são organizados por UUID em subdiretórios: exe/{uuid}/{filename}
    file_path = os.path.join('exe',uuid,filename)
    # Leitura do arquivo em modo binário
    with open(file_path, 'rb') as file:
        # Criação da resposta HTTP com headers apropriados
        # Content-Type para executáveis Windows
        # Content-Disposition força download com nome do arquivo
        response = HttpResponse(file, headers={
            'Content-Type': 'application/vnd.microsoft.portable-executable',
            'Content-Disposition': f'attachment; filename="{filename}"'
        })

    return response

def get_png(request):
    # View para servir arquivos PNG (ícones/logos)
    # Usada pelos workflows do GitHub Actions para baixar ícones customizados
    # Recebe filename e uuid via parâmetros GET
    filename = request.GET['filename']
    uuid = request.GET['uuid']
    #filename = filename+".exe"
    # Construção do caminho: png/{uuid}/{filename}
    file_path = os.path.join('png',uuid,filename)
    # Leitura do arquivo em modo binário
    with open(file_path, 'rb') as file:
        # Resposta HTTP com Content-Type para PNG
        # Content-Disposition força download
        response = HttpResponse(file, headers={
            'Content-Type': 'image/png',
            'Content-Disposition': f'attachment; filename="{filename}"'
        })

    return response

def create_github_run(myuuid):
    # Função auxiliar para criar registro de run no banco de dados
    # Chamada após envio bem-sucedido para API do GitHub
    # Permite rastreamento do status do build
    new_github_run = GithubRun(
        uuid=myuuid,
        status="Starting generator...please wait"
    )
    new_github_run.save()

def update_github_run(request):
    # Endpoint para atualizar status do run (chamado pelo workflow)
    # Workflows do GitHub Actions fazem POST para este endpoint
    # Atualiza status no banco: "Running", "Success", "Failed", etc.
    # Permite que o frontend saiba quando o build terminou
    data = json.loads(request.body)
    myuuid = data.get('uuid')
    mystatus = data.get('status')
    GithubRun.objects.filter(Q(uuid=myuuid)).update(status=mystatus)
    return HttpResponse('')

def resize_and_encode_icon(imagefile):
    # Função para redimensionar e codificar ícones em base64
    # Recebe um arquivo de imagem enviado via formulário
    # Redimensiona para largura máxima de 200px mantendo proporção
    # Retorna imagem codificada em base64 para transmissão
    maxWidth = 200  # Largura máxima permitida para ícones
    try:
        # Carregar imagem do arquivo enviado em chunks
        with io.BytesIO() as image_buffer:
            for chunk in imagefile.chunks():
                image_buffer.write(chunk)
            image_buffer.seek(0)

            img = Image.open(image_buffer)
            imgcopy = img.copy()
    except (IOError, OSError):
        raise ValueError("Uploaded file is not a valid image format.")

    # Verificar se redimensionamento é necessário
    if img.size[0] <= maxWidth:
        # Imagem já tem tamanho adequado, apenas codificar
        with io.BytesIO() as image_buffer:
            imgcopy.save(image_buffer, format=imagefile.content_type.split('/')[1])
            image_buffer.seek(0)
            return_image = ContentFile(image_buffer.read(), name=imagefile.name)
        return base64.b64encode(return_image.read())

    # Calcular altura redimensionada mantendo proporção
    wpercent = (maxWidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))

    # Redimensionar imagem usando LANCZOS (alta qualidade)
    imgcopy = imgcopy.resize((maxWidth, hsize), Image.Resampling.LANCZOS)

    # Salvar imagem redimensionada em buffer
    with io.BytesIO() as resized_image_buffer:
        imgcopy.save(resized_image_buffer, format=imagefile.content_type.split('/')[1])
        resized_image_buffer.seek(0)

        resized_imagefile = ContentFile(resized_image_buffer.read(), name=imagefile.name)

    # Retornar codificação base64 da imagem redimensionada
    resized64 = base64.b64encode(resized_imagefile.read())
    #print(resized64)
    return resized64
 
# Função usada quando acessada de fonte externa, como servidor API RustDesk
def startgh(request):
    # Endpoint alternativo para iniciar builds via API externa
    # Permite integração com outros sistemas (ex: servidor RustDesk)
    # Recebe dados JSON via POST body em vez de formulário web
    #print(request)
    data_ = json.loads(request.body)
    #### Disparar workflow do GitHub, precisa de user, repo, access token
    # Monta URL do workflow baseada na plataforma recebida
    url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-'+data_.get('platform')+'.yml/dispatches'  
    # Prepara payload com todos os parâmetros necessários
    data = {
        "ref":"master",
        "inputs":{
            "server":data_.get('server'),
            "key":data_.get('key'),
            "apiServer":data_.get('apiServer'),
            "custom":data_.get('custom'),
            "uuid":data_.get('uuid'),
            "iconlink":data_.get('iconlink'),
            "logolink":data_.get('logolink'),
            "appname":data_.get('appname'),
            "extras":data_.get('extras'),
            "filename":data_.get('filename'),
            "upload-tag": "Claude Haiku 4.5"  # Tag para habilitar Claude Haiku 4.5
        }
    } 
    # Headers de autenticação idênticos aos da função principal
    headers = {
        'Accept':  'application/vnd.github+json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+_settings.GHBEARER,
        'X-GitHub-Api-Version': '2022-11-28'
    }
    # Envia requisição para GitHub Actions
    response = requests.post(url, json=data, headers=headers)
    print(response)
    # Retorna status 204 (No Content) indicando sucesso
    return HttpResponse(status=204)

def save_png(file, uuid, domain, name):
    # Função para salvar arquivos PNG (ícones/logos) no sistema de arquivos
    # Recebe arquivo (pode ser base64 string ou file object)
    # Salva em png/{uuid}/{name} criando diretório se necessário
    # Retorna JSON com informações do arquivo salvo
    file_save_path = "png/%s/%s" % (uuid, name)
    Path("png/%s" % uuid).mkdir(parents=True, exist_ok=True)

    if isinstance(file, str):  # Verificar se é string base64
        # Se for base64, decodificar e criar objeto ContentFile
        try:
            header, encoded = file.split(';base64,')
            decoded_img = base64.b64decode(encoded)
            file = ContentFile(decoded_img, name=name) # Criar objeto file-like
        except ValueError:
            print("Invalid base64 data")
            return None  # Ou tratar erro
        except Exception as e:  # Capturar exceções gerais na decodificação
            print(f"Error decoding base64: {e}")
            return None
        
    # Salvar arquivo no sistema de arquivos
    with open(file_save_path, "wb+") as f:
        for chunk in file.chunks():
            f.write(chunk)
    # Preparar resposta JSON com metadados do arquivo
    imageJson = {}
    imageJson['url'] = domain
    imageJson['uuid'] = uuid
    imageJson['file'] = name
    #return "%s/%s" % (domain, file_save_path)
    return json.dumps(imageJson)

def save_custom_client(request):
    # Endpoint para salvar cliente customizado enviado externamente
    # Usado por workflows do GitHub Actions para fazer upload do executável gerado
    # Recebe arquivo via multipart/form-data e UUID via POST
    # Salva em exe/{uuid}/{filename} criando diretório se necessário
    file = request.FILES['file']
    myuuid = request.POST.get('uuid')
    file_save_path = "exe/%s/%s" % (myuuid, file.name)
    Path("exe/%s" % myuuid).mkdir(parents=True, exist_ok=True)
    with open(file_save_path, "wb+") as f:
        for chunk in file.chunks():
            f.write(chunk)

    return HttpResponse("File saved successfully!")