"""
Aplicação principal do sistema de agentes inteligentes
"""

import os
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime
from app.agents.agent_manager import AgentManager
from app.crews.crew_manager import CrewManager
from app.crews.task_manager import TaskManager
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
    if 'task_manager' not in st.session_state:
        st.session_state.task_manager = TaskManager()
    if 'crew_manager' not in st.session_state:
        st.session_state.crew_manager = CrewManager(
            st.session_state.agent_manager, 
            st.session_state.task_manager
        )

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

    # Tabs principais
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["🏠 Dashboard", "🤖 Agentes", "📋 Tarefas", "👥 Crews", "📊 Execução"]
    )

    with tab1:
        show_dashboard()

    with tab2:
        show_agents_tab()

    with tab3:
        show_tasks_tab()

    with tab4:
        show_crews_tab()

    with tab5:
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
    for agent_type in manager.list_available_agent_types():
        info = manager.get_agent_info(agent_type) or {}
        name = info.get("name", agent_type)
        role = info.get("role", "-")
        goal = info.get("goal", "-")
        
        with st.expander(f"🤖 {name}"):
            st.write(f"**Função:** {role}")
            st.write(f"**Objetivo:** {goal}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button(
                    f"Configurar {name}", key=f"config_{agent_type}"
                ):
                    if not manager.get_agent(agent_type):
                        agent = manager.create_agent(agent_type)
                        if agent:
                            st.success(f"Agente {name} criado com sucesso!")
                        else:
                            st.error(f"Erro ao criar agente {name}")
                    else:
                        st.info(f"Agente {name} já existe")

            with col2:
                if st.button(f"Testar {name}", key=f"test_{agent_type}"):
                    st.info(f"Teste do agente {name} em desenvolvimento")


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
                    crew_name, selected_agents, selected_tasks, crew_description, **task_params
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
                topic="dados de vendas"
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
                topic="inteligência artificial"
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
            file1 = st.file_uploader("Arquivo Excel 1", type=["xlsx", "xls"], key="excel1")
            if file1:
                # Validar arquivo 1
                from app.utils.tools import validate_excel_file
                import tempfile
                import os
                
                with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                    tmp_file.write(file1.getbuffer())
                    tmp_path = tmp_file.name
                
                validation1 = validate_excel_file(tmp_path)
                os.unlink(tmp_path)  # Limpar arquivo temporário
                
                if validation1["is_valid"]:
                    st.success(f"✅ Arquivo válido: {validation1['total_rows']} linhas, {validation1['total_columns']} colunas")
                    column1 = st.selectbox("Selecionar coluna do Arquivo 1", validation1["columns"])
                else:
                    st.error(f"❌ Erro no arquivo: {validation1['error']}")
                    column1 = None
            else:
                column1 = None
        
        with col2:
            st.write("**Arquivo 2**")
            file2 = st.file_uploader("Arquivo Excel 2", type=["xlsx", "xls"], key="excel2")
            if file2:
                # Validar arquivo 2
                with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                    tmp_file.write(file2.getbuffer())
                    tmp_path = tmp_file.name
                
                validation2 = validate_excel_file(tmp_path)
                os.unlink(tmp_path)  # Limpar arquivo temporário
                
                if validation2["is_valid"]:
                    st.success(f"✅ Arquivo válido: {validation2['total_rows']} linhas, {validation2['total_columns']} colunas")
                    column2 = st.selectbox("Selecionar coluna do Arquivo 2", validation2["columns"])
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
                        import tempfile
                        import os
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp1:
                            tmp1.write(file1.getbuffer())
                            tmp1_path = tmp1.name
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp2:
                            tmp2.write(file2.getbuffer())
                            tmp2_path = tmp2.name
                        
                        # Executar análise completa
                        from app.utils.tools import analyze_excel_similarity, detect_data_patterns, generate_excel_report
                        
                        # Análise de similaridade
                        analysis_results = analyze_excel_similarity(tmp1_path, tmp2_path, column1, column2)
                        
                        # Detectar padrões se solicitado
                        if include_patterns:
                            analysis_results["file1_patterns"] = detect_data_patterns(tmp1_path, column1)
                            analysis_results["file2_patterns"] = detect_data_patterns(tmp2_path, column2)
                        
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
                                f"{analysis_results['similarity_analysis']['average_score']:.1f}%"
                            )
                        
                        with col2:
                            st.metric(
                                "Alta Similaridade", 
                                analysis_results['similarity_analysis']['high_similarity_count']
                            )
                        
                        with col3:
                            st.metric(
                                "Média Similaridade", 
                                analysis_results['similarity_analysis']['medium_similarity_count']
                            )
                        
                        with col4:
                            st.metric(
                                "Baixa Similaridade", 
                                analysis_results['similarity_analysis']['low_similarity_count']
                            )
                        
                        # Recomendações
                        if include_recommendations:
                            st.subheader("💡 Recomendações")
                            for rec in analysis_results['recommendations']:
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
                                mime="text/plain"
                            )
                        
                        # Detalhes das correspondências
                        st.subheader("🔍 Detalhes das Correspondências")
                        
                        # Filtro por score
                        min_score = st.slider("Score mínimo para exibir", 0, 100, 50)
                        
                        matches = analysis_results['detailed_matches']
                        filtered_matches = {k: v for k, v in matches.items() if v['score'] >= min_score}
                        
                        if filtered_matches:
                            # Criar DataFrame para exibição
                            import pandas as pd
                            df_matches = pd.DataFrame([
                                {
                                    'Original': original,
                                    'Correspondência': match_info['match'],
                                    'Score': f"{match_info['score']:.1f}%"
                                }
                                for original, match_info in filtered_matches.items()
                            ])
                            
                            st.dataframe(df_matches, use_container_width=True)
                        else:
                            st.info("Nenhuma correspondência encontrada com o score mínimo selecionado.")
                        
                    except Exception as e:
                        st.error(f"❌ Erro durante a análise: {str(e)}")
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
