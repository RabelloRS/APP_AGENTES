"""
Gerenciador de agentes para o sistema
"""

from crewai import Agent
from typing import Dict, List, Optional
import yaml
import os

class AgentManager:
    """Classe para gerenciar agentes do sistema usando arquivos YAML"""
    
    def __init__(self, config_path: str = "app/config/agents.yaml"):
        self.config_path = config_path
        self.agents: Dict[str, Agent] = {}
        self.available_agents = self._load_agent_configs()
    
    def _load_agent_configs(self) -> Dict:
        """Carrega as configurações dos agentes do arquivo YAML"""
        try:
            if not os.path.exists(self.config_path):
                print(f"Arquivo de configuração não encontrado: {self.config_path}")
                return {}
            
            with open(self.config_path, 'r', encoding='utf-8') as file:
                configs = yaml.safe_load(file)
                return configs or {}
                
        except Exception as e:
            print(f"Erro ao carregar configurações dos agentes: {e}")
            return {}
    
    def reload_configs(self) -> bool:
        """Recarrega as configurações dos agentes do arquivo YAML"""
        try:
            self.available_agents = self._load_agent_configs()
            return True
        except Exception as e:
            print(f"Erro ao recarregar configurações: {e}")
            return False
    
    def create_agent(self, agent_type: str, tools: Optional[list] = None, **kwargs) -> Optional[Agent]:
        """Cria um novo agente do tipo especificado"""
        if agent_type not in self.available_agents:
            print(f"Tipo de agente '{agent_type}' não encontrado nas configurações")
            return None
        
        agent_config = self.available_agents[agent_type].copy()
        
        # Sobrescrever configurações padrão com kwargs
        agent_config.update(kwargs)
        
        # Usar tools fornecidos ou da configuração
        if tools is not None:
            agent_config["tools"] = tools
        
        try:
            agent = Agent(
                role=agent_config["role"],
                goal=agent_config["goal"],
                backstory=agent_config["backstory"],
                tools=agent_config.get("tools", []),
                verbose=agent_config.get("verbose", True),
                allow_delegation=agent_config.get("allow_delegation", False)
            )
            
            self.agents[agent_type] = agent
            return agent
            
        except Exception as e:
            print(f"Erro ao criar agente {agent_type}: {e}")
            return None
    
    def get_agent(self, agent_type: str) -> Optional[Agent]:
        """Retorna um agente existente"""
        return self.agents.get(agent_type)
    
    def get_all_agents(self) -> Dict[str, Agent]:
        """Retorna todos os agentes criados"""
        return self.agents
    
    def list_available_agent_types(self) -> List[str]:
        """Lista todos os tipos de agentes disponíveis"""
        return list(self.available_agents.keys())
    
    def get_agent_info(self, agent_type: str) -> Optional[Dict]:
        """Retorna informações sobre um tipo de agente"""
        return self.available_agents.get(agent_type)
    
    def get_agent_configs(self) -> Dict:
        """Retorna todas as configurações de agentes"""
        return self.available_agents.copy() 