import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import winsound
import random

pagedebut = tk.Tk()
pagedebut.iconbitmap('monkeyicon.ico')
pagedebut.title('Drop')
pagedebut.geometry('600x600')
pagedebut.fond = ImageTk.PhotoImage(Image.open("monkeyfond.png"))
titre = ImageTk.PhotoImage(Image.open("monkeydroptitle.png"))
dessin = tk.Canvas(pagedebut, width=900, height=900)
dessin.place(x=0, y=0)
dessin.create_image(0, 0, anchor=tk.NW, image=pagedebut.fond)
dessin.create_image(105, 40, anchor=tk.NW, image=titre)
winsound.PlaySound('forestdarkjungle.wav', winsound.SND_ASYNC)
 
def monkeydrop():
    winsound.PlaySound(None, winsound.SND_PURGE)

    fen = tk.Toplevel(pagedebut)
    fen.iconbitmap('monkeyicon.ico')
    fen.title('Monkey drop')
    fen.geometry("1100x629")

    pagedebut.withdraw()
    fond = ImageTk.PhotoImage(Image.open("darkfantback2.png"))
    perso = ImageTk.PhotoImage(Image.open("hbdarkmonkey.png"))
    objet = ImageTk.PhotoImage(Image.open("darkbanana.png"))
    fin = ImageTk.PhotoImage(Image.open('youwon.png').convert("RGBA").resize((900, 300)))
    lose = ImageTk.PhotoImage(Image.open('youlose.png').convert("RGBA").resize((400, 300)))
    
    dessin = tk.Canvas(fen, width=1100, height=628)
    dessin.place(x=0, y=0)
    dessin.create_image(0, 0, anchor=tk.NW, image=fond)

    x, y = 500, 400
    sprite = dessin.create_image(x, y, anchor=tk.NW, image=perso)
    jumping = False
    movingleft = False
    movingright = False
    banane_compteur = 0
    game_active = True
    vie_compteur = 3

    counter = Label(fen, text="0/20", font=("Bold", 20))
    counter.place(x=450, y=50 )
    counter2 = Label(fen, text="💜💜💜", font=("Bold", 20))
    counter2.place(x=550, y=50 )
    
    #mouvement
    def jump():
        nonlocal jumping
        if not jumping and game_active:
            jumping = True
            bouger_haut(15)

    def bouger_haut(velocity):
        nonlocal y, jumping
        if velocity > 0:
            dessin.move(sprite, 0, -10)
            y -= 10
            fen.after(20, bouger_haut, velocity - 1)
        else:
            bouger_enbas(15)

    def bouger_enbas(velocity):
        nonlocal y, jumping
        if velocity > 0:
            dessin.move(sprite, 0, 10)
            y += 10
            fen.after(20, bouger_enbas, velocity - 1)
        else:
            jumping = False

    def move_left():
        nonlocal movingleft
        if not movingleft and game_active:
            movingleft = True
            bouger_gauche()

    def bouger_gauche():
        nonlocal x, movingleft
        if movingleft and x > 0:  # limite
            dessin.move(sprite, -20, 0)
            x -= 20
            fen.after(20, bouger_gauche)

    def move_right():
        nonlocal movingright
        if not movingright and game_active:
            movingright = True
            bouger_droite()

    def bouger_droite():
        nonlocal x, movingright
        if movingright and x < 940:  # limite
            dessin.move(sprite, 20, 0)
            x += 20
            fen.after(20, bouger_droite)
    #touches
    def stop_bouger(event):
        nonlocal movingleft, movingright
        if event.keysym == 'q': #arrete de bouger a gauche
            movingleft = False
        elif event.keysym == 'd':
            movingright = False #arrete de bouger a droite

    def clavier(event):
        key = event.keysym
        if key == 'd':
            move_right()
        elif key == 'q':
            move_left()
        elif key == 'space':
            jump()

    #faire tomber les bananes
    def tomber_objet():
        if game_active:
            obj_x = random.randint(0, 950)
            obj = dessin.create_image(obj_x, 0, anchor=tk.NW, image=objet)
            tomb_objet(obj)

    def tomb_objet(obj):
        if game_active:
            dessin.move(obj, 0, 10)
        obj_coords = dessin.coords(obj)  # Récupère les coordonnées de la banane

        if obj_coords is None or len(obj_coords) < 2:  #éviter un plantage si la banane a été supprimé ou mal chargé.
            return  

        sprite_coords = dessin.coords(sprite) # Récupère les coordonnées du personnage

        if obj_coords and sprite_coords:  #Vérifie si les coordonnées de la banane et du personnage existent.
            obj_x, obj_y = obj_coords  # Coordonnées de la banane
            sprite_x, sprite_y = sprite_coords  # Coordonnées du personnage

            if sprite_x - 50 < obj_x < sprite_x + 50 and sprite_y - 50 < obj_y < sprite_y + 50:  #Vérifie si la banane touche le personnage
                compte_banane()
                dessin.delete(obj)
                return  

        if obj_coords[1] < 692:  #Vérifie si la banane est encore à l’écran
            fen.after(50, tomb_objet, obj)  # Continue la chute après 50 ms
        else:
            dessin.delete(obj)  
            nonlocal vie_compteur
            vie_compteur -= 1
            counter2.config(text=f"💜💜💜")
            if vie_compteur == 2:
                counter2.config(text="💜💜")
            if vie_compteur == 1:
                counter2.config(text="💜")
            if vie_compteur == 0:
                counter2.config(text="")
                game_over()
                winsound.PlaySound('8bit-lose.wav', winsound.SND_ASYNC)

    def compte_banane(): #compteur
        nonlocal banane_compteur  
        if banane_compteur <20:
            banane_compteur += 1
            counter.config(text=f"{banane_compteur}/20")
            winsound.PlaySound('coin.wav', winsound.SND_ASYNC)
        if banane_compteur == 20:
            dessin.create_image(140, 110, anchor=tk.NW, image=fin)
            winsound.PlaySound('bswin.wav', winsound.SND_ASYNC)
            stop_game()  

    def game_over():#image (perdu)
        dessin.create_image(375, 110, anchor=tk.NW, image=lose)
        winsound.PlaySound(None, winsound.SND_PURGE)
        stop_game()

    def stop_game():#arreter le jeu
        nonlocal game_active
        game_active = False
        fen.unbind("<KeyPress>")
        fen.unbind("<KeyRelease>")
        replay_button = tk.Button(fen, text='Replay', command=lambda: [fen.destroy(), monkeydrop()], font=("Bold", 14))
        replay_button.place(x=525, y=500)

    def start_jeu():
        if game_active:
            tomber_objet()
            fen.after(1000, start_jeu) #attendre 1 seconde avant de faire tomber une autre banane 
    

    fen.bind("<KeyPress>", clavier)
    fen.bind("<KeyRelease>", stop_bouger)
    fen.focus_set() # Définit le focus sur la fenêtre 'fen' pour que la fenêtre puisse recevoir les touches clavier

    fen.protocol("WM_DELETE_WINDOW", lambda: [pagedebut.deiconify(), fen.destroy(), winsound.PlaySound('forestdarkjungle.wav', winsound.SND_ASYNC)])

    start_jeu()

    #empêcher les images d'être supprimées par Python
    fen.fond = fond
    fen.perso = perso
    fen.objet = objet
    
start_button_image = Image.open("startbutton.png").convert("RGBA").resize((140, 60))
pagedebut.bouton = ImageTk.PhotoImage(start_button_image)

jouer = tk.Button(pagedebut, text='jouer', command=monkeydrop, image=pagedebut.bouton, borderwidth=0)
jouer.pack()
jouer.place(x=240, y=400)

pagedebut.mainloop()
