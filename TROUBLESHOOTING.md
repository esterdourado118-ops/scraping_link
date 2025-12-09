# 🔧 Guia de Solução de Problemas

Soluções para problemas comuns ao usar o LinkedIn Scraper.

---

## 🚨 Erro: SSL CERTIFICATE_VERIFY_FAILED

### Sintoma:
```
urllib3.exceptions.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] 
certificate verify failed: self-signed certificate in certificate chain
```

### Causa:
Você está atrás de um proxy corporativo ou firewall que usa certificados SSL auto-assinados.

### Solução Rápida (Windows):

Execute o script de correção:
```powershell
.\fix_ssl.ps1
```

### Solução Manual:

**Windows PowerShell:**
```powershell
# Temporário (apenas para sessão atual)
$env:WDM_SSL_VERIFY='0'
.\run.ps1 session

# Permanente
[System.Environment]::SetEnvironmentVariable('WDM_SSL_VERIFY','0','User')
```

**Linux/Mac:**
```bash
# Temporário
export WDM_SSL_VERIFY='0'
make session

# Permanente (adicione ao ~/.bashrc ou ~/.zshrc)
echo "export WDM_SSL_VERIFY='0'" >> ~/.bashrc
source ~/.bashrc
```

---

## 📁 Sessão não encontrada

### Sintoma:
```
❌ ERRO: Sessão não encontrada!
👉 Execute primeiro: python setup_linkedin_session.py
```

### Solução:

**Windows:**
```powershell
.\run.ps1 session
```

**Linux/Mac:**
```bash
make session
```

Faça login manualmente no navegador que abrir e pressione ENTER no terminal.

---

## 🌐 Nenhum proxy disponível

### Sintoma:
```
❌ Nenhum proxy disponível!
```

### Solução:

1. Verifique se `proxies.txt` existe
2. Adicione pelo menos um proxy válido:

```
http://usuario:senha@host:porta
```

3. Liste proxies disponíveis:

**Windows:**
```powershell
.\run.ps1 list-proxies
```

**Linux/Mac:**
```bash
make list-proxies
```

---

## 🚫 Execução de scripts desabilitada (Windows)

### Sintoma:
```
cannot be loaded because running scripts is disabled on this system
```

### Solução:

Execute como Administrador:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Confirme com `S`.

---

## 🌐 ChromeDriver não encontrado

### Sintoma:
```
chromedriver not found
Message: 'chromedriver' executable needs to be in PATH
```

### Solução 1 - Atualizar WebDriver Manager:
```bash
pip install --upgrade webdriver-manager
```

### Solução 2 - Download Manual:

1. Verifique sua versão do Chrome:
   - Abra Chrome → `chrome://version`
   - Anote a versão (ex: 120.0.6099.109)

2. Baixe o ChromeDriver compatível:
   - https://googlechromelabs.github.io/chrome-for-testing/

3. Extraia e adicione ao PATH do sistema

**Windows:**
```
C:\chromedriver\chromedriver.exe
```

**Linux/Mac:**
```bash
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
```

---

## 🔴 Chrome não abre

### Verificações:

1. **Chrome instalado?**
   ```
   Baixe: https://www.google.com/chrome/
   ```

2. **Chrome atualizado?**
   - Abra Chrome → Menu → Ajuda → Sobre o Google Chrome
   - Deixe atualizar se necessário

3. **Portas disponíveis?**
   - O Chrome precisa se comunicar em portas locais
   - Verifique se não há firewall bloqueando

---

## 🔐 Proxy pedindo usuário e senha

### Sintoma:
O Chrome abre uma janela pedindo usuário e senha do proxy, mesmo tendo configurado em `proxies.txt`.

### Causa:
O Chrome não aceita autenticação de proxy via argumento `--proxy-server`. É necessário usar uma **extensão do Chrome**.

### Solução:
**O sistema já está configurado para fazer isso automaticamente!**

Quando você coloca um proxy com autenticação no `proxies.txt`:
```
http://usuario:senha@host:porta
```

O sistema detecta automaticamente e cria uma extensão temporária do Chrome que faz a autenticação.

### Verifique:

1. **Formato correto no `proxies.txt`:**
```
http://usernovoaazx2-zone-resi-region-br:josesilva105@cd9bfed8d9466dc4.ika.na.pyproxy.io:16666
```

