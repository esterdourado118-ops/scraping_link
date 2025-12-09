"""
Selenium LinkedIn Scraper - Sistema Modular
============================================

Módulos disponíveis:
- proxy_manager: Gerenciamento e rotação de proxies
- session_manager: Gerenciamento de sessões persistentes do Chrome
- chrome_config: Configurações do Selenium/Chrome
"""

from .proxy_manager import ProxyManager, ProxyRotation
from .session_manager import SessionManager
from .chrome_config import ChromeConfig

__version__ = "1.0.0"
__all__ = [
    'ProxyManager',
    'ProxyRotation',
    'SessionManager',
    'ChromeConfig',
]


