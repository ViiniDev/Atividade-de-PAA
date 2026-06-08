# Atividade de PAA - Divisao e Conquista

Reescrita e implementacao do artigo:

**A Divide and Conquer Algorithm for Electron Microscopy Segmentation**  
Ruba Jebril, Yingde Zhu, Wei Chen e Kamal Al Nasr. ACM-BCB 2020.  
DOI: <https://doi.org/10.1145/3388440.3414700>

Este repositorio contem o relatorio em LaTeX, o artigo escolhido e uma
implementacao didatica do algoritmo de segmentacao por divisao e conquista.

## Estrutura do repositorio

```text
Atividade-de-PAA/
├── artigo/
│   ├── artigo-base.pdf
│   └── link-do-artigo.txt
├── codigo/
│   ├── requirements.txt
│   ├── segmentacao_dc.py
│   └── resultados/
├── latex/
│   ├── main.tex
│   ├── trabalho_paa.tex
│   ├── trabalho_paa.pdf
│   ├── referencias.bib
│   ├── figuras/
│   └── arquivos do template
└── apresentacao/
```

## Sobre a implementacao

O artigo original trabalha com mapas tridimensionais de densidade de cryo-EM,
nos quais cada unidade de volume e chamada de voxel. Para tornar a demonstracao
mais simples e executavel em qualquer computador, a implementacao deste
repositorio usa uma matriz 2D sintetica de densidade.

A adaptacao preserva a estrutura algoritmica principal:

1. filtra pontos abaixo de um limiar de densidade;
2. cria regioes iniciais por uma ideia semelhante ao watershed;
3. divide a entrada em subproblemas menores;
4. resolve cada subproblema recursivamente;
5. combina as regioes parciais por uma fase de merge;
6. gera uma visualizacao do mapa e da segmentacao final.

## Requisitos

- Python 3.10 ou superior;
- `numpy`;
- `matplotlib`.

As dependencias estao listadas em `codigo/requirements.txt`.

## Como executar o codigo

No PowerShell:

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

O arquivo gerado fica em:

```text
codigo/resultados/demo_segmentacao.png
```

## Parametros do script

O script aceita parametros opcionais:

```powershell
python segmentacao_dc.py --tamanho 128 --limiar 0.20 --regioes 4 --tamanho-base 32 --semente 7 --saida resultados\teste.png
```

Principais opcoes:

- `--tamanho`: tamanho da matriz sintetica quadrada.
- `--limiar`: valor minimo de densidade para considerar um ponto relevante.
- `--regioes`: numero alvo/maximo de regioes finais; em alguns mapas sinteticos, o merge pode retornar menos regioes.
- `--tamanho-base`: tamanho minimo usado como caso base da recursao.
- `--semente`: semente aleatoria para reproduzir o mesmo exemplo.
- `--saida`: caminho da imagem de saida.

## Como compilar o relatorio

O PDF ja esta disponivel em:

```text
latex/trabalho_paa.pdf
```

Para recompilar manualmente com MiKTeX/pdflatex:

```powershell
cd E:\PAA\Atividade-de-PAA\latex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
bibtex build\main.aux
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
copy build\main.pdf trabalho_paa.pdf
```

## Observacoes

- A implementacao e didatica e nao substitui ferramentas reais de segmentacao
  de cryo-EM.
- O artigo usa mapas 3D reais, enquanto o codigo usa uma matriz 2D sintetica.
- A simplificacao foi adotada para permitir demonstracao clara da tecnica de
  divisao e conquista dentro do escopo da atividade.
