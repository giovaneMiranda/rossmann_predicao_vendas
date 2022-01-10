# Rossmann Predição de Vendas. 
Este repositório contém analises e dados referentes a rede de drogarias Rossmann. 
Este projeto tem fins acadêmicos.

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

 Note que todas as escolas estão fechadas em feriados e finais de semana

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
