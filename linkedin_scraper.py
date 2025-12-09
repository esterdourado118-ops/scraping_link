"""
LinkedIn Scraper com Sessão Salva e Rotação de Proxy
=====================================================

Script de exemplo para fazer scraping no LinkedIn usando:
- Sessão salva (não precisa fazer login)
- Rotação automática de proxies
- Anti-detecção
- Enriquecimento de dados (API BigDataCorp)

Uso:
    python linkedin_scraper.py
"""

import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from selenium_linkedin import ProxyManager, ProxyRotation, SessionManager, ChromeConfig
from utils import enrich_and_save  # Importar nossa nova função


class LinkedInScraper:
    """
    Scraper do LinkedIn com recursos avançados
    """
    
    def __init__(self, headless: bool = False, use_proxy: bool = True):
        """
        Inicializa o scraper
        
        Args:
            headless: Se True, executa sem interface gráfica
            use_proxy: Se True, usa proxy da lista
        """
        self.headless = headless
        self.use_proxy = use_proxy
        self.driver = None
        
        # Gerenciador de sessão
        self.session_manager = SessionManager(profile_name="linkedin")
        
        # Gerenciador de proxies (se habilitado)
        self.proxy_manager = None
        self.current_proxy = None
        
        if use_proxy:
            self.proxy_manager = ProxyManager(
                proxy_file="proxies.txt",
                rotation_mode=ProxyRotation.SEQUENTIAL
            )
            
        # Lista para armazenar nomes coletados
        self.collected_names = []
    
    def start(self):
        """Inicializa o navegador"""
        print("\n" + "="*60)
        print("INICIANDO LINKEDIN SCRAPER")
        print("="*60 + "\n")
        
        # Verificar se tem sessão salva
        if not self.session_manager.profile_exists():
            print("❌ ERRO: Sessão não encontrada!")
            print("\n👉 Execute primeiro: python setup_linkedin_session.py")
            print("   ou: make session\n")
            return False
        
        # Obter próximo proxy (se habilitado)
        if self.use_proxy and self.proxy_manager:
            self.current_proxy = self.proxy_manager.get_next_proxy()
            
            if not self.current_proxy:
                print("⚠️  Nenhum proxy disponível. Continuando sem proxy...")
        
        # Configurar Chrome
        chrome_config = ChromeConfig(
            headless=self.headless,
            profile_path=self.session_manager.get_profile_path(),
            proxy=self.current_proxy
        )
        
        # Criar driver
        self.driver = chrome_config.create_driver()
        
        print("\n✅ Navegador iniciado!")
        return True
    
    def stop(self):
        """Fecha o navegador"""
        if self.driver:
            print("\n🔴 Fechando navegador...")
            self.driver.quit()
            print("✅ Navegador fechado")
    
    def random_delay(self, min_sec: float = 1.0, max_sec: float = 3.0):
        """Delay aleatório para parecer mais humano"""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)
    
    def navigate_to_linkedin(self):
        """Navega para o LinkedIn"""
        print("\n🌐 Navegando para LinkedIn...")
        self.driver.get("https://www.linkedin.com/feed/")
        self.random_delay(2, 4)
    
    def check_login_status(self) -> bool:
        """
        Verifica se está logado no LinkedIn
        
        Returns:
            True se está logado, False caso contrário
        """
        try:
            # Tentar encontrar elementos que só aparecem quando logado
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "global-nav"))
            )
            print("✅ Login verificado - Você está logado!")
            return True
        except TimeoutException:
            print("❌ Não está logado. Execute o setup da sessão primeiro.")
            return False
    
    def search_people(self, query: str, max_results: int = 10):
        """
        Busca pessoas no LinkedIn e coleta nomes
        
        Args:
            query: Termo de busca
            max_results: Máximo de resultados
        """
        try:
            print(f"\n🔍 Buscando: {query}")
            
            # Ir para busca
            search_url = f"https://www.linkedin.com/search/results/people/?keywords={query}"
            self.driver.get(search_url)
            self.random_delay(3, 5)
            
            # Aguardar resultados carregarem
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".search-results-container"))
            )
            
            print("✅ Resultados carregados")
            
            # Scroll para carregar mais resultados
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            self.random_delay(1, 2)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.random_delay(2, 3)
            
            # Coletar nomes
            results = self.driver.find_elements(By.CSS_SELECTOR, ".entity-result__title-text a span[aria-hidden='true']")
            
            print(f"\n📋 Encontrados {len(results)} resultados na página:\n")
            
            count = 0
            for result in results:
                if count >= max_results:
                    break
                    
                try:
                    name = result.text.strip()
                    if name and name not in self.collected_names:
                        print(f"👤 Coletado: {name}")
                        self.collected_names.append(name)
                        count += 1
                except:
                    continue
            
            print(f"\n✅ Total coletado nesta busca: {count}")
            return count
            
        except Exception as e:
            print(f"❌ Erro na busca: {e}")
            return 0
    
    def enrich_data(self):
        """
        Enriquece os dados coletados usando a API BigDataCorp
        """
        if not self.collected_names:
            print("\n⚠️ Nenhum nome coletado para enriquecer.")
            return
            
        print(f"\n🔄 Iniciando enriquecimento de {len(self.collected_names)} nomes...")
        
        # Chama a função do utils.py
        enrich_and_save(self.collected_names)


def main():
    """Função principal"""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║      LINKEDIN SCRAPER + ENRIQUECIMENTO DE DADOS            ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # Criar scraper
    scraper = LinkedInScraper(
        headless=False,  # True para modo headless, False para ver o navegador
        use_proxy=True   # True para usar proxy, False para não usar
    )
    
    try:
        # Iniciar navegador
        if not scraper.start():
            return
        
        # Navegar para LinkedIn
        scraper.navigate_to_linkedin()
        
        # Verificar login
        if not scraper.check_login_status():
            return
            
        # ========================================================
        # CONFIGURE SUA BUSCA AQUI
        # ========================================================
        termo_busca = "Recrutador TI"  # Exemplo
        quantidade = 5                 # Quantidade de perfis
        # ========================================================
        
        # 1. Buscar e coletar nomes
        scraper.search_people(termo_busca, max_results=quantidade)
        
        # 2. Enriquecer dados (API) e salvar CSV
        scraper.enrich_data()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompido pelo usuário")
    
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    
    finally:
        # Sempre fechar o navegador
        scraper.stop()
    
    print("\n✅ Processo finalizado com sucesso!")


if __name__ == "__main__":
    main()
