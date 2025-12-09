# ====================================================================
# MAKEFILE - LinkedIn Scraper
# ====================================================================
#
# Comandos disponíveis:
#   make install   - Instala todas as dependências
#   make session   - Abre Chrome para fazer login e salvar sessão
#   make scrape    - Executa scraping com sessão salva
#   make test      - Testa se está tudo configurado
#   make clean     - Limpa arquivos temporários
#   make help      - Mostra ajuda
#
# ====================================================================

.PHONY: help install session scrape test clean list-proxies

# Comando padrão
.DEFAULT_GOAL := help

# Cores para output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Mostra esta mensagem de ajuda
	@echo ""
	@echo "$(BLUE)════════════════════════════════════════════════════════════$(NC)"
	@echo "$(BLUE)║           LINKEDIN SCRAPER - MAKEFILE                     ║$(NC)"
	@echo "$(BLUE)════════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(GREEN)Comandos disponíveis:$(NC)"
	@echo ""
	@echo "  $(YELLOW)make install$(NC)       - Instala todas as dependências do Python"
	@echo "  $(YELLOW)make session$(NC)       - Abre Chrome para você fazer login no LinkedIn"
	@echo "                     (Execute isso PRIMEIRO, apenas UMA VEZ)"
	@echo ""
	@echo "  $(YELLOW)make scrape$(NC)        - Executa o scraping do LinkedIn"
	@echo "                     (Usa a sessão salva + proxy automático)"
	@echo ""
	@echo "  $(YELLOW)make test$(NC)          - Testa se está tudo configurado corretamente"
	@echo "  $(YELLOW)make list-proxies$(NC)  - Lista todos os proxies disponíveis"
	@echo "  $(YELLOW)make clean$(NC)         - Limpa arquivos temporários e cache"
	@echo "  $(YELLOW)make help$(NC)          - Mostra esta mensagem"
	@echo ""
	@echo "$(BLUE)════════════════════════════════════════════════════════════$(NC)"
	@echo ""

install: ## Instala as dependências
	@echo "$(BLUE)📦 Instalando dependências...$(NC)"
	pip install -r requirements.txt
	@echo "$(GREEN)✅ Dependências instaladas com sucesso!$(NC)"

session: ## Abre Chrome para fazer login manual e salvar sessão
	@echo ""
	@echo "$(BLUE)════════════════════════════════════════════════════════════$(NC)"
	@echo "$(BLUE)║        CONFIGURAÇÃO DE SESSÃO DO LINKEDIN                 ║$(NC)"
	@echo "$(BLUE)════════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(YELLOW)🚀 Abrindo Chrome para você fazer login...$(NC)"
	@echo ""
	@echo "$(GREEN)👉 Faça login no LinkedIn manualmente$(NC)"
	@echo "$(GREEN)👉 Pressione ENTER após fazer login$(NC)"
	@echo "$(GREEN)👉 Sua sessão será salva automaticamente$(NC)"
	@echo ""
	python setup_linkedin_session.py

scrape: ## Executa o scraping do LinkedIn com sessão salva
	@echo ""
	@echo "$(BLUE)════════════════════════════════════════════════════════════$(NC)"
	@echo "$(BLUE)║           EXECUTANDO SCRAPING DO LINKEDIN                 ║$(NC)"
	@echo "$(BLUE)════════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(GREEN)🤖 Iniciando automação...$(NC)"
	@echo ""
	python linkedin_scraper.py

test: ## Testa a configuração
	@echo ""
	@echo "$(BLUE)════════════════════════════════════════════════════════════$(NC)"
	@echo "$(BLUE)║              TESTANDO CONFIGURAÇÃO                        ║$(NC)"
	@echo "$(BLUE)════════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(YELLOW)🔍 Verificando Python...$(NC)"
	@python --version || (echo "$(RED)❌ Python não encontrado!$(NC)" && exit 1)
	@echo "$(GREEN)✅ Python OK$(NC)"
	@echo ""
	@echo "$(YELLOW)🔍 Verificando Selenium...$(NC)"
	@python -c "import selenium; print('  Versão:', selenium.__version__)" || (echo "$(RED)❌ Selenium não instalado!$(NC)" && exit 1)
	@echo "$(GREEN)✅ Selenium OK$(NC)"
	@echo ""
	@echo "$(YELLOW)🔍 Verificando WebDriver Manager...$(NC)"
	@python -c "import webdriver_manager; print('  WebDriver Manager OK')" || (echo "$(RED)❌ WebDriver Manager não instalado!$(NC)" && exit 1)
	@echo "$(GREEN)✅ WebDriver Manager OK$(NC)"
	@echo ""
	@echo "$(YELLOW)🔍 Verificando módulos personalizados...$(NC)"
	@python -c "from selenium_linkedin import ProxyManager, SessionManager, ChromeConfig; print('  Módulos OK')" || (echo "$(RED)❌ Módulos não encontrados!$(NC)" && exit 1)
	@echo "$(GREEN)✅ Módulos OK$(NC)"
	@echo ""
	@echo "$(YELLOW)🔍 Verificando arquivo de proxies...$(NC)"
	@test -f proxies.txt && echo "$(GREEN)✅ proxies.txt encontrado$(NC)" || echo "$(YELLOW)⚠️  proxies.txt não encontrado$(NC)"
	@echo ""
	@echo "$(GREEN)════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)✅ Tudo configurado corretamente!$(NC)"
	@echo "$(GREEN)════════════════════════════════════════════════════════════$(NC)"
	@echo ""

list-proxies: ## Lista todos os proxies disponíveis
	@echo ""
	@echo "$(BLUE)════════════════════════════════════════════════════════════$(NC)"
	@echo "$(BLUE)║              PROXIES DISPONÍVEIS                          ║$(NC)"
	@echo "$(BLUE)════════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@python -c "from selenium_linkedin import ProxyManager; pm = ProxyManager('proxies.txt'); pm.list_proxies()"
	@echo ""

clean: ## Limpa arquivos temporários
	@echo "$(YELLOW)🧹 Limpando arquivos temporários...$(NC)"
	@rm -rf __pycache__
	@rm -rf selenium_linkedin/__pycache__
	@rm -rf *.pyc
	@rm -rf .pytest_cache
	@rm -rf *.log
	@rm -rf proxy_state.json
	@rm -rf *.png
	@echo "$(GREEN)✅ Arquivos temporários removidos!$(NC)"
	@echo ""
	@echo "$(YELLOW)⚠️  Para deletar a sessão salva do LinkedIn, delete a pasta:$(NC)"
	@echo "   chrome_profiles/"


