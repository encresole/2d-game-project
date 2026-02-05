import pygame

class Particle:
    position=(0,0)

    def __init__(self,chemin,pos):
        self.sheet=pygame.image.load(chemin).convert_alpha()
        self.position=pos
    def draw(self,surface):
        surface.blit(self.sheet,self.position)

class AnimatedSprite:
    def __init__(self, chemin, lignes, colonnes, toAnimate, vitesse=0.2):
        """
        toAnimate = (ligne_start, ligne_end, col_start, col_end)
        """
        self.sheet = pygame.image.load(chemin).convert_alpha()
        self.lignes = lignes
        self.colonnes = colonnes
        self.vitesse = vitesse
        self.frames = []
        self.frame_index = 0

        sheet_rect = self.sheet.get_rect()
        frame_width = sheet_rect.width // colonnes
        frame_height = sheet_rect.height // lignes

        ligne_start, ligne_end, col_start, col_end = toAnimate

        for y in range(ligne_start, ligne_end):
            for x in range(col_start, col_end):
                rect = pygame.Rect(x*frame_width, y*frame_height, frame_width, frame_height)
                self.frames.append(self.sheet.subsurface(rect))

    def draw(self, surface, pos):
        surface.blit(self.frames[int(self.frame_index)], pos)
        self.frame_index += self.vitesse
        if self.frame_index >= len(self.frames):
            self.frame_index = 0



#game varialbles
HEIGHT=400
WIDTH=600
running=True
speed=10
pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

#idle Sprites
idleDown = AnimatedSprite("PlayerSprite/Unarmed/Idle.png", lignes=4, colonnes=12, vitesse=0.06, toAnimate=(0,1,0,5))
idleUp= AnimatedSprite("PlayerSprite/Unarmed/Idle.png", lignes=4, colonnes=12, vitesse=0.06, toAnimate=(3,4,0,1))
idleLeft=AnimatedSprite("PlayerSprite/Unarmed/Idle.png", lignes=4, colonnes=12, vitesse=0.06, toAnimate=(1,2,0,12))
idleRight=AnimatedSprite("PlayerSprite/Unarmed/Idle.png", lignes=4, colonnes=12, vitesse=0.06, toAnimate=(2,3,0,12))

#walking Sprites
walkingDown = AnimatedSprite("PlayerSprite/Unarmed/Run.png", lignes=4, colonnes=8, vitesse=0.15, toAnimate=(0,1,0,8))
walkingUp=AnimatedSprite("PlayerSprite/Unarmed/Run.png", lignes=4, colonnes=8, vitesse=0.15, toAnimate=(3,4,0,8))
walkingLeft=AnimatedSprite("PlayerSprite/Unarmed/Run.png", lignes=4, colonnes=8, vitesse=0.15, toAnimate=(1,2,0,8))
walkingRight=AnimatedSprite("PlayerSprite/Unarmed/Run.png", lignes=4, colonnes=8, vitesse=0.15, toAnimate=(2,3,0,8))

x, y = 100, 200
playerWidth=13
playerHeight=22
playerRectXOffset=25
playerRectYOffsset=22

speed = 2
running = True
moving=False
lookAt="Down"

particleDrawing=[]

def mapBorder(x,y,width,heigth,mapX,mapY):
    ret=[]
    nothing=True
    if x<0:
        ret.append(0-playerRectXOffset)
        nothing=False
    elif x+width>mapX:
        print("entered")
        ret.append(mapX-playerRectXOffset-playerWidth)
        nothing=False
    else:
        ret.append(x-playerRectXOffset)

    if y<0:
        ret.append(0-playerRectYOffsset)
        nothing=False
    elif y+heigth>mapY:
        ret.append(mapY-playerRectYOffsset-playerHeight)
        nothing=False
    else:
        ret.append(y-playerRectYOffsset)

    if nothing:
        return None
    print(ret)
    return ret

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    moving = False 
    playerRect=pygame.Rect(x+playerRectXOffset,y+playerRectYOffsset,playerWidth,playerHeight)
    needReposition=mapBorder(playerRect.x,playerRect.y,playerRect.width,playerRect.height,WIDTH,HEIGHT)
    
    if needReposition is not None:
        x=needReposition[0]
        y=needReposition[1]

    dx = 0
    dy = 0

    if keys[pygame.K_d]:
        dx += 1
        lookAt = "Right"
    if keys[pygame.K_q]:
        dx -= 1
        lookAt = "Left"
    if keys[pygame.K_s]:
        dy += 1
        lookAt = "Down"
    if keys[pygame.K_z]:
        dy -= 1
        lookAt = "Up"
    
    if dx != 0 or dy != 0:
        moving = True
        length = (dx**2 + dy**2) ** 0.5
        dx /= length
        dy /= length

        x += dx * speed
        y += dy * speed
    else:
        moving = False


    #Start drawing
    screen.fill((255, 255, 255)) 
    #Under the player
    pygame.draw.rect(screen,(255,0,0),(50,50,10,10))
    if len(particleDrawing)!=0:
        for particle in particleDrawing:
            particle.draw(screen)
    #Drawing player
    if moving:
        if lookAt=="Right":
            particleDrawing.append(Particle("PlayerSprite/particle.png",(playerRect.x,playerRect.y)))
            walkingRight.draw(screen,(x,y))
        elif lookAt=="Up":
            particleDrawing.append(Particle("PlayerSprite/particle.png",(playerRect.x,playerRect.y)))
            walkingUp.draw(screen,(x,y))
        elif lookAt=="Left":
            particleDrawing.append(Particle("PlayerSprite/particle.png",(playerRect.x,playerRect.y)))
            walkingLeft.draw(screen,(x,y))
        else:
            particleDrawing.append(Particle("PlayerSprite/particle.png",(playerRect.x,playerRect.y)))
            walkingDown.draw(screen,(x,y))
    else:
        if lookAt=="Right":
            idleRight.draw(screen,(x,y))
        elif lookAt=="Up":
            idleUp.draw(screen,(x,y))
        elif lookAt=="Left":
            idleLeft.draw(screen,(x,y))
        else:
            idleDown.draw(screen,(x,y))
    #On the player
    pygame.draw.rect(screen,(0,255,0),(70,50,10,10))

    #End drawing
    pygame.display.flip()
    clock.tick(60)

pygame.quit()


