from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 'time' não é mais necessário, pois não usaremos time.sleep()

class LoginFormTest(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Edge()
        cls.wait_time = 10 
    
        # Criar um usuário de teste
        cls.test_user = User.objects.create_user(
            username='teste', 
            password='123'
        )

    @classmethod
    def tearDownClass(cls):
        """
        Limpeza que roda UMA VEZ após os testes.
        """
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
            EC.element_to_be_clickable((By.ID, 'id_email'))
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

        # --- Teste 1 E-mail vazio
        
        email_assinatura = wait.until(
            EC.element_to_be_clickable((By.ID, 'id_email'))
        )
        botao_assinar = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'btn-primary'))
        )
        
        #----- Teste 2 email ja usado
        email_assinatura.send_keys("") # Envia string vazia para teste
        botao_assinar.click()
        
        email_assinatura.clear() 
        email_assinatura.send_keys("Teste@gmail.com") #email ja cadastrado
        
        botao_assinar.click()
    