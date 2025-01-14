import numpy as np
import time

def creer_grille():
    """Renvoie une matrice 15x15 remplie de 0."""
    return np.zeros((15, 15), dtype=int)

def jouer_joueur(grille, joueur, x, y):
    """Place le pion du joueur à la position (x, y). Retourne -1 si la case est occupée, 1 sinon."""
    if grille[x][y] != 0:
        return -1
    else:
        grille[x][y] = joueur
        return 1

def verifier_gagnant(grille):
    """
    Renvoie le joueur gagnant ou l'état de la partie :
    - Retourne -1 si la partie est nulle.
    - Retourne 0 si la partie continue.
    - Retourne 1 ou 2 si un joueur gagne.
    """
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # (dx, dy)
    for ligne in range(15):
        for colonne in range(15):
            if grille[ligne, colonne] != 0:
                joueur = grille[ligne, colonne]
                for dx, dy in directions:
                    compteur = 1
                    for etape in range(1, 5):
                        nx, ny = ligne + etape * dx, colonne + etape * dy
                        if 0 <= nx < 15 and 0 <= ny < 15 and grille[nx, ny] == joueur:
                            compteur += 1
                        else:
                            break
                    if compteur == 5:
                        return joueur

    if np.any(grille == 0):  # S'il reste des cases vides, la partie continue.
        return 0
    return -1  # Match nul

def afficher_grille(grille):
    """Affiche la grille avec des coordonnées lisibles (A0, A1, ...)."""
    print("  " + " ".join(map(str, range(15))))
    for i in range(15):
        print(chr(65 + i), end=" ")  # Affiche les lettres des lignes
        for j in range(15):
            if grille[i,j]==0:
                print(".", end=" ")
            elif grille[i,j]==1:
                print("X", end=" ")
            else:
                print("O",end=" ")
        print()

def convertir_coords(coord):
    """Convertit une coordonnée 'A0' en (x, y) pour la grille."""
    try:
        ligne = ord(coord[0].upper()) - 65  # Convertir 'A'-'O' en 0-14
        colonne = int(coord[1:])
        if 0 <= ligne < 15 and 0 <= colonne < 15:
            return ligne, colonne
    except (IndexError, ValueError):
        pass
    return None


def score(grille, x, y, joueur):
    """
    Calcule le score d'un coup à la position (x, y) pour le joueur donné, selon les alignements de pions.
    """
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    score = 0
    for dx, dy in directions:
        score += evaluer_alignement(grille, x, y, dx, dy, joueur)
        score += evaluer_alignement_adversaire(grille, x, y, dx, dy, 3 - joueur)
    return score

def evaluer_alignement(grille, x, y, dx, dy, joueur):
    """
    Évalue le score pour l'alignement d'un joueur dans une direction donnée.
    """
    compteur = 0
    serie=0
    serie_finie=False
    for i in range(1,5):
        nx, ny = x + i * dx, y + i * dy
        if 0 <= nx < 15 and 0 <= ny < 15:
            if grille[nx, ny] == joueur:
                compteur += 1
                if serie_finie==False:
                    serie+=1
            elif grille[nx, ny] == 0:
                serie_finie=True
            else:
                break
    serie_finie=False
    for i in range(1,5):
        nx, ny = x - i * dx, y - i * dy
        if 0 <= nx < 15 and 0 <= ny < 15:
            if grille[nx, ny] == joueur:
                compteur += 1
                if serie_finie==False:
                    serie+=1
            elif grille[nx, ny] == 0:
                serie_finie=True
            else:
                break
    if serie>=4:
        return 10000
    elif compteur >= 4:
        return 200
    elif compteur == 3:
        return 100
    elif compteur == 2:
        return 10
    elif compteur == 1:
        return 1
    else:
        return 0

def evaluer_alignement_adversaire(grille, x, y, dx, dy, joueur_adversaire):
    """
    Évalue les alignements de l'adversaire dans une direction donnée.
    """
    compteur = 0
    serie = 0
    serie_finie = False
    for i in range(1,5):
        nx, ny = x + i * dx, y + i * dy
        if 0 <= nx < 15 and 0 <= ny < 15:
            if grille[nx, ny] == joueur_adversaire:
                compteur += 1
                if serie_finie ==False:
                    serie+=1
            elif grille[nx, ny] == 0:
                serie_finie = True
            else:
                break
    serie_finie=False
    for i in range(1,5):
        nx, ny = x - i * dx, y - i * dy
        if 0 <= nx < 15 and 0 <= ny < 15:
            if grille[nx, ny] == joueur_adversaire:
                compteur += 1
                if serie_finie == False:
                    serie+=1
            elif grille[nx, ny] == 0:
                serie_finie=True
            else:
                break        
    if serie>=4:
        return 1000
    elif serie ==3:
        return 200
    elif compteur >= 4:
        return 150
    elif compteur == 3:
        return 50
    else:
        return 0

