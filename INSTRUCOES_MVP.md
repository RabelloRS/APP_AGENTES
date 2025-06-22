# 🎯 INSTRUÇÕES DO MVP - APP_AGENTES

## 📋 Visão Geral do MVP

O **MVP (Produto Mínimo Viável)** do APP_AGENTES é um sistema de **análise e comparação de planilhas Excel** especificamente desenvolvido para aplicações em **engenharia civil**.

### 🎯 Objetivo Principal
Comparar automaticamente duas planilhas Excel e identificar:
- **Similaridades** entre dados
- **Diferenças** e inconsistências
- **Padrões** nos dados
- **Recomendações** baseadas na análise

---

## 🚀 Como Usar o Sistema

### 1. Preparação do Ambiente

#### 1.1. Instalação das Dependências
```bash
# Ativar ambiente virtual
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt
```

#### 1.2. Configuração da API
1. Crie um arquivo `.env` na raiz do projeto
2. Adicione sua chave da API OpenAI:
```env
OPENAI_API_KEY=sua_chave_aqui
```

### 2. Executando o Sistema

#### 2.1. Iniciar a Interface
```bash
streamlit run app/main.py
```

#### 2.2. Acessar a Interface
- Abra o navegador em: `http://localhost:8501`
- Verifique se a API está configurada na sidebar (deve aparecer "✅ API configurada")

### 3. Executando uma Análise

#### 3.1. Navegar para a Análise
1. Clique na aba **"Execução"**
2. No dropdown "Selecionar Crew", escolha **"Crew de Análise de Planilhas"**

#### 3.2. Upload dos Arquivos
1. **Arquivo 1**: Clique em "Arquivo Excel 1" e selecione sua primeira planilha
2. **Arquivo 2**: Clique em "Arquivo Excel 2" e selecione sua segunda planilha
3. Aguarde a validação automática dos arquivos

#### 3.3. Seleção das Colunas
- Após o upload, selecione as colunas que deseja comparar em cada arquivo
- As colunas devem conter dados similares (ex: nomes de materiais, códigos, etc.)

#### 3.4. Configuração das Opções
Marque as opções desejadas:
- ✅ **Detectar padrões nos dados**: Análise da estrutura dos dados
- ✅ **Gerar recomendações**: Sugestões baseadas na análise
- ✅ **Relatório detalhado**: Relatório completo para download

#### 3.5. Executar a Análise
- Clique no botão **"🚀 Executar Tarefa"**
- Aguarde o processamento (pode levar alguns segundos)

---

## 📊 Interpretando os Resultados

### 1. Métricas Principais
- **Score Médio**: Percentual médio de similaridade entre os dados
- **Alta Similaridade**: Quantidade de itens com ≥80% de similaridade
- **Média Similaridade**: Quantidade de itens com 50-79% de similaridade
- **Baixa Similaridade**: Quantidade de itens com <50% de similaridade

### 2. Recomendações
O sistema fornece recomendações automáticas como:
- ✅ **Alta similaridade geral** - os dados são muito similares
- ⚠️ **Similaridade moderada** - verificar inconsistências
- ❌ **Baixa similaridade** - possível problema nos dados

### 3. Padrões Detectados
- **Tipo de dados**: Texto, números, datas, etc.
- **Valores únicos**: Quantidade de valores diferentes
- **Valores nulos**: Quantidade de campos vazios
- **Duplicatas**: Quantidade de linhas duplicadas

### 4. Relatório Detalhado
- **Informações dos arquivos**: Estrutura e estatísticas
- **Análise de similaridade**: Métricas detalhadas
- **Top correspondências**: Melhores e piores matches
- **Download**: Botão para baixar o relatório completo

### 5. Tabela de Correspondências
- **Filtro por score**: Ajuste o score mínimo para exibir
- **Original**: Dados do primeiro arquivo
- **Correspondência**: Dados do segundo arquivo
- **Score**: Percentual de similaridade

---

## 🎯 Casos de Uso Práticos

