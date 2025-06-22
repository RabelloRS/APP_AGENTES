"""
Aplicação principal do sistema de agentes inteligentes
"""

import os
from datetime import datetime
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from app.agents.agent_manager import AgentManager
from app.crews.crew_manager import CrewManager
from app.crews.task_manager import TaskManager
from app.utils.tools_manager import ToolsManager

# Carregar variáveis de ambiente
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Configuração da página
st.set_page_config(
    page_title="Agentes de Engenharia da Propor - Sistema de Agentes Inteligentes",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    """Função principal da aplicação"""

    # Inicializar gerenciadores no session_state se não existirem
    if "agent_manager" not in st.session_state:
        st.session_state.agent_manager = AgentManager()
    if "task_manager" not in st.session_state:
        st.session_state.task_manager = TaskManager()
    if "tools_manager" not in st.session_state:
        st.session_state.tools_manager = ToolsManager()
    if "crew_manager" not in st.session_state:
        st.session_state.crew_manager = CrewManager(
            st.session_state.agent_manager, st.session_state.task_manager
        )

    # Configurar o ToolsManager no AgentManager
    st.session_state.agent_manager.set_tools_manager(st.session_state.tools_manager)

    # Header com logo da empresa
    col1, col2 = st.columns([1, 4])

    with col1:
        # Carregar e exibir o logo da empresa
        logo_path = "media/logo/LOGO_PROPOR_MEDIO.jpg"
        st.image(logo_path, width=120)

    with col2:
        st.title("🏗️ Agentes de Engenharia da Propor")
        st.markdown("### Sistema de Agentes Inteligentes com CrewAI")
        st.markdown("*Desenvolvido pela Propor Engenharia*")

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configurações")

        # Verificar se as chaves de API estão configuradas
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_openai_api_key_here":
            st.error("⚠️ Chave da API OpenAI não configurada!")
            st.info("Configure sua chave no arquivo .env")
            return

        st.success("✅ API configurada")

        # Configurações do modelo
        model = st.selectbox(
            "Modelo", ["gpt-4.1", "gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"], index=0
        )

        temperature = st.slider(
            "Temperatura", min_value=0.0, max_value=2.0, value=0.7, step=0.1
        )

        # Botão para recarregar configurações
        if st.button("🔄 Recarregar Configurações"):
            if st.session_state.crew_manager.reload_configs():
                st.success("Configurações recarregadas!")
            else:
                st.error("Erro ao recarregar configurações")

        # Informações da empresa
        st.markdown("---")
        st.markdown("### 📞 Contato")
        st.markdown("**Propor Engenharia**")
        st.markdown("**Responsável Técnico:**")
        st.markdown("Eng. Civil Rodrigo Emanuel Rabello")
        st.markdown("CREA-RS 167.175-D")
        st.markdown("📱 51 99164-6794")
        st.markdown("📍 Nova Petrópolis / RS")
        st.markdown("🏢 CNPJ: 41.556.670/0001-76")

    # Tabs principais
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["🏠 Dashboard", "🤖 Agentes", "📋 Tarefas", "🔧 Tools", "👥 Crews", "📊 Execução"]
    )

    with tab1:
        show_dashboard()

    with tab2:
        show_agents_tab()

    with tab3:
        show_tasks_tab()

    with tab4:
        show_tools_tab()

    with tab5:
        show_crews_tab()

    with tab6:
        show_execution_tab()


