"""
Gerenciador de crews para o sistema
"""

from typing import Dict, List, Optional
from datetime import datetime

from crewai import Crew, Task

from app.agents.agent_manager import AgentManager
from app.crews.task_manager import TaskManager
from app.utils.database import DatabaseManager


class CrewManager:
    """Classe para gerenciar crews do sistema"""

    def __init__(
        self, agent_manager: AgentManager, task_manager: Optional[TaskManager] = None
    ):
        self.agent_manager = agent_manager
        self.task_manager = task_manager or TaskManager()
        self.crews: Dict[str, Crew] = {}
        self.crew_configs: Dict[str, Dict] = {}
        self.db_manager = DatabaseManager()

    def create_crew(
        self, name: str, agent_types: List[str], description: str = ""
    ) -> Optional[Crew]:
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
                memory=True,
            )

            self.crews[name] = crew
            self.crew_configs[name] = {
                "description": description,
                "agent_types": agent_types,
                "created_at": datetime.now().isoformat(),
            }
            
            # Salvar configuração no banco de dados
            self.db_manager.save_crew_config(name, description, agent_types, [])

            return crew

        except Exception as e:
            print(f"Erro ao criar crew {name}: {e}")
            return None

    def add_task_to_crew(self, crew_name: str, task_type: str, **params) -> bool:
        """Adiciona uma tarefa a uma crew específica"""
        crew = self.get_crew(crew_name)
        if not crew:
            print(f"Crew {crew_name} não encontrada")
            return False

        # Obter o agente responsável pela tarefa
        task_info = self.task_manager.get_task_info(task_type)
        if not task_info:
            print(f"Tipo de tarefa {task_type} não encontrado")
            return False

        agent_type = task_info.get("agent")
        if not agent_type:
            print(f"Agente não especificado para tarefa {task_type}")
            return False

        agent = self.agent_manager.get_agent(agent_type)
        if not agent:
            print(f"Agente {agent_type} não encontrado")
            return False

        # Criar tarefa
        task = self.task_manager.create_task_with_params(task_type, agent, **params)
        if not task:
            return False

        # Adicionar tarefa à crew
        crew.tasks.append(task)
        return True

    def create_crew_with_tasks(
        self,
        name: str,
        agent_types: List[str],
        task_types: List[str],
        description: str = "",
        **task_params,
    ) -> Optional[Crew]:
        """Cria uma crew com agentes e tarefas pré-definidas"""
        crew = self.create_crew(name, agent_types, description)
        if not crew:
            return None

        # Adicionar tarefas
        for task_type in task_types:
            self.add_task_to_crew(name, task_type, **task_params)

        return crew

    def execute_crew_task(self, crew_name: str, task_description: str) -> Optional[str]:
        """Executa uma tarefa usando uma crew específica"""
        crew = self.get_crew(crew_name)
        if not crew:
            print(f"Crew {crew_name} não encontrada")
            return None

        try:
            # Criar tarefa dinâmica
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

    def execute_crew(self, crew_name: str, inputs: Optional[Dict] = None) -> Optional[str]:
        """Executa uma crew com suas tarefas pré-definidas ou cria tarefas dinâmicas"""
        crew = self.get_crew(crew_name)
        if not crew:
            print(f"Crew {crew_name} não encontrada")
            return None

        # Salvar execução no banco de dados
        topic = inputs.get('topic', 'Execução sem tópico') if inputs else 'Execução sem tópico'
        start_time = datetime.now()
        execution_id = self.db_manager.save_execution(crew_name, topic, start_time)

        try:
            # Se não há tarefas pré-definidas, criar uma tarefa dinâmica
            if not crew.tasks:
                print(f"Crew {crew_name} não possui tarefas definidas, criando tarefa dinâmica...")
                
                if not inputs or 'topic' not in inputs:
                    print("Parâmetro 'topic' não fornecido para tarefa dinâmica")
                    self.db_manager.update_execution_result(
                        execution_id, "Erro: Tópico não fornecido", 
                        datetime.now(), "0:00:00", "error", "Parâmetro 'topic' não fornecido"
                    )
                    return None
                
                # Criar tarefa dinâmica baseada no tópico
                topic = inputs['topic']
                task = Task(
                    description=f"Execute a seguinte tarefa: {topic}",
                    expected_output="Resultado detalhado da execução da tarefa",
                    agent=crew.agents[0] if crew.agents else None,
                )
                crew.tasks = [task]
            
            # Executar crew
            result = crew.kickoff()
            end_time = datetime.now()
            duration = str(end_time - start_time).split('.')[0]
            
            # Salvar resultado no banco de dados
            self.db_manager.update_execution_result(
                execution_id, str(result), end_time, duration, "completed"
            )
            
            return str(result)
            
        except Exception as e:
            end_time = datetime.now()
            duration = str(end_time - start_time).split('.')[0]
            error_msg = str(e)
            
            # Salvar erro no banco de dados
            self.db_manager.update_execution_result(
                execution_id, "", end_time, duration, "error", error_msg
            )
            
            print(f"Erro ao executar crew {crew_name}: {e}")
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

    def delete_crew(self, name: str) -> bool:
        """Remove uma crew (mantém o histórico no banco de dados)"""
        if name in self.crews:
            del self.crews[name]
            del self.crew_configs[name]
            # Não deletar do banco de dados para manter histórico
            # self.db_manager.delete_crew_config(name)
            return True
        return False

    def list_crew_names(self) -> List[str]:
        """Lista todos os nomes de crews"""
        return list(self.crews.keys())

    def reload_configs(self) -> bool:
        """Recarrega as configurações de agentes e tarefas"""
        try:
            self.agent_manager.reload_configs()
            self.task_manager.reload_configs()
            return True
        except Exception as e:
            print(f"Erro ao recarregar configurações: {e}")
            return False
