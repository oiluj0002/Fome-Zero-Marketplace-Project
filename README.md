# 1. Problema de negócio

Parabéns! Você acaba de ser contratado como Cientista de Dados da empresa Fome Zero, e a sua principal tarefa nesse momento é ajudar o CEO Kleiton Guerra a identificar pontos chaves da empresa, respondendo às perguntas que ele fizer utilizando dados! 

A empresa Fome Zero é um marketplace de restaurantes. Ou seja, seu core business é facilitar o encontro e negociações de clientes e restaurantes. Os restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas e também uma nota de avaliação dos serviços e produtos do restaurante, dentre outras informações. 

O CEO Guerra também foi recém contratado e precisa entender melhor o negócio para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a Fome Zero, e para isso, ele precisa que seja feita uma análise nos dados da empresa e que sejam gerados dashboards a partir dessas análises, para responder às seguintes perguntas:

### Gerais: 
  
  1. Quantos restaurantes únicos estão registrados? 
  2. Quantos países únicos estão registrados? 
  3. Quantas cidades únicas estão registradas? 
  4. Qual o total de avaliações feitas? 
  5. Qual o total de tipos de culinária registrados? 

### Em relação aos países:

  1. Qual o nome do país que possui mais cidades registradas? 
  2. Qual o nome do país que possui mais restaurantes registrados? 
  3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4 registrados? 
  4. Qual o nome do país que possui a maior quantidade de tipos de culinária distintos? 
  5. Qual o nome do país que possui a maior quantidade de avaliações feitas? 
  6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem entrega? 7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam reservas? 
  8. Qual o nome do país que possui, na média, a maior quantidade de avaliações registradas? 
  9. Qual o nome do país que possui, na média, a maior nota média registrada? 
  10. Qual o nome do país que possui, na média, a menor nota média registrada? 
  11. Qual a média de preço de um prato para dois por país? 

### Em relação às cidades:

  1. Qual o nome da cidade que possui mais restaurantes registrados? 
  2. Qual o nome da cidade que possui mais restaurantes com nota média acima de 4? 
  3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de 2.5? 
  4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
  5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária distintas?
  6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem reservas? 
  7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem entregas? 
  8. Qual o nome da cidade que possui a maior quantidade de restaurantes que aceitam pedidos online? 

### Em relação aos restaurantes:

  1. Qual o nome do restaurante que possui a maior quantidade de avaliações? 
  2. Qual o nome do restaurante com a maior nota média? 
  3. Qual o nome do restaurante que possui o maior valor de um prato para duas pessoas? 
  4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor média de avaliação? 
  5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que possui a maior média de avaliação? 
  6. Os restaurantes que aceitam pedidos online são também, na média, os restaurantes que mais possuem avaliações registradas?
  7. Os restaurantes que fazem reservas são também, na média, os restaurantes que possuem o maior valor médio de um prato para duas pessoas? 
  8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América possuem um valor médio de prato para duas pessoas maior que as churrascarias americanas (BBQ)? 

### Em relação aos tipos de culinária:

  1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a maior média de avaliação? 
  2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do restaurante com a menor média de avaliação? 
  3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a maior média de avaliação? 
  4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do restaurante com a menor média de avaliação? 
  5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a maior média de avaliação? 
  6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do restaurante com a menor média de avaliação? 
  7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a maior média de avaliação? 
  8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do restaurante com a menor média de avaliação? 
  9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a maior média de avaliação? 
  10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do restaurante com a menor média de avaliação? 
  11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas pessoas? 
  12. Qual o tipo de culinária que possui a maior nota média? 
  13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos online e fazem entregas?

# 2. Premissas assumidas para a análise

1. Modelo de negócio presumido foi o Marketplace.
2. A análise foi realizada em Agosto/2023.
3. As 4 principais visões de negócio foram: Visão geral, visão dos países, visão das cidades e visão dos restaurantes.
4. Foi assumida a necessidade de conversão das moedas para Dólar Americano (USD) para facilitar a análise de custo dos pratos.

# 3. Estratégia da solução

O dashboard estratégico foi elaborado utilizando indicadores que refletem as 4 visões de negócio assumidas relativas à empresa:

  1. Visão geral
  2. Visão dos países
  3. Visão das cidades
  4. Visão dos restaurantes

Cada visão é representada pelo seguinte conjunto de métricas:
	
### 1. Visão geral
  1. Quantidade de restaurantes cadastrados
  2. Quantidade de países cadastrados
  3. Quantidade de cidades cadastradas
  4. Total de avaliações realizadas
  5. Tipos de culinária cadastrados
  6. Geolocalização dos restaurantes cadastrados

### 2. Visão dos países
  1. Quantidade de cidades cadastradas por país
  2. Quantidade de restaurantes cadastrados por país
  3. Total de avaliações por país
  4. Avaliação média dos restaurantes por país
  5. Custo médio de um prato para dois
  6. Quantidade de tipos diferentes de culinária por país

### 3. Visão das cidades
  1. Cidades com mais restaurantes cadastrados
  2. Cidades com avaliação média maior que 4.0
  3. Cidades com avaliação média menor que 2.5
  4. Preço médio de um prato para dois por cidade
  5. Quantidade de tipos de culinária por cidade

### 4. Visão dos restaurantes
  1. Melhores restaurantes pelos tipos culinários: Italiano, americano, árabe, japonês e caseiro
  2. Melhores restaurantes independentemente dos tipos culinários
  3. Melhores tipos de culinária
  4. Piores tipos de culinária

# 4. Top 4 insights de dados

1. A Índia é o maior colaborador em número de restaurantes, cidades e avaliações de forma expressiva, porém possui a 3º pior avaliação média de restaurantes.
2. Apenas 4 dos 15 países possuem restaurantes com opção de entrega e pedidos online e todos são asiáticos.
3. Singapura apesar de possuir o menor número de restaurantes cadastrados, possui a maior média de custo de um prato para dois (quase o dobro do 3º colocado).
4. Os Estados Unidos possuem um alto número de cidades com maior custo médio de um prato para dois.

# 5. Produto final do projeto

Painel online, hospedado em um Cloud e disponível para acesso em qualquer dispositivo conectado à internet. 
O painel pode ser acessado através desse link: https://oiluj-fome-zero-dashboard.streamlit.app

# 6. Conclusão 

O objetivo desse projeto é criar um conjunto de gráficos, tabelas e mapas que exibem essas métricas da melhor forma possível para o novo CEO. 

Conclui-se que a Índia é o maior colaborador do aplicativo Fome Zero, seguido pelos Estados Unidos, onde compõem uma fatia expressiva do número de restaurantes cadastrados e usuários utilizando a plataforma.

Também pode-se inferir que há poucos restaurantes cadastrados que possuem a opção de entrega, visto que na demanda atual por serviços de entrega de comida no mundo pós-pandemia da COVID-19 é um sinal negativo para atração de novos usuários.

# 7. Próximos passos

1. Criação de novos filtros
2. Ajustar melhor as visões de negócios