def evaluation_grille(grille, joueur):
    """Évalue le plateau pour un joueur donné."""
    score_total = 0
    for x in range(15):
        for y in range(15):
            if grille[x, y] == joueur:
                score_total += score(grille, x, y, joueur)
            elif grille[x, y] == 3 - joueur:
                score_total -= score(grille, x, y, 3 - joueur)
    return score_total

def minimax(grille, profondeur, maximiser, joueur, alpha, beta):
    """
    Implémentation de l'algorithme Minimax avec élagage alpha-bêta.
    """
    gagnant = verifier_gagnant(grille)
    if gagnant != 0:  # Si la partie est gagnée ou nulle
        if gagnant == joueur:
            return 10000 - (5 - profondeur), None
        elif gagnant == 3 - joueur:  # Adversaire gagne
            return -10000 + (5 - profondeur), None
        return 0, None  # Match nul

    if profondeur == 0:
        return evaluation_grille(grille, joueur), None

    meilleur_coup = None
    if maximiser:
        meilleur_score = -float('inf')
        for x in range(15):
            for y in range(15):
                if grille[x, y] == 0:  # Case libre
                    grille[x, y] = joueur
                    score, _ = minimax(grille, profondeur - 1, False, joueur, alpha, beta)
                    grille[x, y] = 0
                    if score>150 :  print(f"Le coup en  {x},{y} a un score de {score}")
                    if score > meilleur_score:
                        meilleur_score = score
                        meilleur_coup = (x, y)
                    alpha = max(alpha, score)
                    if beta <= alpha:  # Coupure
                        break
        return meilleur_score, meilleur_coup
    else:
        meilleur_score = float('inf')
        for x in range(15):
            for y in range(15):
                if grille[x, y] == 0:  # Case libre
                    grille[x, y] = 3 - joueur  # Joueur adverse
                    score, _ = minimax(grille, profondeur - 1, True, joueur, alpha, beta)
                    grille[x, y] = 0
                    if score < meilleur_score:
                        meilleur_score = score
                        meilleur_coup = (x, y)
                    beta = min(beta, score)
                    if beta <= alpha:  # Coupure
                        break
        return meilleur_score, meilleur_coup

def trouver_meilleur_coup(grille, joueur):
    """Trouve le meilleur coup pour le joueur à l'aide de Minimax."""
    _, meilleur_coup = minimax(grille, 1, True, joueur, -float('inf'), float('inf'))  # Profondeur 3
    return meilleur_coup
 

def jouer():
    """Boucle principale du jeu."""
    grille = creer_grille()
    joueur_humain = int(input("Voulez-vous jouer en tant que Joueur 1 (X) ou Joueur 2 (O) ? (Entrez 1 ou 2) : "))
    joueur_ia = 3 - joueur_humain

    grille[7][7] = 1
    print("\nPremier coup au centre joué !")
    afficher_grille(grille)

    tour = 2  
    joueur_courant = 2

    while verifier_gagnant(grille) == 0:
        if joueur_courant == joueur_humain:
            print("\nC'est votre tour.")
            coord = input("Entrez les coordonnées (ex: A0, B1, etc.) : ")
            x, y = convertir_coords(coord)
            
            # Check placement restrictions based on the turn
            if tour == 1 and (x != 7 or y != 7):
                print("Premier coup doit être au centre (H7). Réessayez.")
                continue
            elif tour == 3 and 4 <= x <= 10 and 4 <= y <= 10:
                print("Vous devez jouer en dehors de la zone centrale (4 à 10) pour ce tour. Réessayez.")
                continue

            if jouer_joueur(grille, joueur_humain, x, y) == -1:
                print("Case occupée. Essayez à nouveau.")
                continue
        else:
            print("\nC'est au tour de l'IA.")
            start_time = time.time()  # Start timing the AI's turn
            coup = trouver_meilleur_coup(grille, joueur_ia)
            if coup:
                jouer_joueur(grille, joueur_ia, coup[0], coup[1])
                print(f"L'IA a joué en {chr(coup[0] + 65)}{coup[1]}.")
            end_time = time.time()  # End timing the AI's turn
            print(f"Temps pris par l'IA pour jouer : {end_time - start_time:.2f} secondes.")
        
        afficher_grille(grille)
        joueur_courant = 3 - joueur_courant
        tour += 1  # Increment the turn counter

    gagnant = verifier_gagnant(grille)
    if gagnant == -1:
        print("Match nul !")
    else:
        print(f"Le joueur {gagnant} a gagné la partie !")

# Lancer le jeu
jouer()
