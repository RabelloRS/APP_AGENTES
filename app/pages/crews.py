"""
Página de Gerenciamento de Crews - Crie e Configure Suas Equipes de Agentes
"""

import streamlit as st
from datetime import datetime

def show_crews_tab():
    """Exibe a aba de gerenciamento de crews."""
    st.header("👥 Gerenciamento de Crews")
    st.markdown("### Crie e configure equipes de agentes especializados")

    # Mapeamento de nomes técnicos para nomes amigáveis
    agent_friendly_names = {
        "researcher": "🔍 Pesquisador",
        "analyst": "📊 Analista", 
        "writer": "✍️ Escritor",
        "reviewer": "🔍 Revisor",
        "coordinator": "🎯 Coordenador",
        "excel_analyst": "📈 Analista de Excel",
        "whatsapp_monitor": "📱 Monitor do WhatsApp",
        "file_downloader": "⬇️ Baixador de Arquivos",
        "file_organizer": "📁 Organizador de Arquivos"
    }
    
    task_friendly_names = {
        "research_task": "🔍 Pesquisa e Coleta de Dados",
        "analysis_task": "📊 Análise e Interpretação",
        "writing_task": "✍️ Redação de Conteúdo",
        "review_task": "🔍 Revisão e Validação",
        "coordination_task": "🎯 Coordenação de Equipe",
        "excel_analysis_task": "📈 Análise de Planilhas",
        "whatsapp_monitoring_task": "📱 Monitoramento do WhatsApp",
        "file_download_task": "⬇️ Download de Arquivos",
        "file_organization_task": "📁 Organização de Arquivos"
    }
    
    agent_descriptions = {
        "researcher": "Especialista em buscar e coletar informações técnicas na internet",
        "analyst": "Profissional que analisa dados e gera insights valiosos",
        "writer": "Especialista em criar conteúdo claro e bem estruturado",
        "reviewer": "Responsável por revisar e validar a qualidade do trabalho",
        "coordinator": "Gerencia o fluxo de trabalho e coordena a equipe",
        "excel_analyst": "Especialista em análise de planilhas e dados estruturados",
        "whatsapp_monitor": "Monitora grupos do WhatsApp e identifica arquivos importantes",
        "file_downloader": "Baixa e gerencia arquivos de diferentes fontes",
        "file_organizer": "Organiza e categoriza arquivos de forma eficiente"
    }
    
    task_descriptions = {
        "research_task": "Coleta informações relevantes sobre o tópico especificado",
        "analysis_task": "Analisa os dados coletados e extrai insights importantes",
        "writing_task": "Cria conteúdo baseado nas análises realizadas",
        "review_task": "Revisa e valida a qualidade do trabalho final",
        "coordination_task": "Coordena o fluxo de trabalho entre os agentes",
        "excel_analysis_task": "Analisa planilhas Excel e extrai informações relevantes",
        "whatsapp_monitoring_task": "Monitora grupos do WhatsApp em busca de arquivos",
        "file_download_task": "Baixa arquivos identificados pelos monitores",
        "file_organization_task": "Organiza os arquivos baixados por categoria"
    }

    crew_manager = st.session_state.crew_manager
    agent_manager = st.session_state.agent_manager
    task_manager = st.session_state.task_manager

    # Guia de criação de crews
    with st.expander("📖 Guia: Como Criar uma Crew Eficiente", expanded=False):
        st.markdown("""
        ### 🎯 **Como Funciona uma Crew**
        
        Uma **Crew** é uma equipe de agentes que trabalham em sequência para completar uma tarefa complexa.
        
        ### 📋 **Fluxo de Trabalho Típico:**
        
        1. **🔍 Pesquisador** → Coleta informações iniciais
        2. **📊 Analista** → Analisa e interpreta os dados
        3. **✍️ Escritor** → Cria o conteúdo final
        4. **🔍 Revisor** → Revisa e valida a qualidade
        
        ### 💡 **Dicas para Crews Eficientes:**
        
        - **Ordem Importante**: Os agentes trabalham na ordem que você selecionar
        - **Especialização**: Cada agente tem ferramentas específicas
        - **Comunicação**: Os agentes passam informações entre si automaticamente
        - **Resultado Final**: O último agente gera o resultado final
        
        ### 🛠️ **Ferramentas por Agente:**
        
        - **Pesquisador**: Busca na internet, lê arquivos Excel
        - **Analista**: Analisa dados, detecta padrões, compara informações
        - **Escritor**: Gera relatórios e conteúdo estruturado
        - **Revisor**: Valida arquivos e verifica qualidade
        """)

    st.markdown("---")

    # Seção de criação de crew
    st.subheader("🚀 Criar Nova Crew")
    
    # Nome da crew
    crew_name = st.text_input(
        "Nome da Crew",
        placeholder="Ex: Equipe de Análise de Mercado",
        help="Dê um nome descritivo para sua equipe de agentes"
    )
    
    # Descrição da crew
    crew_description = st.text_area(
        "Descrição da Crew",
        placeholder="Descreva o objetivo e especialização desta equipe...",
        help="Explique para que serve esta crew e como ela deve trabalhar"
    )
    
    # Seleção de agentes com interface melhorada
    st.markdown("### 🤖 Seleção de Agentes")
    st.info("💡 **Dica**: Selecione os agentes na ordem que devem trabalhar. O primeiro agente inicia o processo e passa informações para o próximo.")
    
    available_agents = agent_manager.list_available_agent_types()
    
    # Mostrar agentes disponíveis com descrições
    selected_agents = []
    
    for i, agent_type in enumerate(available_agents):
        friendly_name = agent_friendly_names.get(agent_type, agent_type)
        description = agent_descriptions.get(agent_type, "Agente especializado")
        
        # Obter ferramentas do agente
        agent_tools = agent_manager.get_agent_tools(agent_type)
        tools_text = ", ".join(agent_tools) if agent_tools else "Nenhuma ferramenta"
        
        with st.expander(f"{friendly_name} ({agent_type})", expanded=False):
            st.markdown(f"**Descrição:** {description}")
            st.markdown(f"**Ferramentas:** {tools_text}")
            
            if st.checkbox(f"Adicionar {friendly_name} à crew", key=f"agent_{i}"):
                selected_agents.append(agent_type)
    
    # Mostrar ordem dos agentes selecionados
    if selected_agents:
        st.markdown("### 📋 Ordem dos Agentes na Crew")
        st.info("Esta é a ordem em que os agentes trabalharão:")
        
        for i, agent_type in enumerate(selected_agents, 1):
            friendly_name = agent_friendly_names.get(agent_type, agent_type)
            st.markdown(f"{i}. {friendly_name}")
    
    # Seleção de tarefas
    st.markdown("### 📝 Seleção de Tarefas")
    st.info("💡 **Dica**: As tarefas serão executadas na ordem dos agentes. Cada agente executa sua tarefa específica.")
    
    available_tasks = task_manager.list_available_task_types()
    selected_tasks = []
    
    for i, task_type in enumerate(available_tasks):
        friendly_name = task_friendly_names.get(task_type, task_type)
        description = task_descriptions.get(task_type, "Tarefa especializada")
        
        with st.expander(f"{friendly_name} ({task_type})", expanded=False):
            st.markdown(f"**Descrição:** {description}")
            
            if st.checkbox(f"Incluir tarefa {friendly_name}", key=f"task_{i}"):
                selected_tasks.append(task_type)
    
    # Botão de criação
    if st.button("🚀 Criar Crew", type="primary", use_container_width=True):
        if not crew_name:
            st.error("Por favor, forneça um nome para a crew.")
        elif not selected_agents:
            st.error("Por favor, selecione pelo menos um agente.")
        elif not selected_tasks:
            st.error("Por favor, selecione pelo menos uma tarefa.")
        elif len(selected_agents) != len(selected_tasks):
            st.warning("⚠️ **Atenção**: O número de agentes e tarefas deve ser igual. Cada agente executa uma tarefa específica.")
            st.info(f"Agentes selecionados: {len(selected_agents)} | Tarefas selecionadas: {len(selected_tasks)}")
        else:
            try:
                st.info(f"🔄 Criando crew '{crew_name}' com {len(selected_agents)} agentes...")
                
                # Criar a crew
                crew = crew_manager.create_crew_with_tasks(
                    crew_name, selected_agents, selected_tasks, crew_description
                )
                
                if crew:
                    st.success(f"✅ Crew '{crew_name}' criada com sucesso!")
                    
                    # Mostrar resumo da crew criada
                    with st.expander("📋 Resumo da Crew Criada", expanded=True):
                        st.markdown(f"**Nome:** {crew_name}")
                        st.markdown(f"**Descrição:** {crew_description}")
                        st.markdown("**Agentes e Tarefas:**")
                        
                        for i, (agent_type, task_type) in enumerate(zip(selected_agents, selected_tasks), 1):
                            agent_name = agent_friendly_names.get(agent_type, agent_type)
                            task_name = task_friendly_names.get(task_type, task_type)
                            st.markdown(f"{i}. {agent_name} → {task_name}")
                    
                    st.info("🎉 A crew está pronta para execução! Vá para a aba 'Execução' para testá-la.")
                    st.rerun()
                else:
                    st.error("❌ Falha ao criar a crew. Verifique os logs no terminal.")
                    
            except Exception as e:
                st.error(f"❌ Erro ao criar crew: {e}")

    st.markdown("---")

    # Lista de crews existentes
    st.subheader("📋 Crews Existentes")
    
    try:
        crews = crew_manager.get_all_crews()
        
        if not crews:
            st.info("Nenhuma crew foi criada ainda. Crie sua primeira crew acima!")
        else:
            for crew_name, crew in crews.items():
                crew_info = crew_manager.get_crew_info(crew_name)
                
                with st.expander(f"👥 {crew_name}", expanded=False):
                    if crew_info:
                        st.markdown(f"**Descrição:** {crew_info.get('description', 'Sem descrição')}")
                        st.markdown(f"**Agentes:** {len(crew.agents)}")
                        st.markdown(f"**Tarefas:** {len(crew.tasks)}")
                        
                        # Mostrar agentes da crew
                        st.markdown("**Agentes na Crew:**")
                        for i, agent in enumerate(crew.agents, 1):
                            agent_role = getattr(agent, 'role', 'Agente')
                            st.markdown(f"{i}. {agent_role}")
                        
                        # Mostrar tarefas da crew
                        if crew.tasks:
                            st.markdown("**Tarefas da Crew:**")
                            for i, task in enumerate(crew.tasks, 1):
                                task_desc = getattr(task, 'description', 'Tarefa')
                                st.markdown(f"{i}. {task_desc[:50]}...")
                    
                    # Botões de ação
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button(f"🗑️ Deletar {crew_name}", key=f"delete_{crew_name}"):
                            if crew_manager.delete_crew(crew_name):
                                st.success(f"Crew '{crew_name}' deletada!")
                                st.rerun()
                            else:
                                st.error("Erro ao deletar crew")
                    
                    with col2:
                        if st.button(f"▶️ Executar {crew_name}", key=f"execute_{crew_name}"):
                            st.info(f"Vá para a aba 'Execução' para executar a crew '{crew_name}'")
    
    except Exception as e:
        st.error(f"Erro ao carregar crews: {e}")