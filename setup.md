## Hospedar o servidor rdgen com docker

1. Primeiro, você precisará fazer um fork deste repositório no GitHub
2. Em seguida, configure um token de acesso refinado do GitHub com permissões para seu repositório rdgen:
    * Faça login na sua conta do GitHub
    * Clique na sua foto de perfil no canto superior direito, clique em Settings
    * Na parte inferior do painel esquerdo, clique em Developer Settings
    * Clique em Personal access tokens
    * Clique em Fine-grained tokens
    * Clique em Generate new token
    * Dê um nome ao token, altere a expiração para o que quiser
    * Em Repository access, selecione Only select repositories, então escolha seu repositório rdgen
    * Dê acesso de Read e Write a actions e workflows
    * Você pode precisar ir para: https://github.com/USERNAME/rdgen/actions e clicar no botão verde Enable Actions para que funcione.
3. Agora, faça login na sua conta do GitHub, vá para a página do seu repositório rdgen (https://github.com/USERNAME/rdgen)
   * Clique em Settings
   * No painel esquerdo, clique em Secrets and variables, então clique em Actions
   * Agora clique em New repository secret
   * Defina o Name como GENURL
   * Defina o Secret como https://rdgen.hostname.com (ou qualquer que seja o servidor acessado)
4. Agora baixe o arquivo docker-compose.yml e preencha as variáveis de ambiente:
  * SECRET_KEY="sua chave secreta" - gere uma chave secreta executando: ```python3 -c 'import secrets; print(secrets.token_hex(100))'```
  * GHUSER="seu nome de usuário do github"
  * GHBEARER="seu token de acesso refinado"
  * PROTOCOL="https" *opcional - padrão é "https", mude para "http" se necessário
  * REPONAME="rdgen" *opcional - padrão é "rdgen", mude se renomeou o repositório ao fazer fork
5. Agora apenas execute ```docker compose up -d```


## Hospedar manualmente:

1. Uma conta do GitHub com um fork deste repositório
2. Um token de acesso refinado do GitHub com permissões para seu repositório rdgen:
    * Faça login na sua conta do GitHub
    * Clique na sua foto de perfil no canto superior direito, clique em Settings
    * Na parte inferior do painel esquerdo, clique em Developer Settings
    * Clique em Personal access tokens
    * Clique em Fine-grained tokens
    * Clique em Generate new token
    * Dê um nome ao token, altere a expiração para o que quiser
    * Em Repository access, selecione Only select repositories, então escolha seu repositório rdgen
    * Dê acesso de Read e Write a actions e workflows
    * Você pode precisar ir para: https://github.com/USERNAME/rdgen/actions e clicar no botão verde Enable Actions para que funcione.
3. Configure variáveis de ambiente/secrets:
    * Variáveis de ambiente no servidor executando rdgen:
        * GHUSER="seu nome de usuário do github"
        * GHBEARER="seu token de acesso refinado"
        * PROTOCOL="https" *opcional - padrão é "https", mude para "http" se necessário
        * REPONAME="rdgen" *opcional - padrão é "rdgen", mude se renomeou o repositório ao fazer fork
    * Secrets do GitHub (configure na sua conta do GitHub para seu repositório rdgen):
        * GENURL="example.com:8000"  *este é o domínio e porta que você está executando rdgen, precisa ser acessível na internet, dependendo de como você configurou, a porta pode não ser necessária

```
# Abra o diretório onde deseja instalar rdgen (mude /opt para onde quiser)
cd /opt

# Clone seu repositório rdgen, mude bryangerlach para seu nome de usuário do github
git clone https://github.com/bryangerlach/rdgen.git

# Abra o diretório rdgen
cd rdgen

# Configure um ambiente virtual python chamado rdgen
python -m venv .venv

# Ative o ambiente virtual python
source .venv/bin/activate

# Instale as dependências python
pip install -r requirements.txt

# Configure o banco de dados
python manage.py migrate

# Execute o servidor, mude 8000 para o que quiser
python manage.py runserver 0.0.0.0:8000
```

abra seu navegador web para yourdomain:8000

use nginx, caddy, traefik, etc. para proxy reverso ssl

### Para iniciar automaticamente o servidor na inicialização, você pode configurar um serviço systemd chamado rdgen.service

substitua user, group e port se necessário  substitua /opt por onde você instalou rdgen  salve o seguinte arquivo como /etc/systemd/system/rdgen.service, e certifique-se de alterar GHUSER, GHBEARER

```
[Unit]
Description=Gerador de Cliente Rustdesk
[Service]
Type=simple
LimitNOFILE=1000000
Environment="GHUSER=seuusuariogithub"
Environment="GHBEARER=seutoken"
PassEnvironment=GHUSER GHBEARER
ExecStart=/opt/rdgen/.venv/bin/python3 /opt/rdgen/manage.py runserver 0.0.0.0:8000
WorkingDirectory=/opt/rdgen/
User=root
Group=root
Restart=always
StandardOutput=file:/var/log/rdgen.log
StandardError=file:/var/log/rdgen.error
# Reiniciar serviço após 10 segundos se o serviço node travar
RestartSec=10
[Install]
WantedBy=multi-user.target
```

então execute isso para habilitar a inicialização automática do serviço na inicialização, e então inicie manualmente desta vez:

```
sudo systemctl enable rdgen.service
sudo systemctl start rdgen.service
```
e para obter o status do servidor, execute:
```
sudo systemctl status rdgen.service
```
