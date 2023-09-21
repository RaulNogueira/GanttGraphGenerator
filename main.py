
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import requests
from io import BytesIO
from dependency_lines import draw_dependency_lines
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Link direto para o download do arquivo no OneDrive
#link = "https://onedrive.live.com/download?resid=418310F3CCC9CD06%21290&authkey=!ADTm63ig8VK0sXo&em=2"

# Baixar o arquivo usando requests
#response = requests.get(link)
#response.raise_for_status()  # Lançará um erro se houver um problema com a solicitação

# Usa o conteúdo baixado para criar um BytesIO stream e carregá-lo diretamente no pandas
#df = pd.read_excel(BytesIO(response.content), sheet_name='Sheet1')

# Lê o dataframe a partir do arquivo Excel se quiser usar localmente
df = pd.read_excel('./task.xlsx', sheet_name='Sheet1')

# Converte as colunas de datas do dataframe para o formato datetime
df['Início'] = pd.to_datetime(df['Início'], dayfirst=True)
df['Due Date'] = pd.to_datetime(df['Due Date'], dayfirst=True)
df['Closing Date'] = pd.to_datetime(df['Closing Date'], dayfirst=True, errors='coerce')

# Converta a coluna "Completo" para uma escala de 0-1 em vez de 0-100
df['Completo'] = df['Completo'] / 100.0

# Calcula a duração estimada de cada tarefa em dias
df['Duração Estimada'] = (df['Due Date'] - df['Início']).dt.days

# Calcula a duração real de cada tarefa em dias, usando a data atual se a tarefa ainda não foi concluída
df['Duração Real'] = df.apply(lambda row: (row['Closing Date'] if pd.notna(row['Closing Date']) else datetime.now()) - row['Início'], axis=1).dt.days

# Define cores para diferentes "tecnologias"
colors_tech = {
    'iOS': '#fcc42e',
    'Android': '#fcc42e',
    'Angular': '#fcc42e',
    'Testes': '#5c9cd4',
    'Acessibilidade': '#c0d8fa',
}

# Define cores para diferentes status
colors_status = {
    'Concluído': '#58D68D',
    'Início': '#5DADE2',
    'Em andamento': '#F4D03F',
    'Atrasado': '#E74C3C',
    'Não iniciado no prazo': '#884EA0',
    'Backlog': '#A6ACAF',
    'Em Produção': '#58D68D',
}

# Define a data de início da tarefa mais antiga no dataframe para usar como referência
p_start = df['Início'].min()
fig = go.Figure()

# Adiciona barras (no fundo) claras para mostrar a duração estimada de cada tarefa
for index, row in df.iterrows():
    for index, row in df.iterrows():
        if isinstance(row['Informação'], str):
            info_list = [row['Atividade'], f"Status: {row['Status']}"] + row['Informação'].split("\n")
            hover_text = "<br>".join(
                ["• " + i if i not in [row['Atividade'], f"Status: {row['Status']}"] else i for i in info_list])
        elif pd.notna(row['Informação']):  # Verifica se a informação não é nan
            hover_text = row['Atividade'] + "<br>" + f"Status: {row['Status']}" + "<br><br>" + str(row['Informação'])
        else:
            hover_text = row['Atividade'] + "<br>" + f"Status: {row['Status']}"

        if row['Status'] == 'Backlog':
            color = colors_status['Backlog']
            opacity = 1.0
        elif row['Status'] == 'Em Produção':
            color = colors_status['Em Produção']
            opacity = 1.0
        else:
            color = colors_tech[row['Tecnologia']]
            opacity = 0.3

        fig.add_trace(go.Bar(
            x=[row['Duração Estimada']],
            y=[row['Atividade']],
            name=row['Tecnologia'],
            orientation='h',
            marker=dict(color=color, opacity=opacity),
            base=(row['Início'] - p_start).days,
            width=0.5,
            showlegend=False,
            hoverinfo="text",  # Mostra apenas o texto definido em 'hovertext'
            hovertext=hover_text  # Dados da coluna "Informação" da planilha formatada para ser exibida
        ))


#Chamada da barra que relaciona itens
#Vindo do dependency_lines.py
fig = draw_dependency_lines(fig, df, p_start)


border_thickness = 0.05

# Sobreposição da barra clara com barras escuras para mostrar a porcentagem concluída de cada tarefa
for index, row in df.iterrows():
    if row['Status'] != 'Backlog':
        # Calcula as posições para as bordas
        left = (row['Início'] - p_start).days
        right = left + row['Duração Real']
        top = index + 0.3 - border_thickness
        bottom = index - 0.3 + border_thickness


        # Cria as linhas que formarão as bordas
        # Lado esquerdo
        fig.add_shape(
            type="line",
            x0=left,
            x1=left,
            y0=bottom,
            y1=top,
            line=dict(color=colors_status[row['Status']], width=10*border_thickness),
            yref='y'
        )

        # Lado direito
        fig.add_shape(
            type="line",
            x0=right,
            x1=right,
            y0=bottom,
            y1=top,
            line=dict(color=colors_status[row['Status']], width=10*border_thickness),
            yref='y'
        )

        # Lado superior
        fig.add_shape(
            type="line",
            x0=left,
            x1=right,
            y0=top,
            y1=top,
            line=dict(color=colors_status[row['Status']], width=10*border_thickness),
            yref='y'
        )

        # Lado inferior
        fig.add_shape(
            type="line",
            x0=left,
            x1=right,
            y0=bottom,
            y1=bottom,
            line=dict(color=colors_status[row['Status']], width=10*border_thickness),
            yref='y'
        )
    for index, row in df.iterrows():
        if row['Status'] == 'Em Produção':
            if pd.notna(row['Closing Date']):  # Certifique-se de que 'Closing Date' não é NaN
                emoji_x_pos = (row['Closing Date'] - p_start).days + 1  # Posição x baseada na "Closing Date"
            else:
                emoji_x_pos = (row['Início'] - p_start).days + row[
                    'Duração Estimada'] + 1  # Se "Closing Date" for NaN, mantém o cálculo anterior

            fig.add_annotation(
                text="🚀",
                x=emoji_x_pos,  # Atualizado para a posição baseada na "Closing Date"
                y=index,
                showarrow=False,
                font=dict(size=18)
            )

