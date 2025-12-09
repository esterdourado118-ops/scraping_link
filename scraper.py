"""
Exemplo de Web Scraper usando Selenium
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from config import get_driver


class WebScraper:
    """
    Classe para realizar web scraping com Selenium
    """
    
    def __init__(self, headless=False):
        """
        Inicializa o scraper
        
        Args:
            headless (bool): Se True, executa sem abrir janela do navegador
        """
        self.headless = headless
        self.driver = None
    
    def start(self):
        """Inicializa o driver do Selenium"""
        print(f"🚀 Iniciando navegador {'(modo headless)' if self.headless else '(modo visual)'}...")
        self.driver = get_driver(headless=self.headless)
        print("✅ Navegador iniciado com sucesso!")
    
    def stop(self):
        """Fecha o driver do Selenium"""
        if self.driver:
            self.driver.quit()
            print("🔴 Navegador fechado.")
    
    def navigate_to(self, url):
        """
        Navega para uma URL
        
        Args:
            url (str): URL de destino
        """
        print(f"🌐 Navegando para: {url}")
        self.driver.get(url)
        time.sleep(2)  # Pequena pausa para carregar
    
    def wait_for_element(self, by, value, timeout=10):
        """
        Espera até que um elemento esteja presente na página
        
        Args:
            by: Tipo de seletor (By.ID, By.CSS_SELECTOR, By.XPATH, etc)
            value: Valor do seletor
            timeout: Tempo máximo de espera em segundos
        
        Returns:
            WebElement ou None se não encontrado
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            print(f"⚠️ Elemento não encontrado: {value}")
            return None
    
    def get_element_text(self, by, value):
        """
        Obtém o texto de um elemento
        
        Args:
            by: Tipo de seletor
            value: Valor do seletor
        
        Returns:
            str: Texto do elemento ou None
        """
        try:
            element = self.driver.find_element(by, value)
            return element.text
        except NoSuchElementException:
            print(f"⚠️ Elemento não encontrado: {value}")
            return None
    
    def get_elements_text(self, by, value):
        """
        Obtém o texto de múltiplos elementos
        
        Args:
            by: Tipo de seletor
            value: Valor do seletor
        
        Returns:
            list: Lista com textos dos elementos
        """
        try:
            elements = self.driver.find_elements(by, value)
            return [elem.text for elem in elements if elem.text]
        except NoSuchElementException:
            print(f"⚠️ Elementos não encontrados: {value}")
            return []
    
    def click_element(self, by, value):
        """
        Clica em um elemento
        
        Args:
            by: Tipo de seletor
            value: Valor do seletor
        """
        try:
            element = self.wait_for_element(by, value)
            if element:
                element.click()
                print(f"✅ Clicado em: {value}")
                time.sleep(1)
        except Exception as e:
            print(f"❌ Erro ao clicar: {e}")
    
    def type_text(self, by, value, text):
        """
        Digita texto em um campo
        
        Args:
            by: Tipo de seletor
            value: Valor do seletor
            text: Texto a ser digitado
        """
        try:
            element = self.wait_for_element(by, value)
            if element:
                element.clear()
                element.send_keys(text)
                print(f"✅ Texto digitado em: {value}")
        except Exception as e:
            print(f"❌ Erro ao digitar: {e}")
    
    def take_screenshot(self, filename="screenshot.png"):
        """
        Tira um screenshot da página
        
        Args:
            filename: Nome do arquivo para salvar
        """
        self.driver.save_screenshot(filename)
        print(f"📸 Screenshot salvo: {filename}")
    
    def get_page_title(self):
        """Retorna o título da página"""
        return self.driver.title
    
    def get_current_url(self):
        """Retorna a URL atual"""
        return self.driver.current_url


def exemplo_google_search():
    """
    Exemplo 1: Busca no Google
    """
    print("\n" + "="*60)
    print("EXEMPLO 1: Busca no Google")
    print("="*60 + "\n")
    
    # Criar scraper (headless=False para ver o navegador)
    scraper = WebScraper(headless=False)
    
    try:
        # Iniciar navegador
        scraper.start()
        
        # Navegar para o Google
        scraper.navigate_to("https://www.google.com")
        
        # Aguardar e obter o título
        print(f"📄 Título da página: {scraper.get_page_title()}")
        
        # Procurar pela caixa de busca e digitar
        scraper.type_text(By.NAME, "q", "Selenium Python Web Scraping")
        
        # Clicar no botão de busca (ou pressionar Enter)
        scraper.click_element(By.NAME, "btnK")
        
        # Aguardar resultados carregarem
        time.sleep(3)
        
        # Pegar os títulos dos resultados
        print("\n🔍 Resultados da busca:")
        results = scraper.get_elements_text(By.CSS_SELECTOR, "h3")
        for i, result in enumerate(results[:5], 1):  # Primeiros 5 resultados
            print(f"{i}. {result}")
        
        # Tirar screenshot
        scraper.take_screenshot("google_search.png")
        
        # Aguardar um pouco para visualizar
        time.sleep(3)
        
    except Exception as e:
        print(f"❌ Erro durante scraping: {e}")
    
    finally:
        # Sempre fechar o navegador
        scraper.stop()


