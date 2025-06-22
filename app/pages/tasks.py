"""
Gerenciamento de Tarefas - Configuração e Visualização de Tarefas
"""

import streamlit as st
from pathlib import Path

def show_tasks_tab():
    """Exibe a aba de gerenciamento de tarefas"""
    st.header("📋 Gerenciamento de Tarefas")
    st.markdown("### Visualize e configure as tarefas disponíveis no sistema")
    
    # Ajuda geral
    with st.expander("ℹ️ Sobre Tarefas", expanded=False):
        st.info("""
        **O que são tarefas?**
        Tarefas são ações específicas que os agentes podem executar para alcançar objetivos.
        
        **Tipos de tarefas disponíveis:**
        - **research_task**: Pesquisa informações sobre um tópico
        - **analysis_task**: Analisa dados e gera insights
        - **writing_task**: Cria conteúdo e relatórios
        - **review_task**: Revisa e valida resultados
        - **excel_analysis_task**: Analisa planilhas Excel
        
        **Como funcionam:**
        1. Cada tarefa tem um agente responsável
        2. Tarefas podem ser combinadas em crews
        3. As tarefas são executadas sequencialmente
        4. O resultado de uma tarefa pode alimentar a próxima
        """)

    # Lista de tarefas disponíveis
    task_manager = st.session_state.task_manager
    
    # Estatísticas das tarefas
    st.subheader("📊 Estatísticas das Tarefas")
    
    total_tasks = len(task_manager.list_available_task_types())
    tasks_with_agents = sum(1 for task_type in task_manager.list_available_task_types() 
                           if task_manager.get_task_info(task_type, {}).get("agent"))
    
    stats_col1, stats_col2 = st.columns(2)
    
    with stats_col1:
        st.metric("Total de Tarefas", total_tasks)
    
    with stats_col2:
        st.metric("Tarefas com Agentes", tasks_with_agents)
    
    st.markdown("---")
    
    # Lista detalhada de tarefas
    st.subheader("📋 Tarefas Disponíveis")
    
    for task_type in task_manager.list_available_task_types():
        info = task_manager.get_task_info(task_type) or {}
        description = info.get("description", "-")
        expected_output = info.get("expected_output", "-")
        agent_type = info.get("agent", "-")
        
        # Determinar categoria da tarefa
        category = "📊 Análise"
        if "research" in task_type:
            category = "🔍 Pesquisa"
        elif "writing" in task_type:
            category = "✍️ Escrita"
        elif "review" in task_type:
            category = "✅ Revisão"
        elif "excel" in task_type:
            category = "📈 Excel"

        with st.expander(f"{category} {task_type}", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Descrição:** {description}")
                st.write(f"**Saída Esperada:** {expected_output}")
                st.write(f"**Agente Responsável:** {agent_type}")
                
                # Mostrar parâmetros se existirem
                if "parameters" in info:
                    st.write("**Parâmetros:**")
                    for param, desc in info["parameters"].items():
                        st.write(f"  - `{param}`: {desc}")
            
            with col2:
                # Status do agente responsável
                if agent_type != "-":
                    agent_manager = st.session_state.agent_manager
                    agent_info = agent_manager.get_agent_info(agent_type)
                    if agent_info:
                        st.success(f"✅ Agente '{agent_info.get('name', agent_type)}' disponível")
                    else:
                        st.error(f"❌ Agente '{agent_type}' não encontrado")
                else:
                    st.warning("⚠️ Nenhum agente atribuído")
                
                # Botão para ver detalhes
                if st.button(f"Ver Detalhes {task_type}", key=f"details_{task_type}"):
                    st.json(info)

    # Informações sobre configuração
    st.markdown("---")
    st.subheader("ℹ️ Informações sobre Configuração")
    
    info_col1, info_col2 = st.columns(2)
    
    with info_col1:
        st.info("""
        **Arquivo de Configuração:**
        `app/config/tasks.yaml`
        
        **Estrutura de uma tarefa:**
        ```yaml
        task_name:
          description: "Descrição da tarefa"
          expected_output: "O que a tarefa deve retornar"
          agent: "tipo_do_agente"
          parameters:
            param1: "Descrição do parâmetro"
        ```
        """)
    
    with info_col2:
        st.info("""
        **Como adicionar novas tarefas:**
        1. Edite o arquivo `tasks.yaml`
        2. Defina a descrição e saída esperada
        3. Atribua um agente responsável
        4. Recarregue as configurações
        5. A nova tarefa estará disponível
        """)
    
    # Visualizar configuração atual
    with st.expander("📄 Visualizar Configuração Atual"):
        try:
            with open("app/config/tasks.yaml", "r", encoding="utf-8") as f:
                current_config = f.read()
            st.code(current_config, language="yaml")

            # Verificar se existe backup
            backup_path = "app/config/tasks.yaml.backup"
            if Path(backup_path).exists():
                st.info("✅ Backup do arquivo original disponível")
                if st.button("📋 Ver Backup"):
                    with open(backup_path, "r", encoding="utf-8") as f:
                        backup_content = f.read()
                    st.code(backup_content, language="yaml")
            else:
                st.info("ℹ️ Nenhum backup encontrado (primeira edição)")

        except Exception as e:
            st.error(f"Erro ao ler arquivo de configuração: {e}")

    # Exemplos de uso
    st.markdown("---")
    st.subheader("💡 Exemplos de Uso")
    
    examples = [
        {
            "title": "Pesquisa Completa",
            "description": "Pesquisar sobre um tópico e gerar relatório",
            "tasks": ["research_task", "analysis_task", "writing_task"],
            "agents": ["researcher", "analyst", "writer"]
        },
        {
            "title": "Análise de Dados",
            "description": "Analisar dados e gerar insights",
            "tasks": ["analysis_task", "writing_task"],
            "agents": ["analyst", "writer"]
        },
        {
            "title": "Análise de Planilhas",
            "description": "Comparar e analisar planilhas Excel",
            "tasks": ["excel_analysis_task"],
            "agents": ["excel_analyst"]
        }
    ]
    
    for example in examples:
        with st.expander(f"📋 {example['title']}", expanded=False):
            st.write(f"**Descrição:** {example['description']}")
            st.write(f"**Tarefas:** {', '.join(example['tasks'])}")
            st.write(f"**Agentes:** {', '.join(example['agents'])}")
            
            if st.button(f"Ver Detalhes - {example['title']}", key=f"example_{example['title']}"):
                st.info("Esta funcionalidade será implementada em breve") 