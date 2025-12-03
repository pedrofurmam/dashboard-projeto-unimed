import pandas as pd

def criar_tabela_estilizada(df, colunas_config=None, mapa_colunas=None):
    """
    Gera uma tabela HTML estilizada com padrão visual Unimed.
    
    Args:
        df: DataFrame com os dados.
        colunas_config: Dicionário de configuração das colunas (formatação, gradiente).
        mapa_colunas: Dicionário para renomear colunas na exibição.
    
    Returns:
        String contendo o HTML da tabela.
    """
    
    if df.empty:
        return "<p>Sem dados para exibir</p>"
    
    html_table = '<div style="border-radius: 12px; overflow: hidden; max-height: 600px; overflow-y: auto; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">'
    html_table += '<table style="width:100%; border-collapse: collapse; font-family: Arial, sans-serif;">'
    
    # Cabeçalho da tabela
    html_table += '<tr style="background-color: #00995D; color: white; font-weight: bold; position: sticky; top: 0;">'
    for col in df.columns:
        nome_coluna = mapa_colunas.get(col, col) if mapa_colunas else col
        html_table += f'<th style="padding: 12px; border: 1px solid #ddd; text-align: left;">{nome_coluna}</th>'
    html_table += '</tr>'
    
    # Linhas da tabela
    for idx, row in df.iterrows():
        html_table += '<tr>'
        for col in df.columns:
            valor = row[col]
            
            # Aplica formatação e gradiente se configurado
            if colunas_config and col in colunas_config:
                config = colunas_config[col]
                if config.get('gradiente', False) and isinstance(valor, (int, float)):
                    # Gradiente de vermelho baseado na intensidade do valor
                    intensidade = min(255, int((valor / df[col].max()) * 255))
                    r = 255
                    g = int(179 * (1 - intensidade / 255))
                    b = int(179 * (1 - intensidade / 255))
                    cor_bg = f'rgb({r}, {g}, {b})'
                    
                    if config.get('formatar', False):
                        valor_fmt = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    else:
                        valor_fmt = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    
                    html_table += f'<td style="padding: 10px; border: 1px solid #ddd; background-color: {cor_bg}; text-align: right;">{valor_fmt}</td>'
                else:
                    if isinstance(valor, (int, float)):
                        if config.get('formatar', False):
                            valor_fmt = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                        else:
                            valor_fmt = f"{valor:,.0f}".replace(",", ".")
                        html_table += f'<td style="padding: 10px; border: 1px solid #ddd; background-color: #E8F5E9; text-align: right;">{valor_fmt}</td>'
                    else:
                        html_table += f'<td style="padding: 10px; border: 1px solid #ddd; background-color: #E8F5E9;">{valor}</td>'
            else:
                # Formatação padrão automática
                if isinstance(valor, (int, float)):
                    nome_col_lower = col.lower()
                    if any(x in nome_col_lower for x in ['valor', 'unitario', 'custo', 'preco', 'vl_']):
                        valor_fmt = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                        html_table += f'<td style="padding: 10px; border: 1px solid #ddd; background-color: #E8F5E9; text-align: right;">{valor_fmt}</td>'
                    else:
                        valor_fmt = f"{valor:,.0f}".replace(",", ".")
                        html_table += f'<td style="padding: 10px; border: 1px solid #ddd; background-color: #E8F5E9; text-align: right;">{valor_fmt}</td>'
                else:
                    html_table += f'<td style="padding: 10px; border: 1px solid #ddd; background-color: #E8F5E9;">{valor}</td>'
        
        html_table += '</tr>'
    
    html_table += '</table>'
    html_table += '</div>'
    
    return html_table


def aplicar_estilo_unimed():
    """
    Aplica o CSS global personalizado da Unimed.
    """
    import streamlit as st
    
    st.markdown("""
        <style>
        /* Estilo dos Cards de KPI */
        [data-testid="stMetric"] {
            background-color: #E8F5E9;
            border-left: 5px solid #00995D;
            padding: 15px;
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        /* Rótulo do KPI */
        [data-testid="stMetricLabel"], 
        [data-testid="stMetricLabel"] > div,
        [data-testid="stMetricLabel"] p {
            font-size: 1.8rem !important;
            font-weight: bold !important;
        }

        /* Valor do KPI */
        [data-testid="stMetricValue"],
        [data-testid="stMetricValue"] > div {
            font-size: 3.5rem !important;
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
        </style>
    """, unsafe_allow_html=True)


def exibir_cabecalho(titulo="Monitoramento de Desperdícios"):
    """
    Exibe o cabeçalho padrão com logos Unimed e UTFPR.
    
    Args:
        titulo: Título exibido no centro do cabeçalho.
    """
    import streamlit as st
    import base64
    import os
    import textwrap
    
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
                {titulo}
            </h2>
        </div>
        <div style="flex: 1; text-align: right;">
            <img src="{src_utfpr}" style="height: 90px; object-fit: contain;">
        </div>
    </div>
    """
    
    st.markdown(textwrap.dedent(header_html), unsafe_allow_html=True)
