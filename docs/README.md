# Documentação do APP_AGENTES

## Visão Geral

O APP_AGENTES é um sistema de agentes inteligentes construído com CrewAI e Streamlit. O sistema permite criar, gerenciar e executar tarefas complexas através de múltiplos agentes especializados que trabalham em conjunto.

## Arquitetura

### Componentes Principais

1. **AgentManager**: Gerencia a criação e configuração de agentes
2. **CrewManager**: Gerencia crews (equipes) de agentes
3. **Config**: Gerencia configurações do sistema
4. **Streamlit Interface**: Interface web para interação com o sistema

### Estrutura de Agentes

O sistema inclui os seguintes tipos de agentes:

- **Pesquisador**: Realiza pesquisas e coleta informações
- **Analista**: Analisa dados e gera insights
- **Escritor**: Cria conteúdo e relatórios
- **Revisor**: Revisa e valida conteúdo
- **Coordenador**: Coordena tarefas entre agentes

## Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` com as seguintes variáveis:

```env
OPENAI_API_KEY=sua_chave_aqui
ANTHROPIC_API_KEY=sua_chave_aqui
DEFAULT_MODEL=gpt-4
DEFAULT_TEMPERATURE=0.7
DEBUG=True
LOG_LEVEL=INFO
```

## Uso

### Executando a Aplicação

```bash
streamlit run app/main.py
```

### Criando Agentes

```python
from app.agents.agent_manager import AgentManager

agent_manager = AgentManager()
researcher = agent_manager.create_agent("researcher")
```

### Criando Crews

```python
from app.crews.crew_manager import CrewManager

crew_manager = CrewManager(agent_manager)
crew = crew_manager.create_crew("Minha Crew", ["researcher", "analyst"])
```

## Desenvolvimento

### Executando Testes

```bash
pytest tests/
```

### Formatação de Código

```bash
black .
flake8 .
```

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request 