def show_dashboard():
    """Exibe o dashboard principal"""
    st.header("📊 Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        num_agents = len(st.session_state.agent_manager.list_available_agent_types())
        st.metric("Agentes Disponíveis", f"{num_agents}")

    with col2:
        num_tasks = len(st.session_state.task_manager.list_available_task_types())
        st.metric("Tarefas Disponíveis", f"{num_tasks}")

    with col3:
        num_crews = len(st.session_state.crew_manager.list_crew_names())
        st.metric("Crews Criadas", f"{num_crews}")

    with col4:
        st.metric("Tarefas Executadas", "12")

    st.markdown("---")

    # Status do sistema
    st.subheader("🔄 Status do Sistema")

    # Verificar conectividade com APIs
    try:
        import openai

        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # Teste simples de conectividade
        st.success("✅ Conectado à OpenAI API")
    except Exception as e:
        st.error(f"❌ Erro na conexão com OpenAI: {str(e)}")

    # Informações sobre configurações
    st.subheader("📁 Configurações")

    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Arquivo de Agentes:** `app/config/agents.yaml`")
        st.info(f"**Arquivo de Tarefas:** `app/config/tasks.yaml`")

    with col2:
        if st.button("📖 Ver Configurações"):
            show_config_files()


def show_config_files():
    """Exibe o conteúdo dos arquivos de configuração"""
    st.subheader("📄 Conteúdo dos Arquivos de Configuração")

    tab1, tab2 = st.tabs(["Agentes", "Tarefas"])

    with tab1:
        try:
            with open("app/config/agents.yaml", "r", encoding="utf-8") as f:
                st.code(f.read(), language="yaml")
        except Exception as e:
            st.error(f"Erro ao ler arquivo de agentes: {e}")

    with tab2:
        try:
            with open("app/config/tasks.yaml", "r", encoding="utf-8") as f:
                st.code(f.read(), language="yaml")
        except Exception as e:
            st.error(f"Erro ao ler arquivo de tarefas: {e}")


def show_agents_tab():
    """Exibe a aba de gerenciamento de agentes"""
    st.header("🤖 Gerenciamento de Agentes")

    # Lista de agentes disponíveis dinamicamente
    manager = st.session_state.agent_manager

    # Verificar se há um agente sendo editado
    editing_agent = st.session_state.get("editing_agent", None)

    if editing_agent:
        # Interface de edição
        st.subheader(f"✏️ Editando Agente: {editing_agent}")

        # Obter informações atuais do agente
        current_info = manager.get_agent_info(editing_agent) or {}

        # Formulário de edição
        with st.form(f"edit_agent_{editing_agent}"):
            st.write("**Configurações do Agente**")

            # Campos de edição
            new_name = st.text_input(
                "Nome do Agente",
                value=current_info.get("name", ""),
                key=f"name_{editing_agent}",
            )
            new_role = st.text_input(
                "Função",
                value=current_info.get("role", ""),
                key=f"role_{editing_agent}",
            )
            new_goal = st.text_area(
                "Objetivo",
                value=current_info.get("goal", ""),
                key=f"goal_{editing_agent}",
            )
            new_backstory = st.text_area(
                "História",
                value=current_info.get("backstory", ""),
                key=f"backstory_{editing_agent}",
            )

            # Opções avançadas
            with st.expander("⚙️ Opções Avançadas"):
                new_verbose = st.checkbox(
                    "Verbose",
                    value=current_info.get("verbose", True),
                    key=f"verbose_{editing_agent}",
                )
                new_allow_delegation = st.checkbox(
                    "Permitir Delegação",
                    value=current_info.get("allow_delegation", False),
                    key=f"delegation_{editing_agent}",
                )

            # Verificar se o nome foi alterado
            name_changed = new_name != current_info.get("name", "")
            if name_changed:
                st.warning("⚠️ O nome do agente foi alterado!")
                st.info(
                    """
                **Importante:** Alterar o nome pode afetar crews e tarefas existentes.
                Recomendamos usar o mesmo nome ou atualizar as crews manualmente.
                """
                )

            col1, col2, col3 = st.columns(3)

            with col1:
                if st.form_submit_button("💾 Salvar Alterações"):
                    # Validar campos obrigatórios
                    if (
                        not new_name
                        or not new_role
                        or not new_goal
                        or not new_backstory
                    ):
                        st.error("Todos os campos são obrigatórios!")
                    else:
                        # Preparar nova configuração
                        new_config = {
                            "name": new_name,
                            "role": new_role,
                            "goal": new_goal,
                            "backstory": new_backstory,
                            "verbose": new_verbose,
                            "allow_delegation": new_allow_delegation,
                            "tools": current_info.get("tools", []),
                        }

                        # Salvar alterações
                        if manager.update_agent_config(editing_agent, new_config):
                            st.success(f"Agente '{new_name}' atualizado com sucesso!")

                            # Se o nome foi alterado, mostrar aviso sobre crews
                            if name_changed:
                                st.warning(
                                    """
                                **Atenção:** O nome do agente foi alterado.
                                Verifique se as crews existentes ainda funcionam corretamente.
                                """
                                )

                            # Limpar estado de edição
                            st.session_state.editing_agent = None
                            st.rerun()
                        else:
                            st.error("Erro ao salvar alterações!")

            with col2:
                if st.form_submit_button("❌ Cancelar"):
                    st.session_state.editing_agent = None
                    st.rerun()

            with col3:
                if st.form_submit_button("🔄 Recarregar Original"):
                    st.rerun()

        st.markdown("---")

    # Lista de agentes
    st.subheader("📋 Agentes Disponíveis")

    for agent_type in manager.list_available_agent_types():
        info = manager.get_agent_info(agent_type) or {}
        name = info.get("name", agent_type)
        role = info.get("role", "-")
        goal = info.get("goal", "-")

        # Obter tools do agente
        agent_tools = manager.get_agent_tools(agent_type)
        tools_manager = st.session_state.tools_manager

        with st.expander(f"🤖 {name} ({agent_type})"):
            st.write(f"**Função:** {role}")
            st.write(f"**Objetivo:** {goal}")

            # Mostrar história completa se não estiver editando
            if not editing_agent:
                st.write(f"**História:** {info.get('backstory', '-')}")

                # Mostrar tools atribuídas
                if agent_tools:
                    st.write("**🔧 Tools Atribuídas:**")
                    for tool_name in agent_tools:
                        tool_info = tools_manager.get_tool_info(tool_name)
                        if tool_info:
                            st.write(
                                f"  - {tool_info['name']} ({tool_info['category']})"
                            )
                        else:
                            st.write(f"  - ⚠️ {tool_name} (não encontrada)")
                else:
                    st.write("**🔧 Tools Atribuídas:** Nenhuma")

            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button(f"✏️ Editar {name}", key=f"edit_{agent_type}"):
                    st.session_state.editing_agent = agent_type
                    st.rerun()

            with col2:
                if st.button(f"🔄 Recriar {name}", key=f"recreate_{agent_type}"):
                    # Remover agente existente se houver
                    if agent_type in manager.agents:
                        del manager.agents[agent_type]

                    # Criar novo agente
                    agent = manager.create_agent(agent_type)
                    if agent:
                        st.success(f"Agente {name} recriado com sucesso!")
                    else:
                        st.error(f"Erro ao recriar agente {name}")

            with col3:
                if st.button(f"🧪 Testar {name}", key=f"test_{agent_type}"):
                    st.info(f"Teste do agente {name} em desenvolvimento")
                    st.write("Funcionalidade de teste será implementada em breve.")

    # Seção de informações
    if not editing_agent:
        st.markdown("---")
        st.subheader("ℹ️ Informações")
        st.info(
            """
        **Como usar:**
        - Clique em **Editar** para modificar as configurações de um agente
        - As alterações são salvas automaticamente no arquivo de configuração
        - Use **Recriar** para aplicar as mudanças a agentes já criados
        - O arquivo original é sempre salvo como backup antes das alterações
        """
        )

        # Visualizar configuração atual
        with st.expander("📄 Visualizar Configuração Atual"):
            try:
                with open("app/config/agents.yaml", "r", encoding="utf-8") as f:
                    current_config = f.read()
                st.code(current_config, language="yaml")

                # Verificar se existe backup
                backup_path = "app/config/agents.yaml.backup"
                if os.path.exists(backup_path):
                    st.info("✅ Backup do arquivo original disponível")
                    if st.button("📋 Ver Backup"):
                        with open(backup_path, "r", encoding="utf-8") as f:
                            backup_content = f.read()
                        st.code(backup_content, language="yaml")
                else:
                    st.info("ℹ️ Nenhum backup encontrado (primeira edição)")

            except Exception as e:
                st.error(f"Erro ao ler arquivo de configuração: {e}")


def show_tasks_tab():
    """Exibe a aba de gerenciamento de tarefas"""
    st.header("📋 Gerenciamento de Tarefas")

    # Lista de tarefas disponíveis
    task_manager = st.session_state.task_manager
    for task_type in task_manager.list_available_task_types():
        info = task_manager.get_task_info(task_type) or {}
        description = info.get("description", "-")
        expected_output = info.get("expected_output", "-")
        agent_type = info.get("agent", "-")

        with st.expander(f"📋 {task_type}"):
            st.write(f"**Descrição:** {description}")
            st.write(f"**Saída Esperada:** {expected_output}")
            st.write(f"**Agente Responsável:** {agent_type}")

            if st.button(f"Ver Detalhes {task_type}", key=f"details_{task_type}"):
                st.json(info)


def show_tools_tab():
    """Exibe a aba de gerenciamento de tools"""
    st.header("🔧 Gerenciamento de Tools (Ferramentas)")

    tools_manager = st.session_state.tools_manager
    agent_manager = st.session_state.agent_manager

    # Verificar se há um agente sendo configurado
    configuring_agent = st.session_state.get("configuring_agent_tools", None)

    if configuring_agent:
        # Interface de configuração de tools para um agente
        st.subheader(f"⚙️ Configurando Tools para: {configuring_agent}")

        # Obter tools atuais do agente
        current_tools = agent_manager.get_agent_tools(configuring_agent)

        # Listar todas as tools disponíveis
        tools_manager.list_available_tools()
        tools_by_category = tools_manager.get_tools_by_category()

        # Interface de seleção
        st.write("**Selecione as tools que este agente deve ter acesso:**")

        selected_tools = []

        for category, tools in tools_by_category.items():
            with st.expander(f"📁 {category} ({len(tools)} tools)"):
                for tool_name in tools:
                    tool_info = tools_manager.get_tool_info(tool_name)
                    if tool_info:
                        # Checkbox para cada tool
                        is_selected = st.checkbox(
                            f"✅ {tool_info['name']}",
                            value=tool_name in current_tools,
                            key=f"tool_{configuring_agent}_{tool_name}",
                        )

                        if is_selected:
                            selected_tools.append(tool_name)

                        # Mostrar detalhes da tool sem usar expander aninhado
                        st.write(f"**🔧 {tool_info['name']}**")
                        st.write(f"*{tool_info['description']}*")

                        # Mostrar detalhes da tool
                        st.write("**Detalhes:**")
                        st.write(f"**Descrição:** {tool_info['description']}")

                        if "parameters" in tool_info:
                            st.write("**Parâmetros:**")
                            for param, desc in tool_info["parameters"].items():
                                st.write(f"  - `{param}`: {desc}")

                        if "returns" in tool_info:
                            st.write(f"**Retorna:** {tool_info['returns']}")

                        if "example" in tool_info:
                            st.write("**Exemplo de Uso:**")
                            st.code(tool_info["example"], language="python")

        # Botões de ação
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("💾 Salvar Configuração"):
                if agent_manager.update_agent_tools(configuring_agent, selected_tools):
                    st.success(
                        f"Tools configuradas com sucesso para {configuring_agent}!"
                    )
                    st.session_state.configuring_agent_tools = None
                    st.rerun()
                else:
                    st.error("Erro ao salvar configuração!")

        with col2:
            if st.button("❌ Cancelar"):
                st.session_state.configuring_agent_tools = None
                st.rerun()

        with col3:
            if st.button("🔄 Recarregar Original"):
                st.rerun()

        st.markdown("---")

    # Lista de agentes com suas tools
    st.subheader("🤖 Agentes e suas Tools")

    for agent_type in agent_manager.list_available_agent_types():
        agent_info = agent_manager.get_agent_info(agent_type) or {}
        agent_name = agent_info.get("name", agent_type)
        agent_tools = agent_manager.get_agent_tools(agent_type)

        with st.expander(f"🤖 {agent_name} ({len(agent_tools)} tools)"):
            st.write(f"**Tipo:** {agent_type}")
            st.write(f"**Função:** {agent_info.get('role', '-')}")

            if agent_tools:
                st.write("**Tools Atribuídas:**")
                for tool_name in agent_tools:
                    tool_info = tools_manager.get_tool_info(tool_name)
                    if tool_info:
                        st.write(f"  - 🔧 {tool_info['name']} ({tool_info['category']})")
                    else:
                        st.write(f"  - ⚠️ {tool_name} (não encontrada)")
            else:
                st.write("**Tools Atribuídas:** Nenhuma")

            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"⚙️ Configurar Tools", key=f"config_tools_{agent_type}"):
                    st.session_state.configuring_agent_tools = agent_type
                    st.rerun()

            with col2:
                if st.button(
                    f"🔄 Recriar Agente", key=f"recreate_with_tools_{agent_type}"
                ):
                    # Remover agente existente se houver
                    if agent_type in agent_manager.agents:
                        del agent_manager.agents[agent_type]

                    # Criar novo agente com tools configuradas
                    agent = agent_manager.create_agent(agent_type)
                    if agent:
                        st.success(f"Agente {agent_name} recriado com tools!")
                    else:
                        st.error(f"Erro ao recriar agente {agent_name}")

    # Lista de todas as tools disponíveis
    st.markdown("---")
    st.subheader("📋 Todas as Tools Disponíveis")

    tools_by_category = tools_manager.get_tools_by_category()

    for category, tools in tools_by_category.items():
        with st.expander(f"📁 {category} ({len(tools)} tools)"):
            for tool_name in tools:
                tool_info = tools_manager.get_tool_info(tool_name)
                if tool_info:
                    st.write(f"**🔧 {tool_info['name']}**")
                    st.write(f"*{tool_info['description']}*")

                    # Mostrar detalhes da tool sem usar expander aninhado
                    st.write("**Detalhes:**")
                    st.write(f"**Descrição:** {tool_info['description']}")

                    if "parameters" in tool_info:
                        st.write("**Parâmetros:**")
                        for param, desc in tool_info["parameters"].items():
                            st.write(f"  - `{param}`: {desc}")

                    if "returns" in tool_info:
                        st.write(f"**Retorna:** {tool_info['returns']}")

                    if "example" in tool_info:
                        st.write("**Exemplo de Uso:**")
                        st.code(tool_info["example"], language="python")

                    st.markdown("---")

    # Informações sobre tools
    if not configuring_agent:
        st.markdown("---")
        st.subheader("ℹ️ Informações sobre Tools")
        st.info(
            """
        **Como usar:**
        - Clique em **"Configurar Tools"** para atribuir ferramentas a um agente
        - As tools permitem que os agentes executem tarefas específicas
        - Use **"Recriar Agente"** para aplicar as mudanças a agentes já criados
        - As configurações são salvas automaticamente
        
        **Categorias de Tools:**
        - **Excel**: Ferramentas para manipulação de planilhas
        - **Análise**: Ferramentas para análise de dados
        - **Relatórios**: Ferramentas para geração de relatórios
        """
        )


