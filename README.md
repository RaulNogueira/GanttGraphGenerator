#Gantt Graph Generator

O Objetivo desse código é apartir de um dataframe, neste caso uma planilha do excel, criar um grafico de Gantt baseado nas tarefas adicionadas na planilha, utilizando a biblioteca Plotly para gerar o grafico

## Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)


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


