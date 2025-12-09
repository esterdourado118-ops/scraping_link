"""
Setup de Sessão do LinkedIn
============================

Execute este script UMA VEZ para fazer login manualmente no LinkedIn.
Sua sessão ficará salva e não precisará fazer login novamente.

Uso:
    python setup_linkedin_session.py
"""

import time
from selenium_linkedin import SessionManager, ChromeConfig


def setup_session():
    """
    Abre o Chrome para você fazer login manualmente no LinkedIn
    """
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║     CONFIGURAÇÃO DE SESSÃO DO LINKEDIN                     ║
    ╚════════════════════════════════════════════════════════════╝
    
    Este script irá:
    1. Abrir o navegador Chrome
    2. Navegar para o LinkedIn
    3. Você faz login manualmente
    4. Sua sessão fica salva automaticamente
    
    """)
    
    # Criar gerenciador de sessão
    session = SessionManager(profile_name="linkedin")
    
    # Verificar se já existe sessão
    if session.profile_exists():
        print("⚠️  Já existe uma sessão salva!")
        resposta = input("Deseja recriar a sessão? (s/n): ").lower()
        
        if resposta == 's':
            session.delete_profile()
            print("🗑️  Sessão anterior deletada\n")
        else:
            print("✅ Mantendo sessão existente")
            return
    
    # Configurar Chrome (modo visual, com perfil, sem proxy)
    print("\n🚀 Abrindo navegador...\n")
    
    chrome_config = ChromeConfig(
        headless=False,  # Modo visual para você fazer login
        profile_path=session.get_profile_path()
    )
    
    # Criar driver
    driver = chrome_config.create_driver()
    
    try:
        # Navegar para LinkedIn
        print("🌐 Navegando para LinkedIn...\n")
        driver.get("https://www.linkedin.com")
        
        print("""
    ╔════════════════════════════════════════════════════════════╗
    ║                    FAÇA SEU LOGIN                          ║
    ╚════════════════════════════════════════════════════════════╝
    
    👉 Faça login no LinkedIn manualmente
    👉 Após fazer login, pressione ENTER aqui no terminal
    👉 Você pode navegar pelo LinkedIn se quiser testar
    
    ⚠️  NÃO FECHE O NAVEGADOR! Apenas pressione ENTER quando terminar.
        """)
        
        # Aguardar usuário fazer login
        input("Pressione ENTER depois de fazer login... ")
        
        print("\n✅ Salvando sessão...")
        
        # A sessão já está salva automaticamente no perfil do Chrome
        print("✅ Sessão salva com sucesso!")
        
        print("""
    ╔════════════════════════════════════════════════════════════╗
    ║                  CONFIGURAÇÃO COMPLETA!                    ║
    ╚════════════════════════════════════════════════════════════╝
    
    ✅ Sua sessão está salva em: {path}
    
    Agora você pode:
    - Fechar este navegador
    - Executar seus scripts de scraping
    - O navegador abrirá já logado automaticamente
    
    📝 Comandos disponíveis:
       make session   - Refazer este setup
       make scrape    - Executar scraping com sessão salva
        """.format(path=session.get_profile_path()))
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    
    finally:
        print("\n🔴 Fechando navegador em 5 segundos...")
        time.sleep(5)
        driver.quit()
        print("✅ Navegador fechado. Sessão está salva!")


if __name__ == "__main__":
    setup_session()


