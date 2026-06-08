# Roteiro completo da apresentacao

Tempo sugerido: 15 a 20 minutos.

Este roteiro acompanha os slides em `apresentacao_paa.pdf`. A ideia nao e ler tudo literalmente, mas usar como guia para treinar a fala.

## Slide 1 - Titulo

Fala sugerida:

> Bom dia/boa noite. Meu nome e Vinicius Wanderley Arruda. Nesta apresentacao vou falar sobre a reescrita e implementacao de um artigo que utiliza a tecnica de Divisao e Conquista. O artigo escolhido aplica essa tecnica em segmentacao de imagens de microscopia eletronica, mais especificamente mapas de cryo-EM.

O que destacar:

- nome do trabalho;
- disciplina;
- professor;
- que a apresentacao cobre artigo, algoritmo e implementacao.

## Slide 2 - Artigo escolhido

Fala sugerida:

> O artigo escolhido se chama "A Divide and Conquer Algorithm for Electron Microscopy Segmentation". Ele foi publicado no ACM-BCB em 2020. Escolhi esse artigo porque a tecnica de Divisao e Conquista aparece diretamente no algoritmo proposto, nao apenas como uma referencia teorica. O objetivo dos autores e segmentar mapas de microscopia eletronica de forma mais eficiente.

O que destacar:

- titulo;
- autores;
- ACM;
- tema;
- justificativa da escolha.

## Slide 3 - Problema

Fala sugerida:

> A cryo-EM gera mapas tridimensionais de densidade de moleculas biologicas. Esses mapas ajudam pesquisadores a estudar proteinas e complexos moleculares. Mas, para modelar essas estruturas, muitas vezes e necessario separar o mapa em partes menores, correspondentes a cadeias ou subunidades. Esse processo e chamado de segmentacao. O problema e que fazer isso manualmente pode ser demorado e depende de conhecimento especializado.

O que destacar:

- entrada: mapa de densidade;
- saida: regioes segmentadas;
- motivacao: facilitar modelagem molecular.

## Slide 4 - Conceitos principais

Fala sugerida:

> Antes do algoritmo, existem tres conceitos importantes. O primeiro e cryo-EM, uma tecnica que congela rapidamente a amostra e usa microscopia eletronica para observar moleculas. O segundo e o mapa de densidade, que e a representacao 3D produzida a partir dessas imagens. Cada unidade desse volume e chamada de voxel. O terceiro e watershed, uma tecnica classica de segmentacao baseada na ideia de separar regioes como bacias em um relevo.

Possivel complemento:

> Em uma imagem 2D falamos em pixel; em uma imagem 3D falamos em voxel.

## Slide 5 - Ideia geral do algoritmo

Fala sugerida:

> A ideia geral do algoritmo segue exatamente o padrao de Divisao e Conquista. Primeiro, o problema e dividido em partes menores. Depois, cada parte e resolvida como um subproblema. Por fim, os resultados parciais sao combinados. No artigo, isso significa dividir o mapa de densidade em subimagens, segmentar cada subimagem e depois mesclar as regioes resultantes.

Ponto importante:

- diga explicitamente: dividir, resolver, combinar.

## Slide 6 - Segmentacao preliminar

Fala sugerida:

> Antes da divisao e conquista, o artigo apresenta uma segmentacao preliminar baseada em watershed. Primeiro, os voxels abaixo de um limiar de densidade sao descartados. Depois, os voxels restantes sao processados em ordem decrescente de densidade. Se um voxel nao toca nenhuma regiao, ele cria uma nova regiao. Se ele toca regioes existentes, ele e associado a uma delas. Depois, regioes pequenas sao mescladas com base nos maximos locais.

Termos para explicar se perguntarem:

- limiar: valor minimo para considerar um voxel relevante;
- maximo local: voxel de maior densidade dentro de uma regiao.

## Slide 7 - Divisao

Fala sugerida:

> A parte de divisao do artigo usa uma estrategia chamada square-root divide-and-conquer. Em vez de dividir o mapa em apenas duas partes, ele divide em aproximadamente raiz de n subimagens, cada uma com aproximadamente raiz de n voxels. Isso reduz o tamanho dos problemas e evita que a fase de combinacao trabalhe com regioes demais ao mesmo tempo.

Exemplo simples:

> Se o mapa fosse muito grande, em vez de segmentar tudo de uma vez, o algoritmo separa em blocos menores.

## Slide 8 - Subproblemas

Fala sugerida:

> Cada subimagem gerada pela divisao passa a ser um novo problema de segmentacao. O algoritmo chama a si mesmo recursivamente para resolver cada bloco. Quando o bloco fica pequeno o suficiente, ele usa a segmentacao preliminar como caso base. Isso e tipico de algoritmos de Divisao e Conquista.

Ponto importante:

- mencionar recursao;
- mencionar caso base.

## Slide 9 - Combinacao

Fala sugerida:

> Depois que os subproblemas sao resolvidos, o algoritmo precisa combinar as regioes obtidas em cada bloco. Essa e a etapa de conquista. Cada subproblema pode gerar ate K regioes, e a fase de merge e aplicada para reduzir as regioes parciais ate chegar a no maximo K regioes finais. O artigo tambem observa que regioes de fronteira entre subimagens precisam de cuidado, porque uma divisao pode cortar uma regiao que deveria permanecer junta.

Ponto importante:

- K = numero desejado ou maximo de regioes finais.

## Slide 10 - Analise de complexidade

Fala sugerida:

> A segmentacao preliminar tem uma parte de ordenacao, com custo O(n log n), mas a fase de merge pode custar O(m² log m), onde m e o numero de regioes preliminares. Esse termo quadratico pode ser caro. Com divisao e conquista, o artigo chega a complexidade O(K² n log n). Como K costuma ser pequeno em relacao ao tamanho do mapa, a ideia se aproxima de O(n log n), tornando o processo mais eficiente.

