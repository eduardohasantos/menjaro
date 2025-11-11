import time
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
from app1 import models

#====COMMAND====
#py manage.py test app1.tests.LoginFormTest.test_favoritos

class LoginFormTest(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        # Configurar opções do Chrome
        chrome_options = Options()
        
        # Configurações para CI/CD
        if os.environ.get('CI') or os.environ.get('GITHUB_ACTIONS'):
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
        
        # Criar um usuário de teste
        cls.test_user = User.objects.create_user(
            username='teste', 
            password='123'
        )
        
        # Criar categorias
        cls.categoria1 = models.Categoria.objects.create(nome="Futebas")
        cls.categoria2 = models.Categoria.objects.create(nome="Casamento")
        
        # Criar notícias
        cls.noticia1 = models.Noticia.objects.create(
            titulo="sou lindo", 
            conteudo="tenho fome", 
            categoria=cls.categoria1
        )
        
        cls.noticia2 = models.Noticia.objects.create(
            titulo="sou feio", 
            conteudo="estou satisfeito", 
            categoria=cls.categoria2
        )
        
        # Se 'favoritos' for ManyToMany, adicione depois da criação:
        # cls.noticia1.favoritos.add(cls.test_user)
        # cls.noticia2.favoritos.add(cls.test_user)
    
    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_notify_success(self):
        login_url = self.live_server_url
        self.browser.get(login_url)
        wait = WebDriverWait(self.browser, self.wait_time)

        botao_notificacao = wait.until(
            EC.element_to_be_clickable((By.ID, 'btn-bell'))
        )
        botao_notificacao.click()

        email_assinatura = wait.until(
            EC.presence_of_element_located((By.ID, 'id_email'))
        )
        email_assinatura.send_keys("Teste@gmail.com")

        botao_assinar = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'btn-primary'))
        )
        botao_assinar.click()

    def test_notify_unsucess(self):
        login_url = self.live_server_url
        self.browser.get(login_url)

        wait = WebDriverWait(self.browser, self.wait_time)
        botao_notificacao = wait.until(
            EC.element_to_be_clickable((By.ID, 'btn-bell'))
        )
        botao_notificacao.click()

        email_assinatura = wait.until(
            EC.presence_of_element_located((By.ID, 'id_email'))
        )
        botao_assinar = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'btn-primary'))
        )
        
        # Teste 1: E-mail vazio
        email_assinatura.send_keys("")
        botao_assinar.click()
        
        # Teste 2: Email já usado
        email_assinatura.clear() 
        email_assinatura.send_keys("Teste@gmail.com")
        botao_assinar.click()
    
    def test_entrar_categoria(self):
        login_url = self.live_server_url
        self.browser.get(login_url)
        wait = WebDriverWait(self.browser, self.wait_time)
        
        botao_categoria = wait.until(
            EC.element_to_be_clickable((By.ID, 'btn-cat'))
        )
        botao_categoria.click()
        
        botao_todas_categorias = wait.until(
            EC.element_to_be_clickable((By.ID, 'categoria-1'))
        )
        botao_todas_categorias.click()

    def test_entrar_noticia(self):
        login_url = self.live_server_url + '/categorias/'
        self.browser.get(login_url)
        wait = WebDriverWait(self.browser, self.wait_time)
        
        botao_noticia = wait.until(
            EC.element_to_be_clickable((By.ID, 'futebas'))
        )
        botao_noticia.click()
        
        botao_noticia_principal = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'ler__mais'))
        )
        botao_noticia_principal.click()
    
    def test_aumentar_fonte(self):
        login_url = self.live_server_url + '/noticia/1/'
        self.browser.get(login_url)
        wait = WebDriverWait(self.browser, self.wait_time)
        
        botao_aumentar_fonte = wait.until(
            EC.element_to_be_clickable((By.ID, 'aumentar-fonte'))
        )
        botao_aumentar_fonte.click()
        botao_aumentar_fonte.click()
        botao_aumentar_fonte.click()

    def test_diminuir_fonte(self):
        login_url = self.live_server_url + '/noticia/1/'
        self.browser.get(login_url)
        wait = WebDriverWait(self.browser, self.wait_time)
        
        botao_diminuir_fonte = wait.until(
            EC.element_to_be_clickable((By.ID, 'diminuir-fonte'))
        )
        botao_diminuir_fonte.click()
        botao_diminuir_fonte.click()
        botao_diminuir_fonte.click()
    
    def test_favoritos(self):
        url = self.live_server_url
        self.browser.get(url)
        wait = WebDriverWait(self.browser, self.wait_time)
        
        #======CENARIO DESFAVORAVEL=====
        botaoFav = self.browser.find_element("xpath", "/html/body/header/div[1]/div/nav/a[3]")
        botaoFav.click()
        
        time.sleep(3)
        
        self.browser.back()
        #====CENARIO FAVORAVEL====
        botaoEstrela = self.browser.find_element("xpath", "//*[@id='noticia-2']/div[2]/form/button")
        
        time.sleep(3)
        
        botaoEstrela.click()
        
        botaoFav = self.browser.find_element("xpath", "/html/body/header/div[1]/div/nav/a[3]")
        botaoFav.click()
        
        time.sleep(3)
        
        # Adicione aqui as ações do teste de favoritos
        # Exemplo:
        # botao_favorito = wait.until(
        #     EC.element_to_be_clickable((By.ID, 'btn-favorito'))
        # )
        # botao_favorito.click()
        
        # Verificação (assertion)
        # self.assertIn("Favoritado", self.browser.page_source)
        
    # ======================
    # PESQUISA
    # ======================
    def test_pesquisa_com_resultados(self):
        """Cenário 1: Pesquisa com resultados"""
        print("\n🔍 Teste: pesquisa com resultados")
        driver = self.browser
        driver.get(f"{self.live_server_url}/")

        driver.find_element(By.ID, "btn-search").click()
        campo_busca = driver.find_element(By.NAME, "q")
        campo_busca.send_keys("economia" + Keys.RETURN)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "noticia"))
        )

        artigos = driver.find_elements(By.CLASS_NAME, "noticia")
        print(f"📰 Foram encontradas {len(artigos)} notícias.")
        assert len(artigos) > 0

    def test_pesquisa_sem_resultados(self):
        """Cenário 2: Pesquisa sem resultados"""
        print("\n🔍 Teste: pesquisa sem resultados")
        driver = self.browser
        driver.get(f"{self.live_server_url}/")

        driver.find_element(By.ID, "btn-search").click()
        campo_busca = driver.find_element(By.NAME, "q")
        campo_busca.send_keys("noticiaquenaoexiste" + Keys.RETURN)

        mensagem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "mensagem-sem-resultados"))
        )
        print("📭 Mensagem exibida:", mensagem.text)
        assert "nenhum resultado" in mensagem.text.lower()