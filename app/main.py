"""
Aplicação principal do sistema de agentes inteligentes
"""

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from app.agents.agent_manager import AgentManager
from app.crews.crew_manager import CrewManager
from app.crews.task_manager import TaskManager
from app.utils.tools_manager import ToolsManager

# Importar páginas
from app.pages.dashboard import show_dashboard
from app.pages.agents import show_agents_tab
from app.pages.tasks import show_tasks_tab
from app.pages.tools import show_tools_tab
from app.pages.crews import show_crews_tab
from app.pages.whatsapp import show_whatsapp_tab
from app.pages.execution import show_execution_tab

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
    try:
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
    except Exception as e:
        st.error(f"Erro ao inicializar gerenciadores: {e}")
        st.stop()

    # Header com logo da empresa
    col1, col2 = st.columns([1, 4])

    with col1:
        # Carregar e exibir o logo da empresa
        try:
            logo_path = "media/logo/LOGO_PROPOR_MEDIO.jpg"
            st.image(logo_path, width=120)
        except Exception as e:
            st.warning(f"Erro ao carregar logo: {e}")

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
            try:
                if st.session_state.crew_manager.reload_configs():
                    st.success("Configurações recarregadas!")
                else:
                    st.error("Erro ao recarregar configurações")
            except Exception as e:
                st.error(f"Erro ao recarregar configurações: {e}")

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

    # Nova API de navegação do Streamlit 1.46.0+
    pages = {
        "🏠 Principal": [
            st.Page(show_dashboard, title="Dashboard", icon="📊"),
        ],
        "🤖 Gerenciamento": [
            st.Page(show_agents_tab, title="Agentes", icon="🤖"),
            st.Page(show_tasks_tab, title="Tarefas", icon="📋"),
            st.Page(show_tools_tab, title="Tools", icon="🔧"),
            st.Page(show_crews_tab, title="Crews", icon="👥"),
        ],
        "📱 Integrações": [
            st.Page(show_whatsapp_tab, title="WhatsApp", icon="📱"),
        ],
        "📊 Execução": [
            st.Page(show_execution_tab, title="Execução", icon="📊"),
        ]
    }

    # Usar st.navigation com posição no topo para melhor organização
    current_page = st.navigation(pages, position="top", expanded=True)
    
    # Executar a página selecionada
    current_page.run()


if __name__ == "__main__":
    main()
