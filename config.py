"""
Configurações do Selenium para Web Scraping
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class SeleniumConfig:
    """
    Classe para configurar o driver do Selenium com Chrome
    """
    
    def __init__(self, headless=False, disable_images=False):
        """
        Inicializa a configuração do Selenium
        
        Args:
            headless (bool): Se True, executa sem abrir janela do navegador
            disable_images (bool): Se True, desabilita carregamento de imagens (mais rápido)
        """
        self.headless = headless
        self.disable_images = disable_images
    
    def get_chrome_options(self):
        """
        Retorna as opções configuradas para o Chrome
        
        Returns:
            Options: Objeto de opções do Chrome configurado
        """
        chrome_options = Options()
        
        # Modo headless (sem interface gráfica)
        if self.headless:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
        
        # Opções para otimizar performance e evitar detecção
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        
        # Desabilitar notificações e popups
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-popup-blocking')
        
        # User agent personalizado (simula navegador real)
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/120.0.0.0 Safari/537.36'
        )
        
        # Desabilitar imagens para carregar mais rápido (opcional)
        if self.disable_images:
            prefs = {
                'profile.managed_default_content_settings.images': 2,
                'profile.default_content_setting_values.notifications': 2,
            }
            chrome_options.add_experimental_option('prefs', prefs)
        
        # Remover flag de automação (evita detecção de bots)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Maximizar janela ao abrir
        chrome_options.add_argument('--start-maximized')
        
        return chrome_options
    
    def create_driver(self):
        """
        Cria e retorna uma instância do WebDriver configurado
        
        Returns:
            webdriver.Chrome: Driver do Chrome configurado
        """
        # Obter opções configuradas
        options = self.get_chrome_options()
        
        # Configurar o serviço do ChromeDriver com webdriver-manager
        # Isso baixa automaticamente a versão correta do ChromeDriver
        service = Service(ChromeDriverManager().install())
        
        # Criar driver
        driver = webdriver.Chrome(service=service, options=options)
        
        # Configurar timeouts
        driver.implicitly_wait(10)  # Espera implícita de 10 segundos
        driver.set_page_load_timeout(30)  # Timeout de carregamento de página
        
        # Executar script para esconder indicadores de automação
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver


# Função auxiliar para criar driver rapidamente
def get_driver(headless=False, disable_images=False):
    """
    Função auxiliar para criar um driver configurado rapidamente
    
    Args:
        headless (bool): Se True, executa sem abrir janela do navegador
        disable_images (bool): Se True, desabilita carregamento de imagens
    
    Returns:
        webdriver.Chrome: Driver do Chrome configurado
    """
    config = SeleniumConfig(headless=headless, disable_images=disable_images)
    return config.create_driver()


