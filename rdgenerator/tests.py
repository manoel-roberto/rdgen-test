# tests.py - Arquivo de testes para o app rdgenerator
# Este arquivo contém os testes automatizados para validar o funcionamento do app
# Testes garantem que mudanças no código não quebrem funcionalidades existentes
# Para mais informações: https://docs.djangoproject.com/pt-br/5.0/topics/testing/

# Importação da classe base TestCase do Django
# Fornece métodos para configurar, executar e verificar testes
from django.test import TestCase

# ESTRUTURA RECOMENDADA PARA TESTES NO RDGENERATOR:
#
# 1. Testes de Modelos:
#    - Verificar criação de GithubRun
#    - Validar campos obrigatórios
#    - Testar métodos do modelo
#
# 2. Testes de Forms:
#    - Validação do GenerateForm
#    - Testar campos obrigatórios
#    - Verificar validação de ícones
#
# 3. Testes de Views:
#    - Testar geração de cliente (mock do GitHub API)
#    - Verificar polling de status
#    - Testar downloads de arquivo
#
# 4. Testes de Integração:
#    - Fluxo completo: form → workflow → download

# EXEMPLO DE TESTE PARA MODELO GITHUBRUN:
#
# from .models import GithubRun
# import uuid
#
# class GithubRunTestCase(TestCase):
#     def setUp(self):
#         # Configuração inicial para cada teste
#         # Executado antes de cada método de teste
#         # Cria dados necessários para os testes
#         self.test_uuid = str(uuid.uuid4())
#
#     def test_create_github_run(self):
#         # Teste de criação de execução
#         # Verifica se conseguimos criar um registro GithubRun
#         run = GithubRun.objects.create(
#             uuid=self.test_uuid,
#             status="Starting..."
#         )
#         # Verificações (assertions)
#         self.assertEqual(run.uuid, self.test_uuid)
#         self.assertEqual(run.status, "Starting...")
#
#     def test_github_run_str_method(self):
#         # Teste do método __str__ (se implementado)
#         run = GithubRun.objects.create(uuid=self.test_uuid, status="Success")
#         expected_str = f"Execução {self.test_uuid} - Status: Success"
#         self.assertEqual(str(run), expected_str)

# EXEMPLO DE TESTE PARA FORM:
#
# from .forms import GenerateForm
# from django.core.files.uploadedfile import SimpleUploadedFile
# import io
#
# class GenerateFormTestCase(TestCase):
#     def test_valid_form(self):
#         # Teste de formulário válido
#         # Testa se formulário aceita dados corretos
#         form_data = {
#             'platform': 'windows',
#             'version': '1.4.2',
#             'exename': 'test.exe'
#         }
#         form = GenerateForm(data=form_data)
#         self.assertTrue(form.is_valid())
#
#     def test_required_fields(self):
#         # Teste de campos obrigatórios
#         # Verifica se campos obrigatórios são validados
#         form = GenerateForm(data={})  # Form vazio
#         self.assertFalse(form.is_valid())
#         self.assertIn('platform', form.errors)
#         self.assertIn('exename', form.errors)
#
#     def test_icon_validation(self):
#         # Teste de validação de ícone
#         # Cria arquivo PNG falso para teste
#         png_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
#         icon_file = SimpleUploadedFile("test.png", png_content, content_type="image/png")
#
#         form_data = {'platform': 'windows', 'exename': 'test.exe'}
#         file_data = {'iconfile': icon_file}
#         form = GenerateForm(data=form_data, files=file_data)
#
#         # Se a validação passar, o ícone é aceito
#         if form.is_valid():
#             self.assertEqual(form.cleaned_data['iconfile'], icon_file)
#
#     def test_invalid_icon_format(self):
#         # Teste de formato de ícone inválido
#         # Tenta enviar arquivo não-PNG
#         jpg_content = b'\xff\xd8\xff\xe0\x00\x10JFIF'
#         icon_file = SimpleUploadedFile("test.jpg", jpg_content, content_type="image/jpeg")
#
#         form_data = {'platform': 'windows', 'exename': 'test.exe'}
#         file_data = {'iconfile': icon_file}
#         form = GenerateForm(data=form_data, files=file_data)
#
#         self.assertFalse(form.is_valid())
#         self.assertIn('iconfile', form.errors)

# EXEMPLO DE TESTE PARA VIEWS:
#
# from django.test import Client
# from django.urls import reverse
# from unittest.mock import patch, MagicMock
# import json
#
# class ViewsTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()  # Cliente de teste para simular requests HTTP
#
#     @patch('rdgenerator.views.requests.post')  # Mock da chamada para GitHub API
#     def test_generate_client_success(self, mock_post):
#         # Teste da view de geração de cliente
#         # Simula resposta bem-sucedida da API do GitHub
#         mock_response = MagicMock()
#         mock_response.status_code = 201
#         mock_response.json.return_value = {'html_url': 'https://github.com/...'}
#         mock_post.return_value = mock_response
#
#         # Dados do formulário
#         form_data = {
#             'platform': 'windows',
#             'version': '1.4.2',
#             'exename': 'test.exe'
#         }
#
#         # Fazer POST para a view
#         response = self.client.post(reverse('generate'), form_data)
#
#         # Verificações
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'success')  # Verificar conteúdo da resposta
#
#     def test_check_status_view(self):
#         # Teste da view de verificação de status
#         # Criar registro no banco para teste
#         GithubRun.objects.create(uuid='test-uuid', status='Building...')
#
#         response = self.client.get(reverse('check_status', args=['test-uuid']))
#         self.assertEqual(response.status_code, 200)
#
#         data = json.loads(response.content)
#         self.assertEqual(data['status'], 'Building...')

# DICAS PARA TESTES NO RDGENERATOR:
# - Use mock para simular chamadas da API do GitHub (evita chamadas reais)
# - Teste uploads de arquivo com arquivos temporários (SimpleUploadedFile)
# - Verifique limpeza de arquivos após testes (usando tearDown)
# - Use fixtures para dados de teste se necessário (fixtures/ ou factories)
# - Execute testes com: python manage.py test rdgenerator
# - Para testes com arquivos: use TemporaryDirectory para arquivos temporários
# - Para testes de API: use responses ou requests-mock
# - Cobertura de testes: use coverage.py para medir cobertura

# Execute os testes quando fizer mudanças no código!