### 1. Comparação de Orçamentos
**Cenário**: Comparar orçamentos de diferentes fornecedores
- **Arquivo 1**: Orçamento do fornecedor A
- **Arquivo 2**: Orçamento do fornecedor B
- **Coluna para comparação**: "Descrição do Material" ou "Código"
- **Resultado**: Identificar diferenças de preços e especificações

### 2. Análise de Variações em Projetos
**Cenário**: Comparar versões diferentes de um projeto
- **Arquivo 1**: Versão inicial do projeto
- **Arquivo 2**: Versão atualizada do projeto
- **Coluna para comparação**: "Item" ou "Descrição"
- **Resultado**: Identificar mudanças e adições

### 3. Controle de Qualidade
**Cenário**: Verificar consistência entre planilhas
- **Arquivo 1**: Planilha de referência
- **Arquivo 2**: Planilha para verificação
- **Coluna para comparação**: "Código" ou "Nome"
- **Resultado**: Detectar erros e inconsistências

---

## 🔧 Exemplo Prático

### Executar o Exemplo Incluído
```bash
python examples/excel_comparison_example.py
```

Este exemplo demonstra:
1. **Criação automática** de planilhas de materiais de construção
2. **Análise completa** de similaridade
3. **Detecção de padrões** nos dados
4. **Geração de relatório** estruturado

### Dados de Exemplo
O exemplo cria duas planilhas com:
- **Arquivo 1**: 10 materiais de construção
- **Arquivo 2**: 12 materiais (incluindo 2 novos)
- **Comparação**: Coluna "Material"

---

## ⚠️ Limitações do MVP

### 1. Tipos de Arquivo
- ✅ Suporta: `.xlsx` e `.xls`
- ❌ Não suporta: `.csv`, `.ods`, outros formatos

### 2. Tamanho dos Arquivos
- **Recomendado**: Até 10.000 linhas por arquivo
- **Máximo**: 50.000 linhas (pode ser lento)

### 3. Tipos de Dados
- ✅ **Texto**: Nomes, descrições, códigos
- ✅ **Números**: Quantidades, preços, medidas
- ⚠️ **Datas**: Funciona, mas melhor como texto
- ❌ **Imagens**: Não suportado

### 4. Análise de Similaridade
- **Algoritmo**: Fuzzy string matching
- **Precisão**: Depende da qualidade dos dados
- **Recomendação**: Use dados limpos e padronizados

---

## 🆘 Solução de Problemas

### Erro: "Chave da API OpenAI não configurada"
**Solução**: 
1. Verifique se o arquivo `.env` existe
2. Confirme se a chave está correta
3. Reinicie o Streamlit

### Erro: "Coluna não encontrada"
**Solução**:
1. Verifique o nome exato da coluna
2. Confirme se o arquivo foi carregado corretamente
3. Use nomes sem espaços ou caracteres especiais

### Erro: "Arquivo inválido"
**Solução**:
1. Verifique se o arquivo é um Excel válido
2. Confirme se não está corrompido
3. Tente abrir o arquivo no Excel primeiro

### Análise muito lenta
**Solução**:
1. Reduza o tamanho dos arquivos
2. Use colunas com menos dados
3. Feche outros programas que consumam memória

---

## 📞 Suporte

### Documentação Adicional
- **README.md**: Visão geral do projeto
- **docs/**: Documentação técnica detalhada
- **examples/**: Exemplos práticos

### Como Reportar Problemas
1. Verifique se o problema não está listado acima
2. Execute o exemplo incluído para testar
3. Abra uma issue no GitHub com:
   - Descrição do problema
   - Passos para reproduzir
   - Arquivos de exemplo (se possível)

---

## 🎉 Próximos Passos

Após dominar o MVP, você pode explorar:
1. **Fase 2**: Integração com normas técnicas (RAG)
2. **Fase 3**: Análise de imagens de patologias
3. **Personalização**: Adaptar para seus casos de uso específicos

**Boa sorte com suas análises! 🚀** 