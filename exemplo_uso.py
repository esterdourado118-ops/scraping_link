"""
Exemplo Completo de Uso do Sistema
===================================

Este arquivo demonstra como usar todos os módulos do sistema
"""

from selenium_linkedin import ProxyManager, ProxyRotation, SessionManager, ChromeConfig
import time


def exemplo_1_apenas_proxy():
    """
    Exemplo 1: Usando apenas o gerenciador de proxies
    """
    print("\n" + "="*60)
    print("EXEMPLO 1: Gerenciador de Proxies")
    print("="*60 + "\n")
    
    # Criar gerenciador de proxies
    pm = ProxyManager(
        proxy_file="proxies.txt",
        rotation_mode=ProxyRotation.SEQUENTIAL
    )
    
    # Listar proxies disponíveis
    pm.list_proxies()
    
    # Obter próximo proxy
    proxy = pm.get_next_proxy()
    
    # Validar proxy
    if proxy:
        print("\n🔍 Validando proxy...")
        is_valid = pm.validate_proxy(proxy)
        
        if is_valid:
            print("✅ Proxy está funcionando!")
        else:
            print("❌ Proxy não está funcionando")
    
    # Obter estatísticas
    stats = pm.get_stats()
    print(f"\n📊 Estatísticas:")
    print(f"   Total de proxies: {stats['total_proxies']}")
    print(f"   Índice atual: {stats['current_index']}")
    print(f"   Modo: {stats['rotation_mode']}")


def exemplo_2_apenas_sessao():
    """
    Exemplo 2: Gerenciando sessões do Chrome
    """
    print("\n" + "="*60)
    print("EXEMPLO 2: Gerenciador de Sessões")
    print("="*60 + "\n")
    
    # Criar gerenciador de sessão
    sm = SessionManager(profile_name="linkedin")
    
    # Listar perfis existentes
    sm.list_profiles()
    
    # Obter informações do perfil
    info = sm.get_info()
    print(f"📁 Informações do perfil:")
    print(f"   Nome: {info['profile_name']}")
    print(f"   Caminho: {info['profile_path']}")
    print(f"   Existe: {info['exists']}")


def exemplo_3_chrome_basico():
    """
    Exemplo 3: Configuração básica do Chrome
    """
    print("\n" + "="*60)
    print("EXEMPLO 3: Chrome Básico (sem proxy, sem sessão)")
    print("="*60 + "\n")
    
    # Configuração simples
    config = ChromeConfig(
        headless=False,  # Modo visual
        window_size=(1280, 720)
    )
    
    # Criar driver
    driver = config.create_driver()
    
    try:
        # Navegar para um site
        print("🌐 Navegando para exemplo.com...")
        driver.get("https://www.example.com")
        time.sleep(3)
        
        # Pegar título
        print(f"📄 Título: {driver.title}")
        
    finally:
        driver.quit()
        print("✅ Navegador fechado")


def exemplo_4_chrome_com_proxy():
    """
    Exemplo 4: Chrome com proxy
    """
    print("\n" + "="*60)
    print("EXEMPLO 4: Chrome com Proxy")
    print("="*60 + "\n")
    
    # Obter proxy
    pm = ProxyManager("proxies.txt")
    proxy = pm.get_next_proxy()
    
    if not proxy:
        print("❌ Nenhum proxy disponível!")
        return
    
    # Configurar Chrome com proxy
    config = ChromeConfig(
        headless=False,
        proxy=proxy
    )
    
    # Criar driver
    driver = config.create_driver()
    
    try:
        # Verificar IP
        print("🔍 Verificando IP através do proxy...")
        driver.get("http://ipinfo.io/json")
        time.sleep(3)
        
        # Mostrar página
        print("✅ Página carregada. Verifique o IP no navegador.")
        time.sleep(5)
        
    finally:
        driver.quit()


def exemplo_5_chrome_com_sessao():
    """
    Exemplo 5: Chrome com sessão salva
    """
    print("\n" + "="*60)
    print("EXEMPLO 5: Chrome com Sessão Salva")
    print("="*60 + "\n")
    
    # Gerenciador de sessão
    sm = SessionManager(profile_name="linkedin")
    
    # Verificar se tem sessão
    if not sm.profile_exists():
        print("⚠️  Sessão não encontrada!")
        print("👉 Execute: make session")
        return
    
    # Configurar Chrome
    config = ChromeConfig(
        headless=False,
        profile_path=sm.get_profile_path()
    )
    
    # Criar driver
    driver = config.create_driver()
    
    try:
        # Navegar para LinkedIn
        print("🌐 Navegando para LinkedIn...")
        driver.get("https://www.linkedin.com/feed/")
        
        print("✅ Se você já fez login antes, deve estar logado automaticamente!")
        time.sleep(10)
        
    finally:
        driver.quit()


def exemplo_6_completo():
    """
    Exemplo 6: Sistema completo (proxy + sessão)
    """
    print("\n" + "="*60)
    print("EXEMPLO 6: Sistema Completo (Proxy + Sessão)")
    print("="*60 + "\n")
    
    # 1. Gerenciador de sessão
    sm = SessionManager(profile_name="linkedin")
    
    if not sm.profile_exists():
        print("⚠️  Sessão não encontrada!")
        print("👉 Execute: make session")
        return
    
    # 2. Gerenciador de proxy
    pm = ProxyManager(
        proxy_file="proxies.txt",
        rotation_mode=ProxyRotation.SEQUENTIAL
    )
    
    proxy = pm.get_next_proxy()
    
    # 3. Configurar Chrome
    config = ChromeConfig(
        headless=False,
        profile_path=sm.get_profile_path(),
        proxy=proxy,
        disable_images=False
    )
    
    # 4. Criar driver
    driver = config.create_driver()
    
    try:
        # Navegar
        print("🌐 Navegando para LinkedIn...")
        driver.get("https://www.linkedin.com/feed/")
        
        print("\n✅ Sistema completo funcionando!")
        print("   - Proxy ativo")
        print("   - Sessão salva")
        print("   - Anti-detecção ativo")
        
        time.sleep(10)
        
    finally:
        driver.quit()


def menu():
    """Menu interativo para escolher exemplos"""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║         EXEMPLOS DE USO - LINKEDIN SCRAPER                 ║
    ╚════════════════════════════════════════════════════════════╝
    
    Escolha um exemplo para executar:
    
    1. Gerenciador de Proxies
    2. Gerenciador de Sessões
    3. Chrome Básico (sem proxy/sessão)
    4. Chrome com Proxy
    5. Chrome com Sessão Salva
    6. Sistema Completo (Proxy + Sessão)
    
    0. Sair
    """)
    
    escolha = input("Digite o número do exemplo (0-6): ").strip()
    
    exemplos = {
        '1': exemplo_1_apenas_proxy,
        '2': exemplo_2_apenas_sessao,
        '3': exemplo_3_chrome_basico,
        '4': exemplo_4_chrome_com_proxy,
        '5': exemplo_5_chrome_com_sessao,
        '6': exemplo_6_completo
    }
    
    if escolha == '0':
        print("\n👋 Até logo!")
        return
    
    if escolha in exemplos:
        try:
            exemplos[escolha]()
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrompido pelo usuário")
        except Exception as e:
            print(f"\n❌ Erro: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("\n❌ Opção inválida!")
    
    # Perguntar se quer executar outro
    print("\n")
    continuar = input("Executar outro exemplo? (s/n): ").lower()
    if continuar == 's':
        menu()


if __name__ == "__main__":
    menu()


