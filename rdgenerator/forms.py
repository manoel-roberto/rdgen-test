# forms.py - Definição dos formulários da aplicação RDGen
# Este arquivo contém os formulários Django usados para coletar configurações
# de personalização dos clientes RustDesk dos usuários.

from django import forms
from PIL import Image

class GenerateForm(forms.Form):
    # Formulário principal para geração de cliente RustDesk personalizado
    # Contém campos para plataforma, versão, configurações de servidor, permissões, etc.
    
    # Campo para seleção da plataforma alvo
    platform = forms.ChoiceField(choices=[('windows','Windows'),('linux','Linux (atualmente indisponível)'),('android','Android'),('macos','macOS')], initial='windows')
    
    # Campo para seleção da versão do RustDesk
    version = forms.ChoiceField(choices=[('master','nightly'),('1.4.2','1.4.2'),('1.4.1','1.4.1'),('1.4.0','1.4.0'),('1.3.9','1.3.9'),('1.3.8','1.3.8'),('1.3.7','1.3.7'),('1.3.6','1.3.6'),('1.3.5','1.3.5'),('1.3.4','1.3.4'),('1.3.3','1.3.3')], initial='1.4.2')
    help_text="'master' é a versão de desenvolvimento (nightly build) com os recursos mais recentes, mas pode ser menos estável"
    
    # Campos para configurações gerais
    delayFix = forms.BooleanField(initial=True, required=False)  # Correção de delay
    cycleMonitor = forms.BooleanField(initial=False, required=False)  # Monitor de ciclo
    xOffline = forms.BooleanField(initial=False, required=False)  # Modo offline
    hidecm = forms.BooleanField(initial=False, required=False)  # Ocultar CM
    removeNewVersionNotif = forms.BooleanField(initial=False, required=False)  # Remover notificação de nova versão
    
    # Campos para configurações gerais do cliente
    exename = forms.CharField(label="Nome para arquivo EXE", required=True)  # Nome do executável
    appname = forms.CharField(label="Nome personalizado do app", required=False)  # Nome do aplicativo
    direction = forms.ChoiceField(widget=forms.RadioSelect, choices=[
        ('incoming', 'Apenas entrada'),
        ('outgoing', 'Apenas saída'),
        ('both', 'Bidirecional')
    ], initial='both')  # Direção da conexão
    installation = forms.ChoiceField(label="Desabilitar instalação", choices=[
        ('installationY', 'Não, habilitar instalação'),
        ('installationN', 'Sim, DESABILITAR instalação')
    ], initial='installationY')  # Controle de instalação
    settings = forms.ChoiceField(label="Desabilitar configurações", choices=[
        ('settingsY', 'Não, habilitar configurações'),
        ('settingsN', 'Sim, DESABILITAR configurações')
    ], initial='settingsY')  # Controle de configurações
    
    # Campos para servidor personalizado
    serverIP = forms.CharField(label="Host", required=False)  # Endereço do servidor
    apiServer = forms.CharField(label="Servidor API", required=False)  # Servidor API
    key = forms.CharField(label="Chave", required=False)  # Chave pública
    urlLink = forms.CharField(label="Link personalizado para links", required=False)  # Link personalizado
    downloadLink = forms.CharField(label="Link personalizado para download de novas versões", required=False)  # Link de download
    compname = forms.CharField(label="Nome da empresa",required=False)  # Nome da empresa
    
    # Campos para personalização visual
    iconfile = forms.FileField(label="Ícone personalizado do app (formato .png)", required=False, widget=forms.FileInput(attrs={'accept': 'image/png'}))  # Upload de ícone
    logofile = forms.FileField(label="Logo personalizado do app (formato .png)", required=False, widget=forms.FileInput(attrs={'accept': 'image/png'}))  # Upload de logo
    iconbase64 = forms.CharField(required=False)  # Ícone em base64 (alternativo)
    logobase64 = forms.CharField(required=False)  # Logo em base64 (alternativo)
    theme = forms.ChoiceField(choices=[
        ('light', 'Claro'),
        ('dark', 'Escuro'),
        ('system', 'Seguir sistema')
    ], initial='system')  # Tema do aplicativo
    themeDorO = forms.ChoiceField(choices=[('default', 'Padrão'),('override', 'Substituir')], initial='default')  # Default ou Override para tema
    
    # Campos para configurações de segurança
    passApproveMode = forms.ChoiceField(choices=[('password','Aceitar sessões via senha'),('click','Aceitar sessões via clique'),('password-click','Aceitar sessões via ambos')],initial='password-click')  # Modo de aprovação
    permanentPassword = forms.CharField(widget=forms.PasswordInput(), required=False)  # Senha permanente
    runasadmin = forms.ChoiceField(choices=[('false','Não'),('true','Sim')], initial='false')  # Executar como admin
    denyLan = forms.BooleanField(initial=False, required=False)  # Negar LAN
    enableDirectIP = forms.BooleanField(initial=False, required=False)  # Habilitar IP direto
    autoClose = forms.BooleanField(initial=False, required=False)  # Fechar automaticamente
    
    # Campos para permissões
    permissionsDorO = forms.ChoiceField(choices=[('default', 'Padrão'),('override', 'Substituir')], initial='default')  # Default ou Override para permissões
    permissionsType = forms.ChoiceField(choices=[('custom', 'Personalizado'),('full', 'Acesso completo'),('view','Compartilhamento de tela')], initial='custom')  # Tipo de permissões
    enableKeyboard =  forms.BooleanField(initial=True, required=False)  # Habilitar teclado
    enableClipboard = forms.BooleanField(initial=True, required=False)  # Habilitar clipboard
    enableFileTransfer = forms.BooleanField(initial=True, required=False)  # Habilitar transferência de arquivos
    enableAudio = forms.BooleanField(initial=True, required=False)  # Habilitar áudio
    enableTCP = forms.BooleanField(initial=True, required=False)  # Habilitar TCP
    enableRemoteRestart = forms.BooleanField(initial=True, required=False)  # Habilitar reinício remoto
    enableRecording = forms.BooleanField(initial=True, required=False)  # Habilitar gravação
    enableBlockingInput = forms.BooleanField(initial=True, required=False)  # Habilitar bloqueio de entrada
    enableRemoteModi = forms.BooleanField(initial=False, required=False)  # Habilitar modificação remota
    
    # Campos adicionais
    removeWallpaper = forms.BooleanField(initial=True, required=False)  # Remover wallpaper
    
    # Campos para configurações manuais avançadas
    defaultManual = forms.CharField(widget=forms.Textarea, required=False)  # Configurações padrão manuais
    overrideManual = forms.CharField(widget=forms.Textarea, required=False)  # Configurações override manuais
    
    # Campos para recursos customizados adicionais
    cycleMonitor = forms.BooleanField(initial=False, required=False)  # Monitor de ciclo (duplicado? verificar)
    xOffline = forms.BooleanField(initial=False, required=False)  # Offline (duplicado? verificar)
    hidecm = forms.BooleanField(initial=False, required=False)  # Ocultar CM (duplicado? verificar)
    removeNewVersionNotif = forms.BooleanField(initial=False, required=False)  # Remover notificação (duplicado? verificar)
    
    def clean_iconfile(self):
        # Método de validação personalizado para o campo iconfile
        # Executado automaticamente quando o formulário é validado
        # Permite verificações adicionais além das validações padrão do Django
        print("checando ícone")  # Log para debug (pode ser removido em produção)

        # Obter o valor limpo do campo iconfile
        image = self.cleaned_data['iconfile']

        # Só validar se uma imagem foi fornecida
        if image:
            try:
                # Abrir imagem usando Pillow (biblioteca Python para processamento de imagens)
                # Pillow suporta diversos formatos: PNG, JPEG, GIF, etc.
                img = Image.open(image)

                # Verificar se é PNG (opcional, mas boa prática para ícones)
                # PNG é recomendado por suportar transparência e ser lossless
                if img.format != 'PNG':
                    raise forms.ValidationError("Apenas imagens PNG são permitidas.")

                # Obter dimensões da imagem (largura, altura)
                # img.size retorna uma tupla (width, height)
                width, height = img.size

                # Verificar dimensões quadradas (largura == altura)
                # Ícones geralmente precisam ser quadrados para boa aparência
                if width != height:
                    raise forms.ValidationError("As dimensões do ícone personalizado do app devem ser quadradas.")

                # Se todas as validações passaram, retornar a imagem
                # Isso permite que o campo seja salvo normalmente
                return image

            # Capturar erros específicos de imagem inválida
            # OSError é levantado quando o arquivo não é uma imagem válida
            except OSError:
                raise forms.ValidationError("Arquivo de ícone inválido. Envie uma imagem PNG válida.")

            # Capturar outros erros de processamento de imagem
            # Pode incluir problemas de memória, formatos não suportados, etc.
            except Exception as e:
                raise forms.ValidationError(f"Erro ao processar ícone: {e}")