def exemplo_quotes_scraping():
    """
    Exemplo 2: Scraping de citações do site quotes.toscrape.com
    """
    print("\n" + "="*60)
    print("EXEMPLO 2: Scraping de Citações")
    print("="*60 + "\n")
    
    # Criar scraper em modo headless (mais rápido)
    scraper = WebScraper(headless=True)
    
    try:
        # Iniciar navegador
        scraper.start()
        
        # Navegar para o site de exemplo
        scraper.navigate_to("http://quotes.toscrape.com")
        
        print(f"📄 Título: {scraper.get_page_title()}")
        
        # Aguardar as citações carregarem
        scraper.wait_for_element(By.CLASS_NAME, "quote")
        
        # Pegar todas as citações da página
        quotes = scraper.driver.find_elements(By.CLASS_NAME, "quote")
        
        print(f"\n📚 Encontradas {len(quotes)} citações:\n")
        
        for i, quote in enumerate(quotes, 1):
            # Pegar o texto da citação
            text = quote.find_element(By.CLASS_NAME, "text").text
            # Pegar o autor
            author = quote.find_element(By.CLASS_NAME, "author").text
            # Pegar as tags
            tags = quote.find_elements(By.CLASS_NAME, "tag")
            tag_list = [tag.text for tag in tags]
            
            print(f"{i}. {text}")
            print(f"   Autor: {author}")
            print(f"   Tags: {', '.join(tag_list)}\n")
        
        # Tirar screenshot
        scraper.take_screenshot("quotes_page.png")
        
    except Exception as e:
        print(f"❌ Erro durante scraping: {e}")
    
    finally:
        scraper.stop()


def exemplo_navegacao_multiplas_paginas():
    """
    Exemplo 3: Navegação entre múltiplas páginas
    """
    print("\n" + "="*60)
    print("EXEMPLO 3: Navegação Entre Páginas")
    print("="*60 + "\n")
    
    scraper = WebScraper(headless=True)
    
    try:
        scraper.start()
        
        # Navegar para a primeira página
        scraper.navigate_to("http://quotes.toscrape.com")
        
        # Coletar citações de 3 páginas
        all_quotes = []
        
        for page in range(1, 4):  # Páginas 1, 2 e 3
            print(f"\n📄 Coletando dados da página {page}...")
            
            # Aguardar citações carregarem
            scraper.wait_for_element(By.CLASS_NAME, "quote")
            
            # Pegar citações da página atual
            quotes = scraper.driver.find_elements(By.CLASS_NAME, "quote")
            
            for quote in quotes:
                text = quote.find_element(By.CLASS_NAME, "text").text
                author = quote.find_element(By.CLASS_NAME, "author").text
                all_quotes.append({"text": text, "author": author})
            
            # Tentar ir para próxima página
            try:
                next_button = scraper.driver.find_element(By.CSS_SELECTOR, ".next > a")
                next_button.click()
                time.sleep(2)
            except NoSuchElementException:
                print("✅ Não há mais páginas.")
                break
        
        print(f"\n📊 Total de citações coletadas: {len(all_quotes)}")
        
        # Mostrar algumas citações
        print("\n🎯 Primeiras 5 citações coletadas:")
        for i, quote in enumerate(all_quotes[:5], 1):
            print(f"{i}. \"{quote['text']}\" - {quote['author']}")
        
    except Exception as e:
        print(f"❌ Erro durante scraping: {e}")
    
    finally:
        scraper.stop()


if __name__ == "__main__":
    """
    Executa os exemplos de scraping
    """
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║         EXEMPLOS DE WEB SCRAPING COM SELENIUM              ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # Descomente o exemplo que deseja executar:
    
    # Exemplo 1: Busca no Google (modo visual)
    # exemplo_google_search()
    
    # Exemplo 2: Scraping de citações (modo headless)
    exemplo_quotes_scraping()
    
    # Exemplo 3: Navegação entre múltiplas páginas
    # exemplo_navegacao_multiplas_paginas()
    
    print("\n✅ Scraping finalizado!")
    print("\n💡 Dica: Edite este arquivo e descomente os exemplos que deseja testar!")


