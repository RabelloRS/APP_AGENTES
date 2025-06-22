"""
Exemplo básico de uso do sistema de agentes com configuração YAML
"""

from app.agents.agent_manager import AgentManager
from app.crews.task_manager import TaskManager
from app.crews.crew_manager import CrewManager

def main():
    """Exemplo de uso básico do sistema"""
    
    print("🤖 Iniciando Sistema de Agentes...")
    
    # 1. Inicializar gerenciadores
    agent_manager = AgentManager()
    task_manager = TaskManager()
    crew_manager = CrewManager(agent_manager, task_manager)
    
    # 2. Listar agentes disponíveis
    print("\n📋 Agentes disponíveis:")
    for agent_type in agent_manager.list_available_agent_types():
        info = agent_manager.get_agent_info(agent_type)
        if info:
            print(f"  - {info['name']} ({agent_type})")
    
    # 3. Listar tarefas disponíveis
    print("\n📋 Tarefas disponíveis:")
    for task_type in task_manager.list_available_task_types():
        info = task_manager.get_task_info(task_type)
        if info:
            print(f"  - {task_type}: {info['description'][:50]}...")
    
    # 4. Criar agentes
    print("\n🔧 Criando agentes...")
    researcher = agent_manager.create_agent("researcher")
    analyst = agent_manager.create_agent("analyst")
    writer = agent_manager.create_agent("writer")
    
    if researcher and analyst and writer:
        print("✅ Agentes criados com sucesso!")
    else:
        print("❌ Erro ao criar agentes")
        return
    
    # 5. Criar crew com tarefas
    print("\n👥 Criando crew de pesquisa...")
    crew = crew_manager.create_crew_with_tasks(
        name="Crew de Pesquisa",
        agent_types=["researcher", "analyst", "writer"],
        task_types=["research_task", "analysis_task", "writing_task"],
        description="Crew para pesquisa e análise de dados",
        topic="inteligência artificial"
    )
    
    if crew:
        print("✅ Crew criada com sucesso!")
        print(f"   Agentes: {len(crew.agents)}")
        print(f"   Tarefas: {len(crew.tasks)}")
    else:
        print("❌ Erro ao criar crew")
        return
    
    # 6. Executar crew (comentado para evitar custos de API)
    print("\n🚀 Crew pronta para execução!")
    print("   Descomente a linha abaixo para executar:")
    print("   result = crew_manager.execute_crew('Crew de Pesquisa')")
    
    # result = crew_manager.execute_crew('Crew de Pesquisa')
    # if result:
    #     print(f"✅ Resultado: {result[:200]}...")
    # else:
    #     print("❌ Erro na execução")

if __name__ == "__main__":
    main() 