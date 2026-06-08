# Guia de estudo para apresentacao

Este guia explica, em portugues e com mais detalhes, o artigo **A Divide and Conquer Algorithm for Electron Microscopy Segmentation** e como ele foi transformado no trabalho de PAA.

## 1. Ideia central do artigo

O artigo trata de um problema de segmentacao em imagens de microscopia crioeletronica, tambem chamada de **cryo-EM**.

Em termos simples, a cryo-EM e uma tecnica usada para visualizar moleculas biologicas muito pequenas, como proteinas e complexos moleculares. O resultado usado pelos pesquisadores nao e apenas uma foto comum, mas um **mapa tridimensional de densidade**. Esse mapa mostra onde provavelmente existe materia biologica dentro de um volume.

O problema e: depois que esse mapa 3D e produzido, os pesquisadores precisam separar a molecula em partes menores, chamadas de cadeias, subunidades ou regioes. Essa separacao e chamada de **segmentacao**.

O artigo propoe um algoritmo que usa **Divisao e Conquista** para fazer essa segmentacao de forma mais eficiente.

## 2. Por que segmentar mapas de cryo-EM?

Uma molecula grande pode ter varias partes. Por exemplo, uma proteina pode possuir mais de uma cadeia. Se o mapa de densidade inteiro for tratado como uma unica massa, fica dificil modelar a estrutura da molecula.

A segmentacao ajuda porque:

- separa regioes que pertencem a partes diferentes da molecula;
- facilita a modelagem estrutural posterior;
- reduz o trabalho manual de especialistas;
- permite analisar cada subunidade separadamente.

O artigo afirma que, quando a imagem e bem segmentada, o processo de modelagem fica mais facil e rapido.

## 3. Conceitos importantes

### 3.1 Cryo-EM

Cryo-EM significa **Cryogenic Electron Microscopy**, ou microscopia crioeletronica.

A ideia geral e:

1. Uma amostra biologica e congelada rapidamente.
2. Esse congelamento preserva a estrutura da molecula em estado proximo ao natural.
3. Um microscopio eletronico captura imagens da amostra.
4. Programas computacionais reconstruiem um mapa 3D da molecula.

Ela e muito usada porque algumas moleculas sao dificeis de estudar por cristalografia ou NMR.

### 3.2 Mapa de densidade

O mapa de densidade e uma representacao numerica do volume da molecula. Cada ponto do mapa possui um valor de intensidade/densidade.

Valores altos indicam regioes onde provavelmente existe materia biologica. Valores baixos podem indicar fundo, ruido ou regioes menos relevantes.

### 3.3 Voxel

Em imagens 2D, usamos o termo **pixel**.

Em imagens 3D, usamos o termo **voxel**, que significa **volumetric pixel**.

Um voxel e uma pequena unidade de volume. No artigo, quando se fala em agrupar voxels, significa agrupar pequenas celulas do mapa 3D para formar regioes maiores.

### 3.4 Segmentacao

Segmentar e dividir uma imagem ou volume em regioes com significado.

No artigo, segmentar significa separar o mapa de densidade em regioes que correspondem as partes da molecula.

### 3.5 Watershed

Watershed e uma tecnica classica de segmentacao. A analogia vem de relevo geografico.

Imagine uma imagem como se fosse um terreno:

- pontos altos representam regioes de maior densidade;
- pontos baixos representam vales;
- diferentes bacias podem ser separadas por fronteiras.

O algoritmo watershed tenta encontrar essas regioes. No artigo, ele e usado para criar uma segmentacao inicial, mas essa segmentacao pode gerar regioes demais. Por isso, depois e necessario fazer uma fase de combinacao/merge.

### 3.6 Segger

Segger e uma ferramenta conhecida para segmentacao de mapas de cryo-EM. O artigo usa o Segger como comparacao.

O Segger tambem usa ideias ligadas a watershed e agrupamento de regioes. No entanto, ele e uma ferramenta interativa, ou seja, depende de alguns ajustes e interacoes do usuario.

## 4. Problema que o artigo tenta resolver

O problema principal e segmentar mapas de cryo-EM de maneira eficiente.

O artigo parte da seguinte observacao:

- a segmentacao preliminar baseada em watershed e rapida para criar regioes iniciais;
- mas a fase de combinar essas regioes pode ficar cara quando ha muitas regioes;
- mapas grandes podem gerar muitas regioes preliminares;
- entao, em vez de combinar tudo de uma vez, os autores dividem o problema em partes menores.

Essa e a entrada da tecnica de Divisao e Conquista.

## 5. Como a Divisao e Conquista aparece no artigo?

