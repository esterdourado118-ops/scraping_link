"""
Gerenciador de Sessões Persistentes do Chrome
==============================================

Gerencia perfis do Chrome para manter sessões (login, cookies, etc)
"""

import os
from pathlib import Path
from typing import Optional


class SessionManager:
    """
    Gerenciador de sessões persistentes usando perfis do Chrome
    """
    
    def __init__(self, profile_name: str = "default"):
        """
        Inicializa o gerenciador de sessões
        
        Args:
            profile_name: Nome do perfil (ex: "linkedin", "default")
        """
        self.profile_name = profile_name
        self.profiles_dir = Path("chrome_profiles")
        self.profile_path = self.profiles_dir / profile_name
        
        # Criar diretório de perfis se não existir
        self._ensure_profiles_directory()
    
    def _ensure_profiles_directory(self):
        """Garante que o diretório de perfis existe"""
        if not self.profiles_dir.exists():
            self.profiles_dir.mkdir(parents=True)
            print(f"📁 Diretório de perfis criado: {self.profiles_dir.absolute()}")
    
    def get_profile_path(self) -> str:
        """
        Obtém o caminho absoluto do perfil
        
        Returns:
            String com caminho absoluto do perfil
        """
        # Criar diretório do perfil se não existir
        if not self.profile_path.exists():
            self.profile_path.mkdir(parents=True)
            print(f"📁 Novo perfil criado: {self.profile_name}")
        else:
            print(f"✅ Usando perfil existente: {self.profile_name}")
        
        return str(self.profile_path.absolute())
    
    def profile_exists(self) -> bool:
        """
        Verifica se o perfil já existe
        
        Returns:
            True se perfil existe, False caso contrário
        """
        return self.profile_path.exists() and len(list(self.profile_path.iterdir())) > 0
    
    def delete_profile(self):
        """Deleta o perfil atual (logout)"""
        if self.profile_path.exists():
            import shutil
            shutil.rmtree(self.profile_path)
            print(f"🗑️ Perfil '{self.profile_name}' deletado")
        else:
            print(f"⚠️ Perfil '{self.profile_name}' não existe")
    
    def list_profiles(self):
        """Lista todos os perfis existentes"""
        if not self.profiles_dir.exists():
            print("📁 Nenhum perfil criado ainda")
            return
        
        profiles = [p.name for p in self.profiles_dir.iterdir() if p.is_dir()]
        
        if not profiles:
            print("📁 Nenhum perfil criado ainda")
        else:
            print(f"\n📋 Perfis disponíveis ({len(profiles)}):")
            print("="*60)
            for profile in profiles:
                marker = "👉" if profile == self.profile_name else "  "
                print(f"{marker} {profile}")
            print("="*60 + "\n")
    
    def get_info(self) -> dict:
        """
        Obtém informações sobre o perfil atual
        
        Returns:
            Dict com informações do perfil
        """
        return {
            'profile_name': self.profile_name,
            'profile_path': str(self.profile_path.absolute()),
            'exists': self.profile_exists(),
            'profiles_dir': str(self.profiles_dir.absolute())
        }


