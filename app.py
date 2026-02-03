## Importa o Streamlit para construir a interface web.
import streamlit as st
## Importa o Pandas para manipular dados tabulares.
import pandas as pd
## Importa o Plotly Express para criar gráficos interativos.
import plotly.express as px


## --- Configuração da Página ---
## Define o título da página, o ícone e o layout para ocupar a largura inteira.
st.set_page_config(
    ## Define o título mostrado na aba do navegador.
    page_title= 'Dashboard de Salarios na Area de Dados ',
    ## Define o ícone mostrado na aba do navegador.
    page_icon= "📊",
    ## Define o layout para usar toda a largura disponível.
    layout="wide",
)
## --- Carregamento dos dados ---
## Carrega o dataset diretamente de uma URL pública.
df = pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")

## --- Barra Lateral (Filtros) ---
## Cria o cabeçalho da barra lateral para filtros.
st.sidebar.header("🔍 Filtros")

## Filtro de Ano
## Coleta e ordena os anos disponíveis no dataset.
anos_disponiveis = sorted(df['ano'].unique())
## Cria o seletor múltiplo de anos na barra lateral.
anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default=anos_disponiveis)

## Filtro de Senioridade
## Coleta e ordena as senioridades disponíveis no dataset.
senioridades_disponiveis = sorted(df['senioridade'].unique())
## Cria o seletor múltiplo de senioridade na barra lateral.
senioridades_selecionadas = st.sidebar.multiselect("Senioridade", senioridades_disponiveis, default=senioridades_disponiveis)
## Filtro por Tipo de Contrato
## Coleta e ordena os tipos de contrato disponíveis no dataset.
contratos_disponiveis = sorted(df['contrato'].unique())
## Cria o seletor múltiplo de contratos na barra lateral.
contratos_selecionados = st.sidebar.multiselect("Tipo de Contrato", contratos_disponiveis, default=contratos_disponiveis)

## Filtro por Tamanho da Empresa
## Coleta e ordena os tamanhos de empresa disponíveis no dataset.
tamanhos_disponiveis = sorted(df['tamanho_empresa'].unique())
## Cria o seletor múltiplo de tamanhos de empresa na barra lateral.
tamanhos_selecionados = st.sidebar.multiselect("Tamanho da Empresa", tamanhos_disponiveis, default=tamanhos_disponiveis)

## --- Filtragem do DataFrame ---
## O dataframe principal é filtrado com base nas seleções feitas na barra lateral.
df_filtrado = df[
    ## Mantém apenas linhas cujo ano está nos anos selecionados.
    (df['ano'].isin(anos_selecionados)) &
    ## Mantém apenas linhas cuja senioridade está nas senioridades selecionadas.
    (df['senioridade'].isin(senioridades_selecionadas)) &
    ## Mantém apenas linhas cujo contrato está nos contratos selecionados.
    (df['contrato'].isin(contratos_selecionados)) &
    ## Mantém apenas linhas cujo tamanho de empresa está nos tamanhos selecionados.
    (df['tamanho_empresa'].isin(tamanhos_selecionados))
]

## --- Conteúdo Principal ---
## Define o título principal da página.
st.title("🎲 Dashboard de Análise de Salários na Área de Dados")
## Mostra uma descrição curta do dashboard.
st.markdown("Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para refinar sua análise.")

## --- Métricas Principais (KPIs) ---
## Exibe o subtítulo da seção de métricas.
st.subheader("Métricas gerais (Salário anual em USD)")

## Verifica se há dados após o filtro.
if not df_filtrado.empty:
    ## Calcula o salário médio no recorte filtrado.
    salario_medio = df_filtrado['usd'].mean()
    ## Calcula o salário máximo no recorte filtrado.
    salario_maximo = df_filtrado['usd'].max()
    ## Conta o total de registros no recorte filtrado.
    total_registros = df_filtrado.shape[0]
    ## Encontra o cargo mais frequente no recorte filtrado.
    cargo_mais_frequente = df_filtrado["cargo"].mode()[0]
## Caso não existam dados filtrados.
else:
    ## Define valores padrão quando não há dados.
    salario_medio, salario_mediano, salario_maximo, total_registros, cargo_mais_comum = 0, 0, 0, ""

## Cria quatro colunas para exibir as métricas.
col1, col2, col3, col4 = st.columns(4)
## Exibe o salário médio na primeira coluna.
col1.metric("Salário médio", f"${salario_medio:,.0f}")
## Exibe o salário máximo na segunda coluna.
col2.metric("Salário máximo", f"${salario_maximo:,.0f}")
## Exibe o total de registros na terceira coluna.
col3.metric("Total de registros", f"{total_registros:,}")
## Exibe o cargo mais frequente na quarta coluna.
col4.metric("Cargo mais frequente", cargo_mais_frequente)

## Insere uma linha divisória na página.
st.markdown("---")

## --- Análises Visuais com Plotly ---
## Exibe o subtítulo da seção de gráficos.
st.subheader("Gráficos")

## Cria duas colunas para os gráficos da primeira linha.
col_graf1, col_graf2 = st.columns(2)

