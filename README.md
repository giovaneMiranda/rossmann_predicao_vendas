# Rossmann Predição de Vendas. 
Este repositório contém analises e dados referentes a rede de drogarias Rossmann. 
Este projeto tem fins acadêmicos.

![](img/Rossmann.png)

## 1. Problema de Negócio
A Rossmann é uma rede de drogarias que opera mais de 3.000 lojas em 7 países europeus. Após reuniões estratégicas de negócio com os gerentes, foi solicitado pelo CFO da empresa, uma previsão de vendas das próximas 6 semanas de cada loja. A causa raiz é o planejamentos das reformas das lojas, onde o orçamento esta atrelado a receita futura das lojas. 

## 2. Premissa de Negócio
Os dados foram extraidos da competição iniciada pela Rossmann no Kaggle, porém é necessário assumir algumas premissas sobre o negócio.

- **Distância da competição:** 
  - A distância está expressada em metros, 
  - Lojas com distância igual a 0 são consideradas lojas sem competição próxima, para evitar viés no algoritmo ML  foi assumido um valor fixo (200000.0 metros), superior ao maior valor no conjunto de dados.  

- **Loja aberta:**
  - Removido o conjunto de dados onde indicava lojas fechadas, pois possuem receita 0.  

- **Sortimento:** 
  - Existe uma hierarquia entre os tipos de sortimento. Desse modo, as lojas com sortimento tipo C devem oferecer o tipo A e B.
  
- **Feriado:** 
  - Escolas estão fechadas em feriados e finais de semana

Atributos    | Definição
------------ | -------------
|id          | Identificador único para cada dupla (Store, Date)|
|Store       | Identificador único para a loja|
|Sales       | Receita referente as vendas do dia |
|Customers   | Número de clientes no dia|
|Open        | Indicador se a loja estava aberta, 0 = fechada 1 = aberta|
|StateHoliday |Indica um feriado estadial. Normalmente todas lojas, com poucas exeções, estão fechadas em feriados estaduais.  a = feriado, b = Feriado de Páscoa, c = Natal, 0 = Nenhum |
|SchoolHoliday| Indicador se (Store, Date) foi afetado pelas férias de escolas|
|StoreType   | Indica o modelo da loja: a, b, c, d|
|Assortment  |Indica o nível de sortimento da loja: a = básico, b = extra, c = estendido |
|CompetitionDistance |Distância em metros até a loja concorrente mais próxima|
|CompetitionOpenSince[Month/Year] | Indica o ano e mês aproximados do momento em que o competidor mais próximo foi aberto|
|Promo       | Indica se a loja está executando|
|Promo2       | Indica se a loja está executando uma promoção continua, 0 = loja não está participando, 1 = loja está participando | 
|Promo2Since[Year/Week]       | Indica ano e semana quando a loja começou a participar da Promo2 |
|PromoInterval     | Descreve os intervalos consecutivos Promo2 é iniciado, nomeando os meses em que a promoção é iniciada novamente. Por exemplo, "Fev, May,Aug,Nov" significa que cada rodada começa em fevereiro, maio, agosto, novembro de qualquer ano para aquela loja |

## 3. Estratégia de Solução

**01. Descrição dos Dados:** O objetivo é usar métricas estatísticas e analise descritiva, como dimensão dos dados e tipos de atributos para identificar dados fora do escopo de negócio.  

**02. Feature Engineering:** Tem como objetivo derivar as variáveis originais, obtendo variáveis que descrevem melhor o fenômeno que será modelado.

**03. Filtragem:** Filtrar linhas e selecionar colunas que não estejão relacionadas com informações para a modelagem e que não correspondam ao escopo de negócio. 

**04. Análise exploratória de dados:** Objetivo de explorar os dados ganhando experiência sobre o negócio, encontrar insights validando as hipóteses de negócio e entender melhor o impacto das variáveis no aprendizagem do modelo. 

**05. Modelagem de Dados:** Preparar os dados para que o modelo aprenda o comportamento do fenômeno.

**06. Seleção de Variáveis:** Seleção dos atributos mais significativas, tornando o modelo simples e garantindo que aprenda o suficiente para generalizar todos os exemplos.

**07. Modelagem de Machine Learning:** Implementar e treinar modelos de Machine Learning.

**08. Hyperparameter Fine Tunning:** Encontrar o conjunto de valores para os parâmetros do modelo selecionado na etapa anterior, com objetivo de maximizar o aprendizado. 

**09. Avaliação do Modelo e Conversão do Modelo em Valores de Negócio:** Converter o desempenho do modelo machine learning em um resultado de negócios.

**10. Implementar Modelo em Produção:** Publicar o modelo em ambientem nuvem para tornar os resultados acessíveis para qualquer consumidor seja pessoa ou serviços. 



## 4. Top 3 Inseghts. 

**Hipótese 01:** Lojas com competidores a menos de 1000m de distancia vendem 10% menos.

**Falso** Como observado lojas ccom competidores a menos de 1000m vendem 50% a mais que as demais, quanto maior a distancia dos competidores menor são as vendas da loja.


**Hipótese 02:** Lojas deveriam vender 5% a mais ao longo dos anos. 

**Falso** Lojas vendem 5% a menos ao longo dos anos. Como observado de 2013 a 2014 teve um baixa de 5% nas vendas, a queda nas vendas em 2015 se da pelo não fechamento do ano, porem o mesmo da sinais de baixa nas vendas.


**Hipótese 03:** Lojas vendem 20% mais no segundo semestre do ano.

**Falso** As lojas vendem aproximadamente 28% menos no segundo semestre.

## 5. Modelo de Machine Learning. 

Todos os algoritmos de Machine Learning foram treinados usando o *Cross Validation* nos dados de treinamento, calculando a performance real do modelo sobre a variabilidade dos dados, assim evitando pegar por acaso o melhor ou pior período. 