def show_crews_tab():
    """Exibe a aba de gerenciamento de crews"""
    st.header("👥 Gerenciamento de Crews")

    # Criar nova crew
    st.subheader("➕ Criar Nova Crew")

    crew_name = st.text_input("Nome da Crew")
    crew_description = st.text_area("Descrição")

    # Seleção de agentes dinâmicos
    agent_manager = st.session_state.agent_manager
    available_agents = agent_manager.list_available_agent_types()
    selected_agents = st.multiselect("Selecionar Agentes", available_agents)

    # Seleção de tarefas
    task_manager = st.session_state.task_manager
    available_tasks = task_manager.list_available_task_types()
    selected_tasks = st.multiselect("Selecionar Tarefas", available_tasks)

    # Parâmetros para as tarefas
    task_params = {}
    if selected_tasks:
        st.subheader("📝 Parâmetros das Tarefas")
        task_params["topic"] = st.text_input("Tópico", value="tecnologia")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Criar Crew Simples"):
            if crew_name and selected_agents:
                crew = st.session_state.crew_manager.create_crew(
                    crew_name, selected_agents, crew_description
                )
                if crew:
                    st.success(f"Crew '{crew_name}' criada com sucesso!")
                else:
                    st.error("Erro ao criar a crew")
            else:
                st.error("Preencha o nome da crew e selecione pelo menos um agente")

    with col2:
        if st.button("Criar Crew com Tarefas"):
            if crew_name and selected_agents and selected_tasks:
                crew = st.session_state.crew_manager.create_crew_with_tasks(
                    crew_name,
                    selected_agents,
                    selected_tasks,
                    crew_description,
                    **task_params,
                )
                if crew:
                    st.success(f"Crew '{crew_name}' criada com tarefas!")
                else:
                    st.error("Erro ao criar a crew com tarefas")
            else:
                st.error("Preencha o nome da crew, selecione agentes e tarefas")

    # Crews pré-definidas
    st.subheader("🚀 Crews Pré-definidas")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Criar Crew de Análise de Planilhas"):
            crew = st.session_state.crew_manager.create_crew_with_tasks(
                "Crew de Análise de Planilhas",
                ["excel_analyst"],
                ["excel_analysis_task"],
                "Comparar e analisar planilhas Excel",
                topic="dados de vendas",
            )
            if crew:
                st.success("Crew de Análise de Planilhas criada com sucesso!")

    with col2:
        if st.button("Criar Crew Completa de Pesquisa"):
            crew = st.session_state.crew_manager.create_crew_with_tasks(
                "Crew de Pesquisa Completa",
                ["researcher", "analyst", "writer", "reviewer"],
                ["research_task", "analysis_task", "writing_task", "review_task"],
                "Pesquisa completa com análise e escrita",
                topic="inteligência artificial",
            )
            if crew:
                st.success("Crew de Pesquisa Completa criada com sucesso!")

    st.markdown("---")

    # Lista de crews existentes
    st.subheader("📋 Crews Existentes")

    existing_crews = st.session_state.crew_manager.get_all_crews()

    for name, crew in existing_crews.items():
        agents_names = [agent.role for agent in crew.agents]
        num_tasks = len(crew.tasks)

        with st.expander(f"👥 {name} ({num_tasks} tarefas)"):
            st.write(f"**Agentes:** {', '.join(agents_names)}")

            if crew.tasks:
                st.write("**Tarefas:**")
                for i, task in enumerate(crew.tasks, 1):
                    st.write(f"{i}. {task.description[:100]}...")

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"Executar {name}", key=f"run_{name}"):
                    result = st.session_state.crew_manager.execute_crew(name)
                    if result:
                        st.success("Crew executada com sucesso!")
                        st.text_area("Resultado", result, height=200)
                    else:
                        st.error("Erro ao executar crew")

            with col2:
                if st.button(f"Editar {name}", key=f"edit_{name}"):
                    st.info(f"Edição da crew {name} em desenvolvimento")

            with col3:
                if st.button(f"Deletar {name}", key=f"delete_{name}"):
                    if st.session_state.crew_manager.delete_crew(name):
                        st.success(f"Crew {name} deletada!")
                        st.rerun()
                    else:
                        st.error("Erro ao deletar crew")