## Renderiza o primeiro gráfico na coluna da esquerda.
with col_graf1:
    ## Verifica se há dados antes de plotar.
    if not df_filtrado.empty:
        ## Calcula os 10 cargos com maior salário médio.
        top_cargos = df_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        ## Cria o gráfico de barras horizontais.
        grafico_cargos = px.bar(
            ## Define o dataframe de origem do gráfico.
            top_cargos,
            ## Define o eixo x como o salário médio.
            x='usd',
            ## Define o eixo y como os cargos.
            y='cargo',
            ## Define a orientação horizontal das barras.
            orientation='h',
            ## Define o título do gráfico.
            title="Top 10 cargos por salário médio",
            ## Define rótulos dos eixos.
            labels={'usd': 'Média salarial anual (USD)', 'cargo': ''}
        )
        ## Ajusta o alinhamento do título e ordenação do eixo y.
        grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        ## Exibe o gráfico no Streamlit.
        st.plotly_chart(grafico_cargos, use_container_width=True)
    ## Caso não existam dados após o filtro.
    else:
        ## Exibe um aviso de ausência de dados.
        st.warning("Nenhum dado para exibir no gráfico de cargos.")

## Renderiza o segundo gráfico na coluna da direita.
with col_graf2:
    ## Verifica se há dados antes de plotar.
    if not df_filtrado.empty:
        ## Cria o histograma de distribuição salarial.
        grafico_hist = px.histogram(
            ## Define o dataframe de origem do histograma.
            df_filtrado,
            ## Define o eixo x como salários.
            x='usd',
            ## Define o número de bins do histograma.
            nbins=30,
            ## Define o título do histograma.
            title="Distribuição de salários anuais",
            ## Define rótulos dos eixos.
            labels={'usd': 'Faixa salarial (USD)', 'count': ''}
        )
        ## Ajusta o alinhamento do título.
        grafico_hist.update_layout(title_x=0.1)
        ## Exibe o histograma no Streamlit.
        st.plotly_chart(grafico_hist, use_container_width=True)
    ## Caso não existam dados após o filtro.
    else:
        ## Exibe um aviso de ausência de dados.
        st.warning("Nenhum dado para exibir no gráfico de distribuição.")

## Cria duas colunas para os gráficos da segunda linha.
col_graf3, col_graf4 = st.columns(2)

## Renderiza o gráfico de tipos de trabalho na coluna da esquerda.
with col_graf3:
    ## Verifica se há dados antes de plotar.
    if not df_filtrado.empty:
        ## Conta a quantidade de registros por tipo de trabalho remoto.
        remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
        ## Renomeia as colunas para melhor leitura no gráfico.
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
        ## Cria o gráfico de pizza para tipos de trabalho.
        grafico_remoto = px.pie(
            ## Define o dataframe de origem do gráfico.
            remoto_contagem,
            ## Define os nomes das fatias.
            names='tipo_trabalho',
            ## Define os valores de cada fatia.
            values='quantidade',
            ## Define o título do gráfico.
            title='Proporção dos tipos de trabalho',
            ## Define o tamanho do furo no centro (donut).
            hole=0.5  
        )
        ## Exibe porcentagens e rótulos nas fatias.
        grafico_remoto.update_traces(textinfo='percent+label')
        ## Ajusta o alinhamento do título.
        grafico_remoto.update_layout(title_x=0.1)
        ## Exibe o gráfico no Streamlit.
        st.plotly_chart(grafico_remoto, use_container_width=True)
    ## Caso não existam dados após o filtro.
    else:
        ## Exibe um aviso de ausência de dados.
        st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")

## Renderiza o gráfico por país na coluna da direita.
with col_graf4:
    ## Verifica se há dados antes de plotar.
    if not df_filtrado.empty:
        ## Filtra apenas o cargo Data Scientist.
        df_ds = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']
        ## Calcula a média salarial por país.
        media_ds_pais = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()
        ## Cria o mapa coroplético por país.
        grafico_paises = px.choropleth(media_ds_pais,
            ## Define o código ISO3 de países.
            locations='residencia_iso3',
            ## Define a cor com base no salário médio.
            color='usd',
            ## Define a escala de cores.
            color_continuous_scale='rdylgn',
            ## Define o título do gráfico.
            title='Salário médio de Cientista de Dados por país',
            ## Define rótulos do gráfico.
            labels={'usd': 'Salário médio (USD)', 'residencia_iso3': 'País'})
        ## Ajusta o alinhamento do título.
        grafico_paises.update_layout(title_x=0.1)
        ## Exibe o mapa no Streamlit.
        st.plotly_chart(grafico_paises, use_container_width=True)
    ## Caso não existam dados após o filtro.
    else:
        ## Exibe um aviso de ausência de dados.
        st.warning("Nenhum dado para exibir no gráfico de países.") 

## --- Tabela de Dados Detalhados ---
## Exibe o subtítulo da seção da tabela.
st.subheader("Dados Detalhados")
## Exibe a tabela com os dados filtrados.
st.dataframe(df_filtrado)



