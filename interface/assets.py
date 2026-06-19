"""Paleta e elementos graficos reutilizaveis da interface Pygame."""

import pygame

LARGURA = 1000
ALTURA = 620
FPS = 60

CORES = {
    "fundo_menu": (217, 255, 184),
    "fundo_jogo": (75, 75, 75),
    "texto": (25, 25, 25),
    "texto_claro": (255, 255, 255),
    "suave": (190, 190, 190),
    "haste": (255, 143, 76),
    "base": (255, 143, 76),
    "selecionado": (255, 232, 85),
    "botao": (245, 72, 72),
    "botao_secundario": (24, 92, 184),
    "botao_verde": (33, 170, 71),
    "botao_desativado": (120, 120, 120),
    "texto_botao": (255, 255, 255),
    "painel": (238, 238, 238),
    "sobreposicao": (30, 30, 30),
    "erro": (255, 116, 116),
    "sucesso": (120, 255, 160),
    "info": (255, 255, 255),
}

CORES_DISCOS = [
    (255, 58, 58),
    (0, 91, 193),
    (11, 190, 103),
    (168, 85, 247),
    (249, 115, 22),
]


def draw_text(superficie, texto, fonte, cor, centro=None, canto_superior_esquerdo=None):
    rotulo = fonte.render(texto, True, cor)
    if centro:
        superficie.blit(rotulo, rotulo.get_rect(center=centro))
    elif canto_superior_esquerdo:
        superficie.blit(rotulo, canto_superior_esquerdo)
    return (
        rotulo.get_rect(center=centro)
        if centro
        else rotulo.get_rect(topleft=canto_superior_esquerdo)
    )


def draw_button(superficie, retangulo, texto, fonte, cor=None):
    cor_botao = cor or CORES["botao"]
    pygame.draw.rect(superficie, cor_botao, retangulo, border_radius=18)
    rotulo = fonte.render(texto, True, CORES["texto_botao"])
    superficie.blit(rotulo, rotulo.get_rect(center=retangulo.center))
