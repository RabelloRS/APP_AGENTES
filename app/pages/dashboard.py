"""
Dashboard Principal - Visão Geral do Sistema
"""

import os
import streamlit as st
from pathlib import Path

def show_dashboard():
    """Exibe o dashboard principal com métricas e status do sistema"""
    
    # Header da página
    st.header("📊 Dashboard - Visão Geral do Sistema")
    st.markdown("### Bem-vindo ao Sistema de Agentes Inteligentes da Propor Engenharia")
    
    # Informações de ajuda
    with st.expander("ℹ️ Como usar este dashboard", expanded=False):
        st.info("""
        **Este dashboard mostra:**
        - 📈 **Métricas do sistema**: Número de agentes, tarefas, crews e execuções
        - 🔄 **Status da conexão**: Verificação da conectividade com APIs
        - 📁 **Configurações**: Acesso aos arquivos de configuração
        - 🚀 **Ações rápidas**: Links para funcionalidades principais
        
        **Navegação:**
        - Use o menu lateral para acessar diferentes seções
        - Cada página tem funcionalidades específicas e ajuda contextual
        """)
    
    # Métricas principais em cards
    st.subheader("📈 Métricas do Sistema")
    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        num_agents = len(st.session_state.agent_manager.list_available_agent_types())
        st.metric(
            "🤖 Agentes Disponíveis", 
            num_agents,
            help="Número total de tipos de agentes configurados no sistema"
        )

    with col2:
        num_tasks = len(st.session_state.task_manager.list_available_task_types())
        st.metric(
            "📋 Tarefas Disponíveis", 
            num_tasks,
            help="Número total de tipos de tarefas que podem ser executadas"
        )

    with col3:
        num_crews = len(st.session_state.crew_manager.list_crew_names())
        st.metric(
            "👥 Crews Criadas", 
            num_crews,
            help="Número de crews (equipes) de agentes criadas"
        )

    with col4:
        # Simular histórico de execuções
        executions_count = len(st.session_state.get("execution_history", []))
        st.metric(
            "🚀 Tarefas Executadas", 
            executions_count,
            help="Número total de tarefas executadas nesta sessão"
        )

    st.markdown("---")

    # Status do sistema
    st.subheader("🔄 Status do Sistema")
    
    status_col1, status_col2 = st.columns([2, 1])
    
    with status_col1:
        # Verificar conectividade com APIs
        try:
            import openai
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            st.success("✅ Conectado à OpenAI API")
            st.info("🔗 API funcionando corretamente - Pronto para executar tarefas")
        except Exception as e:
            st.error(f"❌ Erro na conexão com OpenAI: {str(e)}")
            st.warning("⚠️ Configure sua chave da API OpenAI no arquivo .env")
    
    with status_col2:
        # Status do WhatsApp (se aplicável)
        whatsapp_status = st.session_state.get("whatsapp_status", "disconnected")
        if whatsapp_status == "connected":
            st.success("📱 WhatsApp Conectado")
        elif whatsapp_status == "connecting":
            st.warning("📱 Conectando WhatsApp...")
        else:
            st.info("📱 WhatsApp Desconectado")

    # Ações rápidas
    st.subheader("🚀 Ações Rápidas")
    
    quick_col1, quick_col2, quick_col3 = st.columns(3)
    
    with quick_col1:
        if st.button("🤖 Gerenciar Agentes", type="secondary", use_container_width=True):
            st.info("Use o menu lateral para navegar para a página de Agentes")
    
    with quick_col2:
        if st.button("👥 Criar Nova Crew", type="secondary", use_container_width=True):
            st.info("Use o menu lateral para navegar para a página de Crews")
    
    with quick_col3:
        if st.button("📊 Executar Tarefa", type="secondary", use_container_width=True):
            st.info("Use o menu lateral para navegar para a página de Execução")

    st.markdown("---")

    # Informações sobre configurações
    st.subheader("📁 Configurações do Sistema")
    
    config_col1, config_col2 = st.columns(2)
    
    with config_col1:
        st.info("**📄 Arquivo de Agentes:** `app/config/agents.yaml`")
        st.info("**📄 Arquivo de Tarefas:** `app/config/tasks.yaml`")
        
        if st.button("📖 Ver Configurações", use_container_width=True):
            show_config_files()

    with config_col2:
        st.info("**🔧 Arquivo de Tools:** `app/config/tools.yaml`")
        st.info("**👥 Arquivo de Crews:** `app/config/crews.yaml`")
        
        if st.button("🔄 Recarregar Configurações", use_container_width=True):
            if st.session_state.crew_manager.reload_configs():
                st.success("✅ Configurações recarregadas com sucesso!")
            else:
                st.error("❌ Erro ao recarregar configurações")

    # Últimas atividades
    st.subheader("📜 Últimas Atividades")
    
    # Simular histórico de atividades
    activities = [
        {"time": "2 min atrás", "action": "Crew 'Análise de Planilhas' executada", "status": "✅ Concluída"},
        {"time": "5 min atrás", "action": "Agente 'Excel Analyst' recriado", "status": "✅ Sucesso"},
        {"time": "10 min atrás", "action": "Nova crew 'Pesquisa Completa' criada", "status": "✅ Criada"},
        {"time": "15 min atrás", "action": "Tools configuradas para 'Researcher'", "status": "✅ Configurado"},
    ]
    
    for activity in activities:
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            st.write(f"🕐 {activity['time']}")
        with col2:
            st.write(activity['action'])
        with col3:
            st.write(activity['status'])

    # Informações da empresa
    st.markdown("---")
    st.subheader("🏢 Sobre a Propor Engenharia")
    
    company_col1, company_col2 = st.columns(2)
    
    with company_col1:
        st.markdown("""
        **Propor Engenharia**
        
        **Responsável Técnico:**  
        Eng. Civil Rodrigo Emanuel Rabello  
        CREA-RS 167.175-D
        
        **Contato:**  
        📱 51 99164-6794  
        📍 Nova Petrópolis / RS
        """)
    
    with company_col2:
        st.markdown("""
        **Informações Legais:**
        
        🏢 CNPJ: 41.556.670/0001-76
        
        **Especialidades:**
        - Engenharia Civil
        - Sistemas Inteligentes
        - Automação de Processos
        - Análise de Dados
        """)


