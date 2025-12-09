"""
Utilitários para consulta de dados (BigDataCorp API)
"""
import requests
import json
from typing import Dict, List, Optional
import csv
import os
from datetime import datetime
import sys


class DataEnricher:
    """
    Classe para enriquecer dados usando a API da BigDataCorp
    """
    
    def __init__(self, access_token: str = "ebe272fb-257f-475c-921c-266b8375eb69"):
        """
        Inicializa o enriquecedor
        
        Args:
            access_token: Token de acesso da API
        """
        self.access_token = access_token
        self.api_url = "https://bigboost.bigdatacorp.com.br/peoplev2"
        self.headers = {
            "Content-Type": "application/json"
        }
    
    def consult_person(self, name: str) -> Dict:
        """
        Consulta uma pessoa pelo nome na API
        
        Args:
            name: Nome completo da pessoa
            
        Returns:
            Dict com os dados encontrados (nome, emails, telefones)
        """
        try:
            print(f"[INFO] Consultando API para: {name}")
            
            payload = {
                "Datasets": "basic_data,emails_extended,phones_extended",
                "q": f"name{{{name}}}",
                "AccessToken": self.access_token
            }
            
            response = requests.post(
                self.api_url, 
                headers=self.headers, 
                json=payload,
                timeout=15
            )
            
            if response.status_code != 200:
                print(f"[ERRO] Erro na API: {response.status_code} - {response.text}")
                return self._empty_result(name)
            
            data = response.json()
            
            # Verificar se retornou resultados
            if "Result" not in data or not data["Result"]:
                print(f"[AVISO] Nenhum resultado encontrado para: {name}")
                return self._empty_result(name)
            
            # Pegar o primeiro resultado (melhor match)
            person = data["Result"][0]
            
            # Extrair dados básicos
            full_name = person.get("BasicData", {}).get("Name", name)
            tax_id = person.get("BasicData", {}).get("TaxIdNumber", "")
            
            # Extrair emails
            emails = []
            if "ExtendedEmails" in person:
                email_list = person.get("ExtendedEmails", {}).get("EmailAddresses", [])
                if isinstance(email_list, list):
                    emails = [e.get("Email", "") for e in email_list if "Email" in e]
                elif "Emails" in person.get("ExtendedEmails", {}):
                     emails = person.get("ExtendedEmails", {}).get("Emails", [])
            
            # Extrair telefones
            phones = []
            if "ExtendedPhones" in person:
                phone_list = person.get("ExtendedPhones", {}).get("Phones", [])
                if isinstance(phone_list, list):
                    for p in phone_list:
                        number = p.get("Number", "")
                        area = p.get("AreaCode", "")
                        if number and area:
                            phones.append(f"({area}) {number}")
                        elif number:
                            phones.append(number)
            
            result = {
                "searched_name": name,
                "found_name": full_name,
                "tax_id": tax_id,
                "emails": ", ".join(emails) if emails else "Não encontrado",
                "phones": ", ".join(phones) if phones else "Não encontrado",
                "match_score": person.get("InputNameMatchPercentage", 0)
            }
            
            print(f"[OK] Dados encontrados para {full_name}")
            return result
            
        except Exception as e:
            print(f"[ERRO] Erro ao consultar API: {e}")
            return self._empty_result(name)
    
    def _empty_result(self, name: str) -> Dict:
        """Retorna estrutura vazia em caso de erro"""
        return {
            "searched_name": name,
            "found_name": "ERRO/NÃO ENCONTRADO",
            "tax_id": "",
            "emails": "",
            "phones": "",
            "match_score": 0
        }
    
    def save_to_csv(self, data_list: List[Dict], filename: str = None):
        """
        Salva lista de dados em arquivo CSV
        
        Args:
            data_list: Lista de dicionários com dados
            filename: Nome do arquivo (opcional)
        """
        if not data_list:
            print("[AVISO] Sem dados para salvar")
            return
            
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dados_enriquecidos_{timestamp}.csv"
        
        # Garantir diretório de saída
        os.makedirs("output", exist_ok=True)
        filepath = os.path.join("output", filename)
        
        try:
            fieldnames = ["searched_name", "found_name", "tax_id", "emails", "phones", "match_score"]
            
            file_exists = os.path.isfile(filepath)
            
            with open(filepath, mode='a', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
                
                if not file_exists:
                    writer.writeheader()
                
                for data in data_list:
                    writer.writerow(data)
            
            print(f"[OK] Dados salvos em: {filepath}")
            
        except Exception as e:
            print(f"[ERRO] Erro ao salvar CSV: {e}")


# Função helper simples para uso direto
def enrich_and_save(names: List[str]):
    """
    Função principal para enriquecer lista de nomes e salvar
    """
    enricher = DataEnricher()
    results = []
    
    print(f"\n[INFO] Iniciando enriquecimento de {len(names)} nomes...")
    
    for name in names:
        if not name or len(name.strip()) < 3:
            continue
            
        data = enricher.consult_person(name)
        results.append(data)
        
        # Salvar incrementalmente para não perder dados
        enricher.save_to_csv([data])
        
    print("\n[OK] Processo finalizado!")
    return results


if __name__ == "__main__":
    # Verifica se foi passado argumento pela linha de comando
    if len(sys.argv) > 1:
        # Pega todos os argumentos a partir do índice 1 e junta como uma string
        nome_argumento = " ".join(sys.argv[1:])
        print(f"[INFO] Modo CLI iniciado para: {nome_argumento}")
        enrich_and_save([nome_argumento])
    else:
        print("Uso: python utils.py \"Nome da Pessoa\"")

