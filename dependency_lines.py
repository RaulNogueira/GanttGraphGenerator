
import pandas as pd

#Cria as linhas que conectam as tarefas que são interdependentes
def draw_dependency_lines(fig, df, p_start):
    offset = 0.5
    for index, row in df.iterrows():
        if pd.notna(row['Dependências']):
            dependencies = row['Dependências'].split(";")
            for dep in dependencies:
                dependent_index = df[df['Atividade'] == dep].index[0]

                # Pontos de início e fim para as linhas
                start_x = (df.at[dependent_index, 'Início'] - p_start).days + \
                          (df.at[dependent_index, 'Due Date'] - df.at[dependent_index, 'Início']).days / 2
                end_x = (row['Início'] - p_start).days
                start_y_offset = 0.250  # Offset to start below the bar
                start_y = dependent_index
                end_y = index

                # Verifique as tarefas intermediárias e encontre o espaço vazio
                intermediate_tasks = range(int(min(start_y, end_y)) + 1, int(max(start_y, end_y)))
                free_space_y = None
                for y in reversed(intermediate_tasks):
                    if y not in df.index:
                        free_space_y = y
                        break

                # Se não houver espaço vazio, use o offset padrão
                if free_space_y is None:
                    free_space_y = end_y - offset

                # Desenha a parte vertical da linha de dependência da tarefa de origem
                fig.add_shape(
                    type="line",
                    x0=start_x,
                    x1=start_x,
                    y0=start_y + start_y_offset,  # Start slightly below the bar
                    y1=end_y,  # Extend to the end task
                    line=dict(color="black", width=2)
                )

                # Desenhe a parte horizontal da linha de dependência
                fig.add_shape(
                    type="line",
                    x0=start_x,
                    x1=end_x,
                    y0=end_y,  # Now starts and ends at the dependent task
                    y1=end_y,
                    line=dict(color="black", width=2)
                )

                # Add arrow using annotation at the end of the horizontal line
                fig.add_annotation(
                    x=end_x,
                    y=end_y,
                    xref="x",
                    yref="y",
                    text="",
                    showarrow=True,
                    arrowhead=4,
                    ax=-10,
                    ay=0
                )

    return fig