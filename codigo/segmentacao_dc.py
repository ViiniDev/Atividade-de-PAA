"""Segmentacao por divisao e conquista inspirada no artigo escolhido.

O artigo original trabalha com mapas 3D de densidade de cryo-EM. Para a
atividade, esta implementacao usa matrizes 2D para permitir demonstracao,
testes e visualizacao sem depender de bases grandes ou ferramentas externas.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import math

import matplotlib.pyplot as plt
import numpy as np


BACKGROUND = 0


@dataclass(frozen=True)
class SegmentacaoResultado:
    """Resultado de uma segmentacao."""

    labels: np.ndarray
    quantidade_regioes: int


def vizinhos_8(linha: int, coluna: int, altura: int, largura: int):
    """Gera vizinhos 8-conectados dentro dos limites da imagem."""
    for dl in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dl == 0 and dc == 0:
                continue
            nl, nc = linha + dl, coluna + dc
            if 0 <= nl < altura and 0 <= nc < largura:
                yield nl, nc


def criar_mapa_sintetico(tamanho: int = 96, semente: int = 7) -> np.ndarray:
    """Cria uma imagem sintetica com regioes de densidade para demonstracao."""
    rng = np.random.default_rng(semente)
    y, x = np.mgrid[0:tamanho, 0:tamanho]
    centros = [
        (0.26 * tamanho, 0.30 * tamanho, 1.20, 10.0),
        (0.68 * tamanho, 0.30 * tamanho, 1.05, 12.0),
        (0.50 * tamanho, 0.68 * tamanho, 1.15, 13.0),
        (0.35 * tamanho, 0.78 * tamanho, 0.85, 9.0),
    ]

    mapa = np.zeros((tamanho, tamanho), dtype=float)
    for cy, cx, amplitude, sigma in centros:
        mapa += amplitude * np.exp(-(((x - cx) ** 2 + (y - cy) ** 2) / (2 * sigma**2)))

    mapa += 0.08 * rng.random((tamanho, tamanho))
    mapa = (mapa - mapa.min()) / (mapa.max() - mapa.min())
    return mapa


def segmentacao_preliminar_fase_1(mapa: np.ndarray, limiar: float) -> SegmentacaoResultado:
    """Inicializa regioes por crescimento em ordem decrescente de densidade.

    Esta fase segue a ideia do watershed descrito no artigo: voxels/pixels com
    densidade abaixo do limiar sao ignorados; os demais sao processados do mais
    denso para o menos denso e atribuidos a regioes vizinhas ja existentes.
    """
    altura, largura = mapa.shape
    labels = np.zeros_like(mapa, dtype=int)
    ativos = np.argwhere(mapa >= limiar)
    ordem = sorted(ativos, key=lambda p: mapa[p[0], p[1]], reverse=True)
    proximo_label = 1

    for linha, coluna in ordem:
        contagem = {}
        for nl, nc in vizinhos_8(linha, coluna, altura, largura):
            label = labels[nl, nc]
            if label != BACKGROUND:
                contagem[label] = contagem.get(label, 0) + 1

        if not contagem:
            labels[linha, coluna] = proximo_label
            proximo_label += 1
        else:
            labels[linha, coluna] = max(contagem.items(), key=lambda item: item[1])[0]

    return SegmentacaoResultado(labels=labels, quantidade_regioes=proximo_label - 1)


def maxima_por_regiao(mapa: np.ndarray, labels: np.ndarray) -> dict[int, tuple[int, int]]:
    """Retorna o pixel de maior densidade em cada regiao."""
    maxima = {}
    for label in np.unique(labels):
        if label == BACKGROUND:
            continue
        posicoes = np.argwhere(labels == label)
        melhor = max(posicoes, key=lambda p: mapa[p[0], p[1]])
        maxima[int(label)] = (int(melhor[0]), int(melhor[1]))
    return maxima


def encontrar_ascendente_mais_ingreme(
    mapa: np.ndarray,
    origem: int,
    candidatos: list[int],
    maxima: dict[int, tuple[int, int]],
) -> int | None:
    """Escolhe o maximo local que melhor atrai a regiao de origem."""
    lo, co = maxima[origem]
    melhor_label = None
    melhor_pontuacao = -math.inf

    for destino in candidatos:
        ld, cd = maxima[destino]
        distancia = math.hypot(lo - ld, co - cd)
        if distancia == 0:
            continue
        pontuacao = (mapa[ld, cd] - mapa[lo, co]) / distancia
        if pontuacao > melhor_pontuacao:
            melhor_pontuacao = pontuacao
            melhor_label = destino

    return melhor_label


def renumerar_labels(labels: np.ndarray) -> np.ndarray:
    """Compacta rotulos para 1..K, mantendo 0 como fundo."""
    novo = np.zeros_like(labels)
    proximo = 1
    for label in sorted(int(x) for x in np.unique(labels) if x != BACKGROUND):
        novo[labels == label] = proximo
        proximo += 1
    return novo


def mesclar_regioes(mapa: np.ndarray, labels: np.ndarray, k_final: int) -> SegmentacaoResultado:
    """Fase de combinacao: mescla regioes ate chegar a no maximo K regioes."""
    labels = renumerar_labels(labels)

    while True:
        regioes = [int(x) for x in np.unique(labels) if x != BACKGROUND]
        if len(regioes) <= k_final:
            break

        maxima = maxima_por_regiao(mapa, labels)
        regioes_ordenadas = sorted(regioes, key=lambda r: mapa[maxima[r]])
        metade = max(1, len(regioes_ordenadas) // 2)

        houve_merge = False
        for origem in regioes_ordenadas[:metade]:
            candidatos = [r for r in regioes_ordenadas if r != origem and r in maxima]
            destino = encontrar_ascendente_mais_ingreme(mapa, origem, candidatos, maxima)
            if destino is None:
                continue
            labels[labels == origem] = destino
            houve_merge = True

        labels = renumerar_labels(labels)
        if not houve_merge:
            break

    quantidade = len([x for x in np.unique(labels) if x != BACKGROUND])
    return SegmentacaoResultado(labels=labels, quantidade_regioes=quantidade)


def segmentacao_preliminar(mapa: np.ndarray, limiar: float, k_final: int) -> SegmentacaoResultado:
    """Executa watershed inicial e merge preliminar."""
    inicial = segmentacao_preliminar_fase_1(mapa, limiar)
    return mesclar_regioes(mapa, inicial.labels, k_final)


def dividir_em_blocos(mapa: np.ndarray, partes_por_eixo: int):
    """Divide a matriz em blocos aproximadamente iguais."""
    altura, largura = mapa.shape
    cortes_linhas = np.array_split(np.arange(altura), partes_por_eixo)
    cortes_colunas = np.array_split(np.arange(largura), partes_por_eixo)

    for linhas in cortes_linhas:
        for colunas in cortes_colunas:
            l0, l1 = int(linhas[0]), int(linhas[-1]) + 1
            c0, c1 = int(colunas[0]), int(colunas[-1]) + 1
            yield l0, l1, c0, c1, mapa[l0:l1, c0:c1]


def segmentacao_divisao_conquista(
    mapa: np.ndarray,
    limiar: float,
    k_final: int,
    tamanho_base: int = 32,
) -> SegmentacaoResultado:
    """Segmenta uma imagem usando a estrategia square-root divide-and-conquer."""
    n = mapa.size
    if n <= tamanho_base * tamanho_base:
        return segmentacao_preliminar(mapa, limiar, k_final)

    partes_por_eixo = max(2, round(n ** 0.25))
    labels_global = np.zeros_like(mapa, dtype=int)
    deslocamento = 0

    for l0, l1, c0, c1, bloco in dividir_em_blocos(mapa, partes_por_eixo):
        resultado_bloco = segmentacao_divisao_conquista(bloco, limiar, k_final, tamanho_base)
        labels_bloco = resultado_bloco.labels.copy()
        mascara = labels_bloco != BACKGROUND
        labels_bloco[mascara] += deslocamento
        labels_global[l0:l1, c0:c1] = labels_bloco
        deslocamento = int(labels_global.max())

    return mesclar_regioes(mapa, labels_global, k_final)


def iou_por_regiao(labels: np.ndarray, referencia: np.ndarray) -> list[float]:
    """Calcula IoU maximo de cada regiao segmentada contra uma referencia."""
    scores = []
    for label in [x for x in np.unique(labels) if x != BACKGROUND]:
        seg = labels == label
        melhor = 0.0
        for ref in [x for x in np.unique(referencia) if x != BACKGROUND]:
            gt = referencia == ref
            inter = np.logical_and(seg, gt).sum()
            union = np.logical_or(seg, gt).sum()
            melhor = max(melhor, inter / union if union else 0.0)
        scores.append(melhor)
    return scores


def salvar_visualizacao(mapa: np.ndarray, labels: np.ndarray, saida: Path) -> None:
    """Salva imagem com mapa de densidade e segmentacao."""
    saida.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    axes[0].imshow(mapa, cmap="viridis")
    axes[0].set_title("Mapa de densidade")
    axes[0].axis("off")
    axes[1].imshow(labels, cmap="tab20")
    axes[1].set_title("Regioes segmentadas")
    axes[1].axis("off")
    fig.tight_layout()
    fig.savefig(saida, dpi=160)
    plt.close(fig)


def executar_demo(args: argparse.Namespace) -> None:
    mapa = criar_mapa_sintetico(args.tamanho, args.semente)
    resultado = segmentacao_divisao_conquista(
        mapa,
        limiar=args.limiar,
        k_final=args.regioes,
        tamanho_base=args.tamanho_base,
    )

    salvar_visualizacao(mapa, resultado.labels, Path(args.saida))
    print(f"Regioes encontradas: {resultado.quantidade_regioes}")
    print(f"Visualizacao salva em: {args.saida}")


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Demo de segmentacao por divisao e conquista.")
    parser.add_argument("--tamanho", type=int, default=96, help="largura/altura da matriz sintetica")
    parser.add_argument("--limiar", type=float, default=0.18, help="limiar de densidade")
    parser.add_argument("--regioes", type=int, default=4, help="numero alvo de regioes")
    parser.add_argument("--tamanho-base", type=int, default=32, help="tamanho base da recursao")
    parser.add_argument("--semente", type=int, default=7, help="semente aleatoria")
    parser.add_argument("--saida", default="resultados/demo_segmentacao.png", help="arquivo de saida")
    return parser


if __name__ == "__main__":
    executar_demo(criar_parser().parse_args())
