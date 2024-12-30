# ------------------------------ PARAMETRAGE DU JEU ------------------------------

import pygame, sys
from pygame.locals import *
import random, time

pygame.init()
 
FPS = 60
FramePerSec = pygame.time.Clock()
 
# COULEURS PREDEFINIES
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# COULEURS PREDEFINIES 2
IVORY = (229, 228, 226)

# INFOS ECRAN
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500
 
DISPLAYSURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # SURFACE DE JEU
DISPLAYSURFACE.fill(WHITE)
pygame.display.set_caption("Spill the Tea")

# MISE EN PLACE DU TEXTE
police_titre = pygame.font.Font("Tangerine-Regular.ttf", 40) # CREER UNE POLICE
police_principale = pygame.font.Font("Tangerine-Regular.ttf", 32) # CREER UNE POLICE

# ------------------------------ CLASSES ------------------------------

class Tasse(pygame.sprite.Sprite):
    """
    Crée une tasse de thé
    """
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("assets/tasse_.png")
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT - SCREEN_HEIGHT//6)


        self.nb_vies = 3

        self.delta_x = 5
        self.score = 0

    def afficher(self, surface):
        """
        Affiche l'élément sur la surface donnée en paramètre
        pre: surface (SURFACE)
        post:
        """
        surface.blit(self.image, self.rect) 

    def deplacer(self):
        """
        Modifier la position de la tasse de x sur l'axe des abscisses
        pre:
        post:        
        """
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-1*self.delta_x, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(self.delta_x, 0)

    def augmenter_score(self, score=100):
        """
        Augmente le score avec le nombre donné
        pre: score (int)
        """
        self.score += score
        
    def est_en_etat(self):
        """
        Renvoie si la tasse est en état de continuer d'attraper des potins ou pas.
        """
        return self.nb_vies > 0

