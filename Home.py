import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import base64
import os
import textwrap

# Configuração inicial da página, obrigatório ser o primeiro comando Streamlit
st.set_page_config(
    page_title="Página inicial",
    page_icon="icone-unimed.png",
    layout="wide",
    initial_sidebar_state="expanded",
    
)

# Função responsável por exibir o cabeçalho com as logos
import textwrap

def exibir_cabecalho():
    def get_img_as_base64(file):
        try:
            with open(file, "rb") as f:
                data = f.read()
            return base64.b64encode(data).decode()
        except Exception:
            return None

    # Define o caminho das imagens dinamicamente
    import os
    # Tenta obter o diretório atual do script
    try:
        dir_atual = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        dir_atual = os.getcwd()
    
    # Busca as imagens no diretório correto
    if dir_atual.endswith("pages"):
        path_unimed = os.path.join(dir_atual, "..", "logounimed.png")
        path_utfpr = os.path.join(dir_atual, "..", "logoutfpr.png")
    else:
        path_unimed = os.path.join(dir_atual, "logounimed.png")
        path_utfpr = os.path.join(dir_atual, "logoutfpr.png")

    img_unimed = get_img_as_base64(path_unimed) 
    img_utfpr = get_img_as_base64(path_utfpr) 

    src_unimed = f"data:image/png;base64,{img_unimed}" if img_unimed else ""
    src_utfpr = f"data:image/png;base64,{img_utfpr}" if img_utfpr else ""

    # Estrutura HTML do cabeçalho
    header_html = f"""
    <div style="
        background-color: #00995D; 
        padding: 28px 15px 28px 15px; 
        border-radius: 16px; 
        display: flex; 
        align-items: center; 
        justify-content: space-between; 
        margin-bottom: 32px;
        min-height: 120px;
    ">
        <div style="flex: 1;">
            <img src="{src_unimed}" style="height: 90px; object-fit: contain;">
        </div>
        <div style="flex: 2; text-align: center;">
            <h2 style="color: white; margin: 0; padding: 0; font-family: 'Trebuchet MS', sans-serif; font-size: 2.8rem; letter-spacing: 1px;">
                Monitoramento de Desperdícios
            </h2>
        </div>
        <div style="flex: 1; text-align: right;">
            <img src="{src_utfpr}" style="height: 90px; object-fit: contain;">
        </div>
    </div>
    """
    
    # Renderiza o HTML removendo a indentação extra
    st.markdown(textwrap.dedent(header_html), unsafe_allow_html=True)

# Exibir
exibir_cabecalho()

# Aplica estilos CSS personalizados
def aplicar_estilo_unimed():
    st.markdown("""
        <style>
        /* 1. Estilo dos CARDS de KPI (Métricas) */
        [data-testid="stMetric"] {
            background-color: #E8F5E9; /* Verde muito claro Unimed */
            border-left: 5px solid #00995D; /* Barra verde escura na esquerda */
            padding: 15px;
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        /* Aumentar tamanho do texto dos indicadores (Rótulo) */
        [data-testid="stMetricLabel"], 
        [data-testid="stMetricLabel"] > div,
        [data-testid="stMetricLabel"] p {
            font-size: 1.8rem !important;
            font-weight: bold !important;
        }
        
        /* Aumentar tamanho do Valor numérico */
        [data-testid="stMetricValue"],
        [data-testid="stMetricValue"] > div {
            font-size: 3.5rem !important;
        }
        
        /* 2. Estilo dos TÍTULOS das Seções (h3) */
        h3 {
            border-bottom: 2px solid #00995D;
            padding-bottom: 10px;
            color: #005533;
        }

        /* Estilo para as linhas horizontais (---) */
        hr {
            border-color: #00995D !important;
            background-color: #00995D !important;
            height: 2px !important;
            opacity: 1 !important;
        }
        
        /* 3. Ajuste do Espaçamento do Topo (A CORREÇÃO ESTÁ AQUI) */
        /* Aumentei de 2rem para 4rem para dar espaço ao menu do Streamlit */
        .block-container {
            padding-top: 4rem; 
            padding-bottom: 3rem;
        }
        
        /* 4. Esconder o menu do Streamlit (Opcional - se quiser limpar totalmente) */
        /* Descomente as linhas abaixo se quiser sumir com o menu de 3 pontinhos */
        /*
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;} 
        */
        </style>
    """, unsafe_allow_html=True)

