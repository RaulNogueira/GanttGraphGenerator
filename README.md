#Gantt Graph Generator

EN:
The objective of this code is, from a dataframe, in this case an Excel spreadsheet, to create a Gantt chart based on the tasks added to the spreadsheet, using the Plotly library to generate the chart.

PT BR:
O Objetivo desse código é apartir de um dataframe, neste caso uma planilha do excel, criar um grafico de Gantt baseado nas tarefas adicionadas na planilha, utilizando a biblioteca Plotly para gerar o grafico


## Screenshots

![First Version](https://github.com/RaulNogueira/GanttGraphGenerator/raw/main/img/Gantt.jpg)
![Second Version](https://github.com/RaulNogueira/GanttGraphGenerator/raw/main/img/newplot.png)
![Latest Version](https://github.com/RaulNogueira/GanttGraphGenerator/raw/main/img/screenshot.png)


## Instalação

Para instalar basta clonar o repositório e usar: 

```bash
  pip install -r requirements.txt
```

## Windows x Mac

Não esqueça de mudar/adicionar as linhas:

```bash
    LN6: df = pd.read_excel('/Your/File/Location/', sheet_name='Sheet1')

    LN134: fig.write_html('/Your/File/Location/')
```
## Referência

 - [Plotly Python Documentation](https://plotly.com/python-api-reference/)


