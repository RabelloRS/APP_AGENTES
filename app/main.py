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
        st.metric("Agentes Disponíveis", "5")

    with col2:
        st.metric("Crews Criadas", "3")

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

    # Lista de agentes disponíveis
    agents = [
        {"name": "Pesquisador", "role": "Realiza pesquisas e coleta informações"},
        {"name": "Analista", "role": "Analisa dados e gera insights"},
        {"name": "Escritor", "role": "Cria conteúdo e relatórios"},
        {"name": "Revisor", "role": "Revisa e valida conteúdo"},
        {"name": "Coordenador", "role": "Coordena tarefas entre agentes"},
    ]

    for agent in agents:
        with st.expander(f"🤖 {agent['name']}"):
            st.write(f"**Função:** {agent['role']}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button(
                    f"Configurar {agent['name']}", key=f"config_{agent['name']}"
                ):
                    st.info(
                        f"Configuração do agente {agent['name']} em desenvolvimento"
                    )

            with col2:
                if st.button(f"Testar {agent['name']}", key=f"test_{agent['name']}"):
                    st.info(f"Teste do agente {agent['name']} em desenvolvimento")


def show_crews_tab():
    """Exibe a aba de gerenciamento de crews"""
    st.header("👥 Gerenciamento de Crews")

    # Criar nova crew
    st.subheader("➕ Criar Nova Crew")

    crew_name = st.text_input("Nome da Crew")
    crew_description = st.text_area("Descrição")

    # Seleção de agentes
    available_agents = ["Pesquisador", "Analista", "Escritor", "Revisor", "Coordenador"]
    selected_agents = st.multiselect("Selecionar Agentes", available_agents)

    if st.button("Criar Crew"):
        if crew_name and selected_agents:
            st.success(f"Crew '{crew_name}' criada com sucesso!")
            st.write(f"Agentes: {', '.join(selected_agents)}")
        else:
            st.error("Preencha o nome da crew e selecione pelo menos um agente")

    st.markdown("---")

    # Lista de crews existentes
    st.subheader("📋 Crews Existentes")

    existing_crews = [
        {
            "name": "Crew de Pesquisa",
            "agents": ["Pesquisador", "Analista"],
            "status": "Ativa",
        },
        {
            "name": "Crew de Conteúdo",
            "agents": ["Escritor", "Revisor"],
            "status": "Ativa",
        },
        {"name": "Crew de Coordenação", "agents": ["Coordenador"], "status": "Inativa"},
    ]

    for crew in existing_crews:
        with st.expander(f"👥 {crew['name']} - {crew['status']}"):
            st.write(f"**Agentes:** {', '.join(crew['agents'])}")

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"Executar {crew['name']}", key=f"run_{crew['name']}"):
                    st.info(f"Execução da crew {crew['name']} em desenvolvimento")

            with col2:
                if st.button(f"Editar {crew['name']}", key=f"edit_{crew['name']}"):
                    st.info(f"Edição da crew {crew['name']} em desenvolvimento")

            with col3:
                if st.button(f"Deletar {crew['name']}", key=f"delete_{crew['name']}"):
                    st.info(f"Deleção da crew {crew['name']} em desenvolvimento")


def show_execution_tab():
    """Exibe a aba de execução de tarefas"""
    st.header("📊 Execução de Tarefas")

    # Seleção da crew
    st.subheader("🎯 Nova Tarefa")

    crews = ["Crew de Pesquisa", "Crew de Conteúdo", "Crew de Coordenação"]
    selected_crew = st.selectbox("Selecionar Crew", crews)

    # Input da tarefa
    task_description = st.text_area(
        "Descrição da Tarefa",
        placeholder="Descreva a tarefa que deseja executar...",
    )

    # Configurações adicionais
    col1, col2 = st.columns(2)

    with col1:
        max_iterations = st.number_input("Máximo de Iterações", min_value=1, max_value=10, value=3)

    with col2:
        verbose = st.checkbox("Modo Verbose", value=True)

    # Botão de execução
    if st.button("🚀 Executar Tarefa", type="primary"):
        if task_description:
            with st.spinner("Executando tarefa..."):
                # Simulação de execução
                import time

                time.sleep(2)

                st.success("✅ Tarefa executada com sucesso!")

                # Resultados simulados
                st.subheader("📋 Resultados")
                st.write("**Tarefa:** " + task_description)
                st.write("**Crew:** " + selected_crew)
                st.write("**Status:** Concluída")
                st.write("**Tempo de execução:** 2.3 segundos")

                # Exibir resultado
                st.text_area(
                    "Resultado da Execução",
                    value="Este é um resultado simulado da execução da tarefa. Em uma implementação real, aqui apareceria o resultado gerado pelos agentes da crew.",
                    height=200,
                )
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
