# ====================================================================
# SCRIPTS POWERSHELL - LinkedIn Scraper
# ====================================================================
#
# Como usar:
#   .\run.ps1 install       - Instala dependencias
#   .\run.ps1 session       - Configura login no LinkedIn
#   .\run.ps1 scrape        - Executa scraping
#   .\run.ps1 test          - Testa configuracao
#   .\run.ps1 list-proxies  - Lista proxies
#   .\run.ps1 clean         - Limpa arquivos temporarios
#   .\run.ps1 help          - Mostra ajuda
#
# ====================================================================

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

# Cores
function Write-Blue { Write-Host $args -ForegroundColor Blue }
function Write-Green { Write-Host $args -ForegroundColor Green }
function Write-Yellow { Write-Host $args -ForegroundColor Yellow }
function Write-Red { Write-Host $args -ForegroundColor Red }

# Funcoes
function Show-Help {
    Write-Host ""
    Write-Blue "============================================================"
    Write-Blue "           LINKEDIN SCRAPER - POWERSHELL                    "
    Write-Blue "============================================================"
    Write-Host ""
    Write-Green "Comandos disponiveis:"
    Write-Host ""
    Write-Host "  .\run.ps1 install        - Instala todas as dependencias do Python" -ForegroundColor Yellow
    Write-Host "  .\run.ps1 session        - Abre Chrome para voce fazer login no LinkedIn" -ForegroundColor Yellow
    Write-Host "                             (Execute isso PRIMEIRO, apenas UMA VEZ)"
    Write-Host ""
    Write-Host "  .\run.ps1 scrape         - Executa o scraping do LinkedIn" -ForegroundColor Yellow
    Write-Host "                             (Usa a sessao salva + proxy automatico)"
    Write-Host ""
    Write-Host "  .\run.ps1 test           - Testa se esta tudo configurado corretamente" -ForegroundColor Yellow
    Write-Host "  .\run.ps1 list-proxies   - Lista todos os proxies disponiveis" -ForegroundColor Yellow
    Write-Host "  .\run.ps1 clean          - Limpa arquivos temporarios e cache" -ForegroundColor Yellow
    Write-Host "  .\run.ps1 help           - Mostra esta mensagem" -ForegroundColor Yellow
    
    Write-Host ""
    Write-Blue "============================================================"
    Write-Host ""
}

function Install-Dependencies {
    Write-Host ""
    Write-Blue "Instalando dependencias..."
    Write-Host ""
    
    pip install -r requirements.txt
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Green "Dependencias instaladas com sucesso!"
        Write-Host ""
    } else {
        Write-Red "Erro ao instalar dependencias!"
    }
}

function Setup-Session {
    Write-Host ""
    Write-Blue "============================================================"
    Write-Blue "        CONFIGURACAO DE SESSAO DO LINKEDIN                  "
    Write-Blue "============================================================"
    Write-Host ""
    Write-Yellow "Abrindo Chrome para voce fazer login..."
    Write-Host ""
    Write-Green "-> Faca login no LinkedIn manualmente"
    Write-Green "-> Pressione ENTER apos fazer login"
    Write-Green "-> Sua sessao sera salva automaticamente"
    Write-Host ""
    
    python setup_linkedin_session.py
}

function Start-Scraping {
    Write-Host ""
    Write-Blue "============================================================"
    Write-Blue "           EXECUTANDO SCRAPING DO LINKEDIN                  "
    Write-Blue "============================================================"
    Write-Host ""
    Write-Green "Iniciando automacao..."
    Write-Host ""
    
    python linkedin_scraper.py
}

function Test-Configuration {
    Write-Host ""
    Write-Blue "============================================================"
    Write-Blue "              TESTANDO CONFIGURACAO                         "
    Write-Blue "============================================================"
    Write-Host ""
    
    # Testar Python
    Write-Yellow "Verificando Python..."
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  $pythonVersion"
        Write-Green "Python OK"
    } else {
        Write-Red "Python nao encontrado!"
        return
    }
    Write-Host ""
    
    # Testar Selenium
    Write-Yellow "Verificando Selenium..."
    & python -c "import selenium; print('  Versao:', selenium.__version__)" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        & python -c "import selenium; print('  Versao:', selenium.__version__)"
        Write-Green "Selenium OK"
    } else {
        Write-Red "Selenium nao instalado!"
        Write-Yellow "Execute: .\run.ps1 install"
        return
    }
    Write-Host ""
    
    # Testar WebDriver Manager
    Write-Yellow "Verificando WebDriver Manager..."
    & python -c "import webdriver_manager" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  WebDriver Manager OK"
        Write-Green "WebDriver Manager OK"
    } else {
        Write-Red "WebDriver Manager nao instalado!"
        return
    }
    Write-Host ""
    
    # Testar modulos personalizados
    Write-Yellow "Verificando modulos personalizados..."
    & python -c "from selenium_linkedin import ProxyManager, SessionManager, ChromeConfig" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Modulos OK"
        Write-Green "Modulos OK"
    } else {
        Write-Red "Modulos nao encontrados!"
        return
    }
    Write-Host ""
    
    # Verificar proxies.txt
    Write-Yellow "Verificando arquivo de proxies..."
    if (Test-Path "proxies.txt") {
        Write-Green "proxies.txt encontrado"
    } else {
        Write-Yellow "proxies.txt nao encontrado"
    }
    Write-Host ""
    
    Write-Green "============================================================"
    Write-Green "Tudo configurado corretamente!"
    Write-Green "============================================================"
    Write-Host ""
}

function List-Proxies {
    Write-Host ""
    Write-Blue "============================================================"
    Write-Blue "              PROXIES DISPONIVEIS                           "
    Write-Blue "============================================================"
    Write-Host ""
    
    python _list_proxies.py
    
    Write-Host ""
}

function Clean-Files {
    Write-Yellow "Limpando arquivos temporarios..."
    
    # Remover __pycache__
    if (Test-Path "__pycache__") {
        Remove-Item -Recurse -Force "__pycache__"
    }
    
    if (Test-Path "selenium_linkedin\__pycache__") {
        Remove-Item -Recurse -Force "selenium_linkedin\__pycache__"
    }
    
    # Remover arquivos .pyc
    Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force
    
    # Remover outros arquivos temporarios
    if (Test-Path ".pytest_cache") {
        Remove-Item -Recurse -Force ".pytest_cache"
    }
    
    if (Test-Path "proxy_state.json") {
        Remove-Item -Force "proxy_state.json"
    }
    
    Get-ChildItem -Filter "*.log" | Remove-Item -Force
    Get-ChildItem -Filter "*.png" | Remove-Item -Force
    
    Write-Green "Arquivos temporarios removidos!"
    Write-Host ""
    Write-Yellow "Para deletar a sessao salva do LinkedIn, delete a pasta:"
    Write-Host "   chrome_profiles\"
    Write-Host ""
}

# Executar comando
switch ($Command.ToLower()) {
    "help" { Show-Help }
    "install" { Install-Dependencies }
    "session" { Setup-Session }
    "scrape" { Start-Scraping }
    "test" { Test-Configuration }
    "list-proxies" { List-Proxies }
    "clean" { Clean-Files }
    default {
        Write-Red "Comando invalido: $Command"
        Write-Host ""
        Show-Help
    }
}
