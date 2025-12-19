# Dockerfile para RDGen - Aplicação Django de geração de clientes RustDesk
# Usa imagem base Alpine Linux com Python 3.13 por ser leve e segura
FROM python:3.13-alpine

# Criar usuário não-root para maior segurança (princípio do menor privilégio)
# -D cria usuário sem senha, adequado para containers
RUN adduser -D user
USER user

# Definir diretório de trabalho para a aplicação
WORKDIR /opt/rdgen

# Copiar arquivos do projeto para o container
COPY . .
# Instalar dependências Python e executar migrações do banco de dados
# --no-cache-dir evita armazenar cache do pip, reduzindo tamanho da imagem
# Migrações garantem que o banco esteja atualizado na criação do container
RUN pip install --no-cache-dir -r requirements.txt \
 && python manage.py migrate

# Configurar Python para output não-buferizado (importante para logs em containers)
ENV PYTHONUNBUFFERED=1

# Expor porta 8000 para acesso à aplicação web
EXPOSE 8000

# Healthcheck para verificar se a aplicação está respondendo
# Executa a cada 30s, timeout de 5s, 3 tentativas
# Usa wget --spider para verificar conectividade sem baixar conteúdo
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD wget --spider 0.0.0.0:8000

# Comando para iniciar a aplicação com Gunicorn
# Usa configuração do arquivo gunicorn.conf.py
# Executa aplicação WSGI definida em rdgen.wsgi:application
CMD ["/home/user/.local/bin/gunicorn", "-c", "gunicorn.conf.py", "rdgen.wsgi:application"]
