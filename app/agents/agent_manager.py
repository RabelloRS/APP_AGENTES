"""
Gerenciador de agentes para o sistema
"""

import os
from typing import Dict, List, Optional

import yaml
from crewai import Agent
from langchain.tools import Tool


class AgentManager:
    """Classe para gerenciar agentes do sistema usando arquivos YAML"""

    def __init__(
        self,
        config_path: str = "app/config/agents.yaml",
        tools_config_path: str = "app/config/agent_tools.yaml",
    ):
        self.config_path = config_path
        self.tools_config_path = tools_config_path
        self.agents: Dict[str, Agent] = {}
        self.available_agents = self._load_agent_configs()
        self.agent_tools = self._load_agent_tools_configs()
        self.tools_manager = None  # Será configurado posteriormente

    def set_tools_manager(self, tools_manager):
        """Define o gerenciador de tools para este agent manager"""
        self.tools_manager = tools_manager

    def _load_agent_configs(self) -> Dict:
        """Carrega as configurações dos agentes do arquivo YAML"""
        try:
            if not os.path.exists(self.config_path):
                print(f"Arquivo de configuração não encontrado: {self.config_path}")
                return {}

            with open(self.config_path, "r", encoding="utf-8") as file:
                configs = yaml.safe_load(file)
                return configs or {}

        except Exception as e:
            print(f"Erro ao carregar configurações dos agentes: {e}")
            return {}

    def _load_agent_tools_configs(self) -> Dict:
        """Carrega as configurações de tools dos agentes"""
        try:
            if not os.path.exists(self.tools_config_path):
                # Criar arquivo padrão se não existir
                self._create_default_agent_tools_config()

            with open(self.tools_config_path, "r", encoding="utf-8") as file:
                configs = yaml.safe_load(file)
                return configs or {}

        except Exception as e:
            print(f"Erro ao carregar configurações de tools dos agentes: {e}")
            return {}

    def _create_default_agent_tools_config(self):
        """Cria configuração padrão de tools para agentes"""
        default_config = {
            "researcher": {
                "tools": [
                    "read_excel_file",
                    "compare_text_similarity",
                    "detect_data_patterns",
                ],
                "description": "Tools para pesquisa e análise de dados",
            },
            "analyst": {
                "tools": [
                    "analyze_excel_similarity",
                    "detect_data_patterns",
                    "generate_excel_report",
                ],
                "description": "Tools para análise avançada e geração de relatórios",
            },
            "writer": {
                "tools": ["generate_excel_report"],
                "description": "Tools para geração de conteúdo e relatórios",
            },
            "reviewer": {
                "tools": ["validate_excel_file", "detect_data_patterns"],
                "description": "Tools para validação e revisão de dados",
            },
            "coordinator": {
                "tools": ["read_excel_file", "validate_excel_file"],
                "description": "Tools básicas para coordenação",
            },
            "excel_analyst": {
                "tools": [
                    "read_excel_column",
                    "read_excel_file",
                    "analyze_excel_similarity",
                    "detect_data_patterns",
                    "generate_excel_report",
                    "validate_excel_file",
                ],
                "description": "Todas as tools relacionadas a análise de Excel",
            },
        }

        try:
            with open(self.tools_config_path, "w", encoding="utf-8") as file:
                yaml.dump(
                    default_config,
                    file,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False,
                )
            print(
                f"Arquivo de configuração de tools dos agentes criado: {self.tools_config_path}"
            )
        except Exception as e:
            print(f"Erro ao criar arquivo de configuração de tools dos agentes: {e}")

    def _create_tool_objects(self, tool_names: List[str]) -> List[Tool]:
        """Cria objetos Tool do LangChain a partir dos nomes das tools"""
        if not self.tools_manager:
            print("ToolsManager não configurado. Retornando lista vazia de tools.")
            return []

        tools = []
        for tool_name in tool_names:
            try:
                # Obter a função da tool
                tool_function = self.tools_manager.get_tool_function(tool_name)
                if not tool_function:
                    print(f"Função da tool '{tool_name}' não encontrada")
                    continue

                # Obter informações da tool
                tool_info = self.tools_manager.get_tool_info(tool_name)
                if not tool_info:
                    print(f"Informações da tool '{tool_name}' não encontradas")
                    continue

                # Criar objeto Tool do LangChain
                tool = Tool(
                    name=tool_name,
                    description=tool_info.get("description", f"Tool {tool_name}"),
                    func=tool_function,
                )
                tools.append(tool)

            except Exception as e:
                print(f"Erro ao criar tool '{tool_name}': {e}")
                continue

        return tools

    def reload_configs(self) -> bool:
        """Recarrega as configurações dos agentes do arquivo YAML"""
        try:
            self.available_agents = self._load_agent_configs()
            self.agent_tools = self._load_agent_tools_configs()
            return True
        except Exception as e:
            print(f"Erro ao recarregar configurações: {e}")
            return False

    def create_agent(
        self, agent_type: str, tools: Optional[list] = None, **kwargs
    ) -> Optional[Agent]:
        """Cria um novo agente do tipo especificado"""
        if agent_type not in self.available_agents:
            print(f"Tipo de agente '{agent_type}' não encontrado nas configurações")
            return None

        agent_config = self.available_agents[agent_type].copy()

        # Sobrescrever configurações padrão com kwargs
        agent_config.update(kwargs)

        # Usar tools fornecidos ou da configuração
        if tools is not None:
            # Se tools fornecidos são strings, converter para objetos Tool
            if tools and isinstance(tools[0], str):
                tool_objects = self._create_tool_objects(tools)
            else:
                tool_objects = tools
        else:
            # Usar tools configuradas para este agente
            agent_tools_config = self.agent_tools.get(agent_type, {})
            tool_names = agent_tools_config.get("tools", [])
            tool_objects = self._create_tool_objects(tool_names)

        try:
            agent = Agent(
                role=agent_config["role"],
                goal=agent_config["goal"],
                backstory=agent_config["backstory"],
                tools=tool_objects,
                verbose=agent_config.get("verbose", True),
                allow_delegation=agent_config.get("allow_delegation", False),
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

    def get_agent_tools(self, agent_type: str) -> List[str]:
        """Retorna as tools atribuídas a um agente específico"""
        agent_tools_config = self.agent_tools.get(agent_type, {})
        return agent_tools_config.get("tools", [])

    def update_agent_tools(self, agent_type: str, tools: List[str]) -> bool:
        """Atualiza as tools atribuídas a um agente"""
        try:
            if agent_type not in self.available_agents:
                print(f"Tipo de agente '{agent_type}' não encontrado")
                return False

            # Atualizar configuração na memória
            if agent_type not in self.agent_tools:
                self.agent_tools[agent_type] = {}

            self.agent_tools[agent_type]["tools"] = tools

            # Salvar no arquivo YAML
            return self._save_agent_tools_to_file()

        except Exception as e:
            print(f"Erro ao atualizar tools do agente {agent_type}: {e}")
            return False

    def _save_agent_tools_to_file(self) -> bool:
        """Salva as configurações de tools dos agentes no arquivo YAML"""
        try:
            # Criar backup do arquivo original
            backup_path = f"{self.tools_config_path}.backup"
            if os.path.exists(self.tools_config_path):
                import shutil

                shutil.copy2(self.tools_config_path, backup_path)

            # Salvar nova configuração
            with open(self.tools_config_path, "w", encoding="utf-8") as file:
                yaml.dump(
                    self.agent_tools,
                    file,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False,
                )

            print(
                f"Configurações de tools dos agentes salvas com sucesso em {self.tools_config_path}"
            )
            return True

        except Exception as e:
            print(f"Erro ao salvar configurações de tools dos agentes: {e}")
            return False

    def update_agent_config(self, agent_type: str, new_config: Dict) -> bool:
        """Atualiza a configuração de um agente e salva no arquivo YAML"""
        try:
            if agent_type not in self.available_agents:
                print(f"Tipo de agente '{agent_type}' não encontrado")
                return False

            # Atualizar configuração na memória
            self.available_agents[agent_type].update(new_config)

            # Salvar no arquivo YAML
            return self._save_configs_to_file()

        except Exception as e:
            print(f"Erro ao atualizar configuração do agente {agent_type}: {e}")
            return False

    def _save_configs_to_file(self) -> bool:
        """Salva as configurações atuais no arquivo YAML"""
        try:
            # Criar backup do arquivo original
            backup_path = f"{self.config_path}.backup"
            if os.path.exists(self.config_path):
                import shutil

                shutil.copy2(self.config_path, backup_path)

            # Salvar nova configuração
            with open(self.config_path, "w", encoding="utf-8") as file:
                yaml.dump(
                    self.available_agents,
                    file,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False,
                )

            print(f"Configurações salvas com sucesso em {self.config_path}")
            return True

        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
            return False

    def rename_agent(self, old_type: str, new_type: str) -> bool:
        """Renomeia um tipo de agente"""
        try:
            if old_type not in self.available_agents:
                print(f"Tipo de agente '{old_type}' não encontrado")
                return False

            if new_type in self.available_agents:
                print(f"Tipo de agente '{new_type}' já existe")
                return False

            # Mover configuração para novo nome
            self.available_agents[new_type] = self.available_agents.pop(old_type)

            # Mover configuração de tools
            if old_type in self.agent_tools:
                self.agent_tools[new_type] = self.agent_tools.pop(old_type)

            # Atualizar agentes criados
            if old_type in self.agents:
                self.agents[new_type] = self.agents.pop(old_type)

            # Salvar no arquivo
            success1 = self._save_configs_to_file()
            success2 = self._save_agent_tools_to_file()
            return success1 and success2

        except Exception as e:
            print(f"Erro ao renomear agente: {e}")
            return False