A tecnica aparece de forma direta.

### 5.1 Dividir

O mapa de densidade e dividido em subimagens menores.

O artigo usa uma estrategia chamada **square-root divide and conquer**. Em vez de dividir em apenas duas partes, ele divide a entrada em aproximadamente raiz de `n` subimagens, cada uma com aproximadamente raiz de `n` voxels.

Se `n` e o numero total de voxels:

- numero de subimagens: aproximadamente `sqrt(n)`;
- tamanho de cada subimagem: aproximadamente `sqrt(n)`.

Essa divisao reduz o tamanho dos problemas que precisam ser resolvidos.

### 5.2 Conquistar/resolver subproblemas

Cada subimagem e segmentada recursivamente pelo mesmo algoritmo.

Quando a subimagem fica pequena o suficiente, o algoritmo usa a segmentacao preliminar baseada em watershed.

Essa e a base da recursao.

### 5.3 Combinar

Depois que cada subimagem gera suas regioes, o algoritmo junta as regioes parciais.

Essa combinacao usa a fase de merge da segmentacao preliminar. O objetivo e reduzir as regioes intermediarias ate chegar a no maximo `K` regioes finais.

`K` representa o numero desejado de regioes finais, por exemplo, o numero esperado de cadeias/subunidades.

## 6. Segmentacao preliminar do artigo

Antes da divisao e conquista, os autores apresentam um algoritmo preliminar. Ele tem duas fases.

### 6.1 Fase I: inicializacao das regioes

Entrada: mapa de densidade `D`.

Passos:

1. Aplica suavizacao/filtro.
2. Remove voxels abaixo de um limiar de densidade.
3. Ordena os voxels restantes em ordem decrescente de densidade.
4. Percorre cada voxel:
   - se ele nao toca nenhuma regiao existente, cria uma nova regiao;
   - se ele toca uma regiao, entra nessa regiao;
   - se ele toca varias regioes, entra naquela com mais vizinhos adjacentes.

Essa fase gera varias regioes pequenas e seus maximos locais.

### 6.2 Fase II: merge de regioes

Depois da fase inicial, pode haver regioes demais.

Cada regiao tem um maximo local, isto e, o voxel de maior densidade naquela regiao.

O algoritmo entao:

1. ordena os maximos locais;
2. pega regioes associadas a maximos de menor densidade;
3. procura para qual outro maximo local existe a subida mais ingreme;
4. mescla a regiao atual com a regiao desse maximo;
5. repete ate chegar ao numero desejado de regioes.

A ideia de "subida mais ingreme" tenta decidir qual regiao deve atrair outra regiao, considerando densidade e distancia.

## 7. Por que o algoritmo preliminar pode ser caro?

A Fase I tem custo dominado pela ordenacao:

```text
O(n log n)
```

Mas a Fase II, que faz merge das regioes, pode ter custo:

```text
O(m^2 log m)
```

Onde:

- `n` e o numero de voxels;
- `m` e o numero de regioes preliminares.

Mesmo que `m` seja menor que `n`, ele ainda pode ser grande. O termo quadratico `m^2` pode deixar a combinacao cara.

Por isso o artigo usa divisao e conquista: para diminuir o numero de regioes combinadas de uma vez.

## 8. Complexidade da versao Divide and Conquer

O artigo apresenta a recorrencia:

```text
T(n) = sqrt(n) T(sqrt(n)) + c (K sqrt(n))^2 log(Kn)
```

Interpretacao:

- `sqrt(n) T(sqrt(n))`: existem `sqrt(n)` subproblemas, cada um com tamanho `sqrt(n)`;
- `c (K sqrt(n))^2 log(Kn)`: custo de combinar as regioes produzidas pelos subproblemas;
- `K`: numero de regioes desejadas.

O artigo conclui que a complexidade fica:

```text
O(K^2 n log n)
```

Como `K` normalmente e pequeno em relacao a `n`, os autores simplificam a ideia para algo proximo de:

```text
O(n log n)
```

Essa e a grande otimizacao do artigo.

## 9. Melhoria de fronteira

Um problema da divisao e conquista e que a divisao pode cortar uma regiao que deveria permanecer junta.

Imagine que uma parte da molecula atravessa a fronteira entre duas subimagens. Se cada subimagem for segmentada separadamente, o algoritmo pode tratar essas partes como regioes diferentes.

Para reduzir esse problema, o artigo propoe usar voxels de fronteira no processo de merge. Especialmente voxels com densidade alta nas fronteiras podem ajudar a decidir que regioes de subimagens diferentes devem ser combinadas.

