import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import os
import sys
import textwrap

# Adiciona o diretório raiz ao path para importação de módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from style_utils import criar_tabela_estilizada

# Configuração da página
st.set_page_config(page_title="Almoxarifado Laboratório", page_icon="icone-unimed.png", layout="wide")

# Exibe o cabeçalho padrão
def exibir_cabecalho():
    def get_img_as_base64(file):
        try:
            with open(file, "rb") as f:
                data = f.read()
            return base64.b64encode(data).decode()
        except Exception:
            return None

    # Ajuste dinâmico do caminho das imagens
    try:
        dir_atual = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        dir_atual = os.getcwd()
    
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
    
    st.markdown(textwrap.dedent(header_html), unsafe_allow_html=True)

exibir_cabecalho()

# Aplica estilos CSS personalizados
def aplicar_estilo_unimed():
    st.markdown("""
        <style>
        /* Estilo dos Cards de KPI */
        [data-testid="stMetric"] {
            background-color: #E8F5E9;
            border-left: 5px solid #00995D;
            padding: 12px 8px;
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            max-width: 100%;
            word-break: break-word;
            overflow-wrap: break-word;
        }

        /* Rótulo do KPI */
        [data-testid="stMetricLabel"], 
        [data-testid="stMetricLabel"] > div,
        [data-testid="stMetricLabel"] p {
            font-size: clamp(0.85rem, 2vw, 1.2rem) !important;
            font-weight: bold !important;
            line-height: 1.2 !important;
            margin: 2px auto !important;
            padding: 0 !important;
            word-break: break-word;
            overflow-wrap: break-word;
            width: 100% !important;
            text-align: center !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
        }

        /* Valor do KPI */
        [data-testid="stMetricValue"],
        [data-testid="stMetricValue"] > div {
            font-size: clamp(1.1rem, 3vw, 2.2rem) !important;
            line-height: 1.2 !important;
            margin: 4px 0 !important;
            padding: 0 !important;
            word-break: break-word;
            overflow-wrap: break-word;
        }

        /* Linhas horizontais */
        hr {
            border-color: #00995D !important;
            background-color: #00995D !important;
            height: 2px !important;
            opacity: 1 !important;
        }
        
        /* Títulos das seções */
        h3 {
            border-bottom: 2px solid #00995D;
            padding-bottom: 10px;
            color: #005533;
        }
        
        /* Espaçamento do topo */
        .block-container {
            padding-top: 4rem; 
            padding-bottom: 3rem;
        }
        
        /* Estilo para cards de gráficos */
        .stPlotlyChart {
            background-color: #E8F5E9;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.07);
            margin-bottom: 24px;
            border: 1px solid #e0e0e0;
            border-left: 8px solid #00995D !important;
        }
        
        /* Responsividade das colunas */
        [data-testid="column"] {
            min-width: 0;
            overflow-wrap: break-word;
            word-wrap: break-word;
        }
        
        [data-testid="stMetricLabel"] {
            word-break: break-word;
            white-space: normal !important;
            overflow-wrap: break-word;
        }
        
        [data-testid="stMetricValue"] {
            word-break: break-word;
            overflow-wrap: break-word;
        }
        </style>
    """, unsafe_allow_html=True)

aplicar_estilo_unimed()

