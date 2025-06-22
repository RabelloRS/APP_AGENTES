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
        self.crew_templates: Dict[str, Dict] = {
            "Projeto Padr\u00e3o": {
                "description": "Equipe b\u00e1sica para projetos gerais",
                "agent_types": ["researcher", "analyst", "writer"],
                "workflow": None,
            },
            "An\u00e1lise de Planilhas": {
                "description": "Workflow para compara\u00e7\u00e3o de planilhas",
                "agent_types": ["excel_analyst"],
                "workflow": "planilhas",
            },
        }

        self.workflows: Dict[str, List[str]] = {
            "planilhas": [
                "Ler planilhas",
                "Comparar colunas",
                "Gerar relat\u00f3rio",
            ]
        }

    def create_crew(
        self,
        name: str,
        agent_types: List[str],
        description: str = "",
        workflow: str | None = None,
    ) -> Optional[Crew]:
        """Cria uma nova crew com os agentes especificados"""
        try:
            if workflow and workflow not in self.workflows:
                print(f"Workflow {workflow} não encontrado")
                workflow = None
            # Criar agentes se não existirem
            agents = []
            for agent_type in agent_types:
                agent = self.agent_manager.get_agent(agent_type)
                if not agent:
                    agent = self.agent_manager.create_agent(agent_type)
                if agent:
                    # Validar se o agente possui ferramentas
                    tools = self.agent_manager.get_agent_tools(agent_type)
                    if not tools:
                        print(f"Agente {agent_type} sem ferramentas")
                        continue
                    agents.append(agent)

            if not agents:
                print("Nenhum agente válido foi criado")
                return None

            # Criar crew
            crew = Crew(
                agents=agents,
                tasks=[],  # Tarefas serão adicionadas posteriormente
                verbose=True,
                memory=True,
            )

            self.crews[name] = crew
            self.crew_configs[name] = {
                "description": description,
                "agent_types": agent_types,
                "created_at": "2024-01-01",  # Em produção, usar datetime.now()
                "workflow": workflow,
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
                agent=crew.agents[0] if crew.agents else None,
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

    def list_templates(self) -> List[str]:
        """Retorna os nomes dos templates disponíveis"""
        return list(self.crew_templates.keys())

    def get_template(self, name: str) -> Optional[Dict]:
        """Obtém um template de crew"""
        return self.crew_templates.get(name)

    def execute_workflow(self, crew_name: str) -> List[str]:
        """Executa o workflow associado a uma crew e retorna saídas"""
        crew_info = self.get_crew_info(crew_name)
        if not crew_info:
            return []
        workflow_name = crew_info.get("workflow")
        if not workflow_name:
            return []

        steps = self.workflows.get(workflow_name, [])
        outputs = []
        for step in steps:
            result = self.execute_crew_task(crew_name, step)
            outputs.append(result)
        return outputs