No nosso trabalho, essa melhoria foi explicada, mas implementada de forma simplificada. A implementacao faz um merge global depois da recursao, mas nao reproduz todos os detalhes especificos da regra de fronteira.

## 10. Experimentos do artigo

O artigo testou o metodo em 10 imagens reais de cryo-EM.

As imagens vieram do:

- **EMDB**: banco de mapas de microscopia eletronica;
- **PDB**: banco de estruturas moleculares.

Os autores compararam o algoritmo com o Segger.

O resultado geral foi:

- o metodo proposto teve desempenho competitivo;
- em alguns casos, ficou proximo do Segger;
- os autores destacam que a comparacao e dificil porque o Segger e interativo e depende de parametros/experiencia do usuario.

## 11. O que foi implementado no nosso trabalho?

Nosso codigo esta em:

```text
codigo/segmentacao_dc.py
```

Ele foi feito em Python.

O artigo trabalha com mapas 3D reais, mas nossa implementacao usa matriz 2D sintetica para facilitar:

- execucao em qualquer computador;
- visualizacao do resultado;
- demonstracao da tecnica de divisao e conquista.

Mesmo sendo 2D, a estrutura principal foi preservada:

1. gerar mapa sintetico de densidade;
2. aplicar limiar;
3. criar regioes preliminares;
4. dividir a matriz em blocos;
5. resolver blocos recursivamente;
6. combinar regioes;
7. salvar imagem com resultado.

## 12. Como explicar a implementacao

Voce pode dizer:

> A implementacao nao tenta substituir uma ferramenta real de cryo-EM. Ela e uma versao didatica para demonstrar a tecnica de divisao e conquista usada no artigo. Como mapas 3D reais exigem formatos e ferramentas especializadas, usamos uma matriz 2D sintetica. A logica de dividir, resolver recursivamente e combinar foi preservada.

## 13. Como executar o codigo

Comandos:

```powershell
cd E:\PAA\Atividade-de-PAA\codigo
python -m pip install -r requirements.txt
python segmentacao_dc.py
```

Saida esperada:

```text
Regioes encontradas: 4
Visualizacao salva em: resultados\demo_segmentacao.png
```

## 14. Explicacao da imagem da demonstracao

Na imagem da demonstracao:

- lado esquerdo: mapa sintetico de densidade;
- lado direito: regioes segmentadas.

O mapa sintetico simula regioes de maior densidade. O algoritmo tenta separar essas regioes e depois combina os blocos produzidos pela recursao.

## 15. Pontos fortes do artigo

- Aplica divisao e conquista em um problema real.
- Reduz custo da fase de combinacao.
- Usa uma base conhecida: watershed.
- Compara com uma ferramenta conhecida, o Segger.
- Apresenta analise de complexidade.

## 16. Limitacoes do artigo e da implementacao

### Do artigo

- O artigo e curto.
- A comparacao com Segger nao e totalmente justa, porque Segger e interativo.
- O desempenho depende de parametros como limiar e numero de regioes.

### Da nossa implementacao

- Usa matriz 2D, nao mapa 3D real.
- Usa dados sinteticos, nao imagens reais de cryo-EM.
- A melhoria de fronteira foi simplificada.
- E uma implementacao didatica, nao uma ferramenta profissional.

## 17. Resposta curta para "qual e a tecnica de divisao e conquista?"

> A divisao ocorre quando o mapa de densidade e dividido em subimagens menores. A conquista ocorre quando cada subimagem e segmentada recursivamente. A combinacao ocorre quando as regioes geradas nos subproblemas sao mescladas ate formar a segmentacao final.

## 18. Resposta curta para "por que isso melhora a eficiencia?"

> Porque o algoritmo evita fazer o merge de muitas regioes preliminares de uma vez no mapa inteiro. Ele combina regioes em blocos menores e depois faz uma combinacao global reduzida, diminuindo o impacto do termo quadratico da fase de merge.

## 19. Resposta curta para "por que voces nao usaram dados reais?"

> Porque mapas reais de cryo-EM sao tridimensionais, grandes e exigem formatos/ferramentas especificas. Para a atividade, o objetivo principal era demonstrar a tecnica de divisao e conquista. Por isso usamos uma matriz 2D sintetica, preservando a estrutura do algoritmo.

## 20. Conclusao para decorar

O artigo mostra que divisao e conquista pode ser aplicada alem de exemplos classicos como ordenacao. Nesse caso, ela e usada em segmentacao de imagens biologicas. A tecnica divide o mapa de densidade em partes menores, resolve cada parte e combina os resultados. A implementacao feita no trabalho demonstra essa logica em Python e ajuda a ligar a teoria de PAA com uma aplicacao pratica.
