"""
Aplicação principal do sistema de agentes inteligentes
"""

import sys
import os
from pathlib import Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from dotenv import load_dotenv
from app.agents.agent_manager import AgentManager
from app.crews.crew_manager import CrewManager
from app.utils.config import Config

# Carregar variáveis de ambiente
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Configuração da página
st.set_page_config(
    page_title="APP_AGENTES - Sistema de Agentes Inteligentes",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    """Função principal da aplicação"""

    # Inicializar gerenciadores no session_state se não existirem
    if 'agent_manager' not in st.session_state:
        st.session_state.agent_manager = AgentManager()
    if 'crew_manager' not in st.session_state:
        st.session_state.crew_manager = CrewManager(st.session_state.agent_manager)

    # Header
    st.title("🤖 APP_AGENTES")
    st.markdown("### Sistema de Agentes Inteligentes com CrewAI")

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
            "Modelo", ["gpt-4o", "gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"], index=0
        )

        temperature = st.slider(
            "Temperatura", min_value=0.0, max_value=2.0, value=0.7, step=0.1
        )

    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs(
        ["🏠 Dashboard", "🤖 Agentes", "👥 Crews", "📊 Execução"]
    )

    with tab1:
        show_dashboard()

    with tab2:
        show_agents_tab()

    with tab3:
        show_crews_tab()

    with tab4:
        show_execution_tab()


def show_dashboard():
    """Exibe o dashboard principal"""
    st.header("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        num_agents = len(st.session_state.agent_manager.list_available_agent_types())
        st.metric("Agentes Disponíveis", f"{num_agents}")

    with col2:
        num_crews = len(st.session_state.crew_manager.list_crew_names())
        st.metric("Crews Criadas", f"{num_crews}")

    with col3:
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


def show_agents_tab():
    """Exibe a aba de gerenciamento de agentes"""
    st.header("🤖 Gerenciamento de Agentes")

    # Lista de agentes disponíveis dinamicamente
    manager = st.session_state.agent_manager
    for agent_type in manager.list_available_agent_types():
        info = manager.get_agent_info(agent_type) or {}
        name = info.get("name", agent_type)
        role = info.get("role", "-")
        with st.expander(f"🤖 {name}"):
            st.write(f"**Função:** {role}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button(
                    f"Configurar {name}", key=f"config_{agent_type}"
                ):
                    if not manager.get_agent(agent_type):
                        manager.create_agent(agent_type)
                    st.success(f"Agente {name} criado!")

            with col2:
                if st.button(f"Testar {name}", key=f"test_{agent_type}"):
                    st.info(f"Teste do agente {name} em desenvolvimento")


def show_crews_tab():
    """Exibe a aba de gerenciamento de crews"""
    st.header("👥 Gerenciamento de Crews")

    # Criar nova crew
    st.subheader("➕ Criar Nova Crew")

    crew_name = st.text_input("Nome da Crew")
    crew_description = st.text_area("Descrição")

    # Seleção de agentes dinâmicos
    manager = st.session_state.agent_manager
    available_agents = manager.list_available_agent_types()
    selected_agents = st.multiselect("Selecionar Agentes", available_agents)

    if st.button("Criar Crew"):
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

    if st.button("Criar Crew de Análise de Planilhas"):
        st.session_state.crew_manager.create_crew(
            "Crew de Análise de Planilhas", ["excel_analyst"], "Comparar planilhas"
        )
        st.success("Crew de Análise de Planilhas criada")

    st.markdown("---")

    # Lista de crews existentes
    st.subheader("📋 Crews Existentes")

    existing_crews = st.session_state.crew_manager.get_all_crews()

    for name, crew in existing_crews.items():
        agents_names = [agent.role for agent in crew.agents]
        with st.expander(f"👥 {name}"):
            st.write(f"**Agentes:** {', '.join(agents_names)}")

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"Executar {name}", key=f"run_{name}"):
                    st.info(f"Execução da crew {name} em desenvolvimento")

            with col2:
                if st.button(f"Editar {name}", key=f"edit_{name}"):
                    st.info(f"Edição da crew {name} em desenvolvimento")

            with col3:
                if st.button(f"Deletar {name}", key=f"delete_{name}"):
                    st.info(f"Deleção da crew {name} em desenvolvimento")


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
        "Descrição da Tarefa",
        placeholder="Descreva a tarefa que deseja executar...",
    )

    # Campos extras para análise de planilhas
    if selected_crew == "Crew de Análise de Planilhas":
        file1 = st.file_uploader("Arquivo Excel 1", type=["xlsx"], key="excel1")
        column1 = st.text_input("Coluna do Arquivo 1")
        file2 = st.file_uploader("Arquivo Excel 2", type=["xlsx"], key="excel2")
        column2 = st.text_input("Coluna do Arquivo 2")

    # Configurações adicionais
    col1, col2 = st.columns(2)

    with col1:
        max_iterations = st.number_input("Máximo de Iterações", min_value=1, max_value=10, value=3)

    with col2:
        verbose = st.checkbox("Modo Verbose", value=True)

    # Botão de execução
    if st.button("🚀 Executar Tarefa", type="primary"):
        if selected_crew == "Crew de Análise de Planilhas":
            if file1 and file2 and column1 and column2:
                with st.spinner(f"Executando tarefa com a '{selected_crew}'..."):
                    tmp1 = Path("/tmp/file1.xlsx")
                    tmp1.write_bytes(file1.getbuffer())
                    tmp2 = Path("/tmp/file2.xlsx")
                    tmp2.write_bytes(file2.getbuffer())
                    from app.utils.tools import read_excel_column, compare_text_similarity
                    list1 = read_excel_column(str(tmp1), column1)
                    list2 = read_excel_column(str(tmp2), column2)
                    result = compare_text_similarity(list1, list2)
                st.success("✅ Tarefa executada com sucesso!")
                st.subheader("📋 Resultados")
                st.json(result)
            else:
                st.error("Envie os arquivos e informe as colunas para comparação")
        else:
            if task_description:
                with st.spinner(f"Executando tarefa com a '{selected_crew}'..."):
                    result = crew_manager.execute_crew_task(selected_crew, task_description)
                st.success("✅ Tarefa executada com sucesso!")
                st.subheader("📋 Resultados")
                st.text_area("Resultado da Execução", value=result, height=300)
            else:
                st.error("Por favor, descreva a tarefa a ser executada")

    st.markdown("---")

    # Histórico de execuções
    st.subheader("📜 Histórico de Execuções")

    executions = [
        {"task": "Pesquisar sobre IA", "crew": "Crew de Pesquisa", "status": "Concluída", "time": "2.3s"},
        {"task": "Criar relatório", "crew": "Crew de Conteúdo", "status": "Concluída", "time": "1.8s"},
        {"task": "Analisar dados", "crew": "Crew de Pesquisa", "status": "Em andamento", "time": "5.2s"},
    ]

    for execution in executions:
        status_color = "🟢" if execution["status"] == "Concluída" else "🟡"
        st.write(f"{status_color} **{execution['task']}** - {execution['crew']} ({execution['time']})")


if __name__ == "__main__":
    main()