2. **Não deve ter espaços ou quebras de linha no meio da URL**

3. **Teste se o proxy funciona:**
```powershell
python -c "import requests; r = requests.get('http://ipinfo.io/json', proxies={'http': 'http://usuario:senha@host:porta'}); print(r.json())"
```

### O que acontece automaticamente:

Quando você executa:
```powershell
.\run.ps1 session
```

O sistema:
1. ✅ Detecta que o proxy tem autenticação (`@` na URL)
2. ✅ Cria uma extensão do Chrome automaticamente
3. ✅ Configura o proxy na extensão
4. ✅ Remove a extensão após uso

**Você NÃO precisa fazer nada manualmente!**

---

## 🔄 Proxy não funciona

### Teste o proxy:

**Windows:**
```powershell
python -c "import requests; r = requests.get('http://ipinfo.io/json', proxies={'http': 'http://usuario:senha@host:porta'}); print(r.json())"
```

**Linux/Mac:**
```bash
curl -x http://usuario:senha@host:porta http://ipinfo.io/json
```

### Formato correto do proxy:

```
# Com autenticação
http://usuario:senha@host:porta
socks5://usuario:senha@host:porta

# Sem autenticação
http://host:porta
host:porta
```

### Validar proxy no Python:

```python
from selenium_linkedin import ProxyManager

pm = ProxyManager("proxies.txt")
proxy = pm.get_next_proxy()

if pm.validate_proxy(proxy):
    print("✅ Proxy funcionando!")
else:
    print("❌ Proxy com problema")
```

---

## 🐍 Python não encontrado

### Windows:

1. Baixe Python: https://www.python.org/downloads/
2. Durante instalação, marque "Add Python to PATH"
3. Reinicie o terminal

Verificar:
```powershell
python --version
```

### Linux/Mac:

```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip

# Mac
brew install python3
```

---

## 📦 Módulos não encontrados

### Sintoma:
```
ModuleNotFoundError: No module named 'selenium'
```

### Solução:

**Windows:**
```powershell
.\run.ps1 install
```

**Linux/Mac:**
```bash
make install
```

**Ou manualmente:**
```bash
pip install -r requirements.txt
```

---

## 🔒 LinkedIn bloqueia/detecta bot

### Prevenção:

1. **Use delays maiores:**
   ```python
   scraper.random_delay(3, 6)  # 3-6 segundos
   ```

2. **Não faça scraping massivo:**
   - Limite requisições por hora
   - Faça pausas longas entre execuções

3. **Use proxies rotativos:**
   - Adicione múltiplos proxies em `proxies.txt`
   - Sistema roda automaticamente

4. **Ative modo headless:**
   ```python
   scraper = LinkedInScraper(headless=True)
   ```

5. **Respeite rate limits:**
   - Máximo 10-20 perfis por sessão
   - Pause 1 hora entre execuções

---

## 🗑️ Resetar tudo e começar de novo

**Windows:**
```powershell
# Limpar arquivos temporários
.\run.ps1 clean

# Deletar sessão salva
Remove-Item -Recurse -Force chrome_profiles

# Reinstalar
.\run.ps1 install

# Reconfigurar sessão
.\run.ps1 session
```

**Linux/Mac:**
```bash
# Limpar
make clean

# Deletar sessão
rm -rf chrome_profiles

# Reinstalar
make install

# Reconfigurar
make session
```

---

## 💬 Ainda com problemas?

1. Execute o teste de configuração:

**Windows:**
```powershell
.\run.ps1 test
```

**Linux/Mac:**
```bash
make test
```

2. Verifique os logs de erro completos

3. Verifique se está usando proxy corporativo

4. Teste sem proxy primeiro (comente linhas em `proxies.txt`)

---

## 📋 Checklist de Diagnóstico

- [ ] Python 3.8+ instalado
- [ ] Chrome instalado e atualizado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Sessão configurada (`.\run.ps1 session`)
- [ ] Proxies configurados (se necessário)
- [ ] Variável WDM_SSL_VERIFY=0 (se em proxy corporativo)
- [ ] Firewall não está bloqueando Python/Chrome
- [ ] Antivírus não está bloqueando Selenium

---

**Se o problema persistir, revise os logs de erro e verifique as mensagens específicas.** 🔍