# Chame a função logo após o cabeçalho
aplicar_estilo_unimed()

# Ajustes de CSS para a barra lateral
st.markdown("""
    <style>
    /* Mantém a largura padrão do sidebar */
    [data-testid="stSidebar"] {
        width: 320px !important;
        background-color: #E8F5E9 !important;
    }
    
    /* Estilo dos links de navegação (Nomes das páginas) */
    [data-testid="stSidebarNav"] span {
        color: #00995D !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
    }
    
    /* Garante que os elementos do sidebar não sejam truncados */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        width: 100% !important;
    }
    
    /* Forçar altura e permitir múltiplas linhas no multiselect */
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] input {
        min-height: 60px !important;
        line-height: 1.5 !important;
    }
    
    /* Quebra de linha no label */
    [data-testid="stSidebar"] .stMultiSelect label {
        white-space: normal !important;
        display: block !important;
        overflow: visible !important;
        word-break: break-word !important;
        line-height: 1.4 !important;
    }
    
    /* Tags com quebra de linha */
    [data-testid="stSidebar"] [data-baseweb="tag"] {
        white-space: normal !important;
        word-break: break-word !important;
        line-height: 1.3 !important;
        flex-wrap: wrap !important;
    }
    
    /* Container do input */
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] > div {
        flex-wrap: wrap !important;
    }
    </style>
""", unsafe_allow_html=True)

# Título da página
st.title("📊 Visão Geral dos Centros de Custos")
st.markdown("---")

# Carrega os dados com cache para otimizar performance
@st.cache_data
def carregar_dados():
    try:
        df_completo = pd.read_csv('df_dashboard_completo.csv')
        df_kpis = pd.read_csv('df_dashboard_centros_kpis.csv')
        df_farmacia = pd.read_csv('df_dashboard_farmacia.csv')
        df_almox = pd.read_csv('df_dashboard_almoxarifado.csv')
        # Novo arquivo para risco logarítmico (agora usando o arquivo correto com nomes padronizados)
        df_risco_log = pd.read_csv('df_dashboard_risco_completo_v3.csv')
        # Novo arquivo consolidado com consumo total
        df_consolidado = pd.read_csv('df_consolidado_total_consumido.csv')
        return df_completo, df_kpis, df_farmacia, df_almox, df_risco_log, df_consolidado
    except FileNotFoundError as e:
        st.error(f"Erro ao encontrar arquivo: {e}")
        return None, None, None, None, None, None

# Carrega os dataframes
df_completo, df_kpis, df_farmacia, df_almox, df_risco_log, df_consolidado = carregar_dados()


# Mapeamento para legendas mais amigáveis
legenda_map = {
    "1. Farmácia Central (Gigante)": "Farmácia Central",
    "2. Almoxarifado Lab (Estoque)": "Almoxarifado Laboratório",
    "3. Rede Assistencial (Operação)": "Outros Centros",
}

# Mapeamento inverso (para converter de volta aos valores originais)
legenda_map_inverso = {v: k for k, v in legenda_map.items()}

# Configuração da barra lateral e filtros
st.sidebar.header("🎛️ Filtros Globais")

# Filtro de seleção de ano
if 'ano' in df_completo.columns:
    anos_disponiveis = sorted(df_completo['ano'].unique(), reverse=True)
    # Mudamos de selectbox para multiselect
    # default=anos_disponiveis faz com que todos venham marcados inicialmente
    ano_selecionado = st.sidebar.multiselect(
        "Selecione o(s) Ano(s):", 
        anos_disponiveis, 
        default=anos_disponiveis
    )
else:
    st.sidebar.error("Coluna 'ano' não encontrada.")
    ano_selecionado = []

