import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Adiciona o diretório raiz ao path para importação de módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from style_utils import exibir_cabecalho, aplicar_estilo_unimed, criar_tabela_estilizada

# Configuração inicial da página
st.set_page_config(page_title="Unidades Operacionais",
                   page_icon="icone-unimed.png",
                   layout="wide")

# Exibe o cabeçalho padrão
exibir_cabecalho()

# Aplica estilos CSS personalizados
aplicar_estilo_unimed()

# Ajustes de CSS para a barra lateral
st.markdown("""
    <style>
    /* Expande a largura do sidebar para exibir textos completos */
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
    
    /* Expandir labels dos multiselect no sidebar */
    [data-testid="stSidebar"] .stMultiSelect label {
        white-space: normal !important;
        overflow: visible !important;
    }
    
    /* Expandir opcoes dos multiselect no sidebar */
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] {
        min-width: 100% !important;
    }
    
    /* Garantir que as opções do multiselect exibem completamente */
    [data-testid="stSidebar"] .stMultiSelect > div > div {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏥 Rede Assistencial")

st.markdown("""
Nesta visão, analisamos os **43 centros de custo** que compõem a rotina hospitalar.
O objetivo é direcionar ações corretivas específicas para cada perfil de comportamento identificado.
""")
st.markdown("---")

# Carrega os dados necessários
@st.cache_data
def carregar_dados():
    try:
        df_completo = pd.read_csv('df_dashboard_completo.csv')
        df_kpis = pd.read_csv('df_dashboard_centros_kpis.csv')
        return df_completo, df_kpis
    except FileNotFoundError:
        return None, None

df_completo, df_kpis = carregar_dados()

# Mapeamento para simplificar nomes dos perfis
perfil_cluster_simplificado = {
    '4. Alto Risco (Crítico)': 'Alto Risco',
    '3. Médio Risco (Alta Frequência)': 'Médio Risco',
    '2. Baixo Risco (Rotina)': 'Baixo Risco',
    '1. Risco Mínimo (Eventual)': 'Risco Mínimo'
}

if df_completo is not None:
    
    # Filtra e processa os dados de micro clusters, removendo outliers
    df_risco = pd.read_csv('df_dashboard_risco_completo_v3.csv')
    # Remove centros de custo que são outliers
    outliers = ["FARMÁCIA CENTRAL", "ALMOXARIFADO LABORATORIO"]
    perfil_outlier = "5. Outlier Corporativo (Gigantes)"
    df_micro = df_risco[
        (~df_risco['ds_centro_custo'].str.upper().isin([o.upper() for o in outliers])) &
        (df_risco['perfil_risco_log'] != perfil_outlier)
    ].copy()
    # Obtém a lista de perfis disponíveis
    micro_perfis = df_micro['perfil_risco_log'].unique().tolist()
    st.sidebar.header("Filtros dos Perfis de Micro Cluster")
    micro_perfis_sel = st.sidebar.multiselect(
        "Filtrar por Perfil de Micro Cluster:",
        micro_perfis,
        default=micro_perfis,
        format_func=lambda x: perfil_cluster_simplificado.get(x, x)
    )

    st.sidebar.markdown("---")
    st.sidebar.info(
        """
        **Legenda dos Perfis:**
        
        🔴 **Alto Risco:** Crítico  
        🟠 **Médio Risco:** Alta Frequência  
        🟡 **Baixo Risco:** Rotina  
        🟢 **Risco Mínimo:** Eventual  
        """
    )

    # Filtra os dados com base na seleção do usuário
    df_micro_filtrado = df_micro[df_micro['perfil_risco_log'].isin(micro_perfis_sel)]
    # Remove duplicatas para evitar contagem dupla
    df_micro_unicos = df_micro_filtrado.drop_duplicates(subset=['ds_centro_custo', 'perfil_risco_log'])


    # Exibição dos KPIs dos micro clusters

    col1, col2, col3 = st.columns(3)
    with col1:
        valor_total = df_micro_unicos['valor_total'].sum()
        valor_formatado = f"R$ {valor_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        st.metric("💰 Desperdício Total ", valor_formatado)
    with col2:
        erros_total = df_micro_unicos['frequencia_erros'].sum()
        st.metric("❗ Total de Erros", f"{int(erros_total):,}".replace(",", "."))
    with col3:
        quantidade_unidades = df_micro_unicos['qt_estoque'].sum() if 'qt_estoque' in df_micro_unicos.columns else 0
        st.metric("📦 Unidades", f"{int(quantidade_unidades):,}".replace(",", "."))

    st.markdown("---")

    # Análise visual dos micro clusters
    st.subheader("🧩 Perfis de Comportamento (Micro Clusters)")

    # Gráfico de barras: Impacto financeiro por perfil

    df_micro_agg = df_micro_unicos.groupby('perfil_risco_log')['valor_total'].sum().reset_index().sort_values('valor_total', ascending=True)
    # Simplifica os nomes dos perfis para o gráfico
    df_micro_agg['perfil_risco_log'] = df_micro_agg['perfil_risco_log'].map(perfil_cluster_simplificado)
    fig_micro = px.bar(
        df_micro_agg,
        x='valor_total',
        y='perfil_risco_log',
        orientation='h',
        title="<b>Impacto Financeiro por Perfil de Micro Cluster</b>",
        text_auto='.2s',
        color='perfil_risco_log',
        labels={'perfil_risco_log': 'Perfil', 'valor_total': 'Valor Total'}
    )
    fig_micro.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            x=0.75,
            y=0.95,
            font=dict(size=14),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#00995D',
            borderwidth=1
        )
    )
    with st.container():
        st.plotly_chart(fig_micro, use_container_width=True)

    # Seção de plano de ação e análise detalhada
    st.subheader("📊 Análise detalhada")
    
    def definir_acao(perfil):
        if 'Rotina' in perfil: return '🔄 Treinamento de Processo (Reciclagem)'
        elif 'Críticos' in perfil: return '🔍 Auditoria de Inventário (Itens Caros)'
        elif 'Risco' in perfil: return '⚖️ Revisão de Protocolo (Controlados)'
        elif 'Vencimento' in perfil: return '📅 Mutirão de Validade (Ajuste)'
        else: return 'Monitoramento'

    # Gera tabela de plano de ação baseada nos dados
    df_acao = df_micro_unicos[['ds_centro_custo', 'perfil_risco_log', 'valor_total', 'frequencia_erros']].copy()
    df_acao = df_acao.sort_values('valor_total', ascending=False)
    # Simplifica nomes dos perfis na tabela
    df_acao['perfil_risco_log'] = df_acao['perfil_risco_log'].map(perfil_cluster_simplificado)
    # Remove colunas desnecessárias
    for col in ['id', 'Ação Recomendada']:
        if col in df_acao.columns:
            df_acao = df_acao.drop(columns=[col])

    # Renderiza a tabela estilizada
    colunas_config = {
        'valor_total': {'formatar': True, 'gradiente': True}
    }
    
    mapa_colunas = {
        'ds_centro_custo': 'Centro de Custo',
        'perfil_risco_log': 'Perfil',
        'valor_total': 'Desperdício (R$)',
        'frequencia_erros': 'Qtd. Erros'
    }
    
    html_table = criar_tabela_estilizada(df_acao, colunas_config, mapa_colunas)
    st.markdown(html_table, unsafe_allow_html=True)

    st.markdown("---")

    # Detalhamento por centro de custo (Drill-down)
    st.subheader("🔬 Raio-X Operacional: Detalhe por Centro")
    st.markdown("Selecione um centro específico abaixo para investigar a fundo os motivos e produtos.")


    # Lista de centros disponíveis para seleção
    centros_disponiveis = df_micro_unicos.sort_values('valor_total', ascending=False)['ds_centro_custo'].unique()

    centro_selecionado = st.selectbox(
        "Selecione o Centro de Custo:", 
        centros_disponiveis,
        index=0
    )

    if centro_selecionado:
        # Filtra detalhes do centro selecionado
        df_detalhe = df_completo[df_completo['ds_centro_custo'] == centro_selecionado].copy()
        # Obtém dados consolidados do centro
        dados_centro = df_micro_unicos[df_micro_unicos['ds_centro_custo'] == centro_selecionado].iloc[0]


        st.markdown(f"### 📋 Resumo: {centro_selecionado}")

        # Identifica a operação com maior impacto
        operacao_predominante = None
        acao_recomendada = "Monitoramento"
        cor_card = "#1976D2"  # Azul padrão
        if not df_detalhe.empty and 'ds_operacao' in df_detalhe.columns and 'vl_estoque' in df_detalhe.columns:
            op_agg = df_detalhe.groupby('ds_operacao')['vl_estoque'].sum().sort_values(ascending=False)
            if not op_agg.empty:
                operacao_predominante = op_agg.index[0]
        # Define a ação recomendada baseada na operação
        def recomendar_acao_operacao(operacao):
            if operacao is None:
                return "Monitoramento"
            op = operacao.lower()
            if "vencid" in op:
                return "📅 Mutirão de Validade (Ajuste de Estoque)"
            elif "quebra" in op or "contamina" in op:
                return "🔬 Revisão de Armazenamento e Transporte"
            elif "consumo" in op:
                return "🔄 Treinamento de Consumo Consciente"
            elif "devolu" in op:
                return "↩️ Revisão de Processo de Devolução"
            elif "doaç" in op:
                return "🎁 Auditoria de Doações"
            elif "execuç" in op or "prescri" in op:
                return "📝 Revisão de Prescrição Médica"
            elif "troca comercial" in op:
                return "💱 Revisão de Trocas Comerciais"
            elif "sobras" in op:
                return "⚖️ Ajuste de Planejamento de Compras"
            else:
                return "Monitoramento"
        acao_recomendada = recomendar_acao_operacao(operacao_predominante)

        # Define a cor do card de acordo com a criticidade
        perfil = str(dados_centro['perfil_risco_log']).lower()
        if any(x in perfil for x in ["crític", "alto", "grave"]):
            cor_card = "#D32F2F"  # Vermelho
        elif any(x in perfil for x in ["rotina", "moderado", "médio"]):
            cor_card = "#FFEB3B"  # Amarelo
        else:
            cor_card = "#1976D2"  # Azul

        # Exibe card com resumo e recomendação
        perfil_simplificado = perfil_cluster_simplificado.get(dados_centro['perfil_risco_log'], dados_centro['perfil_risco_log'])
        st.markdown(f'''
            <div style="background-color: {cor_card}; color: {'#000' if cor_card=='#FFEB3B' else '#fff'}; padding: 24px 18px; border-radius: 12px; margin-bottom: 12px;">
                <span style="font-size:1.3rem;font-weight:bold;">Perfil:</span> {perfil_simplificado}<br>
                <span style="font-size:1.1rem;">Operação predominante: <b>{operacao_predominante if operacao_predominante else 'N/A'}</b></span>
            </div>
            <div style="background: #f5f5f5; border-radius: 8px; padding: 12px 18px; margin-bottom: 18px; border-left: 6px solid {cor_card};">
                <span style="font-size:1.1rem;font-weight:bold;">Ação Recomendada:</span> {acao_recomendada}
            </div>
        ''', unsafe_allow_html=True)

        kpi1, kpi2 = st.columns(2)
        with kpi1:
            valor_custo = dados_centro['valor_total']
            valor_custo_fmt = f"R$ {valor_custo:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            st.metric("💰 Desperdício Total", valor_custo_fmt)
        with kpi2:
            st.metric("📉 Quantidade de Erros", f"{dados_centro['frequencia_erros']:.0f} erros")

        # --- BLOCO: CAUSA RAIZ (GRÁFICO DE PIZZA) ---
        st.markdown("### 🧩 Causa Raiz: Por que o desperdício acontece?")
        causas_kpis = df_kpis[df_kpis['ds_centro_custo'] == centro_selecionado]
        causa_cols = [
            'Consumo', 'Devolução Paciente', 'Doações - saída', 'Execução Prescrição',
            'Medicamentos Controlados Vencidos', 'Perdas e Quebras', 'Perdas por estabilidade',
            'Produtos vencidos', 'Quebras e Contaminações', 'Quebras/Contaminação Med Controlados',
            'Saída por troca comercial', 'Sobras por estabilidade'
        ]
        if not causas_kpis.empty:
            soma = causas_kpis[causa_cols].sum(axis=1).values[0]
            if soma > 0:
                causa_percent = (causas_kpis[causa_cols].iloc[0] / soma * 100)
                causa_percent = causa_percent[causa_percent > 0]  # Exibir apenas causas relevantes
                fig_causa = px.pie(
                    names=causa_percent.index,
                    values=causa_percent.values,
                    title=f"<b>Distribuição das Causas Raiz - {centro_selecionado}</b>",
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_causa.update_traces(textposition='inside', textinfo='percent')
                fig_causa.update_layout(
                    height=500,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=80, r=150),
                    legend=dict(
                        x=0.75,
                        y=0.5,
                        font=dict(size=13),
                        bgcolor='rgba(255,255,255,0.8)',
                        bordercolor='#00995D',
                        borderwidth=1
                    )
                )
                st.plotly_chart(fig_causa, use_container_width=True)
            else:
                st.info("Nenhuma causa raiz relevante para este centro.")
        else:
            st.info("Centro não encontrado no dataframe de causas.")

        # --- BLOCO 3: TOP ITENS (AGORA COM VALOR E QUANTIDADE) ---
        st.markdown("#### 📋 Materiais Críticos por Desperdício")
        

        if not df_detalhe.empty:
            # 1. Preparar os dados para a tabela
            df_itens_centro = df_detalhe.groupby(['ds_material_hospital', 'ds_operacao']).agg({
                'vl_estoque': 'sum',
                'qt_estoque': 'sum',
                'valor_unitario': 'mean'
            }).reset_index()
            # Ordenar e pegar Top 20
            df_itens_centro = df_itens_centro.sort_values('vl_estoque', ascending=False).head(20)
            
            # 2. Preparar dados para tabela estilizada
            df_itens_exibir = df_itens_centro[[
                'ds_material_hospital', 'ds_operacao', 'vl_estoque', 'qt_estoque', 'valor_unitario'
            ]].copy()
            
            # Configurar colunas com gradiente
            colunas_config_itens = {
                'vl_estoque': {'formatar': True, 'gradiente': True}
            }
            
            mapa_colunas_itens = {
                'ds_material_hospital': 'Produto',
                'ds_operacao': 'Motivo',
                'vl_estoque': 'Valor Total (R$)',
                'qt_estoque': 'Qtd.',
                'valor_unitario': 'Valor Unit. (R$)'
            }
            
            html_table_itens = criar_tabela_estilizada(df_itens_exibir, colunas_config_itens, mapa_colunas_itens)
            st.markdown(html_table_itens, unsafe_allow_html=True)
        else:
            st.info("Não há itens registrados para este centro.")

else:
    st.error("Arquivos de dados não encontrados. Verifique se 'df_dashboard_completo.csv' está na pasta.")