# Adiciona uma barra vermelha para tarefas com um problema durante intervalos específicos
for index, row in df.iterrows():
    if pd.notna(row['Bugs']):  # Verifica se a coluna 'Bugs' contém dados
        intervals = row['Bugs'].split(';')
        for interval in intervals:
            start_date_str, end_date_str = interval.split('-')
            start_date = pd.to_datetime(start_date_str.strip(), dayfirst=True)
            end_date = pd.to_datetime(end_date_str.strip(), dayfirst=True)

            # Calcula a duração do problema em dias
            problem_duration = (end_date - start_date).days

            fig.add_trace(go.Bar(
                x=[problem_duration],
                y=[row['Atividade']],
                name="Problema",
                orientation='h',
                marker=dict(color='red', opacity=0.5),
                base=(start_date - p_start).days,
                width=0.5,
                showlegend=False,
                hoverinfo="text",
                hovertext=f"Problema de {start_date_str.strip()} a {end_date_str.strip()}"
            ))

# Adiciona linhas tracejadas para mostrar o data estimada de cada tarefa
for index, row in df.iterrows():
    due_date_pos = (row['Due Date'] - p_start).days
    fig.add_shape(
        type="line",
        x0=due_date_pos,
        x1=due_date_pos,
        y0=index - 0.4,
        y1=index + 0.4,
        line=dict(color="black", width=1.5, dash="dash"),
        yref='y',
    )

# Adiciona uma linha tracejada para mostrar o dia atual no gráfico
current_day = (datetime.now() - p_start).days
fig.add_shape(
    type="line",
    x0=current_day,
    x1=current_day,
    y0=0, # ajuste comecar na borda inferior da barra
    y1=1, # ajuste terminar na borda superior da barra
    yref='paper',
    line=dict(color="orange", width=2, dash="dash"),
)


# Geração de ticks e posições
dates = pd.date_range(start=p_start, end=df['Due Date'].max(), freq='2W-MON')
x_ticks = [date.strftime('%d-%b') for date in dates]
x_ticks_pos = [(date - p_start).days for date in dates]

# Adiciona anotações de Sprint no gráfico
sprint_number = 1  # Número inicial da Sprint
for pos in x_ticks_pos:
    fig.add_annotation(
        text=f"Sprint {sprint_number}",
        x=pos+7,
        y=1.05,  # posição y para colocar no topo
        yref='paper',
        showarrow=False,
        font=dict(size=10)
    )
    sprint_number += 1

# Sua legenda personalizada
legend_elements = [
    ("Em Dev", "Amarelo", '#fcc42e'),
    ("Em Testes", "Azul", '#5c9cd4'),
    ("Em Implantação", "Verde", '#58D68D'),
    ("Demanda Paralisada", "Vermelho", '#E74C3C'),
    ("Refinamento", "Roxo", '#884EA0'),
    ("Produção", "🚀", None)
]

# Posições iniciais da legenda
legend_x = 0.1  # Posição inicial da legenda em relação ao gráfico (começa da esquerda)
legend_y = -0.1  # Posição vertical da legenda em relação ao gráfico (fora do gráfico)

# Cria a legenda usando anotações
for name, color_description, color_code in legend_elements:
    symbol = "■" if color_code else "🚀"  # Se não tiver um código de cor, use o emoji do foguete

    # Cor do símbolo ou emoji
    color = f'<span style="color:{color_code};">{symbol}</span>' if color_code else symbol

    fig.add_annotation(
        text=f"{color} {name} ({color_description})",
        x=legend_x,
        y=legend_y,
        xref='paper',
        yref='paper',
        showarrow=False,
        align='left',
        bgcolor="white",
        borderpad=4
    )

    # Distancia da posição x para a próxima anotação na legenda.
    legend_x += 0.125

fig.update_layout(
    title="Gráfico de Gantt: Progresso das Atividades",
    barmode='overlay',
    xaxis=dict(tickvals=x_ticks_pos, ticktext=x_ticks, gridcolor="grey", linecolor="grey"),
    yaxis=dict(autorange="reversed", linecolor="grey", tickfont=dict(size=12)),  # Ajuste da fonte do eixo y
    width=None,
    height=None,
    plot_bgcolor='white',  # Cor de fundo do gráfico
    paper_bgcolor='white',  # Cor de fundo do papel
    font=dict(color="black"),  # Cor da fonte
    title_font=dict(color="black"),  # Cor da fonte do título
    bargap=0  # Espaçamento entre barras
)

# Salva o gráfico como um arquivo HTML
fig.write_html("./docs/index.html", auto_open=True)
# Exibe o gráfico use para testes
#fig.show()

