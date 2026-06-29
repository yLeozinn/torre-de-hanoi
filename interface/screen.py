"""Tela principal em Pygame para jogar Torre de Hanoi."""

import pygame

from dados.dashboard import build_summary
from dados.tracker import GameTracker
from interface.assets import (
    ALTURA,
    CORES,
    CORES_DISCOS,
    FPS,
    LARGURA,
    draw_button,
    draw_text,
)
from interface.feedback import Feedback
from logica.movements import move_disk
from logica.state import GameState


class HanoiScreen:
    def __init__(self, total_discos=3):
        pygame.init()
        self.janela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Torre de Hanói Educacional")
        self.relogio = pygame.time.Clock()
        self.fonte_titulo = pygame.font.SysFont("arial", 56, bold=True)
        self.fonte_grande = pygame.font.SysFont("arial", 34, bold=True)
        self.fonte = pygame.font.SysFont("arial", 24, bold=True)
        self.fonte_pequena = pygame.font.SysFont("arial", 18)

        self.tela = "menu"
        self.total_discos = total_discos
        self.minimo_discos = 1
        self.maximo_discos = 5
        self.estado = GameState(total_discos)
        self.contador = GameTracker(total_discos)
        self.registros = []
        self.feedback = Feedback()
        self.torre_selecionada = None

        self.centros_torres = {"A": 245, "B": 500, "C": 755}
        self.area_tabuleiro = pygame.Rect(90, 130, 820, 365)

        self.botao_jogar = pygame.Rect(410, 300, 180, 46)
        self.botao_creditos = pygame.Rect(694, 300, 120, 46)
        self.botao_dados = pygame.Rect(185, 300, 120, 46)
        self.botao_menos = pygame.Rect(410, 220, 42, 42)
        self.botao_mais = pygame.Rect(548, 220, 42, 42)
        self.botao_menu = pygame.Rect(18, 18, 130, 34)
        self.botao_reiniciar = pygame.Rect(18, 60, 130, 34)
        self.botao_voltar = pygame.Rect(18, 18, 130, 34)
        self.botao_menu_vitoria = pygame.Rect(325, 402, 160, 42)
        self.botao_jogar_novamente = pygame.Rect(515, 402, 160, 42)

    def run(self):
        executando = True
        while executando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    executando = False
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    self.handle_click(evento.pos)

            self.draw()
            self.relogio.tick(FPS)

        pygame.quit()

    def handle_click(self, posicao):
        if self.tela == "menu":
            self.handle_menu_click(posicao)
        elif self.tela == "credits":
            if self.botao_voltar.collidepoint(posicao):
                self.tela = "menu"
        elif self.tela == "dashboard":
            if self.botao_voltar.collidepoint(posicao):
                self.tela = "menu"
        elif self.tela == "victory":
            self.handle_victory_click(posicao)
        else:
            self.handle_game_click(posicao)

    def handle_menu_click(self, posicao):
        if self.botao_menos.collidepoint(posicao):
            self.total_discos = max(self.minimo_discos, self.total_discos - 1)
        elif self.botao_mais.collidepoint(posicao):
            self.total_discos = min(self.maximo_discos, self.total_discos + 1)
        elif self.botao_jogar.collidepoint(posicao):
            self.start_game()
        elif self.botao_creditos.collidepoint(posicao):
            self.tela = "credits"
        elif self.botao_dados.collidepoint(posicao):
            self.tela = "dashboard"

    def handle_game_click(self, posicao):
        if self.botao_menu.collidepoint(posicao):
            self.tela = "menu"
            return
        if self.botao_reiniciar.collidepoint(posicao):
            self.reset_game()
            return

        torre_clicada = self.tower_at_position(posicao)
        if torre_clicada is None:
            return

        if self.torre_selecionada is None:
            if self.estado.top_disk(torre_clicada) is None:
                self.feedback.set_error("Essa torre esta vazia.")
                return
            self.torre_selecionada = torre_clicada
            self.feedback.set_info(f"Torre {torre_clicada} selecionada.")
            return

        moveu, mensagem = move_disk(self.estado, self.torre_selecionada, torre_clicada)
        if moveu:
            self.contador.register_move()
            self.feedback.set_info(mensagem)
            if self.estado.is_complete():
                self.contador.finish()
                self.registros.append(self.contador.summary())
                self.feedback.set_success("Desafio concluido.")
                self.tela = "victory"
        else:
            self.feedback.set_error(mensagem)
        self.torre_selecionada = None

    def handle_victory_click(self, posicao):
        if self.botao_menu_vitoria.collidepoint(posicao):
            self.tela = "menu"
        elif self.botao_jogar_novamente.collidepoint(posicao):
            self.start_game()

    def start_game(self):
        self.estado = GameState(self.total_discos)
        self.contador = GameTracker(self.total_discos)
        self.feedback = Feedback()
        self.torre_selecionada = None
        self.tela = "game"

    def tower_at_position(self, posicao):
        x, y = posicao
        if not self.area_tabuleiro.collidepoint(posicao):
            return None
        for nome, centro_x in self.centros_torres.items():
            if centro_x - 105 <= x <= centro_x + 105 and y >= 150:
                return nome
        return None

    def reset_game(self):
        self.estado.reset()
        self.contador.reset()
        self.torre_selecionada = None
        self.feedback.set_info("Jogo reiniciado.")

    def draw(self):
        if self.tela == "menu":
            self.draw_menu()
        elif self.tela == "credits":
            self.draw_credits()
        elif self.tela == "dashboard":
            self.draw_dashboard()
        elif self.tela == "victory":
            self.draw_game()
            self.draw_victory_modal()
        else:
            self.draw_game()
        pygame.display.flip()

    def draw_menu(self):
        self.janela.fill(CORES["fundo_menu"])
        draw_text(
            self.janela,
            "Torre de Hanói",
            self.fonte_titulo,
            CORES["texto"],
            centro=(LARGURA // 2, 120),
        )

        pygame.draw.line(self.janela, CORES["fundo_jogo"], (190, 372), (810, 372), 8)
        for x in self.centros_torres.values():
            pygame.draw.line(self.janela, CORES["fundo_jogo"], (x, 175), (x, 370), 8)

        pygame.draw.circle(self.janela, CORES["selecionado"], (LARGURA // 2, 241), 36)
        draw_button(self.janela, self.botao_menos, "-", self.fonte, CORES["botao_verde"])
        draw_button(self.janela, self.botao_mais, "+", self.fonte, CORES["botao_verde"])
        draw_text(
            self.janela,
            str(self.total_discos),
            self.fonte_grande,
            CORES["texto"],
            centro=(LARGURA // 2, 241),
        )
        draw_text(
            self.janela,
            "Discos",
            self.fonte_pequena,
            CORES["texto"],
            centro=(LARGURA // 2, 276),
        )

        draw_button(self.janela, self.botao_jogar, "JOGAR", self.fonte, CORES["botao"])
        draw_button(
            self.janela,
            self.botao_creditos,
            "Créditos",
            self.fonte,
            CORES["botao_secundario"],
        )
        draw_button(
            self.janela,
            self.botao_dados,
            "Dados",
            self.fonte,
            CORES["botao_dados"],
        )

    def draw_credits(self):
        self.janela.fill(CORES["fundo_menu"])
        draw_button(self.janela, self.botao_voltar, "Voltar", self.fonte_pequena, CORES["botao_desativado"])
        draw_text(self.janela, "Créditos", self.fonte_titulo, CORES["texto"], centro=(LARGURA // 2, 115))
        linhas = [
            "Projeto Torre de Hanói Educacional",
            "Professora Adria",
            "Desenvolvido por: <<<<<<(dps colocar nomes):>>>>>>"
            # Dps separar bonitinho os nomes, talvez com emojis ou algo do tipo
        ]
        for indice, linha in enumerate(linhas):
            draw_text(
                self.janela,
                linha,
                self.fonte if indice == 0 else self.fonte_pequena,
                CORES["texto"],
                centro=(LARGURA // 2, 230 + indice * 42),
            )

    def draw_dashboard(self):
        self.janela.fill(CORES["fundo_menu"])
        draw_button(self.janela, self.botao_voltar, "Voltar", self.fonte_pequena, CORES["botao_desativado"])
        draw_text(self.janela, "Dados", self.fonte_titulo, CORES["texto"], centro=(LARGURA // 2, 115))

        linhas = build_summary(self.registros).splitlines()
        for indice, linha in enumerate(linhas):
            draw_text(
                self.janela,
                linha,
                self.fonte if indice == 0 else self.fonte_pequena,
                CORES["texto"],
                centro=(LARGURA // 2, 210 + indice * 36),
            )

    def draw_game(self):
        self.janela.fill(CORES["fundo_jogo"])
        draw_button(self.janela, self.botao_menu, "Menu Inicial", self.fonte_pequena, CORES["botao_desativado"])
        draw_button(self.janela, self.botao_reiniciar, "Reiniciar", self.fonte_pequena, CORES["botao_desativado"])
        self.draw_towers()
        self.draw_footer()

    def draw_towers(self):
        base_y = self.area_tabuleiro.bottom - 30
        pygame.draw.rect(self.janela, CORES["base"], (120, base_y, 760, 14), border_radius=7)
        for nome, centro_x in self.centros_torres.items():
            cor_haste = CORES["selecionado"] if nome == self.torre_selecionada else CORES["haste"]
            pygame.draw.rect(self.janela, cor_haste, (centro_x - 6, 185, 12, base_y - 185), border_radius=6)
            self.draw_disks(nome, centro_x, base_y)

    def draw_disks(self, nome_torre, centro_x, base_y):
        altura_disco = 28
        largura_maxima = 170
        for nivel, disco in enumerate(self.estado.torres[nome_torre]):
            largura = 55 + int((disco / self.total_discos) * largura_maxima)
            x = centro_x - largura // 2
            y = base_y - ((nivel + 1) * altura_disco)
            cor = CORES_DISCOS[(disco - 1) % len(CORES_DISCOS)]
            pygame.draw.rect(
                self.janela,
                cor,
                (x, y, largura, altura_disco - 4),
                border_radius=10,
            )

    def draw_footer(self):
        cor = CORES.get(self.feedback.tipo, CORES["info"])
        draw_text(
            self.janela,
            self.feedback.mensagem,
            self.fonte_pequena,
            cor,
            canto_superior_esquerdo=(32, 570),
        )

        metricas = f"Movimentos: {self.contador.movimentos}   Tempo: {self.contador.elapsed_seconds()}s"
        rotulo = self.fonte_pequena.render(metricas, True, CORES["texto_claro"])
        self.janela.blit(rotulo, rotulo.get_rect(bottomright=(LARGURA - 24, ALTURA - 24)))

    def draw_victory_modal(self):
        sobreposicao = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        sobreposicao.fill((0, 0, 0, 135))
        self.janela.blit(sobreposicao, (0, 0))

        modal = pygame.Rect(220, 165, 560, 310)
        pygame.draw.rect(self.janela, CORES["painel"], modal, border_radius=12)
        pygame.draw.rect(self.janela, CORES["haste"], modal, width=4, border_radius=12)

        draw_text(self.janela, "Parabéns!", self.fonte_grande, CORES["texto"], centro=(LARGURA // 2, 220))
        mensagem = (
            f"Você concluiu em {self.contador.movimentos} movimentos. "
            f"A solução ideal utiliza {self.contador.optimal_moves()} movimentos."
        )
        draw_text(self.janela, mensagem, self.fonte_pequena, CORES["texto"], centro=(LARGURA // 2, 292))
        draw_text(self.janela, "Bom trabalho!", self.fonte, CORES["texto"], centro=(LARGURA // 2, 340))
        draw_button(
            self.janela,
            self.botao_menu_vitoria,
            "Menu Inicial",
            self.fonte_pequena,
            CORES["botao_secundario"],
        )
        draw_button(
            self.janela,
            self.botao_jogar_novamente,
            "Jogar de novo",
            self.fonte_pequena,
            CORES["botao"],
        )


def run_game(total_discos=3):
    HanoiScreen(total_discos).run()
