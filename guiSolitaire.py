# Grégory Coutable 2022
# Partage sous licence Creative Commons :
# https://creativecommons.org/licenses/by-sa/3.0/fr/
#
# Version 1

import pygame
from pygame.locals import *
#pour le rendre dispo de n'importe où
import os
pathname = os.path.dirname(__file__)

class GUIsolitaire (object):
    
    def __init__(self):
        """
        Initialise une fenètre du jeu puissance 4 et l'affiche totalement vide.
        Cette classe ne contient aucun attribut publique.
        """
        
        #initialisation de pygame
        pygame.init()
        #on définit la fenêtre de base de notre jeu
        self.fenetre = pygame.display.set_mode((600, 800))
        #un titre sur cette fenêtre
        pygame.display.set_caption("Solitaire")
        #Chargement et collage du fond
        self.fond = pygame.image.load(os.path.join(pathname, "fond.png")).convert()
        
        #Chargement des images des pièces
        self.imgPiece = [pygame.image.load(os.path.join(pathname, "coupelle.png")).convert_alpha(), pygame.image.load(os.path.join(pathname, "bille.png")).convert_alpha()]
        
        
        self.refresh([[-1 for i in range(7)] for j in range(7)],'Le solitaire')
        
        


    
    def refresh(self, g, t):
        """
        Cette méthode rafraichie l'affichage du jeu de solitaire conformément à la grille passée en argument.
        
        g est une grille de 7*7 éléments.
        Par exemple g[0][0] est la case en haut a gauche, g[6][6] est la case en bas à droite.
        0 désigne une coupelle vide, 1 une bille, tout autre valeur n'affiche rien !
        
        t est un texte à afficher, centré dans le bandeau du haut.
        """
        #vérification de la taille de g
        assert len(g) == 7, "La grille de jeu doit être une liste de 7 listes de 7 éléments !"
        assert len(g[0]) == 7, "La grille de jeu doit être une liste de 7 listes de 7 éléments !"
        
        #réinitialisation du fond
        self.fenetre.blit(self.fond, (0,0))

        #offset pour la premiere pièce
        x0 = 65
        y0 = 165 
        dx = 70
        dy = 70
        for y in range(len(g)):
            for x in range(len(g[y])):
                if g[y][x] in (0, 1):
                    self.fenetre.blit(self.imgPiece[g[y][x]], (x0 + x*dx, y0 + y*dy))

        #zone de texte
        #adaptation automatique de la taille de la police dans la zone de saisie
        wPol = 40
        taille = False
        while not taille:
            police = pygame.font.SysFont("Arial Black", wPol)
            texte = police.render(t, True, "#3F48CB")
            if texte.get_width() < 600:
                taille = True
            else:
                wPol = int(wPol * 0.8)
        
        #Une surface pour centrer le texte sur le bandeau du haut
        surfText = pygame.Rect(0, 0, 600, 60)
        surfText2 = pygame.Rect(0, 60, 600, 60)
        #pour centrer le texte
        rectTexte = texte.get_rect()
        rectTexte.center = surfText.center
        self.fenetre.blit(texte, rectTexte)
        
        #Rafraîchissement de l'écran
        pygame.display.update()
        
    def waitClick(self):
        """
        Cette méthode attend l'action d'un joueur. Elle gère trois type d'actions :
            - demande fermeture de la fenètre : fermeture propre de la fenètre pygame et fin du programme python.
            - click sur la fenetre : retourne un tuple contenant les coordonnées de l'emplacement cliqué.
            - appui sur les touches y, n, s, r, c, d, o : retourne le caractère correspondant.
        Une fois exécutée, on ne peut sortir de cette méthode que par l'une de ces trois actions.

        """
        while True:
            #Limitation de vitesse de la boucle
            pygame.time.Clock().tick(30)
            
            for event in pygame.event.get():    #Attente des événements
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                    
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:   #Si clic gauche
                        return (event.pos[0] - 65)//70, (event.pos[1] - 165)//70
                    
                if event.type == KEYDOWN:
                    touches = {K_RIGHT : '_R', K_LEFT : '_L', K_UP : '_U', K_DOWN : '_D', K_RETURN : '_E', K_BACKSPACE : '_B', K_ESCAPE : '_S'}
                    touche = event.key
                    if touche in touches:
                        return touches[touche]
                    return event.unicode
                    
                         
if __name__ == "__main__":
    import time
    #instanciation d'une fenètre de puissance 4
    j = GUIsolitaire()
    time.sleep(2)
    
    #création d'une grille vierge
    g = [[-1, -1, 0, 0, 0, -1, -1],
         [-1, 0, 0, 0, 0, 0, -1],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [-1, 0, 0, 0, 0, 0, -1],
         [-1, -1, 0, 0, 0, -1, -1]]

    j.refresh(g, 'Le plateau est vide !')
    time.sleep(2)
    
    for y in range(7):
        for x in range(7):
            if g[y][x] == 0 and (x, y) != (3, 3) :
                g[y][x] = 1
                j.refresh(g, 'Remplissage ...')
                time.sleep(0.1)
            
    j.refresh(g, 'A vous de jouer ... un texte trop long')
    
    while True:
        #attente d'un click souris, saisie d'un numéro de colonne ou fermeture de la fenètre
        print(j.waitClick())

        
