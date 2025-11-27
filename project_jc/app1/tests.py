import time
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from django.contrib.auth import get_user_model
import os
from app1 import models

#====COMMAND====
#py manage.py test app1.tests.AutomatedTests.test_favoritos

User = get_user_model()

class AutomatedTests(StaticLiveServerTestCase):
    
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
        
        cls.browser = webdriver.Chrome(options=chrome_options)
        cls.browser.implicitly_wait(10)
        cls.wait_time = 30  # Para os WebDriverWait
        cls.isE2E = False
        
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
        
        cls.usuario1 = models.User.objects.create(
            email="macacoprego@gmail.com",
            username="souLindo123",
            password="123"
        )
        
        # Se 'favoritos' for ManyToMany, adicione depois da criação:
        # cls.noticia1.favoritos.add(cls.test_user)
        # cls.noticia2.favoritos.add(cls.test_user)
    
    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def running_page(self, page=""):
        self.browser.get(f"{self.live_server_url}/{page}/")
    
    def get_submit_button(self):
        return self.browser.find_elements(By.XPATH, "//button[@type='submit']")
    
    def acoesPausadas(self, tempo=2):
        time.sleep(tempo)
        return self.browser
    
    
    def test_login(self, username="jonesManoel", password="jamesBond"):
        self.running_page("accounts/login")
        username_input = self.browser.find_element(By.NAME, "username")
        username_input.send_keys(username)
        password_input = self.browser.find_element(By.NAME, "password")
        password_input.send_keys(password)
        self.browser.find_element(By.XPATH, '/html/body/section/div/form/button').click()
        # time.sleep(5) # Uso do WebDriverWait é preferível para estabilidade

    def test_register(self):
        email = "jones@gmail.com"
        username = "jonesManoel"
        password = "jamesBond"
        
        self.running_page("accounts/register")
        self.browser.find_element(By.NAME, "username").send_keys(username)
        self.browser.find_element(By.NAME, "email").send_keys(email)
        self.browser.find_element(By.NAME, "password1").send_keys(password)
        self.browser.find_element(By.NAME, "password2").send_keys(password)
        
        self.browser.find_elements(By.XPATH, '//button[@type="submit"]')[1].click()
        
        # O registro deve levar ao login, então forçamos o login em seguida
        #self.test_login(username, password)
   
    def test_notify_success(self):
        if not self.isE2E:
            self.test_register()
        
        login_url = self.live_server_url
        self.browser.get(login_url)
        wait = WebDriverWait(self.browser, self.wait_time)

        botao_notificacao = wait.until(
            EC.element_to_be_clickable((By.ID, 'btn-bell'))
        )
        botao_notificacao.click()

        time.sleep(1)

        email_assinatura = wait.until(
            EC.presence_of_element_located((By.ID, 'id_email'))
        )
        email_assinatura.send_keys("Teste@gmail.com")

        botao_assinar = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'btn-primary'))
        )
        botao_assinar.click()

        time.sleep(1)

    def test_notify_unsucess(self):
        if not self.isE2E:
            self.test_register()
        
        login_url = self.live_server_url
        self.browser.get(login_url)

        wait = WebDriverWait(self.browser, self.wait_time)
        botao_notificacao = wait.until(
            EC.element_to_be_clickable((By.ID, 'btn-bell'))
        )
        botao_notificacao.click()

        time.sleep(2)

        email_assinatura = wait.until(
            EC.presence_of_element_located((By.ID, 'id_email'))
        )
        botao_assinar = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'btn-primary'))
        )
        
        # Teste 1: E-mail vazio
        email_assinatura.send_keys("")
        botao_assinar.click()
        
        time.sleep(2)
        # Teste 2: Email já usado
        email_assinatura.clear() 
        email_assinatura.send_keys("Teste@gmail.com")
        botao_assinar.click()
        
        time.sleep(2)
    
    def test_entrar_categoria(self):
        if not self.isE2E:
            self.test_register()
        
        login_url = self.live_server_url
        self.browser.get(login_url)
        wait = WebDriverWait(self.browser, self.wait_time)
        
        botao_categoria = wait.until(
            EC.element_to_be_clickable((By.ID, 'btn-cat'))
        )
        botao_categoria.click()
        
        botao_todas_categorias = wait.until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/main/div/ul/li[2]/a'))
        )
        botao_todas_categorias.click()

    def test_entrar_noticia(self):
        if not self.isE2E:
            self.test_register()
        
        login_url = self.live_server_url + '/categorias/1'
        self.browser.get(login_url)
        wait = WebDriverWait(self.browser, self.wait_time)
        
        botao_noticia = wait.until(
            EC.element_to_be_clickable((By.ID, 'noticia_1'))
        )
        botao_noticia.click()
        
        botao_noticia_principal = wait.until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/main/section/article/div[1]/a'))
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
        time.sleep(2)

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
        time.sleep(2)
    
    def test_favoritos(self):
       
        #======CENARIO DESFAVORAVEL=====
        self.running_page("meus-favoritos")
        time.sleep(2)
        self.running_page()
        
        if not self.isE2E: 
           self.test_register()
        wait = WebDriverWait(self.browser, self.wait_time)
    
        #====CENARIO FAVORAVEL====
        botaoEstrela = self.browser.find_element("xpath", "//*[@id='noticia-2']/div[2]/form/button")
        botaoEstrela.click()
        
        time.sleep(3)
        
        botaoFav = self.acoesPausadas(3).find_element(By.ID, "btn-mf")
        botaoFav.click()
        
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
        
        if not self.isE2E:
            self.test_register() 
        
        """Cenário 1: Pesquisa com resultados"""
        print("\n🔍 Teste: pesquisa com resultados")
        driver = self.browser
        driver.get(f"{self.live_server_url}/")

        driver.find_element(By.ID, "search-toggle").click()
        campo_busca = driver.find_element(By.NAME, "q")
        campo_busca.send_keys("sou lindo" + Keys.RETURN)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "noticia"))
        )

        artigos = driver.find_elements(By.CLASS_NAME, "noticia")
        time.sleep(3)
        print(f"\n📰 Foram encontradas {len(artigos)} notícias.\n")
        assert len(artigos) > 0

    def test_pesquisa_sem_resultados(self):
        
        if not self.isE2E:
            self.test_register()
        
        """Cenário 2: Pesquisa sem resultados"""
        print("\n🔍 Teste: pesquisa sem resultados")
        driver = self.browser
        driver.get(f"{self.live_server_url}/")

        driver.find_element(By.ID, "search-toggle").click()
        campo_busca = driver.find_element(By.NAME, "q")
        campo_busca.send_keys("noticiaquenaoexiste" + Keys.RETURN)
        
    def test_comentar(self):
        
        if not self.isE2E:
            self.test_register()
        
        self.browser.find_element(By.XPATH, "//*[@id='noticia-1']/div[1]/a").click()
        
        self.browser.find_element(By.NAME, "texto").send_keys("jones manoel")
        self.acoesPausadas(2).find_element(By.XPATH, "/html/body/main/div[1]/section/div[2]/form/button")