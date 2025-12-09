"""
Configurações do Chrome para Selenium
======================================

Configuração otimizada do Chrome com suporte a:
- Perfis persistentes
- Proxies
- Modo headless/visual
- Anti-detecção
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from typing import Optional, Dict
import os
import ssl
import re


class ChromeConfig:
    """
    Configurador do Chrome para Selenium
    """
    
    def __init__(
        self,
        headless: bool = False,
        profile_path: Optional[str] = None,
        proxy: Optional[Dict[str, str]] = None,
        disable_images: bool = False,
        window_size: tuple = (1920, 1080)
    ):
        """
        Inicializa a configuração do Chrome
        
        Args:
            headless: Se True, executa sem interface gráfica
            profile_path: Caminho para perfil do Chrome (sessão persistente)
            proxy: Dict com configuração de proxy
            disable_images: Se True, desabilita carregamento de imagens
            window_size: Tamanho da janela (largura, altura)
        """
        self.headless = headless
        self.profile_path = profile_path
        self.proxy = proxy
        self.disable_images = disable_images
        self.window_size = window_size
    
    def get_chrome_options(self) -> Options:
        """
        Cria e retorna opções configuradas para o Chrome
        
        Returns:
            Options: Objeto de opções do Chrome
        """
        options = Options()
        
        # ====== PERFIL PERSISTENTE ======
        if self.profile_path:
            options.add_argument(f'--user-data-dir={self.profile_path}')
            print(f"📁 Usando perfil: {self.profile_path}")
        
        # ====== PROXY ======
        if self.proxy:
            proxy_str = self.proxy.get('http', '')
            if proxy_str:
                # Extrair apenas host:port para --proxy-server
                if '://' in proxy_str:
                    # Formato: http://user:pass@host:port
                    protocol = proxy_str.split('://')[0]
                    rest = proxy_str.split('://')[1]
                    
                    if '@' in rest:
                        # Tem autenticação - NÃO configurar aqui
                        # Será tratado pela extensão no create_driver
                        print(f"🔐 Proxy com autenticação será configurado via extensão")
                    else:
                        # Sem autenticação
                        options.add_argument(f'--proxy-server={proxy_str}')
                        print(f"🔄 Proxy configurado")
                else:
                    # Formato simples: host:port
                    options.add_argument(f'--proxy-server={proxy_str}')
                    print(f"🔄 Proxy configurado")
        
        # ====== MODO HEADLESS ======
        if self.headless:
            options.add_argument('--headless=new')  # Novo modo headless
            options.add_argument('--disable-gpu')
            print("👻 Modo headless ativado")
        
        # ====== ANTI-DETECÇÃO ======
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        # ====== USER AGENT ======
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/120.0.0.0 Safari/537.36'
        )
        
        # ====== OTIMIZAÇÕES ======
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        
        # Tamanho da janela
        if not self.headless:
            options.add_argument(f'--window-size={self.window_size[0]},{self.window_size[1]}')
        
        # ====== PREFERÊNCIAS ======
        prefs = {}
        
        # Desabilitar imagens (opcional)
        if self.disable_images:
            prefs['profile.managed_default_content_settings.images'] = 2
            print("🖼️ Imagens desabilitadas")
        
        # Desabilitar notificações
        prefs['profile.default_content_setting_values.notifications'] = 2
        
        # Desabilitar geolocalização
        prefs['profile.default_content_setting_values.geolocation'] = 2
        
        # Aplicar preferências
        if prefs:
            options.add_experimental_option('prefs', prefs)
        
        return options
    
    def create_driver(self) -> webdriver.Chrome:
        """
        Cria e retorna um driver do Chrome configurado
        
        Returns:
            webdriver.Chrome: Driver configurado
        """
        print("🚀 Inicializando Chrome...")
        
        # Verificar se proxy tem autenticação
        if self.proxy:
            proxy_str = self.proxy.get('http', '')
            if '@' in proxy_str and '://' in proxy_str:
                # Proxy com autenticação - usar extensão
                print("🔐 Proxy com autenticação detectado - usando extensão...")
                return self._create_driver_with_auth_proxy()
        
        # Proxy sem autenticação ou sem proxy - método padrão
        # Obter opções
        options = self.get_chrome_options()
        
        # Desabilitar verificação SSL para WebDriver Manager (resolve problemas com proxies)
        os.environ['WDM_SSL_VERIFY'] = '0'
        
        # Configurar serviço do ChromeDriver
        service = Service(ChromeDriverManager().install())
        
        # Criar driver
        driver = webdriver.Chrome(service=service, options=options)
        
        # Configurar timeouts
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(60)
        
        # Script anti-detecção
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
                
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['pt-BR', 'pt', 'en-US', 'en']
                });
            '''
        })
        
        print("✅ Chrome iniciado com sucesso!")
        
        return driver
    
    def _create_driver_with_auth_proxy(self) -> webdriver.Chrome:
        """
        Cria driver com proxy autenticado usando extensão (método interno)
        Extrai credenciais automaticamente do self.proxy
        
        Returns:
            webdriver.Chrome: Driver configurado com proxy autenticado
        """
        if not self.proxy:
            raise ValueError("Proxy não configurado")
        
        proxy_str = self.proxy.get('http', '')
        
        # Parsear proxy: protocol://user:pass@host:port
        import re
        match = re.match(r'(\w+)://([^:]+):([^@]+)@([^:]+):(\d+)', proxy_str)
        
        if not match:
            raise ValueError(f"Formato de proxy inválido: {proxy_str}")
        
        protocol, user, password, host, port = match.groups()
        
        print(f"   Usuário: {user}")
        print(f"   Host: {host}:{port}")
        
        return self.create_driver_with_auth_proxy(host, int(port), user, password)
    
    def create_driver_with_auth_proxy(
        self,
        proxy_host: str,
        proxy_port: int,
        proxy_user: str,
        proxy_pass: str
    ) -> webdriver.Chrome:
        """
        Cria driver com proxy autenticado usando extensão
        (Método alternativo para proxies com autenticação)
        
        Args:
            proxy_host: Host do proxy
            proxy_port: Porta do proxy
            proxy_user: Usuário do proxy
            proxy_pass: Senha do proxy
        
        Returns:
            webdriver.Chrome: Driver configurado
        """
        import zipfile
        from pathlib import Path
        
        print(f"🔧 Criando extensão de proxy...")
        
        # Criar extensão de proxy
        manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy Auth",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""
        
        background_js = """
