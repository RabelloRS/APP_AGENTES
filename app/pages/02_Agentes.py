"""
Gerenciamento de Agentes - Criação e Configuração de Agentes Inteligentes
"""

import streamlit as st
from pathlib import Path

def show_agent_edit_form(editing_agent, manager):
    """Exibe o formulário de edição de um agente"""
    st.subheader(f"✏️ Editando Agente: {editing_agent}")
    
    # Ajuda para edição
    with st.expander("ℹ️ Como editar um agente", expanded=False):
        st.info("""
        **Campos obrigatórios:**
        - **Nome**: Identificador único do agente
        - **Função**: Papel específico do agente no sistema
        - **Objetivo**: Meta principal que o agente deve alcançar
        - **História**: Contexto e personalidade do agente
        
        **Opções avançadas:**
        - **Verbose**: Mostra detalhes durante execução
        - **Permitir Delegação**: Permite que o agente delegue tarefas
        
        **Importante:** Alterar o nome pode afetar crews existentes!
        """)

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
            help="Nome único para identificar o agente"
        )
        new_role = st.text_input(
            "Função",
            value=current_info.get("role", ""),
            key=f"role_{editing_agent}",
            help="Papel específico do agente (ex: Analista de Dados, Pesquisador)"
        )
        new_goal = st.text_area(
            "Objetivo",
            value=current_info.get("goal", ""),
            key=f"goal_{editing_agent}",
            help="Meta principal que o agente deve alcançar"
        )
        new_backstory = st.text_area(
            "História",
            value=current_info.get("backstory", ""),
            key=f"backstory_{editing_agent}",
            help="Contexto, experiência e personalidade do agente"
        )

        # Opções avançadas
        with st.expander("⚙️ Opções Avançadas"):
            new_verbose = st.checkbox(
                "Verbose",
                value=current_info.get("verbose", True),
                key=f"verbose_{editing_agent}",
                help="Mostra detalhes durante a execução das tarefas"
            )
            new_allow_delegation = st.checkbox(
                "Permitir Delegação",
                value=current_info.get("allow_delegation", False),
                key=f"delegation_{editing_agent}",
                help="Permite que o agente delegue tarefas para outros agentes"
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
            if st.form_submit_button("💾 Salvar Alterações", type="primary"):
                # Validar campos obrigatórios
                if not new_name or not new_role or not new_goal or not new_backstory:
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


def show_agent_entry(agent_type, info, editing_agent, manager, tools_manager):
    """Exibe uma entrada de agente na lista"""
    name = info.get("name", agent_type)
    role = info.get("role", "-")
    goal = info.get("goal", "-")
    agent_tools = manager.get_agent_tools(agent_type)

    with st.expander(f"🤖 {name} ({agent_type})", expanded=False):
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
                        st.write(f"  - {tool_info['name']} ({tool_info['category']})")
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


def show_agents_tab():
    """Exibe a aba de gerenciamento de agentes"""
    st.header("🤖 Gerenciamento de Agentes")
    st.markdown("### Crie, configure e gerencie seus agentes inteligentes")
    
    # Ajuda geral
    with st.expander("ℹ️ Sobre Agentes Inteligentes", expanded=False):
        st.info("""
        **O que são agentes?**
        Agentes são entidades inteligentes que executam tarefas específicas usando IA.
        
        **Tipos de agentes disponíveis:**
        - **Researcher**: Pesquisa informações e dados
        - **Analyst**: Analisa dados e gera insights
        - **Writer**: Cria conteúdo e relatórios
        - **Reviewer**: Revisa e valida resultados
        - **Excel Analyst**: Especializado em análise de planilhas
        
        **Como usar:**
        1. **Editar**: Modifique configurações dos agentes
        2. **Recriar**: Aplique mudanças a agentes existentes
        3. **Testar**: Verifique se o agente funciona corretamente
        4. **Configurar Tools**: Atribua ferramentas específicas
        """)

    # Lista de agentes disponíveis dinamicamente
    manager = st.session_state.agent_manager

    # Verificar se há um agente sendo editado
    editing_agent = st.session_state.get("editing_agent", None)

    if editing_agent:
        show_agent_edit_form(editing_agent, manager)
        st.markdown("---")

    # Lista de agentes
    st.subheader("📋 Agentes Disponíveis")

    tools_manager = st.session_state.tools_manager
    for agent_type in manager.list_available_agent_types():
        info = manager.get_agent_info(agent_type) or {}
        show_agent_entry(agent_type, info, editing_agent, manager, tools_manager)

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

    # Estatísticas dos agentes
    st.markdown("---")
    st.subheader("📊 Estatísticas dos Agentes")
    
    agent_stats = {
        "Total de Agentes": len(manager.list_available_agent_types()),
        "Agentes com Tools": sum(1 for agent_type in manager.list_available_agent_types() 
                               if manager.get_agent_tools(agent_type)),
        "Agentes Verbose": sum(1 for agent_type in manager.list_available_agent_types() 
                             if manager.get_agent_info(agent_type, {}).get("verbose", False)),
        "Agentes com Delegação": sum(1 for agent_type in manager.list_available_agent_types() 
                                   if manager.get_agent_info(agent_type, {}).get("allow_delegation", False))
    }
    
    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
    
    with stats_col1:
        st.metric("Total", agent_stats["Total de Agentes"])
    
    with stats_col2:
        st.metric("Com Tools", agent_stats["Agentes com Tools"])
    
    with stats_col3:
        st.metric("Verbose", agent_stats["Agentes Verbose"])
    
    with stats_col4:
        st.metric("Com Delegação", agent_stats["Agentes com Delegação"]) 