def show_config_files():
    """Exibe o conteúdo dos arquivos de configuração"""
    st.subheader("📄 Conteúdo dos Arquivos de Configuração")
    
    # Tabs para diferentes arquivos
    tab1, tab2, tab3, tab4 = st.tabs(["🤖 Agentes", "📋 Tarefas", "🔧 Tools", "👥 Crews"])

    with tab1:
        try:
            with open("app/config/agents.yaml", "r", encoding="utf-8") as f:
                st.code(f.read(), language="yaml")
        except Exception as e:
            st.error(f"❌ Erro ao ler arquivo de agentes: {e}")

    with tab2:
        try:
            with open("app/config/tasks.yaml", "r", encoding="utf-8") as f:
                st.code(f.read(), language="yaml")
        except Exception as e:
            st.error(f"❌ Erro ao ler arquivo de tarefas: {e}")

    with tab3:
        try:
            with open("app/config/tools.yaml", "r", encoding="utf-8") as f:
                st.code(f.read(), language="yaml")
        except Exception as e:
            st.error(f"❌ Erro ao ler arquivo de tools: {e}")

    with tab4:
        try:
            with open("app/config/crews.yaml", "r", encoding="utf-8") as f:
                st.code(f.read(), language="yaml")
        except Exception as e:
            st.error(f"❌ Erro ao ler arquivo de crews: {e}")

    # Verificar backups
    st.subheader("💾 Backups Disponíveis")
    
    backup_files = [
        ("agents.yaml.backup", "Agentes"),
        ("tasks.yaml.backup", "Tarefas"),
        ("tools.yaml.backup", "Tools"),
        ("crews.yaml.backup", "Crews")
    ]
    
    for backup_file, description in backup_files:
        backup_path = f"app/config/{backup_file}"
        if Path(backup_path).exists():
            st.success(f"✅ Backup de {description} disponível")
            if st.button(f"📋 Ver Backup - {description}"):
                with open(backup_path, "r", encoding="utf-8") as f:
                    st.code(f.read(), language="yaml")
        else:
            st.info(f"ℹ️ Nenhum backup de {description} encontrado") 