var config = {
    mode: "fixed_servers",
    rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
    }
};

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
    callbackFn,
    {urls: ["<all_urls>"]},
    ['blocking']
);
""" % (proxy_host, proxy_port, proxy_user, proxy_pass)
        
        # Criar arquivo ZIP da extensão
        plugin_path = Path('proxy_auth_plugin.zip')
        
        with zipfile.ZipFile(plugin_path, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        
        print(f"📦 Extensão criada: {plugin_path}")
        
        # Configurar Chrome com extensão (SEM proxy nas opções - a extensão cuida disso)
        # Salvar proxy atual
        original_proxy = self.proxy
        self.proxy = None  # Temporariamente remover para não adicionar --proxy-server
        
        options = self.get_chrome_options()
        options.add_extension(str(plugin_path))
        
        # Restaurar proxy
        self.proxy = original_proxy
        
        # Desabilitar verificação SSL
        os.environ['WDM_SSL_VERIFY'] = '0'
        
        # Criar driver
        print(f"🚀 Iniciando Chrome com extensão de proxy...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Configurar timeouts
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(60)
        
        # Script anti-detecção
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
                
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['pt-BR', 'pt', 'en-US', 'en']
                });
            '''
        })
        
        # Limpar arquivo de extensão após alguns segundos
        import time
        time.sleep(2)
        try:
            if plugin_path.exists():
                plugin_path.unlink()
                print(f"🗑️ Extensão temporária removida")
        except:
            pass  # Arquivo pode estar em uso
        
        print("✅ Chrome iniciado com proxy autenticado!")
        
        return driver