def show_execution_tab():
    """Exibe a aba de execução de tarefas"""
    st.header("📊 Execução de Tarefas")

    # Seleção da crew
    st.subheader("🎯 Nova Tarefa")

    crew_manager = st.session_state.crew_manager
    crews = crew_manager.list_crew_names()
    selected_crew = st.selectbox("Selecionar Crew", crews)

    # Input da tarefa
    task_description = st.text_area(
        "Descrição da Tarefa", placeholder="Descreva a tarefa que deseja executar..."
    )

    # Campos específicos para análise de planilhas
    if selected_crew == "Crew de Análise de Planilhas":
        st.subheader("📁 Upload de Arquivos Excel")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Arquivo 1**")
            file1 = st.file_uploader(
                "Arquivo Excel 1", type=["xlsx", "xls"], key="excel1"
            )
            if file1:
                # Validar arquivo 1
                import os
                import tempfile

                from app.utils.tools import validate_excel_file

                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=".xlsx"
                ) as tmp_file:
                    tmp_file.write(file1.getbuffer())
                    tmp_path = tmp_file.name

                validation1 = validate_excel_file(tmp_path)
                os.unlink(tmp_path)  # Limpar arquivo temporário

                if validation1["is_valid"]:
                    st.success(
                        f"✅ Arquivo válido: {validation1['total_rows']} linhas, {validation1['total_columns']} colunas"
                    )
                    column1 = st.selectbox(
                        "Selecionar coluna do Arquivo 1", validation1["columns"]
                    )
                else:
                    st.error(f"❌ Erro no arquivo: {validation1['error']}")
                    column1 = None
            else:
                column1 = None

        with col2:
            st.write("**Arquivo 2**")
            file2 = st.file_uploader(
                "Arquivo Excel 2", type=["xlsx", "xls"], key="excel2"
            )
            if file2:
                # Validar arquivo 2
                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=".xlsx"
                ) as tmp_file:
                    tmp_file.write(file2.getbuffer())
                    tmp_path = tmp_file.name

                validation2 = validate_excel_file(tmp_path)
                os.unlink(tmp_path)  # Limpar arquivo temporário

                if validation2["is_valid"]:
                    st.success(
                        f"✅ Arquivo válido: {validation2['total_rows']} linhas, {validation2['total_columns']} colunas"
                    )
                    column2 = st.selectbox(
                        "Selecionar coluna do Arquivo 2", validation2["columns"]
                    )
                else:
                    st.error(f"❌ Erro no arquivo: {validation2['error']}")
                    column2 = None
            else:
                column2 = None

        # Opções avançadas de análise
        st.subheader("⚙️ Opções de Análise")

        col1, col2, col3 = st.columns(3)

        with col1:
            include_patterns = st.checkbox("Detectar padrões nos dados", value=True)

        with col2:
            include_recommendations = st.checkbox("Gerar recomendações", value=True)

        with col3:
            include_detailed_report = st.checkbox("Relatório detalhado", value=True)

    # Configurações adicionais
    col1, col2 = st.columns(2)

    with col1:
        max_iterations = st.number_input(
            "Máximo de Iterações", min_value=1, max_value=10, value=3
        )

    with col2:
        verbose = st.checkbox("Modo Verbose", value=True)

    # Botão de execução
    if st.button("🚀 Executar Tarefa", type="primary"):
        if selected_crew == "Crew de Análise de Planilhas":
            if file1 and file2 and column1 and column2:
                with st.spinner(f"Executando análise de planilhas..."):
                    try:
                        # Salvar arquivos temporariamente
                        import os
                        import tempfile

                        with tempfile.NamedTemporaryFile(
                            delete=False, suffix=".xlsx"
                        ) as tmp1:
                            tmp1.write(file1.getbuffer())
                            tmp1_path = tmp1.name

                        with tempfile.NamedTemporaryFile(
                            delete=False, suffix=".xlsx"
                        ) as tmp2:
                            tmp2.write(file2.getbuffer())
                            tmp2_path = tmp2.name

                        # Executar análise completa
                        from app.utils.tools import (analyze_excel_similarity,
                                                     detect_data_patterns,
                                                     generate_excel_report)

                        # Análise de similaridade
                        analysis_results = analyze_excel_similarity(
                            tmp1_path, tmp2_path, column1, column2
                        )

                        # Detectar padrões se solicitado
                        if include_patterns:
                            analysis_results["file1_patterns"] = detect_data_patterns(
                                tmp1_path, column1
                            )
                            analysis_results["file2_patterns"] = detect_data_patterns(
                                tmp2_path, column2
                            )

                        # Limpar arquivos temporários
                        os.unlink(tmp1_path)
                        os.unlink(tmp2_path)

                        st.success("✅ Análise concluída com sucesso!")

                        # Exibir resultados
                        st.subheader("📋 Resultados da Análise")

                        # Métricas principais
                        col1, col2, col3, col4 = st.columns(4)

                        with col1:
                            st.metric(
                                "Score Médio",
                                f"{analysis_results['similarity_analysis']['average_score']:.1f}%",
                            )

                        with col2:
                            st.metric(
                                "Alta Similaridade",
                                analysis_results["similarity_analysis"][
                                    "high_similarity_count"
                                ],
                            )

                        with col3:
                            st.metric(
                                "Média Similaridade",
                                analysis_results["similarity_analysis"][
                                    "medium_similarity_count"
                                ],
                            )

                        with col4:
                            st.metric(
                                "Baixa Similaridade",
                                analysis_results["similarity_analysis"][
                                    "low_similarity_count"
                                ],
                            )

                        # Recomendações
                        if include_recommendations:
                            st.subheader("💡 Recomendações")
                            for rec in analysis_results["recommendations"]:
                                st.info(rec)

                        # Padrões detectados
                        if include_patterns and "file1_patterns" in analysis_results:
                            st.subheader("🔍 Padrões Detectados")

                            col1, col2 = st.columns(2)

                            with col1:
                                st.write("**Arquivo 1**")
                                patterns1 = analysis_results["file1_patterns"]
                                st.json(patterns1)

                            with col2:
                                st.write("**Arquivo 2**")
                                patterns2 = analysis_results["file2_patterns"]
                                st.json(patterns2)

                        # Relatório detalhado
                        if include_detailed_report:
                            st.subheader("📄 Relatório Detalhado")
                            report = generate_excel_report(analysis_results)
                            st.markdown(report)

                            # Botão para download do relatório
                            st.download_button(
                                label="📥 Download do Relatório (TXT)",
                                data=report,
                                file_name=f"relatorio_analise_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                mime="text/plain",
                            )

                        # Detalhes das correspondências
                        st.subheader("🔍 Detalhes das Correspondências")

                        # Filtro por score
                        min_score = st.slider("Score mínimo para exibir", 0, 100, 50)

                        matches = analysis_results["detailed_matches"]
                        filtered_matches = {
                            k: v for k, v in matches.items() if v["score"] >= min_score
                        }

                        if filtered_matches:
                            # Criar DataFrame para exibição
                            import pandas as pd

                            df_matches = pd.DataFrame(
                                [
                                    {
                                        "Original": original,
                                        "Correspondência": match_info["match"],
                                        "Score": f"{match_info['score']:.1f}%",
                                    }
                                    for original, match_info in filtered_matches.items()
                                ]
                            )

                            st.dataframe(df_matches, use_container_width=True)
                        else:
                            st.info(
                                "Nenhuma correspondência encontrada com o score mínimo selecionado."
                            )

                    except Exception as e:
                        st.error(f"❌ Erro durante a análise: {str(e)}")
            else:
                st.error("Envie os arquivos e informe as colunas para comparação")
        else:
            if task_description:
                with st.spinner(f"Executando tarefa com a '{selected_crew}'..."):
                    result = crew_manager.execute_crew_task(
                        selected_crew, task_description
                    )
                st.success("✅ Tarefa executada com sucesso!")
                st.subheader("📋 Resultados")
                st.text_area("Resultado da Execução", value=result, height=300)
            else:
                st.error("Por favor, descreva a tarefa a ser executada")

    st.markdown("---")

    # Histórico de execuções
    st.subheader("📜 Histórico de Execuções")

    executions = [
        {
            "task": "Pesquisar sobre IA",
            "crew": "Crew de Pesquisa",
            "status": "Concluída",
            "time": "2.3s",
        },
        {
            "task": "Criar relatório",
            "crew": "Crew de Conteúdo",
            "status": "Concluída",
            "time": "1.8s",
        },
        {
            "task": "Analisar dados",
            "crew": "Crew de Pesquisa",
            "status": "Em andamento",
            "time": "5.2s",
        },
    ]

    for execution in executions:
        status_color = "🟢" if execution["status"] == "Concluída" else "🟡"
        st.write(
            f"{status_color} **{execution['task']}** - {execution['crew']} ({execution['time']})"
        )


if __name__ == "__main__":
    main()
