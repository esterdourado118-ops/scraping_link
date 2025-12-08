# 📋 Guia Rápido de Comandos

## 🪟 Windows (PowerShell)

### Comandos Principais

```powershell
# Ver ajuda
.\run.ps1 help

# Instalar dependências
.\run.ps1 install

# Configurar login no LinkedIn (executar 1 vez)
.\run.ps1 session

# Executar scraping
.\run.ps1 scrape

# Testar configuração
.\run.ps1 test

# Listar proxies
.\run.ps1 list-proxies

# Limpar cache
.\run.ps1 clean
```

### Fluxo de Uso

```powershell
# 1. Primeira vez - Instalar
.\run.ps1 install

# 2. Configurar login (apenas 1 vez)
.\run.ps1 session

# 3. Executar scraping (sempre que quiser)
.\run.ps1 scrape
```

---

## 🐧 Linux/Mac (Makefile)

### Comandos Principais

```bash
# Ver ajuda
make help

# Instalar dependências
make install

# Configurar login no LinkedIn (executar 1 vez)
make session

# Executar scraping
make scrape

# Testar configuração
make test

# Listar proxies
make list-proxies

# Limpar cache
make clean
```

### Fluxo de Uso

```bash
# 1. Primeira vez - Instalar
make install

# 2. Configurar login (apenas 1 vez)
make session

# 3. Executar scraping (sempre que quiser)
make scrape
```

---

## 🐍 Python Direto (Todas as plataformas)

### Comandos Principais

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar login (executar 1 vez)
python setup_linkedin_session.py

# Executar scraping
python linkedin_scraper.py

# Exemplos interativos
python exemplo_uso.py
```

---

## ⚠️ Problemas Comuns

### Windows: "make não é reconhecido"

**Solução:** Use `.\run.ps1` em vez de `make`

```powershell
.\run.ps1 help
```

### Windows: "Execução de scripts desabilitada"

**Solução:** Execute no PowerShell como Administrador:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Depois pressione `S` para confirmar.

### "Sessão não encontrada"

**Solução:** Configure o login primeiro:

```powershell
# Windows
.\run.ps1 session

# Linux/Mac
make session
```

### "Nenhum proxy disponível"

**Solução:** Edite o arquivo `proxies.txt` e adicione proxies:

```
http://usuario:senha@host:porta
```

---

## 📂 Estrutura de Arquivos

```
pegaemailLINKEDIN/
├── run.ps1                      # ⚙️ Script PowerShell (Windows)
├── Makefile                     # ⚙️ Makefile (Linux/Mac)
├── setup_linkedin_session.py   # 🔧 Configurar login
├── linkedin_scraper.py          # 🤖 Executar scraping
├── exemplo_uso.py               # 📚 Exemplos
├── proxies.txt                  # 🌐 Lista de proxies
└── selenium_linkedin/           # 📦 Módulos
    ├── proxy_manager.py
    ├── session_manager.py
    └── chrome_config.py
```

---

## 🎯 Próximos Passos

1. **Instalar dependências**
2. **Configurar login no LinkedIn** (`session`)
3. **Executar scraping** (`scrape`)
4. **Personalizar** `linkedin_scraper.py`

---

**Documentação completa:** [README.md](README.md)

**Guia Windows:** [QUICKSTART_WINDOWS.md](QUICKSTART_WINDOWS.md)

**Guia Rápido:** [QUICKSTART.md](QUICKSTART.md)