# Filtro de mês, dependente do ano selecionado
if 'mes' in df_completo.columns and ano_selecionado:
    # Filtra os meses disponíveis APENAS nos anos que foram selecionados
    # Note o uso de .isin() em vez de ==
    meses_disponiveis = sorted(df_completo[df_completo['ano'].isin(ano_selecionado)]['mes'].unique())
    
    mes_selecionado = st.sidebar.multiselect(
        "Selecione o(s) Mês(es):", 
        meses_disponiveis, 
        default=meses_disponiveis
    )
else:
    mes_selecionado = []

# Filtro de macro perfil
if 'macro_perfil' in df_completo.columns:
    perfis_disponiveis = df_completo['macro_perfil'].unique()
    # Mapear os valores para legenda legível
    perfis_legenda = [legenda_map.get(perfil, perfil) for perfil in perfis_disponiveis]
    # Multiselect com valores legíveis, mas convertendo de volta aos originais
    perfil_selecionado_legenda = st.sidebar.multiselect(
        "Filtrar Macro Perfil:", 
        perfis_legenda,
        default=perfis_legenda
    )
    # Converter de volta aos valores originais para filtro
    perfil_selecionado = [legenda_map_inverso.get(p, p) for p in perfil_selecionado_legenda]
else:
    perfil_selecionado = []

# Aplica os filtros selecionados aos dados
# Verifica se o usuário selecionou pelo menos um item em cada filtro
if ano_selecionado and mes_selecionado and perfil_selecionado:
    df_filtrado = df_completo[
        (df_completo['ano'].isin(ano_selecionado)) &     # MUDANÇA AQUI: .isin()
        (df_completo['mes'].isin(mes_selecionado)) &
        (df_completo['macro_perfil'].isin(perfil_selecionado))
    ]
else:
    df_filtrado = pd.DataFrame() # Cria vazio se limpar todos os filtros

# Informações sobre o projeto na barra lateral
with st.sidebar.expander("ℹ️ Sobre o Projeto"):
    st.write("""
    **Projeto - Ciência de Dados**
    **Tema:** Inteligência de Custos Hospitalares
    
    **Metodologia:**
    - 🧹 Limpeza de Ruído (Consumo vs Perda)
    - 🤖 Clusterização em 2 Camadas (K-Means)
    - 📊 Detecção de Outliers (Farmácia/Almox.)
    
    **Objetivo:** Identificar padrões de desperdício e gerar planos de ação automáticos.
    """)

# Exibição dos indicadores principais (KPIs)
# Ajuste no título para mostrar "Vários Anos" se for o caso
if len(ano_selecionado) > 1:
    titulo_periodo = "Período Selecionado"
elif len(ano_selecionado) == 1:
    titulo_periodo = str(ano_selecionado[0])
else:
    titulo_periodo = "Nenhum Período"

#st.subheader(f"Visão Geral - {titulo_periodo}")

if not df_filtrado.empty:
    # Cálculos
    total_desperdicio = df_filtrado['vl_estoque'].sum()
    qtd_itens = df_filtrado['qt_estoque'].sum()
    qtd_centros = df_filtrado['ds_centro_custo'].nunique()

    # Cards
    col1, col2, col3 = st.columns(3)

    with col1:
        valor_formatado = f"R$ {total_desperdicio:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        st.metric("💰 Valor Desperdiçado", valor_formatado)
    with col2:
        valor_formatado_itens = f"{qtd_itens:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
        st.metric("📦 Quantidade de Itens", valor_formatado_itens)
    with col3:
        st.metric("🏥 Centros Afetados", f"{qtd_centros} setores")
else:
    st.warning("⚠️ Nenhum dado encontrado. Por favor, selecione pelo menos um Ano, um Mês e um Perfil nos filtros laterais.")

st.markdown("---")


# Gráficos e visualizações da página inicial

