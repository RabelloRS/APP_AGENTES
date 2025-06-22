"""
Gerenciador de crews para o sistema
"""

from crewai import Crew, Task
from typing import Dict, List, Optional
from app.agents.agent_manager import AgentManager

class CrewManager:
    """Classe para gerenciar crews do sistema"""
    
    def __init__(self, agent_manager: AgentManager):
        self.agent_manager = agent_manager
        self.crews: Dict[str, Crew] = {}
        self.crew_configs: Dict[str, Dict] = {}
    
    def create_crew(self, name: str, agent_types: List[str], description: str = "") -> Optional[Crew]:
        """Cria uma nova crew com os agentes especificados"""
        try:
            # Criar agentes se não existirem
            agents = []
            for agent_type in agent_types:
                agent = self.agent_manager.get_agent(agent_type)
                if not agent:
                    agent = self.agent_manager.create_agent(agent_type)
                if agent:
                    agents.append(agent)
            
            if not agents:
                print("Nenhum agente válido foi criado")
                return None
            
            # Criar crew
            crew = Crew(
                agents=agents,
                tasks=[],  # Tarefas serão adicionadas posteriormente
                verbose=True,
                memory=True
            )
            
            self.crews[name] = crew
            self.crew_configs[name] = {
                "description": description,
                "agent_types": agent_types,
                "created_at": "2024-01-01"  # Em produção, usar datetime.now()
            }
            
            return crew
            
        except Exception as e:
            print(f"Erro ao criar crew {name}: {e}")
            return None
    
    def get_crew(self, name: str) -> Optional[Crew]:
        """Retorna uma crew existente"""
        return self.crews.get(name)
    
    def get_all_crews(self) -> Dict[str, Crew]:
        """Retorna todas as crews criadas"""
        return self.crews
    
    def get_crew_info(self, name: str) -> Optional[Dict]:
        """Retorna informações sobre uma crew"""
        return self.crew_configs.get(name)
    
    def execute_crew_task(self, crew_name: str, task_description: str) -> Optional[str]:
        """Executa uma tarefa usando uma crew específica"""
        crew = self.get_crew(crew_name)
        if not crew:
            print(f"Crew {crew_name} não encontrada")
            return None
        
        try:
            # Criar tarefa
            task = Task(
                description=task_description,
                expected_output="Resultado da execução da tarefa",
                agent=crew.agents[0] if crew.agents else None
            )
            
            # Executar crew
            result = crew.kickoff()
            return str(result)
            
        except Exception as e:
            print(f"Erro ao executar tarefa na crew {crew_name}: {e}")
            return None
    
    def delete_crew(self, name: str) -> bool:
        """Remove uma crew"""
        if name in self.crews:
            del self.crews[name]
            del self.crew_configs[name]
            return True
        return False
    
    def list_crew_names(self) -> List[str]:
        """Lista todos os nomes de crews"""
        return list(self.crews.keys()) 