# 🚀 Instruções de Uso - Agentes de Engenharia da Propor

## 📞 Informações da Empresa

**Propor Engenharia**  
**Responsável Técnico:** Eng. Civil Rodrigo Emanuel Rabello  
**CREA-RS:** 167.175-D  
**Telefone:** 51 99164-6794  
**Localização:** Nova Petrópolis / RS  
**CNPJ:** 41.556.670/0001-76

## ✅ Setup Concluído!

O projeto foi configurado com sucesso! Aqui está o que foi criado:

### 📁 Estrutura do Projeto
```
Agentes de Engenharia da Propor/
├── app/                    # Aplicação principal
│   ├── main.py            # Interface Streamlit
│   ├── agents/            # Gerenciador de agentes
│   ├── crews/             # Gerenciador de crews
│   └── utils/             # Utilitários
├── tests/                 # Testes unitários
├── docs/                  # Documentação
├── venv/                  # Ambiente virtual Python
├── requirements.txt       # Dependências
├── .env                   # Configurações (você precisa editar)
├── run.bat               # Script para executar (Windows)
└── README.md             # Documentação principal
```

### 🔧 Próximos Passos

#### 1. Configurar Chaves de API
Edite o arquivo `.env` e adicione suas chaves de API:

```env
OPENAI_API_KEY=sua_chave_openai_aqui
ANTHROPIC_API_KEY=sua_chave_anthropic_aqui
```

**Como obter as chaves:**
- **OpenAI**: Acesse https://platform.openai.com/api-keys
- **Anthropic**: Acesse https://console.anthropic.com/

#### 2. Executar a Aplicação

**Opção 1 - Script Automático (Recomendado):**
```bash
# Windows
run.bat
```

**Opção 2 - Manual:**
```bash
# Ativar ambiente virtual
venv\Scripts\activate

# Executar aplicação
streamlit run app/main.py
```

#### 3. Acessar a Interface
A aplicação será aberta automaticamente em: **http://localhost:8501**

### 🎯 Funcionalidades Disponíveis

1. **Dashboard**: Visão geral do sistema
2. **Agentes**: Gerenciar e editar agentes especializados
3. **Tarefas**: Visualizar e gerenciar tarefas disponíveis
4. **Tools**: Gerenciar ferramentas e atribuí-las aos agentes
5. **Crews**: Criar e gerenciar equipes de agentes
6. **Execução**: Executar tarefas com as crews

### ✏️ Editando Agentes

A aba **Agentes** permite editar completamente as configurações dos agentes:

#### Como Editar um Agente:
1. Clique na aba **"Agentes"**
2. Expanda o agente desejado
3. Clique em **"✏️ Editar [Nome do Agente]"**
4. Modifique os campos:
   - **Nome do Agente**: Nome exibido na interface
   - **Função**: Papel do agente no sistema
   - **Objetivo**: Meta principal do agente
   - **História**: Background e contexto do agente
   - **Opções Avançadas**: Verbose e delegação
5. Clique em **"💾 Salvar Alterações"**

#### Recursos de Edição:
- ✅ **Salvamento Automático**: Alterações são salvas no arquivo YAML
- ✅ **Backup Automático**: Arquivo original é preservado
- ✅ **Validação**: Campos obrigatórios são verificados
- ✅ **Recriação**: Botão para aplicar mudanças a agentes existentes
- ✅ **Visualização**: Ver configuração atual e backup

#### Importante:
- Alterações no nome podem afetar crews existentes
- Use **"🔄 Recriar"** para aplicar mudanças a agentes já criados
- O arquivo de backup está disponível em `app/config/agents.yaml.backup`

### 🔧 Gerenciando Tools (Ferramentas)

A aba **Tools** permite gerenciar e atribuir ferramentas aos agentes:

#### Como Configurar Tools para um Agente:
1. Clique na aba **"Tools"**
2. Na seção "Agentes e suas Tools", clique em **"⚙️ Configurar Tools"**
3. Selecione as ferramentas desejadas para o agente
4. Clique em **"💾 Salvar Configuração"**
5. Use **"🔄 Recriar Agente"** para aplicar as mudanças

#### Categorias de Tools Disponíveis:
- **📁 Excel**: Ferramentas para manipulação de planilhas
  - Ler Coluna Excel
  - Ler Arquivo Excel
  - Análise de Similaridade Excel
  - Validar Arquivo Excel
- **📁 Análise**: Ferramentas para análise de dados
  - Comparar Similaridade de Texto
  - Detectar Padrões nos Dados
- **📁 Relatórios**: Ferramentas para geração de relatórios
  - Gerar Relatório Excel

#### Recursos de Tools:
- ✅ **Atribuição Flexível**: Cada agente pode ter tools específicas
- ✅ **Descrições Detalhadas**: Informações completas sobre cada ferramenta
- ✅ **Exemplos de Uso**: Código de exemplo para cada tool
- ✅ **Persistência**: Configurações salvas automaticamente
- ✅ **Categorização**: Tools organizadas por categoria

### 🔍 Testando o Sistema

1. Abra a aplicação no navegador
2. Verifique se a API está configurada (sidebar)
3. Teste a criação de agentes
4. Crie uma crew com múltiplos agentes
5. Execute uma tarefa de exemplo

### 🛠️ Desenvolvimento

**Executar testes:**
```bash
venv\Scripts\activate
pytest tests/
```

**Formatar código:**
```bash
venv\Scripts\activate
black .
```

**Verificar qualidade:**
```bash
venv\Scripts\activate
flake8 .
```

### 📚 Recursos Adicionais

- **Documentação**: Veja `docs/README.md`
- **Exemplos**: Consulte o código em `app/`
- **Configurações**: Edite `app/utils/config.py`

### 🆘 Suporte

Se encontrar problemas:

1. Verifique se o Python 3.12+ está instalado
2. Confirme se as chaves de API estão corretas
3. Verifique se o ambiente virtual está ativo
4. Consulte os logs de erro no terminal

### 🎉 Pronto para Usar!

O sistema está configurado e pronto para criar agentes inteligentes com CrewAI e Streamlit!

---

**Dica**: Mantenha o arquivo `.env` seguro e nunca o compartilhe no GitHub. 