if not df_filtrado.empty:
    st.markdown('<span style="font-size:2rem; font-weight:600">📈 Análise Gráfica</span>', unsafe_allow_html=True)

    # CSS global para cards de gráficos e tabelas
    st.markdown("""
    <style>
    /* Estilo para todos os elementos que contém gráficos Plotly */
    div[data-testid="stVerticalBlock"]:has(> div > div.js-plotly-plot) {
        background-color: #E8F5E9;
        border-radius: 12px;
        padding: 32px 24px;
        border-left: 8px solid #00995D;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.07);
        margin-bottom: 24px;
    }
    
    /* Estilo para cards de gráficos dentro de expanders */
    .stExpander > div > div > div[data-testid="stVerticalBlock"] > div:has(div.js-plotly-plot):first-child {
        background-color: #E8F5E9;
        border-radius: 12px;
        padding: 32px 24px;
        border-left: 8px solid #00995D;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.07);
        margin-bottom: 24px;
    }
    
    /* Estilo para cards de tabelas dentro de expanders */
    .stExpander > div > div > div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stDataFrame"]) {
        background-color: #E8F5E9 !important;
        border-radius: 12px;
        padding: 32px 24px;
        border-left: 8px solid #00995D;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.07);
        margin-bottom: 24px;
    }
    
    /* Força o fundo verde em todos os elementos da tabela */
    .stExpander div[data-testid="stDataFrame"] {
        background-color: #E8F5E9 !important;
    }
    
    .stExpander div[data-testid="stDataFrame"] > div {
        background-color: #E8F5E9 !important;
    }
    
    .stExpander div[data-testid="stDataFrame"] table {
        background-color: #E8F5E9 !important;
    }
    
    .stExpander div[data-testid="stDataFrame"] thead tr th {
        background-color: #C8E6C9 !important;
    }
    
    .stExpander div[data-testid="stDataFrame"] tbody tr td {
        background-color: #E8F5E9 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Gráfico de distribuição por macro perfil
    # Agrupando os dados para o gráfico de pizza
    df_perfil = df_filtrado.groupby('macro_perfil')['vl_estoque'].sum().reset_index()
    
    df_perfil['macro_perfil_legenda'] = df_perfil['macro_perfil'].map(legenda_map).fillna(df_perfil['macro_perfil'])
   
    
    fig_pizza = px.pie(
        df_perfil,
        values='vl_estoque',
        names='macro_perfil_legenda',
        title="<b>Distribuição do Desperdício por Perfil (Onde está o dinheiro desperdiçado?)</b>",
        hole=0.4,
        color='macro_perfil_legenda',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig_pizza.update_traces(textinfo='percent', textposition='inside')
    fig_pizza.update_layout(
        height=550,
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            x=1,
            y=0.5,
            xanchor='left',
            font=dict(size=26, color='#444')
        ),
        title_font_size=24
    )
    
    # Card estilizado para o gráfico de pizza
    with st.container():
        st.plotly_chart(fig_pizza, use_container_width=True)

    # Gráfico comparativo: Consumo vs Desperdício
    # Pegando os 10 centros que mais desperdiçaram
    if df_consolidado is not None and not df_consolidado.empty:
        # Carregar dados consolidados e ordenar pelos 10 maiores desperdícios
        df_consolidado_top10 = df_consolidado.nlargest(10, 'desperdicio_total')[['ds_centro_custo', 'desperdicio_total', 'valor_consumido_total']].copy()
        
        # Renomear colunas para melhor legibilidade no gráfico
        df_consolidado_melted = df_consolidado_top10.melt(
            id_vars=['ds_centro_custo'],
            value_vars=['valor_consumido_total', 'desperdicio_total'],
            var_name='Tipo',
            value_name='Valor'
        )
        
        # Mapeamento para legenda amigável
        tipo_map = {
            'valor_consumido_total': 'Consumo Total',
            'desperdicio_total': 'Desperdício Total'
        }
        df_consolidado_melted['Tipo'] = df_consolidado_melted['Tipo'].map(tipo_map)
        
        # Criar gráfico de barras agrupadas
        fig_comparativo = px.bar(
            df_consolidado_melted,
            x='ds_centro_custo',
            y='Valor',
            color='Tipo',
            barmode='group',
            title="<b>Top 10 Centros: Consumo Total vs Desperdício Total</b>",
            labels={
                'ds_centro_custo': 'Centro de Custo',
                'Valor': 'Valor (R$)',
                'Tipo': 'Tipo de Valor'
            },
            color_discrete_map={
                'Consumo Total': '#2E7D32',  # Verde escuro
                'Desperdício Total': '#D32F2F'  # Vermelho
            }
        )
        
        fig_comparativo.update_layout(
            xaxis=dict(
                tickangle=-45,
                tickfont=dict(color='#444', size=11),
                linecolor='#444',
                gridcolor='#888'
            ),
            yaxis=dict(
                tickfont=dict(color='#444'),
                linecolor='#444',
                gridcolor='#888',
                tickformat='$,.0f'
            ),
            height=550,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title_font_size=24,
            legend=dict(
                x=1,
                y=1.15,
                xanchor='right',
                yanchor='top',
                font=dict(size=18, color='#444')
            ),
            hovermode='x unified'
        )
        
        fig_comparativo.update_traces(textposition='auto', textangle=0)
        
        # Card estilizado para o gráfico comparativo
        with st.container():
            st.plotly_chart(fig_comparativo, use_container_width=True)

    # Gráfico dos 10 maiores centros de custo
    # Agora ocupa a largura total, facilitando a leitura dos nomes
    df_ranking = df_filtrado.groupby('ds_centro_custo')['vl_estoque'].sum().reset_index()
    df_ranking = df_ranking.sort_values('vl_estoque', ascending=False).head(10)
    
    fig_ranking = px.bar(
        df_ranking,
        x='vl_estoque',
        y='ds_centro_custo',
        orientation='h',
        title="<b>Top 10 Centros de Custo (Ranking Financeiro)</b>",
        text_auto='.2s',
        color='vl_estoque',
        color_continuous_scale='Reds',
        labels={
            'ds_centro_custo': 'Centro de Custo',
            'vl_estoque': 'Volume'
        }
    )
    fig_ranking.update_layout(
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(color='#444'),
            linecolor='#444',
            gridcolor='#fff',  # Remove linhas horizontais (deixa branco)
            showgrid=False     # Não exibe grid horizontal
        ),
        xaxis=dict(
            tickfont=dict(color='#444'),
            linecolor='#444',
            gridcolor='#888',  # Mantém linhas verticais
            showgrid=True
        ),
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font_size=24,
        legend=dict(font=dict(color='#444'))
    )
    
    # Card estilizado para o gráfico de ranking
    with st.container():
        st.plotly_chart(fig_ranking, use_container_width=True)

    # Gráfico de evolução temporal
    df_tempo = df_filtrado.groupby(['ano', 'mes'])['vl_estoque'].sum().reset_index()
    
    # Criar coluna "Periodo" para ordenação correta
    df_tempo['periodo'] = df_tempo['ano'].astype(str) + "-" + df_tempo['mes'].astype(str).str.zfill(2)
    df_tempo = df_tempo.sort_values('periodo')

    fig_tempo = px.line(
        df_tempo,
        x='periodo',
        y='vl_estoque',
        markers=True,
        title="<b>Evolução do Desperdício ao Longo do Tempo</b>",
        labels={'vl_estoque': 'Valor (R$)', 'periodo': 'Mês/Ano'}
    )
    fig_tempo.update_traces(line_color='#d62728', line_width=4)
    fig_tempo.update_layout(
        xaxis=dict(
            tickfont=dict(color='#444'),
            linecolor='#444',
            gridcolor='#888',
            tickmode='array',
            tickvals=list(df_tempo['periodo']),
            ticktext=list(df_tempo['periodo'])
        ),
        yaxis=dict(tickfont=dict(color='#444'), linecolor='#444', gridcolor='#888'),
        height=450,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_font_size=24,
        legend=dict(font=dict(color='#444'))
    )
    
    # Card estilizado para o gráfico temporal
    with st.container():
        st.plotly_chart(fig_tempo, use_container_width=True)

    # Mapa de calor de sazonalidade
    st.subheader("🔥 Mapa de Calor: Intensidade do Desperdício")
    
    with st.expander("Ver Mapa de Calor (Sazonalidade por Centro)", expanded=False):
        # Preparando os dados: Pivot Table
        # Linhas: Centros | Colunas: Mês/Ano | Valores: Custo
        df_heatmap = df_filtrado.copy()
        df_heatmap['periodo'] = df_heatmap['ano'].astype(str) + "-" + df_heatmap['mes'].astype(str).str.zfill(2)
        df_pivot = df_heatmap.groupby(['ds_centro_custo', 'periodo'])['vl_estoque'].sum().reset_index()
        top_centros = df_filtrado.groupby('ds_centro_custo')['vl_estoque'].sum().nlargest(15).index
        df_pivot = df_pivot[df_pivot['ds_centro_custo'].isin(top_centros)]
        matriz_calor = df_pivot.pivot(index='ds_centro_custo', columns='periodo', values='vl_estoque').fillna(0)
        fig_heat = px.imshow(
            matriz_calor,
            labels=dict(x="Mês", y="Centro de Custo", color="Desperdício (R$)"),
            x=matriz_calor.columns,
            y=matriz_calor.index,
            color_continuous_scale='Reds',
            aspect="auto",
            title="<b>Sazonalidade dos Top 15 Centros</b>"
        )
        fig_heat.update_layout(
            xaxis=dict(
                tickfont=dict(color='#444'),
                linecolor='#444',
                gridcolor='#888',
                tickmode='array',
                tickvals=list(matriz_calor.columns),
                ticktext=list(matriz_calor.columns)
            ),
            yaxis=dict(tickfont=dict(color='#444'), linecolor='#444', gridcolor='#888'),
            height=600,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title_font_size=24,
            coloraxis_colorbar=dict(title_font=dict(color='#444'), tickfont=dict(color='#444'))
        )
        with st.container():
            st.markdown("""
            <style>
            div[data-testid="stVerticalBlock"] > div:has(div.js-plotly-plot):first-child {
                background-color: #E8F5E9;
                border-radius: 12px;
                padding: 32px 24px;
                border-left: 8px solid #00995D;
                box-shadow: 2px 2px 5px rgba(0,0,0,0.07);
                margin-bottom: 24px;
            }
            </style>
            """, unsafe_allow_html=True)
            st.plotly_chart(fig_heat, use_container_width=True)
        st.caption("Nota: Exibindo apenas os 15 maiores centros para melhor visualização.")

    # Tabela com dados detalhados
    with st.expander("▼ Ver Dados Detalhados (Tabela)", expanded=False):
        # Preparar os dados
        df_tabela = df_filtrado.groupby(['ds_centro_custo', 'macro_perfil'])['vl_estoque'].sum().reset_index()
        df_tabela = df_tabela.sort_values('vl_estoque', ascending=False)
        # Traduzir a coluna 'macro_perfil' usando legenda_map
        df_tabela['perfil_legenda'] = df_tabela['macro_perfil'].map(legenda_map).fillna(df_tabela['macro_perfil'])

        # Construir HTML da tabela manualmente
        html = '<style>.tabela-verde{width:100%;border-collapse:collapse;font-family:sans-serif;}'
        html += '.tabela-verde thead{background-color:#C8E6C9;}'
        html += '.tabela-verde th{background-color:#C8E6C9;color:#005533;padding:12px;text-align:left;font-weight:bold;border-bottom:2px solid #00995D;}'
        html += '.tabela-verde tbody tr{background-color:#E8F5E9;}'
        html += '.tabela-verde td{background-color:#E8F5E9;padding:10px 12px;border-bottom:1px solid #C8E6C9;}'
        html += '.tabela-verde tbody tr:hover{background-color:#C8E6C9;}'
        html += '.tabela-verde tbody tr:hover td{background-color:#C8E6C9;}</style>'
        html += '<table class="tabela-verde"><thead><tr><th>Centro de Custo</th><th>Perfil</th><th>Valor Desperdiçado (R$)</th></tr></thead><tbody>'

        # Adicionar linhas de dados
        for _, row in df_tabela.iterrows():
            valor_formatado = f"R$ {row['vl_estoque']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            html += f'<tr><td>{row["ds_centro_custo"]}</td><td>{row["perfil_legenda"]}</td><td>{valor_formatado}</td></tr>'

        html += '</tbody></table>'

        st.markdown(html, unsafe_allow_html=True)



   
st.subheader("🧠 Validação do Modelo (Por que estes grupos?)")
st.markdown("""
<style>
/* Aumenta o tamanho das abas (tabs) do Streamlit */
.stTabs [data-baseweb="tab"] {
    font-size: 1.4rem !important;
    padding: 16px 32px !important;
    height: 60px !important;
}
.stTabs [data-baseweb="tab"] > div {
    font-size: 1.4rem !important;
}
</style>
""", unsafe_allow_html=True)

# Criamos abas para separar a validação da Camada 1 e Camada 2
tab1, tab2 = st.tabs(["1️⃣ Validação dos Gigantes (Macro)", "2️⃣ Validação dos Perfis (Micro)"])

# Aba 1: Análise dos grandes centros (Outliers)
with tab1:
    st.markdown("""
    **Objetivo:** Provar que a Farmácia Central e o Almoxarifado não poderiam ser analisados junto com os outros centros.
    
    O gráfico abaixo usa **Escala Logarítmica**. Note como os Gigantes  estão isolados 
    no canto superior direito, criando uma distância estatística dos demais.
    """)
    
    # Scatter Plot com Log Scale (Ideal para mostrar Outliers de Magnitude)
    # Usamos o df_kpis (uma linha por centro) para não poluir
    if not df_kpis.empty:
        # Adiciona coluna de legenda amigável
        df_kpis['macro_perfil_legenda'] = df_kpis['macro_perfil'].map(legenda_map).fillna(df_kpis['macro_perfil'])
        fig_macro = px.scatter(
            df_kpis,
            x='qtd_total',
            y='custo_total',
            color='macro_perfil_legenda',
            size='custo_total',
            hover_name='ds_centro_custo',
            log_x=True,
            log_y=True,
            title="<b> Gigantes vs. Rede</b>",
            labels={'qtd_total': 'Volume (Log)', 'custo_total': 'Custo Financeiro (Log)', 'macro_perfil_legenda': 'Perfil'},
            color_discrete_sequence=['red', 'blue', 'green']
        )
        # Customiza os ticks logarítmicos para valores mais amigáveis
        import numpy as np
        # Eixo X
        min_x = df_kpis['qtd_total'].replace(0, np.nan).dropna().min()
        max_x = df_kpis['qtd_total'].max()
        x_ticks = [10**i for i in range(int(np.floor(np.log10(min_x))), int(np.ceil(np.log10(max_x)))+1)] if min_x > 0 else [1, 10, 100, 1000, 10000, 100000]
        x_ticktext = [f'{int(x):,}'.replace(",", ".") for x in x_ticks]
        # Eixo Y
        min_y = df_kpis['custo_total'].replace(0, np.nan).dropna().min()
        max_y = df_kpis['custo_total'].max()
        y_ticks = [10**i for i in range(int(np.floor(np.log10(min_y))), int(np.ceil(np.log10(max_y)))+1)] if min_y > 0 else [1, 10, 100, 1000, 10000, 100000]
        y_ticktext = [f'R$ {int(y):,}'.replace(",", ".") for y in y_ticks]
        fig_macro.update_layout(
            xaxis=dict(
                tickfont=dict(color='#444'),
                linecolor='#444',
                gridcolor='#888',
                tickmode='array',
                tickvals=x_ticks,
                ticktext=x_ticktext,
                type='log'
            ),
            yaxis=dict(
                tickfont=dict(color='#444'),
                linecolor='#444',
                gridcolor='#888',
                tickmode='array',
                tickvals=y_ticks,
                ticktext=y_ticktext,
                type='log'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title_font_size=24,
            legend=dict(font=dict(color='#444'))
        )
        # Card estilizado para o gráfico scatter
        with st.container():
            st.plotly_chart(fig_macro, use_container_width=True)
    
# Aba 2: Análise dos perfis operacionais
with tab2:
    st.markdown("""
    **Objetivo:** Provar que, dentro da Rede Assistencial, existem comportamentos distintos (Features).
    
    Este **Gráfico de Radar** normaliza as variáveis (0 a 1) para mostrar a "Assinatura" de cada cluster.
    Veja como cada grupo "puxa" o gráfico para uma ponta diferente (Frequência, Custo ou Mix).
    """)
    
    # Prepara os dados para o gráfico de radar
    if df_risco_log is not None and not df_risco_log.empty:
        needed_cols = ['valor_total', 'quantidade_total', 'frequencia_erros', 'perfil_risco_log']
        if all(col in df_risco_log.columns for col in needed_cols):
            # Permitir filtro de perfis (clusters) na interface
            perfis_disponiveis = df_risco_log['perfil_risco_log'].unique().tolist()
            perfis_selecionados = st.multiselect(
                'Selecione os perfis para visualizar:',
                options=perfis_disponiveis,
                default=perfis_disponiveis,
                key='radar_perfis'
            )
            df_risco_filtrado = df_risco_log[df_risco_log['perfil_risco_log'].isin(perfis_selecionados)]
            if df_risco_filtrado.empty:
                st.warning('Selecione ao menos um perfil para visualizar o radar.')
            else:
                # Agrupa por perfil e calcula médias
                avg_radar = df_risco_log.groupby('perfil_risco_log')[['valor_total', 'quantidade_total', 'frequencia_erros']].mean().reset_index()
                # Aplica escala logarítmica
                import numpy as np
                for col in ['valor_total', 'quantidade_total', 'frequencia_erros']:
                    # Soma 1 para evitar log(0)
                    avg_radar[col + '_log'] = np.log10(avg_radar[col] + 1)
                # Normaliza os valores (0 a 1)
                scaler = MinMaxScaler()
                features_log = ['valor_total_log', 'quantidade_total_log', 'frequencia_erros_log']
                avg_radar_norm = avg_radar.copy()
                avg_radar_norm[features_log] = scaler.fit_transform(avg_radar[features_log])
                # Filtra os perfis selecionados
                avg_radar_norm = avg_radar_norm[avg_radar_norm['perfil_risco_log'].isin(perfis_selecionados)]
                # Cria o gráfico de radar
                fig_radar = go.Figure()
                for i, row in avg_radar_norm.iterrows():
                    fig_radar.add_trace(go.Scatterpolar(
                        r=row[features_log].values,
                        theta=['Valor Total (log)', 'Quantidade Total (log)', 'Frequência de Erros (log)'],
                        fill='toself',
                        name=str(row['perfil_risco_log'])
                    ))
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 1],
                            linecolor='#444',
                            gridcolor='#888',
                            tickfont=dict(color='#444')
                        ),
                        angularaxis=dict(
                            linecolor='#444',
                            gridcolor='#888',
                            tickfont=dict(color='#444')
                        )
                    ),
                    showlegend=True,
                    title="<b>Assinatura dos Principais Perfis de Risco (Escala Logarítmica)</b>",
                    paper_bgcolor='rgba(0,0,0,0)',
                    title_font_size=24,
                    legend=dict(font=dict(color='#444'))
                )
                with st.container():
                    st.plotly_chart(fig_radar, use_container_width=True)
                # Exibe análise descritiva
                st.markdown('---')
                st.markdown('**Resumo dos Perfis (médias originais):**')
                st.dataframe(avg_radar[['perfil_risco_log', 'valor_total', 'quantidade_total', 'frequencia_erros']].set_index('perfil_risco_log').round(2))
                st.info("""
                **Interpretação:**
                * Cada linha representa um perfil de risco.
                * As variáveis são exibidas em escala logarítmica para melhor diferenciação.
                * Veja a tabela acima para os valores médios reais de cada perfil.
                """)
        else:
            st.error(f"Colunas necessárias não encontradas: {needed_cols}. Colunas atuais: {df_risco_log.columns.tolist()}")