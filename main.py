import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import requests
from io import BytesIO

# Link direto para o download do arquivo no OneDrive
link = "https://onedrive.live.com/download?resid=418310F3CCC9CD06%21290&authkey=!ADTm63ig8VK0sXo&em=2"

# Baixar o arquivo usando requests
response = requests.get(link)
response.raise_for_status()  # Lançará um erro se houver um problema com a solicitação

# Usa o conteúdo baixado para criar um BytesIO stream e carregá-lo diretamente no pandas
df = pd.read_excel(BytesIO(response.content), sheet_name='Sheet1')

# Lê o dataframe a partir do arquivo Excel
#df = pd.read_excel('./task.xlsx', sheet_name='Sheet1')

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
    'iOS': '#C0C0C0',
    'Android': '#D3D3D3',
    'Angular': '#A9A9A9',
    'Testes': '#808080',
    'Acessibilidade': '#696969',
}

# Define cores para diferentes status
colors_status = {
    'Concluído': '#58D68D',
    'Início': '#5DADE2',
    'Em andamento': '#F4D03F',
    'Atrasado': '#E74C3C',
    'Não iniciado no prazo': '#884EA0',
    'Backlog': '#A6ACAF'
}

# Define a data de início mais antiga no dataframe para usar como referência e Inicializa um objeto Figure do Plotly
p_start = df['Início'].min()
fig = go.Figure()

# Adiciona barras claras para mostrar a duração estimada de cada tarefa
for index, row in df.iterrows():
    if row['Status'] == 'Backlog':
        color = colors_status['Backlog']
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
        showlegend=False
    ))

# Sobreponha a barra clara com barras escuras para mostrar a porcentagem concluída de cada tarefa
for index, row in df.iterrows():
    if row['Status'] != 'Backlog':
        if row['Status'] == "Atrasado":
            text = "Atrasado"
        elif row['Status'] == "Não iniciado no prazo":
            text = "Iniciado fora do prazo"
        else:
            text = None

        fig.add_trace(go.Bar(
            x=[row['Duração Real']],
            y=[row['Atividade']],
            name=row['Status'],
            orientation='h',
            marker=dict(color=colors_status[row['Status']]),
            base=(row['Início'] - p_start).days,
            width=0.5,
            text=text,
            textposition='auto',
            hovertext=row['Status'],
            showlegend=False
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
    y0=0, # ajuste para que comece na borda inferior da barra
    y1=1, # ajuste para que termine na borda superior da barra
    yref='paper',
    line=dict(color="orange", width=2, dash="dash"),
)

# Atualiza o layout do gráfico
dates = pd.date_range(start=p_start, end=df['Due Date'].max(), freq='W-MON')
x_ticks = [date.strftime('%d-%b') for date in dates]
x_ticks_pos = [(date - p_start).days for date in dates]

fig.update_layout(
    title="Gráfico de Gantt: Progresso das Atividades",
    barmode='overlay',
    xaxis=dict(tickvals=x_ticks_pos, ticktext=x_ticks, gridcolor="grey", linecolor="grey"),
    yaxis=dict(autorange="reversed", linecolor="grey", tickfont=dict(size=7)),  # Ajuste da fonte do eixo y
    width=800,
    height=400,
    plot_bgcolor='#344454',  # Cor de fundo do gráfico
    paper_bgcolor='#344454',  # Cor de fundo do papel
    font=dict(color="white"),  # Cor da fonte
    title_font=dict(color="white"),  # Cor da fonte do título
    bargap=0.2  # Espaçamento entre barras
)

# Salva o gráfico como um arquivo HTML
fig.write_html("./grafico_gantt.html")
# Exibe o gráfico use para testes sõ
fig.show()
