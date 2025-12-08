"""
Teste de Integração API BigDataCorp
"""
from utils import enrich_and_save

def teste_api():
    print("🧪 Iniciando teste da API BigDataCorp...")
    
    # Nomes para teste
    nomes = [
        "Guilherme Henrique Angelo Dias",
        "Maria Rodrigues"  # Do seu exemplo
    ]
    
    # Executar enriquecimento
    enrich_and_save(nomes)
    
    print("\n✅ Teste concluído! Verifique a pasta 'output/'")

if __name__ == "__main__":
    teste_api()