# CSS para expandir o sidebar
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        width: 320px !important;
        background-color: #E8F5E9 !important;
    }
    
    [data-testid="stSidebarNav"] span {
        color: #00995D !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        width: 100% !important;
    }
    
    [data-testid="stSidebar"] .stMultiSelect label {
        white-space: normal !important;
        overflow: visible !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] {
        min-width: 100% !important;
    }
    
    [data-testid="stSidebar"] .stMultiSelect > div > div {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧪Almoxarifado Laboratório")
st.markdown("---")

# Carregamento de dados
@st.cache_data
def carregar_dados_lab():
    try:
        df = pd.read_csv('df_dashboard_almoxarifado.csv')
        return df
    except FileNotFoundError:
        return None

df_lab = carregar_dados_lab()

if df_lab is not None:
    
    # Filtros laterais
    st.sidebar.header("Filtros de Materiais")
    
    with st.sidebar.expander("ℹ️ Legenda dos Perfis"):
        st.markdown("""
        <div style="height: 200px; overflow-y: auto; padding-right: 5px;">
            <ul style="margin-bottom: 0;">
                <li><strong>Alto Custo:</strong> Itens tecnológicos de valor unitário altíssimo.</li>
                <li><strong>Médio Custo:</strong> Kits de diagnóstico intermediários.</li>
                <li><strong>Baixo Custo:</strong> Itens de alto giro e baixo valor.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    perfis = df_lab['perfil_produto'].unique()
    
    def simplificar_nome_lab(nome):
        if "Alto Custo" in nome: return "Alto Custo"
        if "Médio Custo" in nome: return "Médio Custo"
        if "Baixo Custo" in nome: return "Baixo Custo"
        return nome

    opcoes_amigaveis = sorted(list(set([simplificar_nome_lab(p) for p in perfis])))
    
    selecao_amigavel = st.sidebar.multiselect("Filtrar Perfil:", opcoes_amigaveis, default=opcoes_amigaveis)
    
    perfil_selecionado = [p for p in perfis if simplificar_nome_lab(p) in selecao_amigavel]
    
    curvas = sorted(df_lab['classe_abc'].unique())
    abc_selecionado = st.sidebar.multiselect("Filtrar ABC:", curvas, default=['A', 'B', 'C'])
    
    if perfil_selecionado and abc_selecionado:
        df_filtrado = df_lab[
            (df_lab['perfil_produto'].isin(perfil_selecionado)) & 
            (df_lab['classe_abc'].isin(abc_selecionado))
        ]
    else:
        df_filtrado = df_lab

    # Exibição dos KPIs
    col1, col2, col3 = st.columns(3)
    with col1:
        valor_lab = df_filtrado['vl_estoque'].sum()
        valor_lab_fmt = f"R$ {valor_lab:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        st.metric("💰 Desperdício Filtrado", valor_lab_fmt)
    with col2:
        qt_desperdicada = df_filtrado['qt_estoque'].sum()
        qt_desperdicada_fmt = f"{int(qt_desperdicada)}"
        st.metric("🧪 Quantidade Total Desperdiçada", qt_desperdicada_fmt)
    with col3:
        st.metric("⚠️ Causa Principal", df_filtrado['ds_operacao'].mode()[0] if not df_filtrado.empty else "N/A")

    # Diagnóstico Estratégico
    st.subheader("📊 Diagnóstico Estratégico")
    
    st.markdown("""
    <style>
    /* Estilo para todos os elementos que contém gráficos Plotly */
    .stPlotlyChart {
        background-color: #E8F5E9;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.07);
        margin-bottom: 24px;
        border: 1px solid #e0e0e0;
        border-left: 8px solid #00995D !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("##### Distribuição de Desperdício por Perfil de Produto")
    fig_perfil = px.pie(
        df_filtrado, values='vl_estoque', names='perfil_produto',
        hole=0.4, color='perfil_produto',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_perfil.update_traces(textposition='inside', textinfo='percent', textfont=dict(size=18))
    fig_perfil.update_layout(
        height=450, 
        margin=dict(t=0, b=0, l=0, r=150),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=0.75,
            font=dict(size=18)
        )
    )
    with st.container():
        st.plotly_chart(fig_perfil, use_container_width=True)

    # Lista de Ataque
    st.subheader("📋 Lista de Ataque (Laboratório)")

    df_tabela = df_filtrado[[
        'ds_material_hospital', 'perfil_produto', 'classe_abc', 
        'ds_operacao', 'vl_estoque', 'qt_estoque'
    ]].sort_values('vl_estoque', ascending=False).copy()
    
    df_tabela['vl_unitario'] = df_tabela['vl_estoque'] / df_tabela['qt_estoque'].replace(0, 1)
    
    df_tabela_estilizada = df_tabela[[
        'ds_material_hospital', 'perfil_produto', 'classe_abc', 
        'ds_operacao', 'vl_estoque', 'vl_unitario', 'qt_estoque'
    ]].copy()
    
    colunas_config = {
        'vl_estoque': {'formatar': False, 'gradiente': True},
        'vl_unitario': {'formatar': False}
    }
    
    mapa_colunas = {
        'ds_material_hospital': 'Material',
        'perfil_produto': 'Perfil',
        'classe_abc': 'ABC',
        'ds_operacao': 'Motivo',
        'vl_estoque': 'Valor (R$)',
        'vl_unitario': 'Preço Unit. (R$)',
        'qt_estoque': 'Qtd'
    }
    
    html_table = criar_tabela_estilizada(df_tabela_estilizada, colunas_config, mapa_colunas)
    st.markdown(html_table, unsafe_allow_html=True)
    
    csv = df_tabela.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Baixar CSV", data=csv, file_name="laboratorio_lista_ataque.csv", mime="text/csv")

    # Investigação Temporal
    st.subheader("📈 Investigação Temporal: Histórico do Item")
    
    @st.cache_data
    def carregar_dados_completo():
        try: return pd.read_csv('df_dashboard_completo.csv')
        except: return None

    df_full = carregar_dados_completo()

    if df_full is not None:
        df_lab_full = df_full[df_full['ds_centro_custo'].str.contains('Almoxarifado', case=False)].copy()
        
        produtos_disponiveis = df_filtrado['ds_material_hospital'].unique()
        
        produto_investigado = st.selectbox(
            "Selecione um material para ver o histórico:",
            options=produtos_disponiveis,
            index=0 if len(produtos_disponiveis) > 0 else None
        )
        
        if produto_investigado:
            df_prod_tempo = df_lab_full[df_lab_full['ds_material_hospital'] == produto_investigado].copy()
            
            if not df_prod_tempo.empty:
                df_prod_tempo['periodo'] = df_prod_tempo['ano'].astype(str) + "-" + df_prod_tempo['mes'].astype(str).str.zfill(2)
                
                # Dados para a Tabela
                df_tabela_detalhada = df_prod_tempo.groupby(['periodo', 'ds_operacao'])['vl_estoque'].sum().reset_index().sort_values('periodo')
                
                def get_acao_recomendada(motivo):
                    motivo = str(motivo).lower()
                    if 'vencid' in motivo: return "Revisar Quantidade Comprada"
                    if 'quebra' in motivo: return "Treinamento de manuseio"
                    if 'contamina' in motivo: return "Treinamento de manuseio"
                    if 'perda' in motivo: return "Investigar processo de uso"
                    return "Monitorar ocorrência"

                df_tabela_detalhada['acao_recomendada'] = df_tabela_detalhada['ds_operacao'].apply(get_acao_recomendada)

                # Dados para o Gráfico
                df_chart_data = df_tabela_detalhada.groupby('periodo')['vl_estoque'].sum().reset_index()
                
                # Série completa de meses
                min_periodo = df_chart_data['periodo'].min()
                max_periodo = df_chart_data['periodo'].max()
                
                min_ano, min_mes = map(int, min_periodo.split('-'))
                max_ano, max_mes = map(int, max_periodo.split('-'))
                
                periodos_completos = []
                ano, mes = min_ano, min_mes
                while (ano, mes) <= (max_ano, max_mes):
                    periodos_completos.append(f"{ano}-{mes:02d}")
                    mes += 1
                    if mes > 12:
                        mes = 1
                        ano += 1
                
                df_completo = pd.DataFrame({'periodo': periodos_completos, 'vl_estoque': 0.0})
                
                df_prod_temp_indexed = df_chart_data.set_index('periodo')[['vl_estoque']]
                df_completo_indexed = df_completo.set_index('periodo')
                df_completo_indexed.update(df_prod_temp_indexed)
                df_completo = df_completo_indexed.reset_index()
                
                df_grafico = df_completo[df_completo['periodo'].str.startswith(('2023', '2024'))].copy()
                
                meses_pt = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
                df_grafico['label_data'] = df_grafico['periodo'].apply(
                    lambda x: f"{meses_pt[int(x.split('-')[1])-1]}/{x.split('-')[0][-2:]}"
                )
                
                media_valor = df_grafico['vl_estoque'].mean()
                max_valor = df_grafico['vl_estoque'].max()
                
                # Gráfico de Barras
                fig_tempo_prod = px.bar(
                    df_grafico,
                    x='label_data',
                    y='vl_estoque',
                    title=f"<b>Histórico Completo: {produto_investigado}</b>",
                    labels={'label_data': 'Período', 'vl_estoque': 'Valor Desperdiçado (R$)'},
                    color='vl_estoque',
                    color_continuous_scale=['#E8F5E9', '#A5D6A7', '#FFD700', '#FF6B6B', '#D32F2F'],
                    text=df_grafico['vl_estoque'].apply(lambda x: f'R$ {x:,.0f}' if x > 0 else ''),
                    custom_data=['periodo']
                )
                
                fig_tempo_prod.update_traces(
                    textposition='outside',
                    hovertemplate='<b>%{customdata[0]}</b><br>Valor: R$ %{y:,.2f}<extra></extra>',
                    marker=dict(
                        line=dict(color='#00995D', width=1)
                    )
                )
                
                fig_tempo_prod.update_layout(
                    height=520,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(232,245,232,0.3)',
                    xaxis=dict(
                        title='<b>Período (Mês/Ano)</b>',
                        tickangle=0,
                        tickfont=dict(size=11, color='#005533'),
                        title_font=dict(size=14, color='#005533'),
                        showgrid=False,
                        showline=True,
                        linewidth=2,
                        linecolor='#00995D'
                    ),
                    yaxis=dict(
                        tickprefix='R$ ',
                        tickformat='.2s',
                        title='<b>Valor Desperdiçado</b>',
                        title_font=dict(size=14, color='#005533'),
                        gridcolor='rgba(0,153,93,0.1)',
                        showline=True,
                        linewidth=2,
                        linecolor='#00995D',
                        gridwidth=1
                    ),
                    coloraxis_showscale=False,
                    showlegend=False,
                    margin=dict(b=80, t=80, l=80, r=80),
                    hovermode='x unified'
                )
                
                with st.container():
                    st.plotly_chart(fig_tempo_prod, use_container_width=True)
                
                # Tabela com detalhamento mensal
                st.markdown("##### 📅 Detalhamento Mensal")
                
                df_tabela_meses = df_tabela_detalhada[['periodo', 'ds_operacao', 'acao_recomendada', 'vl_estoque']].copy()
                
                colunas_config = {
                    'vl_estoque': {'formatar': True, 'gradiente': True}
                }
                
                mapa_colunas = {
                    'periodo': 'Mês/Ano',
                    'ds_operacao': 'Motivo',
                    'acao_recomendada': 'Ação Recomendada',
                    'vl_estoque': 'Valor Desperdiçado'
                }
                
                html_table_meses = criar_tabela_estilizada(df_tabela_meses, colunas_config, mapa_colunas)
                st.markdown(html_table_meses, unsafe_allow_html=True)
            else:
                st.warning("Histórico não encontrado para este item.")

    else:
        st.warning("Base completa não disponível.")

else:
    st.error("Arquivo 'df_dashboard_almoxarifado.csv' não encontrado.")