import pygame
from pygame.locals import *
import os

class GUIsolitaire(object):
    def __init__(self):
        pygame.init()
        self.fenetre = pygame.display.set_mode((600, 800))
        pygame.display.set_caption("Solitaire")

        self.path = os.path.dirname(__file__)

        self.fond = pygame.image.load(os.path.join(self.path, "fond.png")).convert()
        self.imgPiece = [pygame.image.load(os.path.join(self.path, "coupelle.png")).convert_alpha(),
                         pygame.image.load(os.path.join(self.path, "bille.png")).convert_alpha()]

        self.memoGrille = [[-1 for i in range(7)] for j in range(7)]
        self.texte = 'Le Solitaire'

        self.tan_pearl = os.path.join(self.path, "tan-pearl.otf")
        self.font = pygame.font.Font(self.tan_pearl, 24)
        self.chrono_font = pygame.font.Font(self.tan_pearl, 50)

        self.memoTime = 0
        self.gameTime = 0
        self._enableTime = False
        self.refresh()

    def _updateTime(self):
        self.gameTime = pygame.time.get_ticks() - self.memoTime

    def resetTime(self):
        self.memoTime = pygame.time.get_ticks()
        self.gameTime = 0

    def getTime(self):
        return self.gameTime // 1000

    def stopTime(self):
        self._enableTime = False

    def startTime(self):
        self._enableTime = True

    def chronoIsEnable(self):
        return self._enableTime

    def refresh(self, g=None, t=None):
        if g is None:
            g = self.memoGrille
        else:
            self.memoGrille = g
        if t is None:
            t = self.texte
        else:
            self.texte = t

        assert len(g) == 7, "La grille de jeu doit être une liste de 7 listes de 7 éléments !"
        assert len(g[0]) == 7, "La grille de jeu doit être une liste de 7 listes de 7 éléments !"

        self.fenetre.blit(self.fond, (0, 0))

        x0 = 65
        y0 = 165
        dx = 70
        dy = 70
        for y in range(len(g)):
            for x in range(len(g[y])):
                if g[y][x] in (0, 1):
                    self.fenetre.blit(self.imgPiece[g[y][x]], (x0 + x * dx, y0 + y * dy))

        wPol = 40
        taille = False
        while not taille:
            if t == 'Le Solitaire':
                police = pygame.font.Font(self.tan_pearl, wPol)
            else:
                police = pygame.font.SysFont("Roboto", wPol)
            texte = police.render(t, True, "#FFFFFF")
            if texte.get_width() < 600:
                taille = True
            else:
                wPol = int(wPol * 0.8)

        surfText = pygame.Rect(0, 0, 600, 60)
        surfText2 = pygame.Rect(0, 60, 600, 60)
        rectTexte = texte.get_rect()
        rectTexte.center = surfText.center
        self.fenetre.blit(texte, rectTexte)

        if self._enableTime:
            txtChrono = self.chrono_font.render(str(self.getTime()) + 's', True, '#2e2e2e')
            rectTxt = txtChrono.get_rect()
            rectTxt.center = surfText2.center
            self.fenetre.blit(txtChrono, rectTxt)

        pygame.display.update()

    def waitClick(self):
        while True:
            pygame.time.Clock().tick(30)

            if self._enableTime:
                self._updateTime()
                self.refresh()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        return (event.pos[0] - 65) // 70, (event.pos[1] - 165) // 70

                if event.type == KEYDOWN:
                    touches = {K_RIGHT: '_R', K_LEFT: '_L', K_UP: '_U', K_DOWN: '_D', K_RETURN: '_E', K_BACKSPACE: '_B',
                               K_ESCAPE: '_S'}
                    touche = event.key
                    if touche in touches:
                        return touches[touche]
                    return event.unicode

    def is_valid_move(self, x1, y1, x2, y2):
        if self.memoGrille[y1][x1] == 1 and self.memoGrille[y2][x2] == 0:
            if abs(x1 - x2) == 2 and y1 == y2:
                xm = (x1 + x2) // 2
                if self.memoGrille[y1][xm] == 1:
                    return True
            if abs(y1 - y2) == 2 and x1 == x2:
                ym = (y1 + y2) // 2
                if self.memoGrille[ym][x1] == 1:
                    return True
        return False

    def make_move(self, x1, y1, x2, y2):
        if self.is_valid_move(x1, y1, x2, y2):
            self.memoGrille[y1][x1] = 0
            self.memoGrille[y2][x2] = 1

            # Bille sur le point d'être supprimée
            if x1 == x2:
                self.memoGrille[(y1 + y2) // 2][x1] = 2
            else:
                self.memoGrille[y1][(x1 + x2) // 2] = 2
            self.refresh()

            # Suppression de la bille
            if x1 == x2:
                self.memoGrille[(y1 + y2) // 2][x1] = 0
            else:
                self.memoGrille[y1][(x1 + x2) // 2] = 0
                gui.resetTime()
            self.refresh()

if __name__ == "__main__":
    import time

    gui = GUIsolitaire()
    time.sleep(2)

    g = [[-1, -1, 0, 0, 0, -1, -1],
         [-1, 0, 0, 0, 0, 0, -1],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [-1, 0, 0, 0, 0, 0, -1],
         [-1, -1, 0, 0, 0, -1, -1]]

    gui.refresh(g, 'Le plateau est vide !')
    time.sleep(2)

    for y in range(7):
        for x in range(7):
            if g[y][x] == 0 and (x, y) != (3, 3):
                g[y][x] = 1
                gui.refresh(g, 'Remplissage ...')
                time.sleep(0.1)

    gui.refresh(g, 'A vous de jouer ... un clic et le chrono démarre !!')

    move_count = 0
    gui.resetTime()
    gui.stopTime()
    while True:
        if move_count % 2 == 0:
            click1 = gui.waitClick()
            click2 = gui.waitClick()
            gui.make_move(click1[0], click1[1], click2[0], click2[1])
            move_count += 1
            gui.startTime()
        else:
            click1 = gui.waitClick()
            click2 = gui.waitClick()
            gui.make_move(click1[0], click1[1], click2[0], click2[1])
            move_count += 1
