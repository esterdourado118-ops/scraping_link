# 🤖 LinkedIn Scraper - Sistema Modular Completo

Sistema profissional de web scraping para LinkedIn com:
- ✅ **Sessão persistente** (não precisa fazer login toda vez)
- ✅ **Rotação automática de proxies** (suporta PyProxy e outros)
- ✅ **Arquitetura modular** (código organizado em módulos)
- ✅ **Anti-detecção** (user-agent, delays aleatórios, etc)
- ✅ **Scripts PowerShell + Makefile** (comandos simples para Windows, Linux e Mac)

---

## 🪟 **IMPORTANTE - Usuários Windows**

**Não use `make` no Windows!** Use o script PowerShell incluído:

```powershell
.\run.ps1 help          # Ver todos os comandos
.\run.ps1 session       # Configurar login
.\run.ps1 scrape        # Executar scraping
```

Veja [QUICKSTART_WINDOWS.md](QUICKSTART_WINDOWS.md) para guia completo Windows.

---

## 📋 Índice

- [Estrutura do Projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Instalação Rápida](#instalação-rápida)
- [Como Usar](#como-usar)
- [Comandos Disponíveis](#comandos-disponíveis)
- [Módulos Disponíveis](#módulos-disponíveis)
- [Configuração de Proxies](#configuração-de-proxies)
- [Avisos Legais](#avisos-legais)

---

## 📁 Estrutura do Projeto

```
pegaemailLINKEDIN/
├── selenium_linkedin/          # 📦 Módulo principal
│   ├── __init__.py            # Exports dos módulos
│   ├── proxy_manager.py       # Gerenciador de proxies
│   ├── session_manager.py     # Gerenciador de sessões
│   └── chrome_config.py       # Configurações do Chrome
│
├── setup_linkedin_session.py  # 🔧 Script para fazer login (1x)
├── linkedin_scraper.py         # 🤖 Script de scraping principal
├── proxies.txt                 # 📝 Lista de proxies
├── run.ps1                     # ⚙️  Comandos PowerShell (Windows)
├── Makefile                    # ⚙️  Comandos Make (Linux/Mac)
├── requirements.txt            # 📦 Dependências Python
└── README.md                   # 📖 Este arquivo

Gerados automaticamente:
├── chrome_profiles/            # 💾 Perfis do Chrome (sessões)
└── proxy_state.json           # 📊 Estado da rotação de proxies
```

---

## 🔧 Pré-requisitos

1. **Python 3.8+** instalado
2. **Google Chrome** instalado e atualizado
3. **pip** (gerenciador de pacotes Python)

**Nota:** Não precisa instalar Make no Windows! Use o script PowerShell `run.ps1` incluído.

---

## 🚀 Instalação Rápida

### Passo 1: Instalar dependências

**Windows (PowerShell):**
```powershell
.\run.ps1 install
```

**Linux/Mac (Make):**
```bash
make install
```

**Ou manualmente:**
```bash
pip install -r requirements.txt
```

### Passo 2: Configurar proxies (opcional)

Edite o arquivo `proxies.txt` e adicione seus proxies:

```
http://usuario:senha@host:porta
```

Seu proxy PyProxy já está configurado como exemplo!

### Passo 3: Fazer login no LinkedIn (uma vez)

**Windows (PowerShell):**
```powershell
.\run.ps1 session
```

**Linux/Mac (Make):**
```bash
make session
```

Isso irá:
1. Abrir o Chrome
2. Navegar para o LinkedIn
3. Você faz login manualmente
4. Sessão fica salva automaticamente

**⚠️ Execute este comando APENAS UMA VEZ!**

---

## 💻 Como Usar

### Opção 1: Usar Scripts (Recomendado)

**Windows (PowerShell):**
```powershell
# 1. Configurar sessão (apenas primeira vez)
.\run.ps1 session

# 2. Executar scraping
.\run.ps1 scrape

# 3. Ver todos os comandos
.\run.ps1 help
```

**Linux/Mac (Make):**
```bash
# 1. Configurar sessão (apenas primeira vez)
make session

# 2. Executar scraping
make scrape

# 3. Ver todos os comandos
make help
```

### Opção 2: Executar scripts Python diretamente

```bash
# Configurar sessão
python setup_linkedin_session.py

# Executar scraping
python linkedin_scraper.py
```

---

## ⚙️ Comandos Disponíveis

### Windows (PowerShell)

| Comando | Descrição |
|---------|-----------|
| `.\run.ps1 help` | Mostra ajuda com todos os comandos |
| `.\run.ps1 install` | Instala todas as dependências |
| `.\run.ps1 session` | **Abre Chrome para fazer login** (executar 1x) |
| `.\run.ps1 scrape` | **Executa scraping** com sessão salva |
| `.\run.ps1 test` | Testa se está tudo configurado |
| `.\run.ps1 list-proxies` | Lista proxies disponíveis |
| `.\run.ps1 clean` | Limpa arquivos temporários |

### Linux/Mac (Makefile)

| Comando | Descrição |
|---------|-----------|
| `make help` | Mostra ajuda com todos os comandos |
| `make install` | Instala todas as dependências |
| `make session` | **Abre Chrome para fazer login** (executar 1x) |
| `make scrape` | **Executa scraping** com sessão salva |
| `make test` | Testa se está tudo configurado |
| `make list-proxies` | Lista proxies disponíveis |
| `make clean` | Limpa arquivos temporários |

**Nota para Windows:** Se aparecer erro sobre execução de scripts, execute:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

---

## 📦 Módulos Disponíveis

### 1. ProxyManager (`selenium_linkedin.proxy_manager`)

Gerencia e rotaciona proxies automaticamente.

```python
from selenium_linkedin import ProxyManager, ProxyRotation

# Criar gerenciador
pm = ProxyManager(
    proxy_file="proxies.txt",
    rotation_mode=ProxyRotation.SEQUENTIAL
)

# Obter próximo proxy
proxy = pm.get_next_proxy()

# Listar proxies
pm.list_proxies()

# Validar proxy
if pm.validate_proxy(proxy):
    print("Proxy válido!")
```

**Modos de rotação:**
- `ProxyRotation.SEQUENTIAL` - Usa proxies em ordem
- `ProxyRotation.RANDOM` - Escolhe aleatoriamente
- `ProxyRotation.MANUAL` - Você escolhe manualmente

### 2. SessionManager (`selenium_linkedin.session_manager`)

Gerencia perfis do Chrome para manter sessões.

```python
from selenium_linkedin import SessionManager

# Criar gerenciador
sm = SessionManager(profile_name="linkedin")

# Obter caminho do perfil
profile_path = sm.get_profile_path()

# Verificar se existe
if sm.profile_exists():
    print("Sessão já configurada!")

# Deletar perfil (logout)
sm.delete_profile()
```

### 3. ChromeConfig (`selenium_linkedin.chrome_config`)

Configura o Chrome com todas as otimizações.

```python
from selenium_linkedin import ChromeConfig

# Criar configuração
config = ChromeConfig(
    headless=False,          # Modo visual
    profile_path="...",      # Caminho do perfil
    proxy={"http": "..."},   # Proxy
    disable_images=True      # Desabilitar imagens
)

# Criar driver
driver = config.create_driver()

# Usar driver
driver.get("https://linkedin.com")
```

---

## 🔄 Configuração de Proxies

### Formato do arquivo `proxies.txt`

```bash
# HTTP com autenticação (PyProxy)
http://usuario:senha@host:porta

# SOCKS5 com autenticação
socks5://usuario:senha@host:porta

# Proxy simples (sem autenticação)
host:porta

# HTTP sem autenticação
http://host:porta
```

### Seu proxy PyProxy já configurado:

```
http://usernovoaazx2-zone-resi-region-br:josesilva105@cd9bfed8d9466dc4.ika.na.pyproxy.io:16666
```

### Testar proxy:

```bash
make list-proxies
```

Ou manualmente:
```python
from selenium_linkedin import ProxyManager

pm = ProxyManager("proxies.txt")
proxy = pm.get_next_proxy()
pm.validate_proxy(proxy)
```

---

## 🎯 Exemplo de Uso Completo

```python
from selenium_linkedin import (
    ProxyManager, 
    ProxyRotation,
    SessionManager, 
    ChromeConfig
)

# 1. Configurar sessão
session = SessionManager(profile_name="linkedin")

# 2. Configurar proxy
proxy_manager = ProxyManager(
    proxy_file="proxies.txt",
    rotation_mode=ProxyRotation.SEQUENTIAL
)
proxy = proxy_manager.get_next_proxy()

# 3. Configurar Chrome
config = ChromeConfig(
    headless=False,
    profile_path=session.get_profile_path(),
    proxy=proxy
)

# 4. Criar driver e usar
driver = config.create_driver()

try:
    driver.get("https://www.linkedin.com/feed/")
    
    # Seu código de scraping aqui
    # ...
    
finally:
    driver.quit()
```

---

## ⚠️ Avisos Legais

### Importante sobre Scraping no LinkedIn:

1. **Termos de Serviço**: O LinkedIn proíbe scraping automatizado em seus Termos de Serviço
2. **Uso Responsável**: Use este código apenas para fins educacionais e de pesquisa
3. **Limitações**: Implemente delays adequados entre requisições
4. **API Oficial**: Sempre que possível, use a [API oficial do LinkedIn](https://developer.linkedin.com/)
5. **Riscos**: Scraping pode resultar em suspensão ou banimento da conta

### Boas Práticas:

- ✅ Use delays aleatórios entre ações (já implementado)
- ✅ Não faça scraping massivo (respeite o servidor)
- ✅ Use proxies rotativos para distribuir requisições
- ✅ Limite o número de páginas/perfis por sessão
- ✅ Implemente tratamento de erros adequado
- ❌ Não compartilhe dados scraped publicamente
- ❌ Não use para spam ou atividades maliciosas

---

## 🔧 Solução de Problemas

### "Sessão não encontrada"

Execute primeiro:

**Windows:**
```powershell
.\run.ps1 session
```

**Linux/Mac:**
```bash
make session
```

### "Nenhum proxy disponível"

Verifique se `proxies.txt` tem proxies válidos:

**Windows:**
```powershell
.\run.ps1 list-proxies
```

**Linux/Mac:**
```bash
make list-proxies
```

### "Termo 'make' não é reconhecido" (Windows)

Use o script PowerShell:
```powershell
.\run.ps1 help
```

### "Execução de scripts desabilitada" (Windows)

Execute no PowerShell como Administrador:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
Depois pressione `S` para confirmar.

### "ChromeDriver não encontrado"

O WebDriver Manager deve baixar automaticamente. Se der erro:
```bash
pip install --upgrade webdriver-manager
```

### Chrome não abre

Verifique se o Chrome está instalado e atualizado.

### Proxy não funciona

Teste manualmente:
```python
from selenium_linkedin import ProxyManager
pm = ProxyManager()
proxy = pm.get_next_proxy()
pm.validate_proxy(proxy)
```

### Erro SSL: "CERTIFICATE_VERIFY_FAILED" (Proxy com SSL)

Se você está atrás de um proxy corporativo e recebe erro de certificado SSL:

**Solução 1 - Variável de Ambiente (Recomendado):**

Windows PowerShell:
```powershell
$env:WDM_SSL_VERIFY='0'
.\run.ps1 session
```

Linux/Mac:
```bash
export WDM_SSL_VERIFY='0'
make session
```

**Solução 2 - Permanente no PowerShell:**

Adicione ao seu perfil PowerShell:
```powershell
[System.Environment]::SetEnvironmentVariable('WDM_SSL_VERIFY','0','User')
```

**Solução 3 - Download Manual do ChromeDriver:**

1. Baixe o ChromeDriver compatível com sua versão do Chrome:
   - https://googlechromelabs.github.io/chrome-for-testing/
2. Coloque o arquivo em uma pasta (ex: `C:\chromedriver\`)
3. Adicione ao PATH do sistema

**Nota:** O código já está configurado para desabilitar verificação SSL automaticamente quando necessário.

---

## 📚 Recursos Adicionais

- [Documentação Selenium](https://selenium-python.readthedocs.io/)
- [WebDriver Manager](https://github.com/SergeyPirogov/webdriver_manager)
- [PyProxy.io](https://pyproxy.io/) - Serviço de proxies usado

---

## 🎓 Próximos Passos

**Windows:**
1. ✅ Execute `.\run.ps1 test` para verificar configuração
2. ✅ Execute `.\run.ps1 session` para fazer login uma vez
3. ✅ Configure seus proxies em `proxies.txt`
4. ✅ Edite `linkedin_scraper.py` com suas automações
5. ✅ Execute `.\run.ps1 scrape` para testar
6. ✅ Adapte o código para suas necessidades

**Linux/Mac:**
1. ✅ Execute `make test` para verificar configuração
2. ✅ Execute `make session` para fazer login uma vez
3. ✅ Configure seus proxies em `proxies.txt`
4. ✅ Edite `linkedin_scraper.py` com suas automações
5. ✅ Execute `make scrape` para testar
6. ✅ Adapte o código para suas necessidades

---

## 📝 Notas Finais

- Sistema completamente modular e reutilizável
- Pronto para produção com boas práticas
- Suporta múltiplos proxies com rotação automática
- Sessões persistentes eliminam necessidade de login
- Anti-detecção implementado

---

**Desenvolvido para scraping profissional e eficiente! 🚀**

*Última atualização: Dezembro 2025*