class Potin(pygame.sprite.Sprite):
    """
    Crée un potin
    """
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("assets/potin_.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(20, SCREEN_WIDTH-20), 15)

        self.vitesse = 1
        self.delta_x = 0
        self.delta_y = 2

    def afficher(self, surface):
        """
        Affiche l'élément sur la surface donnée en paramètre
        """
        surface.blit(self.image, self.rect)

    def augmenter_vitesse(self, n):
        """
        Augmente de n la vitesse d'un potin
        pre: n (int)
        post:
        """
        self.vitesse = n

    def diriger_x(self, x):
        """
        Modifie la direction d'un potin sur l'axe horizontal
        pre: x (int)
        post:
        """
        self.delta_x = x

    def diriger_y(self, y):
        """
        Modifie la direction d'un potin sur l'axe vertical
        pre: y (int)
        post:
        """
        self.delta_y = y

    def deplacer(self):
        """
        Met à jour la postion de l'objet sur l'écran
        pre:
        post:
        """
        if self.rect.bottom < SCREEN_HEIGHT: # SI LE LUTIN EST DANS L'ECRAN 
            self.rect.move_ip(self.delta_x*self.vitesse, self.delta_y*self.vitesse)
        else: self.kill() # SI LE LUTIN SORT DE L'ECRAN 

class The(pygame.sprite.Sprite):
    """
    Crée du thé
    """
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("assets/the_.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(20, SCREEN_WIDTH-20), 15)

        self.vitesse = 1
        self.delta_x = 0
        self.delta_y = 2

    def afficher(self, surface): 
        """
        Affiche l'élément sur la surface donnée en paramètre
        """
        surface.blit(self.image, self.rect)

    def augmenter_vitesse(self, n):
        """
        Augmente de n la vitesse d'un potin
        pre: n (int)
        post:
        """
        self.vitesse = n

    def deplacer(self):
        """
        Met à jour la postion de l'objet sur l'écran
        pre:
        post:
        """
        if self.rect.bottom < SCREEN_HEIGHT: # SI LE LUTIN EST DANS L'ECRAN 
            self.rect.move_ip(self.delta_x*self.vitesse, self.delta_y*self.vitesse)
        else: self.kill() # SI LE LUTIN SORT DE L'ECRAN 

class Potins_trouvés:
    def __init__(self, potin):
        self.potin = potin
    
    def ouvrir_potin(self):
        self.potin.ouvert = True

    def afficher_potin(self, surface, coordonnees):
        txt = police_principale.render(self.potin.text, True, BLACK)
        txt.blit(surface, coordonnees)
    
class Collection_potin:
    def __init__(self):
        self.collection = {}
        for i in range(1, 12): # 11 POTINS DONT 1 SECRET -----------------------------------------------------------
            self.collection[f"{i}"] = None
    
    def ajouter_potin(self, numero, potin):
        self.collection[f"{numero}"] = potin
    
    def acces_potin(self, numero):
        return self.collection[f"{numero}"]

class Bouton(pygame.sprite.Sprite):
    def __init__(self, agrandissement, pos, img, num=None):
        super().__init__()
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*agrandissement, self.image.get_height()*agrandissement))
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.numero = num
    
    def collision_avec_curseur(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def afficher(self, surface):
        """
        Affiche l'élément sur la surface donnée en paramètre
        """
        surface.blit(self.image, self.rect)

# ------------------------------ FONCTION COLLISION ------------------------------

def gerer_collision_TASSE_POTINS():
    """
    Gère la collision entre l'objet et le lutin entré en paramètre
    pre: lutin (sprite), groupe
    post:
    Règles:
        SELON LE NOMBBRE DE VIES AFFICHER UNE COULEUR
        POUR CHAQUE LUTIN TOUCHE ON TUE LE LUTIN, 
        ON FISSURE LA TASSE ET ON CONSERVE LE SCORE.
        ON REPREND LA PARTIE
    """
    colidedSprite = pygame.sprite.spritecollideany(TASSE, POTINS)
    if colidedSprite != None:
        colidedSprite.kill()
        TASSE.augmenter_score()
        pygame.display.update()
    return None

def gerer_collision_TASSE_THE():
    """
    Gère la collision entre l'objet et le lutin entré en paramètre
    pre: lutin (sprite), groupe
    post:
    Règles:
        SELON LE NOMBBRE DE VIES AFFICHER UNE COULEUR
        POUR CHAQUE LUTIN TOUCHE ON TUE LE LUTIN, 
        ON FISSURE LA TASSE ET ON CONSERVE LE SCORE.
        ON REPREND LA PARTIE
    """
    colidedSprite = pygame.sprite.spritecollideany(TASSE, THE)

    if colidedSprite != None:
        colidedSprite.kill()

        pygame.display.update()
        TASSE.nb_vies -= 1 # OK

        # A VOIR SI ON REND INVULNERABLE UN MOMENT
    return None

def gerer_collision_THE_POTIN():
    """
    Gère la collision entre l'objet et le lutin entré en paramètre
    pre: lutin (sprite), groupe
    post:
    """
    for sprite_T in THE: # SI LE THE RENTRE EN COLLISION AVEC UN POTIN
        collided = pygame.sprite.spritecollideany(sprite_T, POTINS)
        if collided != None:
            collided.kill() # TUER LE POTIN
    return None


# ------------------------------ GROUPES ------------------------------

def deplacer_groupe(groupe):
    """
    Permet de mettre à jour la position d'un groupe
    """
    for sprite in groupe:
        sprite.deplacer()

# ------------------------------ TEXTES ------------------------------

def afficher_score(score, surface):
    """
    Affiche le score
    """
    score_aff = police_titre.render(f"Score : {score}", True, BLACK)
    surface.blit(score_aff, (20, SCREEN_HEIGHT-60))

def afficher_vies(vies, surface):
    """
    Affiche les vie du joueur
    """
    score_aff = police_titre.render(f"x{vies} lives", True, BLACK)
    surface.blit(score_aff, (SCREEN_WIDTH - 90, SCREEN_HEIGHT-60))

def afficher_potin_collection(num, collection_complete):
    num = str(num)
    potin = collection_complete.collection[num]
    lignes = []
    if potin:
        for i in range(len(potin)-1, 0, -1):
            if potin[i] == "-" or i == 1:
                lignes.append(potin[i+1:])
                potin = potin[:i]
        lignes.reverse()
        lignes.append("Press ESC to return to your collection")
        return lignes
    else: 
        return ["   You haven't unclocked this gossip yet !", "Press ESC to return to your collection"]
        

# ------------------------------ SPAWN ------------------------------

def spawn(index_spawn):
    """
    Crée les prochains lutins à apparaître
    """
    
    global heure_precedente_potins
    global heure_precedente_the
    global heure_actuelle_potins
    global heure_actuelle_the
    delais_spawn = { 
        "POTINS": [(950, 1050), (875, 950), (700, 850), (500, 501), (200, 201),(50,51)], 
        "THE": [(1100, 1200), (1000, 1100), (800, 900), (700, 701), (200, 201),(50, 51)]
    }
    nouvelle_vitesse = 1
    if index_spawn == 1:
        nouvelle_vitesse = 1.5
    elif index_spawn >= 2:
        nouvelle_vitesse = 2
    elif index_spawn >= 4:
        nouvelle_vitesse = 3
    

    if heure_actuelle_the - heure_precedente_the >= random.randint(delais_spawn["THE"][index_spawn][0], delais_spawn["THE"][index_spawn][1]):
            nouv_the = The()
            nouv_the.augmenter_vitesse(nouvelle_vitesse)
            all_sprites.add(nouv_the)
            THE.add(nouv_the)
            heure_precedente_the = heure_actuelle_the
        
    if heure_actuelle_potins - heure_precedente_potins >= random.randint(delais_spawn["POTINS"][index_spawn][0], delais_spawn["POTINS"][index_spawn][1]):
        nouv_potin = Potin()
        nouv_potin.augmenter_vitesse(nouvelle_vitesse)
        all_sprites.add(nouv_potin)
        POTINS.add(nouv_potin)
        heure_precedente_potins = heure_actuelle_potins

# ------------------------------  JEU ------------------------------

POTINS = pygame.sprite.Group()
THE = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
BOUTON_COLLECTION = Bouton(1.5, (520, 450), "assets/potin_.png")

# INITIALISATION DES VARIABLES POUR GERER LE TEMPS

heure_globale = pygame.time.get_ticks()
heure_precedente_potins =  pygame.time.get_ticks()
heure_precedente_the = pygame.time.get_ticks()
accueil = True
jeu = False
collection = False

# COLLECTION DES POTINS
COMPLETED_COLLECTION = Collection_potin()
list_potins = [
    "  Steffy P from biology is pregnant", # --------------- 1  ---------------
    "  I went to this bookshop/café and had a cookie -\
some days ago. And when it was time to go, -\
I ate my last piece of cookie and went to the bar to pay. -\
So I paid, and the girl asked me \"Is it good ?\" -\
and I said \"Yeah I'm done paying, it's good, can I go ?\". -\
Actualy she was asking if the cookie was good, and -\
I understood that when she kept staring at me like -\
\"Gurl what the duck are you talking about\". Ankward. -\
So I said \"Oh yeah the cookie was good !\". The cookie wasn't good -\
it was delicious, like I could eat a thousand like it. -\
But I couldn't say that because I ran away from -\
this ankward situation.", # --------------- 2 ---------------
    "  I almost drown aproximately 6 to 8 times in my life but -\
it's okay. Let's just say I had a lot of opportunities to taste -\
the sea. And the pool. And a river twice. Also a bath tub but -\
it doesn't count. And the fact that my parents were watching -\
me everytime didn't stopped me from tasting the water. -\
It was still fun ! I loved going to swim !-\
", # --------------- 3 ---------------
    "  Hello Kitty is not a cat. She is human. -\
I don't know if you have already seen humans with cat ears -\
but I did not. So ??? What the hell is going on ?", # --------------- 4 ---------------
    "  Koalas sleep aproximately 22 hours a day. -\
And I know people who should take exemple on them -\
because they are like in debt of sleep. Like they -\
are using energy they don't have and they are sleep deprived. -\
Go to sleep please.", # --------------- 5 ---------------
    "  Coffe is the second most loved beverage in the world -\
the first one being water. -\
I prefer tea, like very hot tea. So I can take my time to -\
spill it. ", # --------------- 6 ---------------
    "  Honey is sweeter than sugar. I love honey -\
beecause it makes the buzz all the time.", # --------------- 7 ---------------
    "  Arthur Rimbaud, a french poet, wrote a poem called-\
\"Le sonnet du trou du cul\", which mean \"The balad of -\
the butthole\".  Very demure, very mindful, very cutesy.", # --------------- 8 ---------------
    "  Actually NASA stands for \"National Aeronautics and Space-\
Administration\", and not \"Never A Straight Answer\"-\
or \"No Actual Space Achievement\". How strange...", # --------------- 9 ---------------
    "  If you unlock all the gossips, you may find a secret one...", # --------------- 10 ---------------
    "  You discovered the secret gossip ! - \
This game was made with love and tea by M_ ! -\
I hope you had fun !", # --------------- 11 ---------------

]
for i in range(len(list_potins)):
    COMPLETED_COLLECTION.ajouter_potin(i+1, list_potins[i])

COLLECTION_PLAYER = Collection_potin() # ON L'UTILISERA PLUS TARD

# ANIMATIONS D'ACCUEIL

# ANIMATION TUTO BAG ET GOSSIP
animations_suivantes_bag = {
    "assets/bag/Bag_1.png": "assets/bag/Bag_2.png",
    "assets/bag/Bag_2.png": "assets/bag/Bag_3.png",
    "assets/bag/Bag_3.png": "assets/bag/Bag_4.png",
    "assets/bag/Bag_4.png": "assets/bag/Bag_5.png",
    "assets/bag/Bag_5.png": "assets/bag/Bag_1.png"
}

animations_suivantes_goss = {
    "assets/goss/Goss_1.png": "assets/goss/Goss_2.png",
    "assets/goss/Goss_2.png": "assets/goss/Goss_3.png",
    "assets/goss/Goss_3.png": "assets/goss/Goss_4.png",
    "assets/goss/Goss_4.png": "assets/goss/Goss_5.png",
    "assets/goss/Goss_5.png": "assets/goss/Goss_1.png"
}
class Image:
    def __init__(self, img, dict_):
        self.img_path = img
        self.dict_img_suivante = dict_
        self.horloge_animations = pygame.time.get_ticks()
    
    def changer_animation(self, x):
        """
        """
        heure_actuelle = pygame.time.get_ticks()
        if heure_actuelle - self.horloge_animations > 500:
            self.img_path = self.dict_img_suivante[self.img_path]
            self.horloge_animations = heure_actuelle
        DISPLAYSURFACE.blit(pygame.image.load(self.img_path), (x, SCREEN_HEIGHT // 3 * 2))

IMG_GOSS = Image("assets/goss/Goss_5.png", animations_suivantes_goss)
IMG_TEA = Image("assets/bag/Bag_5.png", animations_suivantes_bag)

# ANIMATION SACHETS ET PAPIERS QUI TOMBENT SUR LES COTE EN CASCADE
horloge_animations_the = pygame.time.get_ticks()
horloge_animations_potins = pygame.time.get_ticks()

last_ = "GOSS"

def cascade():
    """
    Crée les prochains lutins à apparaître
    """
    global horloge_animations_potins
    global last_
    
    heure_potin = pygame.time.get_ticks()

    nouvelle_vitesse = 2
    if heure_potin - horloge_animations_potins >= 500/nouvelle_vitesse:
        if last_ == "TEA":
            for x in [SCREEN_WIDTH - 20, 20]:
                nouv_potin = Potin()
                nouv_potin.augmenter_vitesse(nouvelle_vitesse)
                nouv_potin.rect.center = (x, 15)
                all_sprites.add(nouv_potin)
                POTINS.add(nouv_potin)
                last_ = "GOSS"
        else: 
            for x in [SCREEN_WIDTH - 20, 20]:
                nouv_the = The()
                nouv_the.augmenter_vitesse(nouvelle_vitesse)
                nouv_the.rect.center = (x, 15)
                all_sprites.add(nouv_the)
                THE.add(nouv_the)
                last_ = "TEA"
        horloge_animations_potins = heure_potin
    return None

# BOUCLE DU JEU
while True:

    # --------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------- ACCUEIL ------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------------
    while accueil:
        # SI APPUI SUR LA CROIX OU ESC
        for event in pygame.event.get():              
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if BOUTON_COLLECTION.collision_avec_curseur():
                    accueil = False
                    collection = True
                    jeu = False
        if pygame.key.get_pressed()[K_ESCAPE]:
            pygame.quit()
            sys.exit()

        # JOUER
        if pygame.key.get_pressed()[K_SPACE]:
            accueil = False
            collection = False
            jeu = True
        # REAFFICHER L'ECRAN
        DISPLAYSURFACE.fill(WHITE)

        # ANIMATION DE TUTO
        IMG_GOSS.changer_animation(SCREEN_WIDTH//2 - 130)
        IMG_TEA.changer_animation(SCREEN_WIDTH//2 + 20)

        # ANIMATION CASCADE
        cascade()
        
        # AFFICHER CES SPRITES
        for sprite in all_sprites:
            sprite.afficher(DISPLAYSURFACE)

        BOUTON_COLLECTION.afficher(DISPLAYSURFACE)
        txt = police_principale.render("Access to you collection:", False, BLACK)
        DISPLAYSURFACE.blit(txt, (300, 435))
        
        deplacer_groupe(POTINS)
        deplacer_groupe(THE)

        # TEXTES
        stt = police_titre.render("Play \"  Spill the Tea  \"", True, BLACK)
        DISPLAYSURFACE.blit(stt, (SCREEN_WIDTH//2 - 120, 100))

        stt = police_principale.render("Avoid tea bags and catch the gossip written on scraps of paper !", True, BLACK)
        DISPLAYSURFACE.blit(stt, (SCREEN_WIDTH//2 - 230, 200))

        inst = police_principale.render("Press SPACE to start playing !", True, BLACK)
        DISPLAYSURFACE.blit(inst, (SCREEN_WIDTH//2 - 130, 250))

        # REAFFICHER L'ECRAN
        pygame.display.update()
        FramePerSec.tick(FPS)

    # TOUT REINITIALISER

    for sprite in THE:
        sprite.kill()
    for sprite in all_sprites:
        sprite.kill()
    for sprite in POTINS:
        sprite.kill()

    # METTRE EN PLACE LA COLLECTION

    BOUTONS = pygame.sprite.Group()
    BOUTON_POS = [
        (104, 75),
        (341, 221),
        (473, 81),
        (110, 300),
        (291, 419),
        (499, 329),
        (285, 107),
        (137, 179),
        (280, 344),
        (488, 443),
        (60, 443)
    ]
    BOUTON_AGG = [1, 2, 3]
    for num, potin in COLLECTION_PLAYER.collection.items(): # REMPLACER
            num = int(num)
            pos = BOUTON_POS[num-1]
            img = ""

            if potin: img = "assets/potin_.png"
            else: img = "assets/potin_locked.png"
            
            p = Bouton(BOUTON_AGG[num%3], pos, img, num)
            BOUTONS.add(p)
    POTIN_A_AFFICHER = None

    # --------------------------------------------------------------------------------------------------------------
    # --------------------------------------------- COLLECTION -----------------------------------------------------
    # --------------------------------------------------------------------------------------------------------------
    while collection:
        ESC = False
        for event in pygame.event.get():              
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                for b in BOUTONS:
                    if b.collision_avec_curseur():
                       POTIN_A_AFFICHER = afficher_potin_collection(b.numero, COLLECTION_PLAYER)
        if pygame.key.get_pressed()[K_ESCAPE]:
            if POTIN_A_AFFICHER:
                POTIN_A_AFFICHER = None
            else:
                jeu = False
                accueil = True
                collection = False
            ESC = True
        
        # AFFICHER
        DISPLAYSURFACE.fill(WHITE)
        if POTIN_A_AFFICHER:
            x = 100
            y = 80
            for l in POTIN_A_AFFICHER:
                txt = police_principale.render(l, False, BLACK)
                DISPLAYSURFACE.blit(txt, (x, y))
                y += 30
        else:
            for b in BOUTONS:
                b.afficher(DISPLAYSURFACE)
            t = police_principale.render("Press ESC to return to the main screen.", False, BLACK)
            DISPLAYSURFACE.blit(t, (160, 25))

        pygame.display.update()
        FramePerSec.tick(FPS)

        if ESC:
            time.sleep(0.4) # EVITER QU'APPUYER UNE FOIS NE PROVOQUE PLUSIEURS ACTIONS

    for sprite in THE:
        sprite.kill()
    for sprite in all_sprites:
        sprite.kill()
    for sprite in POTINS:
        sprite.kill()

    TASSE = Tasse()

    POTINS = pygame.sprite.Group()
    THE = pygame.sprite.Group()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(TASSE)

    heure_globale = pygame.time.get_ticks()
    heure_precedente_potins =  pygame.time.get_ticks()
    heure_precedente_the = pygame.time.get_ticks()

    high_score = 0
    new_gossip_unlocked = False

    # --------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------- JEU ------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------------
    while jeu:
        # SI APPUI SUR LA CROIX OU ESC
        for event in pygame.event.get():              
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        # REVENIR A L'ACCEUIL
        if pygame.key.get_pressed()[K_RETURN]:
            jeu = False
            accueil = True
            collection = False

        # TOUJOURS PERMETTRE LE DEPLACEMENT DE LA TASSE DU JOUEUR
        if TASSE.est_en_etat():
            TASSE.deplacer()
        deplacer_groupe(POTINS)
        deplacer_groupe(THE)

        if TASSE.est_en_etat():
            # TOUJOURS VERIFIER S'IL Y A DES COLISIONS
            gerer_collision_TASSE_POTINS()
            gerer_collision_TASSE_THE()
            if TASSE.est_en_etat():
                gerer_collision_THE_POTIN()

        # APPARITION D'UN LUTIN TOUTES LES "delais_spawn" MILLISECONDES POUR CHAQUE OBJET RESPECTIF    

        heure_actuelle_potins = pygame.time.get_ticks()
        heure_actuelle_the = pygame.time.get_ticks()
        heure_globale_actuelle = pygame.time.get_ticks()

        if TASSE.est_en_etat():
            if heure_globale_actuelle - heure_globale < 5000: # PENDANT LES 6 PREMIERES SECONDES DE JEU
                spawn(0) # FONCTION QUI GERE LES APPARITIONS
            elif heure_globale_actuelle - heure_globale < 12000: # PENDANT LES 12 PREMIERES SECONDES DE JEU
                spawn(1)
            elif heure_globale_actuelle - heure_globale < 21000: # PENDANT LES 21 PREMIERES SECONDES DE JEU
                spawn(2)
            elif heure_globale_actuelle - heure_globale < 26000: # PENDANT LES 26 PREMIERES SECONDES DE JEU
                spawn(3)
            else: # LE RESTE DU TEMPS
                spawn(4) 
        else: # ANIMATION DU GAME OVER
            spawn(5)
        
        # GESTION DU MEILLEUR SCORE
        if TASSE.score > high_score:
            high_score = TASSE.score
        # --------------- ZONE DE GESTION DE L'ECRAN ---------------
        
        # REAFFICHER L'ECRAN
        DISPLAYSURFACE.fill(WHITE)

        # GESTION DU GAME OVER
        if not TASSE.est_en_etat():
            # LE GAME OVER
            TASSE.kill()
            game_over_texte_1 = police_titre.render("  - Game Over -", True, BLACK, WHITE)
            DISPLAYSURFACE.blit(game_over_texte_1, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
            game_over_texte_1 = police_principale.render(f"Your score was {TASSE.score}, well done !", True, BLACK)
            DISPLAYSURFACE.blit(game_over_texte_1, (SCREEN_WIDTH * round((1 - 0.40) / 2, 3), SCREEN_HEIGHT//2 + 30)) # 1 - TAILLE TEXTE / 2
            restart_texte = police_principale.render("Press SPACE to play again", True, BLACK)
            DISPLAYSURFACE.blit(restart_texte, (SCREEN_WIDTH * round((1 - 0.45) /2, 3), SCREEN_HEIGHT//2 + 60))
            restart_texte = police_principale.render("Press Return to return to the welcome screen", True, BLACK)
            DISPLAYSURFACE.blit(restart_texte, (SCREEN_WIDTH * round((1 - 0.60) /2, 3), SCREEN_HEIGHT//2 + 90))
            
            if TASSE.score > 100:
                txt = police_principale.render("Go see your collection, new gossip unlocked !", True, BLACK)
                DISPLAYSURFACE.blit(txt, (SCREEN_WIDTH * round((1 - 0.52) /2, 3), SCREEN_HEIGHT//2 + 120))
                if not new_gossip_unlocked:
                    for i in range(TASSE.score // 100):
                        r = random.randint(1, 10)
                        COLLECTION_PLAYER.ajouter_potin(r, COMPLETED_COLLECTION.acces_potin(r))                    
                    completed = True
                    for c, p in COLLECTION_PLAYER.collection.items():
                        if not p and c != "11":
                                completed = False
                    if completed:
                        COLLECTION_PLAYER.ajouter_potin(11, COMPLETED_COLLECTION.acces_potin(11))
                    new_gossip_unlocked = True


            # RELANCER UNE PARTIE
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_SPACE]:
                TASSE = Tasse()
                POTINS = pygame.sprite.Group()
                THE = pygame.sprite.Group()

                all_sprites = pygame.sprite.Group()
                all_sprites.add(TASSE)
                heure_globale = pygame.time.get_ticks()
                new_gossip_unlocked = False

        
        # AFFICHER CHAQUE ELEMENT:
        # SPRITES
        for sprite in all_sprites:
            sprite.afficher(DISPLAYSURFACE)
        
        # SCORE
        afficher_score(TASSE.score, DISPLAYSURFACE)

        # VIES
        afficher_vies(TASSE.nb_vies, DISPLAYSURFACE)

        # MEILLEUR SCORE
        high_score_aff = police_titre.render(f"High Score: {high_score}", True, BLACK)
        DISPLAYSURFACE.blit(high_score_aff, (20, 20))
        
        # REAFFICHER L'ECRAN
        pygame.display.update()
        FramePerSec.tick(FPS)

    for sprite in THE:
        sprite.kill()
    for sprite in all_sprites:
        sprite.kill()
    for sprite in POTINS:
        sprite.kill()