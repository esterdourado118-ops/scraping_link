"""
Gerenciador de Proxies com Rotação
===================================

Suporta:
- HTTP/HTTPS proxies
- SOCKS5 proxies
- Proxies com autenticação (usuário:senha)
- Rotação sequencial e aleatória
- Validação de proxies
"""

import random
import json
import os
from pathlib import Path
from enum import Enum
from typing import List, Optional, Dict
import requests


class ProxyRotation(Enum):
    """Tipos de rotação de proxy"""
    SEQUENTIAL = "sequential"  # Usa proxies em ordem
    RANDOM = "random"          # Escolhe aleatoriamente
    MANUAL = "manual"          # Usuário escolhe manualmente


class ProxyManager:
    """
    Gerenciador de proxies com suporte a rotação e validação
    """
    
    def __init__(
        self,
        proxy_file: str = "proxies.txt",
        rotation_mode: ProxyRotation = ProxyRotation.SEQUENTIAL,
        state_file: str = "proxy_state.json"
    ):
        """
        Inicializa o gerenciador de proxies
        
        Args:
            proxy_file: Arquivo com lista de proxies
            rotation_mode: Modo de rotação (SEQUENTIAL, RANDOM, MANUAL)
            state_file: Arquivo para salvar estado (último proxy usado)
        """
        self.proxy_file = proxy_file
        self.rotation_mode = rotation_mode
        self.state_file = state_file
        self.proxies: List[Dict[str, str]] = []
        self.current_index = 0
        
        # Carregar proxies do arquivo
        self._load_proxies()
        
        # Carregar estado anterior (se existir)
        self._load_state()
    
    def _load_proxies(self):
        """Carrega proxies do arquivo"""
        if not os.path.exists(self.proxy_file):
            print(f"⚠️ Arquivo {self.proxy_file} não encontrado. Criando arquivo vazio...")
            Path(self.proxy_file).touch()
            return
        
        with open(self.proxy_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            
            # Ignorar linhas vazias e comentários
            if not line or line.startswith('#'):
                continue
            
            # Parsear proxy
            proxy_dict = self._parse_proxy(line)
            if proxy_dict:
                self.proxies.append(proxy_dict)
        
        print(f"✅ {len(self.proxies)} proxies carregados de {self.proxy_file}")
    
    def _parse_proxy(self, proxy_str: str) -> Optional[Dict[str, str]]:
        """
        Parseia string de proxy em diferentes formatos
        
        Formatos suportados:
        - http://user:pass@host:port
        - socks5://user:pass@host:port
        - host:port
        - http://host:port
        
        Returns:
            Dict com 'http' e 'https' ou None se inválido
        """
        try:
            proxy_str = proxy_str.strip()
            
            # Formato: tipo://user:pass@host:port
            if '://' in proxy_str:
                # Já está no formato correto
                if proxy_str.startswith('socks5://'):
                    return {
                        'http': proxy_str,
                        'https': proxy_str,
                        'type': 'socks5'
                    }
                else:
                    return {
                        'http': proxy_str,
                        'https': proxy_str,
                        'type': 'http'
                    }
            
            # Formato: host:port (sem protocolo)
            else:
                return {
                    'http': f'http://{proxy_str}',
                    'https': f'http://{proxy_str}',
                    'type': 'http'
                }
        
        except Exception as e:
            print(f"⚠️ Erro ao parsear proxy '{proxy_str}': {e}")
            return None
    
    def _load_state(self):
        """Carrega estado anterior (último proxy usado)"""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                    self.current_index = state.get('current_index', 0)
                    
                    # Garantir que o índice está dentro do range
                    if self.current_index >= len(self.proxies):
                        self.current_index = 0
                    
                    print(f"📍 Estado anterior carregado: índice {self.current_index}")
            except Exception as e:
                print(f"⚠️ Erro ao carregar estado: {e}")
    
    def _save_state(self):
        """Salva estado atual (último proxy usado)"""
        try:
            with open(self.state_file, 'w') as f:
                json.dump({'current_index': self.current_index}, f)
        except Exception as e:
            print(f"⚠️ Erro ao salvar estado: {e}")
    
    def get_next_proxy(self) -> Optional[Dict[str, str]]:
        """
        Obtém próximo proxy de acordo com o modo de rotação
        
        Returns:
            Dict com proxy ou None se não houver proxies
        """
        if not self.proxies:
            print("❌ Nenhum proxy disponível!")
            return None
        
        if self.rotation_mode == ProxyRotation.SEQUENTIAL:
            proxy = self.proxies[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.proxies)
            
        elif self.rotation_mode == ProxyRotation.RANDOM:
            proxy = random.choice(self.proxies)
            
        else:  # MANUAL
            proxy = self.proxies[self.current_index]
        
        # Salvar estado
        self._save_state()
        
        # Mostrar qual proxy está sendo usado (sem senha)
        proxy_display = self._get_proxy_display(proxy)
        print(f"🔄 Usando proxy: {proxy_display}")
        
        return proxy
    
    def _get_proxy_display(self, proxy: Dict[str, str]) -> str:
        """Obtém string de proxy para exibição (sem senha)"""
        proxy_str = proxy.get('http', '')
        
        # Remover senha da exibição
        if '@' in proxy_str:
            try:
                protocol = proxy_str.split('://')[0]
                rest = proxy_str.split('://')[1]
                
                if '@' in rest:
                    auth, host = rest.split('@', 1)
                    if ':' in auth:
                        user = auth.split(':')[0]
                        return f"{protocol}://{user}:***@{host}"
            except:
                pass
        
        return proxy_str
    
    def get_proxy_by_index(self, index: int) -> Optional[Dict[str, str]]:
        """
        Obtém proxy por índice específico
        
        Args:
            index: Índice do proxy (0-based)
        
        Returns:
            Dict com proxy ou None se índice inválido
        """
        if 0 <= index < len(self.proxies):
            self.current_index = index
            self._save_state()
            return self.proxies[index]
        else:
            print(f"❌ Índice {index} inválido! Total de proxies: {len(self.proxies)}")
            return None
    
    def validate_proxy(self, proxy: Dict[str, str], timeout: int = 10) -> bool:
        """
        Valida se um proxy está funcionando
        
        Args:
            proxy: Dict com proxy
            timeout: Tempo máximo de espera em segundos
        
        Returns:
            True se proxy funciona, False caso contrário
        """
        try:
            print(f"🔍 Validando proxy...")
            response = requests.get(
                'http://ipinfo.io/json',
                proxies=proxy,
                timeout=timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                ip = data.get('ip', 'desconhecido')
                country = data.get('country', '?')
                city = data.get('city', '?')
                print(f"✅ Proxy válido! IP: {ip} | Local: {city}, {country}")
                return True
            else:
                print(f"❌ Proxy retornou status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Proxy inválido: {e}")
            return False
    
    def list_proxies(self):
        """Lista todos os proxies disponíveis"""
        if not self.proxies:
            print("❌ Nenhum proxy disponível!")
            return
        
        print(f"\n📋 Proxies disponíveis ({len(self.proxies)}):")
        print("="*60)
        
        for i, proxy in enumerate(self.proxies):
            proxy_display = self._get_proxy_display(proxy)
            marker = "👉" if i == self.current_index else "  "
            print(f"{marker} [{i}] {proxy_display}")
        
        print("="*60)
        print(f"Modo de rotação: {self.rotation_mode.value}")
        print(f"Próximo índice: {self.current_index}\n")
    
    def get_proxy_for_selenium(self, proxy: Dict[str, str]) -> str:
        """
        Converte proxy dict para formato do Selenium
        
        Args:
            proxy: Dict com proxy
        
        Returns:
            String no formato adequado para Selenium
        """
        return proxy.get('http', '')
    
    def reset_rotation(self):
        """Reseta a rotação para o início"""
        self.current_index = 0
        self._save_state()
        print("🔄 Rotação resetada para o início")
    
    def get_stats(self) -> Dict:
        """
        Retorna estatísticas sobre os proxies
        
        Returns:
            Dict com estatísticas
        """
        return {
            'total_proxies': len(self.proxies),
            'current_index': self.current_index,
            'rotation_mode': self.rotation_mode.value,
            'has_proxies': len(self.proxies) > 0
        }


