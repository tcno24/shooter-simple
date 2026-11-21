from pygame import * 
from random import randint

font.init()
font = font.Font(None, 36)

img_lose = 'defeat.jpg'
img_win = 'victory.jpg'
backround = 'umbara.png'

blaster = 'blaster bolt.png'
trooper = 'cody.png'
clanker = 'droideka.png'

score = 0 #blancos destruidos
goal = 50 #blancos necesarios
lost = 0 #blancos perdidos creo
max_lost = 3 #maximos disparos fallidos

#Clases.................................................................................................................................................

#clase padre
class gamesprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_size_x, player_size_y):
        super().__init__()
        #imagen y velocidad
        self.image = transform.scale(image.load(player_image), (player_size_x, player_size_y))
        self.speed = player_speed
        #Rectangulo de colision
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    #Copiar y pegar la imagen en Newposition
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#Clase jugador
class player(gamesprite):
    #Movimiento
    
    def update_wasd(self):
        keys = key.get_pressed() #Detecta las teclas presionada
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 75:
            self.rect.x += self.speed
        if keys[K_s] and self.rect.y < win_hight - 100:
            self.rect.y += self.speed
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
    def update_ad(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 75:
            self.rect.x += self.speed
    def update_arrows(self):
        keys = key.get_pressed() #Detecta las teclas presionada
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 75:
            self.rect.x += self.speed
        if keys[K_DOWN] and self.rect.y < win_hight - 100:
            self.rect.y += self.speed
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
    def update_arrows_lr(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 75:
            self.rect.x += self.speed

    #disparar
    def fire(self):
        bullet = Bullet(blaster, self.rect.centerx, self.rect.top, -15, 20, 15)
        bolts.add(bullet)

class enemy(gamesprite):
    health = 2  
    #movimiento                           
    def update(self):
      self.rect.y += self.speed
      global lost
      # desaparece si alcanza el borde de la pantalla
      if self.rect.y > win_hight:
          self.rect.x = randint(80, win_width - 80)
          self.rect.y = 0
          lost = lost + 1

    def takedamage(self):
        global score
        self.health -= 1 
        if self.health <= 0:
            self.kill()
            score +=1

# clase del objeto de la bala   
class Bullet(gamesprite):
  # movimiento del enemigo
  def update(self):
      self.rect.y += self.speed
      # desaparece si alcanza el borde de la pantalla
      if self.rect.y < 0:
          self.kill()

#Ventana
win_hight = 800
win_width = 700
window = display.set_mode((win_width, win_hight))
display.set_caption("game window")
backround = image.load(backround)
backround = transform.scale(backround, (win_width, win_hight))

#player y objetos
player1 = player(trooper, win_width/2, win_hight-150, 5, 60, 100)

#Probablemente lo que no hemos visto 
clankas = sprite.Group()
for i in range(1, 6):
    monster = enemy(clanker, randint(80, win_width - 80), -40, randint(1, 2), 90, 70)
    clankas.add(monster)

bolts = sprite.Group()

#Parametros
finish = False

#Ciclo principal................................................................................................................................................................
corre = True
while corre:
    time.delay(20)  #FPS, pausa de 0.05
    for e in event.get(): #Encontrar el evento
        if e.type == QUIT: #Si el evento es QUIT
            corre = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                 player1.fire()
            if e.key == K_RETURN and finish == True:
                finish = False
                score = 0
                clankas.empty()
                player1.rect.x = win_width/2
                for i in range(1, 6):
                    monster = enemy(clanker, randint(80, win_width - 80), -40, randint(1, 2), 90, 70)
                    clankas.add(monster)

    if not finish:
        window.fill((255,255,255))
        window.blit(backround, (0, 0))

        #texto
        text = font.render("Puntaje:" + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font.render("Falló: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))    
        
        #updates, resets, etc...
        player1.update_arrows_lr()
        bolts.update()
        clankas.update()
        
        player1.reset()
        clankas.draw(window)
        bolts.draw(window)

        collision = sprite.groupcollide(clankas, bolts, False, True)  
         
        for c in collision: 
            c.takedamage()
            if c.health <= 0:
                monster = enemy(clanker, randint(80, win_width - 80), -40, randint(1, 5), 90, 70)
                clankas.add(monster)

        if sprite.spritecollide(player1, clankas, False) or lost >= max_lost:
            finish = True
            img= image.load(img_lose)
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_hight)), (0, 0))

        if score >= goal:
            finish = True
            img = image.load(img_win)
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_hight)), (0, 0))

    
    display.update()



time.delay(50)