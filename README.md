# Agentes de Engenharia da Propor - Sistema de Agentes Inteligentes

Um sistema de agentes inteligentes construído com CrewAI e Streamlit para criar, gerenciar e executar tarefas complexas através de múltiplos agentes especializados.

**Desenvolvido pela Propor Engenharia**

## 📞 Informações da Empresa

**Propor Engenharia**  
**Responsável Técnico:** Eng. Civil Rodrigo Emanuel Rabello  
**CREA-RS:** 167.175-D  
**Telefone:** 51 99164-6794  
**Localização:** Nova Petrópolis / RS  
**CNPJ:** 41.556.670/0001-76

## 🚀 Características

- **CrewAI Integration**: Sistema de agentes colaborativos
- **Streamlit Interface**: Interface web moderna e responsiva
- **Multi-Agent System**: Agentes especializados para diferentes tarefas
- **Environment Management**: Configuração segura de chaves de API
- **Best Practices**: Estrutura organizada seguindo padrões Python
- **📱 WhatsApp Integration**: Monitoramento e download automático de arquivos

## 🆕 Novas Funcionalidades

### 📱 WhatsApp - Download de Arquivos
- **Monitoramento de Grupos**: Conecta ao WhatsApp Web e monitora grupos específicos
- **Detecção de Links**: Identifica links de serviços em nuvem (Google Drive, OneDrive, Dropbox, etc.)
- **Download Automático**: Baixa arquivos de múltiplas fontes
- **Renomeação Inteligente**: Adiciona timestamp ao nome dos arquivos
- **Organização por Data**: Organiza arquivos em pastas por data

**Serviços Suportados:**
- Google Drive
- OneDrive
- Dropbox
- MEGA
- MediaFire
- Arquivos anexados diretamente no WhatsApp

## 📋 Pré-requisitos

- Python 3.12+
- Git
- Conta na OpenAI (para chaves de API)
- Chrome/Chromium (para funcionalidade WhatsApp)

## 🛠️ Instalação

### 1. Clone o repositório
```bash
cd Agentes_de_Engenharia_da_Propor
```

### 2. Crie e ative o ambiente virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
```bash
# Copie o template
copy env_template.txt .env

# Edite o arquivo .env com suas chaves de API
# OPENAI_API_KEY=sua_chave_aqui
```

## 🚀 Como usar

### Executar a aplicação Streamlit
```bash
streamlit run app/main.py
```

### Usar a funcionalidade WhatsApp
1. Acesse a aplicação Streamlit
2. Navegue para a aba "📱 WhatsApp"
3. Configure o nome do grupo e pasta de download
4. Conecte ao WhatsApp e execute o monitoramento
5. Baixe os arquivos encontrados

### Executar testes
```bash
pytest tests/
```

### Formatar código
```bash
black .
```

## 📁 Estrutura do Projeto

```
Agentes_de_Engenharia_da_Propor/
├── app/                    # Aplicação principal
│   ├── main.py            # Entry point do Streamlit
│   ├── agents/            # Definições dos agentes
│   ├── crews/             # Configurações das crews
│   └── utils/             # Utilitários
├── tests/                 # Testes unitários
├── docs/                  # Documentação
│   └── WHATSAPP_GUIDE.md # Guia da funcionalidade WhatsApp
├── examples/              # Exemplos de uso
│   └── whatsapp_crew_example.py
├── requirements.txt       # Dependências Python
├── .gitignore            # Arquivos ignorados pelo Git
├── env_template.txt      # Template de variáveis de ambiente
└── README.md             # Este arquivo
```

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` baseado no `env_template.txt`:

- `OPENAI_API_KEY`: Sua chave da API OpenAI
- `ANTHROPIC_API_KEY`: Sua chave da API Anthropic (opcional)
- `DEFAULT_MODEL`: Modelo padrão (ex: gpt-4)
- `DEFAULT_TEMPERATURE`: Temperatura para geração de texto

### Configuração WhatsApp

Para funcionalidade completa do WhatsApp:
- Instale o Chrome/Chromium
- O webdriver será baixado automaticamente
- Configure permissões de escrita na pasta de downloads

## 📚 Documentação

- **[Guia WhatsApp](docs/WHATSAPP_GUIDE.md)**: Documentação completa da funcionalidade WhatsApp
- **[Arquitetura](docs/ARCHITECTURE.md)**: Documentação da arquitetura do sistema
- **[Estrutura do Projeto](docs/PROJECT_STRUCTURE.md)**: Detalhes da estrutura do projeto

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

Se você encontrar algum problema ou tiver dúvidas:
- Abra uma issue no GitHub
- Entre em contato: 51 99164-6794
- Email: suporte@propor.com.br

## 🔄 Atualizações

Para atualizar o projeto:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
``` 