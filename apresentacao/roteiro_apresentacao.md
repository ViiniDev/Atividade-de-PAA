# Roteiro da apresentacao

Tempo sugerido: 15 a 20 minutos.

## 1. Titulo

Apresente o tema, seu nome, disciplina e professor. Diga que o trabalho e uma reescrita com implementacao de um artigo que usa divisao e conquista.

## 2. Artigo escolhido

Informe o titulo do artigo, autores, evento ACM-BCB 2020 e DOI. Explique que o artigo foi escolhido porque a tecnica de divisao e conquista aparece diretamente no algoritmo.

## 3. Problema

Explique que a cryo-EM gera mapas de densidade de moleculas biologicas. Para modelar uma molecula, e necessario separar o mapa em regioes correspondentes a cadeias ou subunidades. Essa separacao e chamada segmentacao.

## 4. Conceitos principais

Explique rapidamente:

- cryo-EM: tecnica de microscopia para observar moleculas congeladas;
- mapa de densidade: representacao 3D da molecula;
- voxel: unidade de volume do mapa 3D;
- watershed: tecnica classica de segmentacao inspirada em bacias hidrograficas.

## 5. Ideia geral

Mostre o ciclo principal: dividir, resolver subproblemas e combinar. Diga que o algoritmo primeiro faz uma segmentacao preliminar e depois usa divisao e conquista para reduzir o custo da combinacao.

## 6. Segmentacao preliminar

Explique que pontos abaixo de um limiar sao descartados, pontos restantes sao processados por densidade, regioes iniciais sao criadas e depois regioes pequenas sao mescladas.

## 7. Divisao

Explique que o artigo usa square-root divide-and-conquer: divide o mapa em aproximadamente raiz de n subimagens, cada uma com raiz de n voxels.

## 8. Subproblemas

Explique que cada subimagem e resolvida recursivamente. Quando o bloco fica pequeno, usa a segmentacao preliminar como caso base.

## 9. Combinacao

Explique que as regioes parciais sao reunidas e mescladas ate atingir no maximo K regioes finais. Essa e a etapa de conquista do algoritmo.

## 10. Complexidade

Compare a versao preliminar com a versao divide-and-conquer:

- preliminar: O(n log n + m^2 log m);
- divide-and-conquer: O(K^2 n log n), que para K pequeno se aproxima de O(n log n).

## 11. Implementacao

Diga que a implementacao foi feita em Python. O artigo usa mapas 3D reais, mas a implementacao usa matriz 2D sintetica para facilitar execucao e visualizacao. Reforce que a estrutura do algoritmo foi preservada.

## 12. Demonstracao

Mostre a imagem: a esquerda o mapa sintetico de densidade, a direita as regioes segmentadas. Explique que o script gera a matriz, divide recursivamente e combina as regioes.

## 13. Comparacao

Explique que o artigo compara com Segger, uma ferramenta conhecida de segmentacao para cryo-EM. O artigo relata desempenho competitivo, embora a comparacao seja dificil porque as ferramentas exigem parametros e interacao diferentes.

## 14. Limitacoes

Assuma claramente as limitacoes:

- implementacao 2D em vez de 3D;
- dados sinteticos em vez de mapas reais;
- tratamento de fronteira simplificado.

Finalize dizendo que, mesmo assim, a implementacao demonstra a tecnica de divisao e conquista.

## 15. Conclusao

Reforce as tres ideias principais:

- o problema pratico e segmentar mapas de cryo-EM;
- divisao e conquista reduz o custo da combinacao;
- o codigo demonstra divisao, recursao e merge.
