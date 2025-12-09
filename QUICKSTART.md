# 🚀 Quick Start - LinkedIn Scraper

Guia rápido para começar em 5 minutos!

---

## ⚡ Instalação em 3 Passos

### 1️⃣ Instalar Dependências

```bash
make install
```

ou

```bash
pip install -r requirements.txt
```

### 2️⃣ Fazer Login no LinkedIn (Uma Vez)

```bash
make session
```

Isso irá:
- ✅ Abrir o Chrome
- ✅ Você faz login manualmente
- ✅ Sessão fica salva automaticamente

**Execute apenas UMA VEZ!**

### 3️⃣ Executar Scraping

```bash
make scrape
```

Pronto! O navegador abrirá já logado e com proxy ativo.

---

## 📝 Comandos Principais

| Comando | O que faz |
|---------|-----------|
| `make help` | Ver todos os comandos |
| `make session` | Configurar login (1x) |
| `make scrape` | Executar scraping |
| `make test` | Testar configuração |

---

## 🔧 Configuração de Proxy (Opcional)

Edite `proxies.txt`:

```
http://usuario:senha@host:porta
```

Seu proxy PyProxy já está configurado como exemplo!

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

```bash
python exemplo_uso.py
```

Menu com 6 exemplos diferentes!

---

## ❓ Problemas?

### "Sessão não encontrada"
```bash
make session
```

### "Nenhum proxy disponível"
Edite `proxies.txt` e adicione proxies

### Chrome não abre
Verifique se Chrome está instalado

### Ver ajuda completa
```bash
make help
```

---

## 📚 Documentação Completa

Veja `README.md` para documentação detalhada.

---

**Tudo pronto! Comece agora:** `make session` 🚀


