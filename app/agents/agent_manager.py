"""
Gerenciador de agentes para o sistema
"""

from crewai import Agent
from typing import Dict, List, Optional
import os


class AgentManager:
    """Classe para gerenciar agentes do sistema"""

    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        # Ferramentas disponíveis por tipo de agente (simplificado)
        self.agent_tools: Dict[str, List[str]] = {
            "researcher": ["web_search", "pdf_reader"],
            "analyst": ["statistical_analysis"],
            "writer": ["text_formatter"],
            "reviewer": ["norm_checker"],
            "coordinator": ["communication_hub"],
            "excel_analyst": ["read_excel", "compare_text"],
        }
        self.available_agents = {
            "researcher": {
                "name": "Pesquisador",
                "role": "Pesquisador especializado",
                "goal": "Realizar pesquisas detalhadas e coleta de informações",
                "backstory": "Especialista em pesquisa com vasta experiência em coleta e análise de dados",
            },
            "analyst": {
                "name": "Analista",
                "role": "Analista de dados",
                "goal": "Analisar dados e gerar insights valiosos",
                "backstory": "Analista experiente com forte background em análise quantitativa e qualitativa",
            },
            "writer": {
                "name": "Escritor",
                "role": "Escritor de conteúdo",
                "goal": "Criar conteúdo de alta qualidade baseado em pesquisas",
                "backstory": "Escritor profissional com experiência em diversos tipos de conteúdo",
            },
            "reviewer": {
                "name": "Revisor",
                "role": "Revisor de conteúdo",
                "goal": "Revisar e validar conteúdo para garantir qualidade",
                "backstory": "Revisor experiente com olho crítico para detalhes e qualidade",
            },
            "coordinator": {
                "name": "Coordenador",
                "role": "Coordenador de equipe",
                "goal": "Coordenar tarefas entre diferentes agentes",
                "backstory": "Coordenador experiente em gerenciamento de projetos e equipes",
            },
            "excel_analyst": {
                "name": "Analista de Excel",
                "role": "Especialista em planilhas",
                "goal": "Analisar dados de planilhas Excel",
                "backstory": "Profissional focado em manipulação e comparação de planilhas",
            },
        }

    def create_agent(
        self, agent_type: str, tools: Optional[list] = None, **kwargs
    ) -> Optional[Agent]:
        """Cria um novo agente do tipo especificado"""
        if agent_type not in self.available_agents:
            return None

        agent_config = self.available_agents[agent_type].copy()
        agent_config.update(kwargs)

        if tools is None:
            tools = self.agent_tools.get(agent_type, [])

        try:
            agent = Agent(
                role=agent_config["role"],
                goal=agent_config["goal"],
                backstory=agent_config["backstory"],
                tools=tools,
                verbose=True,
                allow_delegation=False,
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

    def get_agent_tools(self, agent_type: str) -> List[str]:
        """Retorna a lista de ferramentas disponíveis para o agente"""
        return self.agent_tools.get(agent_type, [])