Se quiser simplificar:

> O ganho vem de nao fazer uma combinacao enorme de uma vez.

## Slide 11 - Implementacao desenvolvida

Fala sugerida:

> A implementacao foi feita em Python. O artigo trabalha com mapas 3D reais de cryo-EM, mas para a atividade eu implementei uma versao didatica usando uma matriz 2D sintetica. Essa simplificacao permite executar e visualizar o algoritmo facilmente, mas preserva a estrutura principal: aplicar limiar, criar regioes preliminares, dividir em blocos, resolver recursivamente e combinar.

Se perguntarem por que 2D:

> Porque o foco da atividade e demonstrar a tecnica de Divisao e Conquista, e mapas 3D reais exigem formatos e ferramentas especificas.

## Slide 12 - Demonstracao pratica

Fala sugerida:

> Nesta imagem, a esquerda temos o mapa sintetico de densidade gerado pelo codigo. As regioes mais intensas simulam partes importantes do mapa. A direita temos o resultado da segmentacao. O algoritmo dividiu a matriz, resolveu os blocos e depois combinou as regioes. Na execucao padrao, ele encontra 4 regioes.

Se for demonstrar no terminal:

```powershell
cd E:\PAA\Atividade-de-PAA\codigo
python segmentacao_dc.py
```

Saida esperada:

```text
Regioes encontradas: 4
Visualizacao salva em: resultados\demo_segmentacao.png
```

## Slide 13 - Comparacao

Fala sugerida:

> O artigo compara o metodo proposto com o Segger, que e uma ferramenta conhecida para segmentacao de mapas de cryo-EM. Os autores dizem que a comparacao nao e perfeita, porque o Segger e interativo e depende de parametros e experiencia do usuario. Mesmo assim, o metodo proposto apresentou desempenho competitivo nos testes com 10 imagens reais.

O que destacar:

- Segger e referencia pratica;
- metodo proposto e competitivo;
- comparacao tem limitacoes.

## Slide 14 - Limitacoes

Fala sugerida:

> A principal limitacao da nossa implementacao e que ela usa uma matriz 2D sintetica, enquanto o artigo usa mapas 3D reais. Alem disso, o tratamento especial de fronteiras foi simplificado. Entao o codigo nao e uma ferramenta biologica completa, mas sim uma implementacao didatica para mostrar a tecnica de Divisao e Conquista.

Importante:

- assumir limitacoes com seguranca;
- reforcar que o objetivo da atividade foi cumprido.

## Slide 15 - Conclusao

Fala sugerida:

> Como conclusao, o artigo mostra uma aplicacao pratica de Divisao e Conquista fora dos exemplos classicos. A tecnica ajuda a segmentar mapas de cryo-EM dividindo o problema em subproblemas menores e combinando os resultados. A implementacao em Python demonstra essa ideia na pratica, conectando a teoria da disciplina com um problema real de processamento de imagens e bioinformatica.

Tres frases para memorizar:

- O problema e segmentar mapas de densidade de cryo-EM.
- A tecnica divide o mapa, resolve subproblemas e combina regioes.
- A implementacao demonstra essa estrutura em Python.

## Slide 16 - Perguntas

Fala sugerida:

> Obrigado. Estou disponivel para perguntas.

## Perguntas provaveis e respostas

### 1. Onde exatamente esta a Divisao e Conquista?

Resposta:

> Na divisao do mapa em subimagens, na resolucao recursiva de cada subimagem e na combinacao das regioes segmentadas ao final.

### 2. Por que o artigo nao usa divisao binaria?

Resposta:

> Ele usa square-root divide-and-conquer para reduzir melhor o custo da fase de merge. A ideia e gerar varios subproblemas menores em vez de apenas dois subproblemas grandes.

### 3. O que e voxel?

Resposta:

> Voxel e o equivalente 3D do pixel. Em vez de representar um ponto em uma imagem plana, ele representa uma pequena celula de volume em um mapa tridimensional.

### 4. O que e watershed?

Resposta:

> Watershed e uma tecnica de segmentacao baseada em uma analogia com relevo. Ela separa regioes como se fossem bacias hidrograficas em uma superficie.

### 5. Por que a implementacao usa 2D se o artigo usa 3D?

Resposta:

> Porque a atividade pede a implementacao da ideia do algoritmo. Mapas 3D reais exigem formatos e ferramentas especificas. A versao 2D permite demonstrar claramente divisao, recursao e combinacao.

### 6. A implementacao reproduz exatamente o artigo?

Resposta:

> Nao exatamente. Ela e uma adaptacao didatica. A estrutura principal foi preservada, mas os dados reais 3D e o tratamento completo de fronteiras foram simplificados.

### 7. Qual foi a principal otimizacao?

Resposta:

> A principal otimizacao foi evitar o merge global de muitas regioes preliminares. O algoritmo divide o mapa, faz merges menores e depois combina os resultados.

### 8. Qual e a complexidade final?

Resposta:

> O artigo apresenta O(K² n log n). Como K e o numero de regioes desejadas e costuma ser pequeno, a complexidade e interpretada como proxima de O(n log n).

### 9. O que e Segger?

Resposta:

> Segger e uma ferramenta usada para segmentar mapas de cryo-EM. O artigo compara o metodo proposto com o Segger.

### 10. Qual a conclusao principal?

Resposta:

> Divisao e Conquista pode ser aplicada a problemas praticos de segmentacao, reduzindo o custo de combinacao e tornando o processamento mais eficiente.
