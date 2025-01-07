import numpy as np


def creer_grille():
    """
    Renvoie une matrice 15x15 remplie de 0
    """
    return np.zeros((15, 15), dtype=int)


def jouer_joueur(grille, joueur, x, y):
    if grille[y][x] != 0:
        print("Case pleine, impossible de jouer")
        return -1
    else:
        grille[y][x] = joueur
        return 1


def verifier_gagnant(grille):
    """
    Renvoie le joueur si un des joueurs a gagné, si la partie est finie et 
    que personne a gagné cela renvoie -1 et si on peut encore jouer, cela renvoie 0
    """
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # (dx, dy)
    for ligne in range(15):
        for colonne in range(15):
            if not grille[ligne, colonne] == 0:
                joueur = grille[ligne, colonne]
                #vérifier pour chaque direction
                for dx, dy in directions:
                    compteur = 1
                    for etape in range(1, 5):
                        nx, ny = ligne + etape * dx, colonne + etape * dy
                        if 0 <= nx < 15 and 0 <= ny < 15 and grille[nx, ny] == joueur:
                            compteur += 1
                        else:
                            break
                    if compteur == 5:  #si 5 alignés, on retourne le joueur gagnant
                        return joueur

    #si aucune victoire, vérifier si la grille est encore jouable
    if np.any(grille == 0):  #si une case est vide, on peut encore jouer
        return 0

    #sinon, personne n'a gagné et la grille est pleine
    return -1

def jouer():
    grille = creer_grille()
    grille[7][7]=1
    tour1 = True 
    while (verifier_gagnant(grille))==0:
        print("C'est au joueur 2 de jouer")
        print(grille)
        x = int(input("Ecrire x"))
        y = int(input("Ecrire y"))
        while (jouer_joueur(grille,2,x,y)==-1):
            x = int(input("Réecrire x"))
            y = int(input("Réecrire y"))
        if (verifier_gagnant(grille)!=0): break 
        print("C'est au joueur 1 de jouer")
        print(grille)
        x = int(input("Ecrire x"))
        y = int(input("Ecrire y"))
        if tour1 == False:
            while (jouer_joueur(grille,1,x,y)==-1):
                x = int(input("Réecrire x"))
                y = int(input("Réecrire y"))
        else:
            while(4<=x<=10 and 4<=y<=10):
                x = int(input("Réecrire x"))
                y = int(input("Réecrire y"))
            jouer_joueur(grille,1, x, y)
            tour1=False
        
    if (verifier_gagnant(grille)==-1):
        print("Aucun gagnant !")
    else:
        print(f"Le joueur {verifier_gagnant(grille)} a gagné la partie !")
        

def score(grille, x, y, joueur):
    """
    Calcule le score d'un coup à la position (x, y) pour le joueur donné, selon les alignements de pions.
    """
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  #(dx, dy) pour 4 directions: horizontale, verticale, diagonale, inverse
    score = 0

    for dx, dy in directions:
        score += evaluer_alignement(grille, x, y, dx, dy, joueur)  #score pour les alignements de notre côté
        score -= evaluer_alignement_adversaire(grille, x, y, dx, dy, 3 - joueur)  #soustraire les alignements de l'adversaire

    return abs(score)


def evaluer_alignement(grille, x, y, dx, dy, joueur):
    """
    Évalue le score pour l'alignement d'un joueur (joueur 1 ou joueur 2) dans une direction donnée.
    """
    compteur = 0

    for i in range(-4, 5):  #vérifier jusqu'à 4 cases dans chaque direction
        nx, ny = x + i * dx, y + i * dy
        if 0 <= nx < 15 and 0 <= ny < 15:
            if grille[nx, ny] == joueur:
                compteur += 1
            elif grille[nx, ny] == 0:
                continue  #case vide
            else:
                break  #case de l'adversaire, on arrête l'alignement

    if compteur == 4:
        return 10000  #4 pions alignés
    elif compteur == 3:
        return 100  #3 pions alignés
    elif compteur == 2:
        return 10  #2 pions alignés
    elif compteur == 1:
        return 1  #1 pion aligné
    elif compteur == 0:
       return 0  #pas d'alignement


def evaluer_alignement_adversaire(grille, x, y, dx, dy, joueur_adversaire):
    """
    Évalue les alignements de l'adversaire (joueur 1 ou joueur 2) dans une direction donnée.
    """
    compteur = 0
    for i in range(-4, 5):  #vérifier jusqu'à 4 cases dans chaque direction
        nx, ny = x + i * dx, y + i * dy
        if 0 <= nx < 15 and 0 <= ny < 15: 
            if grille[nx, ny] == joueur_adversaire:
                compteur += 1
            elif grille[nx, ny] == 0:
                continue  #case vide
            else:
                break  #case de notre joueur, on arrête l'alignement

    if compteur == 4:
        return 1000  #4 pions alignés de l'adversaire (on veut les bloquer)
    elif compteur == 3:
        return 50  #3 pions alignés de l'adversaire (on veut les bloquer)
    else:
        return 0  #sinon pas de pénalité
    
    
def trouver_meilleur_coup(grille, joueur):
    """
    Trouve la case avec le meilleur score pour l'IA en évaluant toutes les cases vides.
    """
    meilleur_score = -float('inf')
    meilleur_coup = None

    for x in range(15):
        for y in range(15):
            if grille[x, y] == 0:  #si la case est vide, on l'évalue
                s = score(grille, x, y, joueur)
                if s > meilleur_score:
                    meilleur_score = s
                    meilleur_coup = (x, y)

    return meilleur_coup
    
    
    
    
    
    
