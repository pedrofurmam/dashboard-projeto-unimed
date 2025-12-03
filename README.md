# Dashboard de Gestão - Unimed

Este projeto é um dashboard interativo desenvolvido em Python utilizando a biblioteca **Streamlit**. O objetivo é fornecer visualizações estratégicas sobre a Rede Assistencial, Farmácia Central e Almoxarifado de Laboratório, permitindo o acompanhamento de KPIs e consumo de materiais.

## 📋 Funcionalidades

O dashboard é dividido em páginas temáticas para facilitar a navegação e análise:

### 🏠 Página Inicial (`Home.py`)
- Visão geral do sistema.
- Navegação centralizada para os módulos do dashboard.

### 🏥 1. Rede Assistencial (`pages/1_Rede_Assistencial.py`)
- Monitoramento de unidades operacionais.
- Indicadores de desempenho (KPIs) das unidades.
- Análise de riscos e conformidade.

### 💊 2. Farmácia Central (`pages/2_Farmacia_Central.py`)
- Gestão de estoque e consumo da farmácia.
- Visualização de curvas de consumo.
- Tabelas detalhadas com formatação condicional para itens críticos.

### 🧪 3. Almoxarifado Laboratório (`pages/3_Almoxarifado_Laboratorio.py`)
- Controle de insumos laboratoriais.
- Análise de movimentação de materiais.
- Relatórios visuais de estoque.

## 🛠️ Tecnologias Utilizadas

- **[Python 3.x](https://www.python.org/)**: Linguagem base do projeto.
- **[Streamlit](https://streamlit.io/)**: Framework para criação do dashboard web.
- **[Pandas](https://pandas.pydata.org/)**: Manipulação e análise de dados.
- **[Plotly](https://plotly.com/python/)**: Criação de gráficos interativos.
- **[Scikit-learn](https://scikit-learn.org/)**: Utilizado para normalização de dados (MinMaxScaler).

## 📂 Estrutura do Projeto

```
dashboard/
├── Home.py                        # Página principal da aplicação
├── style_utils.py                 # Funções auxiliares de estilo e componentes visuais
├── pages/                         # Páginas adicionais do dashboard
│   ├── 1_Rede_Assistencial.py
│   ├── 2_Farmacia_Central.py
│   └── 3_Almoxarifado_Laboratorio.py
├── icone-unimed.png               # Ícone da aplicação
├── logounimed.png                 # Logo da Unimed
├── logoutfpr.png                  # Logo da UTFPR
└── .gitignore                     # Arquivos ignorados pelo Git (ex: CSVs)
```

## 🚀 Como Executar o Projeto

### Pré-requisitos

Certifique-se de ter o Python instalado em sua máquina. Em seguida, instale as bibliotecas necessárias:

```bash
pip install streamlit pandas plotly scikit-learn numpy
```

### Arquivos de Dados (CSVs)

⚠️ **Importante:** Os arquivos de dados (`.csv`) não estão incluídos neste repositório por questões de privacidade e tamanho. Para executar o dashboard, você deve colocar os seguintes arquivos na raiz do projeto:

- `df_consolidado_total_consumido.csv`
- `df_dashboard_almoxarifado.csv`
- `df_dashboard_centros_kpis.csv`
- `df_dashboard_completo.csv`
- `df_dashboard_farmacia.csv`
- `df_dashboard_risco_completo_v3.csv`

### Executando a Aplicação

No terminal, navegue até a pasta do projeto e execute o comando:

```bash
streamlit run Home.py
```

O dashboard será aberto automaticamente no seu navegador padrão.

## 🎨 Personalização Visual

O projeto utiliza um módulo `style_utils.py` para manter a consistência visual, aplicando as cores e identidade visual da Unimed (Verde #00995D) em tabelas, cabeçalhos e gráficos.

---
**Desenvolvido para análise estratégica de dados da Unimed.**
