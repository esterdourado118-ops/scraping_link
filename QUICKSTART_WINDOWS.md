# 🚀 Quick Start - LinkedIn Scraper (Windows)

Guia rápido para Windows PowerShell!

---

## ⚡ Instalação em 3 Passos

### 1️⃣ Instalar Dependências

```powershell
.\run.ps1 install
```

ou

```powershell
pip install -r requirements.txt
```

### 2️⃣ Fazer Login no LinkedIn (Uma Vez)

```powershell
.\run.ps1 session
```

Isso irá:
- ✅ Abrir o Chrome
- ✅ Você faz login manualmente
- ✅ Sessão fica salva automaticamente
- ✅ **Proxy com autenticação configurado automaticamente!**

**Execute apenas UMA VEZ!**

### 3️⃣ Executar Scraping

```powershell
.\run.ps1 scrape
```

Pronto! O navegador abrirá já logado e com proxy ativo.

---

## 📝 Comandos Principais (PowerShell)

| Comando | O que faz |
|---------|-----------|
| `.\run.ps1 help` | Ver todos os comandos |
| `.\run.ps1 install` | Instalar dependências |
| `.\run.ps1 session` | Configurar login (1x) |
| `.\run.ps1 scrape` | Executar scraping |
| `.\run.ps1 test` | Testar configuração |
| `.\run.ps1 list-proxies` | Listar proxies |
| `.\run.ps1 clean` | Limpar cache |

---

## 🔐 Configuração de Proxy com Autenticação

**Seu proxy PyProxy já está configurado!**

O sistema detecta **automaticamente** proxies com autenticação e cria uma extensão do Chrome para fazer login.

**Formato no `proxies.txt`:**
```
http://usuario:senha@host:porta
```

**Exemplo (PyProxy):**
```
http://usernovoaazx2-zone-resi-region-br:josesilva105@cd9bfed8d9466dc4.ika.na.pyproxy.io:16666
```

**Você NÃO precisa:**
- ❌ Instalar extensões manualmente
- ❌ Configurar proxy no Chrome
- ❌ Digitar usuário e senha

**O sistema faz tudo automaticamente!** ✅

---

## 🚨 Problemas Comuns

### ⚠️ Erro SSL: "CERTIFICATE_VERIFY_FAILED"

Se você está atrás de um proxy corporativo:

**Solução Rápida:**
```powershell
.\fix_ssl.ps1
```

**Ou manualmente:**
```powershell
$env:WDM_SSL_VERIFY='0'
.\run.ps1 session
```

### ⚠️ "Execução de scripts desabilitada"

Execute como Administrador:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Depois pressione `S` para confirmar.

### ⚠️ "Sessão não encontrada"
```powershell
.\run.ps1 session
```

### ⚠️ "Nenhum proxy disponível"
Edite `proxies.txt` e adicione proxies

### ⚠️ Chrome não abre
Verifique se Chrome está instalado

### ⚠️ Ver ajuda completa
```powershell
.\run.ps1 help
```

Ou veja: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 💡 Personalizar Scraping

Edite o arquivo `linkedin_scraper.py`:

```python
def main():
    scraper = LinkedInScraper(
        headless=False,  # True = sem janela
        use_proxy=True   # True = usar proxy
    )
    
    scraper.start()
    
    # SEU CÓDIGO AQUI:
    scraper.search_people("Python Developer")
    # ...
    
    scraper.stop()
```

---

## 🎯 Exemplos Prontos

Execute exemplos interativos:

```powershell
python exemplo_uso.py
```

Menu com 6 exemplos diferentes!

---

## 🎯 Alternativa: Executar Diretamente

Se preferir não usar `run.ps1`:

```powershell
# Instalar
pip install -r requirements.txt

# Configurar sessão
python setup_linkedin_session.py

# Executar scraping
python linkedin_scraper.py

# Testar
python -c "from selenium_linkedin import ProxyManager; print('OK')"
```

---

## 📚 Documentação Completa

- [README.md](README.md) - Documentação completa
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Solução de problemas
- [exemplo_uso.py](exemplo_uso.py) - Exemplos de código

---

## 🎓 Fluxo Completo Recomendado

```powershell
# 1. Testar configuração
.\run.ps1 test

# 2. Fazer login (apenas 1x)
.\run.ps1 session

# 3. Executar scraping
.\run.ps1 scrape

# 4. Ver proxies disponíveis
.\run.ps1 list-proxies
```

---

**Tudo pronto! Comece agora:** 

```powershell
.\run.ps1 session
```

Depois:

```powershell
.\run.ps1 scrape
```

🚀

---

## 🔑 Dica: Proxy com Autenticação

O sistema **detecta automaticamente** quando seu proxy tem usuário e senha e configura tudo para você!

Apenas coloque no `proxies.txt`:
```
http://usuario:senha@host:porta
```

**Pronto!** Não precisa fazer mais nada. 🎉
