import pygame
pygame.init()

Timer = 30
screenwidth = 500
screenheight = 480
Health = 10
win = pygame.display.set_mode((screenwidth,screenheight))
pygame.display.set_caption("First game")

walkRight = [pygame.image.load('images/R1.png'), pygame.image.load('images/R2.png'), pygame.image.load('images/R3.png'), pygame.image.load('images/R4.png'), pygame.image.load('images/R5.png'), pygame.image.load('images/R6.png'), pygame.image.load('images/R7.png'), pygame.image.load('images/R8.png'), pygame.image.load('images/R9.png')]
walkLeft = [pygame.image.load('images/L1.png'), pygame.image.load('images/L2.png'), pygame.image.load('images/L3.png'), pygame.image.load('images/L4.png'), pygame.image.load('images/L5.png'), pygame.image.load('images/L6.png'), pygame.image.load('images/L7.png'), pygame.image.load('images/L8.png'), pygame.image.load('images/L9.png')]
bg = pygame.image.load('images/bg.jpg')
char = pygame.image.load('images/standing.png')

clock = pygame.time.Clock()
clock2 = pygame.time.Clock()
bulletsound = pygame.mixer.Sound('music/bullet.mp3')
hitsound = pygame.mixer.Sound('music/hit.mp3')

music = pygame.mixer.music.load('music/music.mp3')
pygame.mixer.music.play(-1)

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpcount = 10
        self.left =True
        self.right=False
        self.walkCount=0
        self.score = 0
        self.standing = True
        self.hitbox = (self.x+17, self.y+2, 31, 57)
        self.lives = 5

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):        
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[man.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x,self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x+17, self.y+2, 31, 57)
    
    def hit(self):
        self.x = 60
        self.y = 410
        self.isJump = False
        self.jumpcount = 10
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('--HIT--', 1, (255,0,0))
        win.blit(text, (250 - (text.get_width()/2), 200))
        pygame.display.update()
        i = 0
        while i < 100:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.quit:
                    i = 101
                    pygame.quit()
    
class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8*facing
    
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

class enemy(object):
    walkRight = [pygame.image.load('images/R1E.png'), pygame.image.load('images/R2E.png'), pygame.image.load('images/R3E.png'), pygame.image.load('images/R4E.png'), pygame.image.load('images/R5E.png'), pygame.image.load('images/R6E.png'), pygame.image.load('images/R7E.png'), pygame.image.load('images/R8E.png'), pygame.image.load('images/R9E.png'), pygame.image.load('images/R10E.png'), pygame.image.load('images/R11E.png')]
    walkLeft = [pygame.image.load('images/L1E.png'), pygame.image.load('images/L2E.png'), pygame.image.load('images/L3E.png'), pygame.image.load('images/L4E.png'), pygame.image.load('images/L5E.png'), pygame.image.load('images/L6E.png'), pygame.image.load('images/L7E.png'), pygame.image.load('images/L8E.png'), pygame.image.load('images/L9E.png'), pygame.image.load('images/L10E.png'), pygame.image.load('images/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [0, self.end]
        self.walkCount = 0
        self.vel = 3
        self.health = 10
        self.hitbox = (self.x+17, self.y+2, 31, 57)
        self.visible = True
        self.level = 1
    
    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        if self.visible:
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1]-20, 31, 10))
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1]-20, (31*self.health)/Health, 10))
        self.hitbox = (self.x+17, self.y+2, 31, 57)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0
        else:
            if self.x  > self.path[0]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0

    def hit(self):
        global Health
        if self.health > 1:
            self.health -= 1*self.level
        else:
            font1 = pygame.font.SysFont('comicsans', 100)
            self.level += 1
            text = font1.render('LEVEL ' + str(self.level), 1, (255,0,0))
            win.blit(text, (250 - (text.get_width()/2), 200))
            pygame.display.update()
            i = 0
            while i < 100:
                pygame.time.delay(10)
                i += 1
                for event in pygame.event.get():
                    if event.type == pygame.quit:
                        i = 101
                        pygame.quit()
            self.health = Health*2
            self.vel = 1.4*self.vel
            Health *= 2

def redrawGamewindow():
    win.blit(bg, (0,0))
    text = font.render('Score:' + str(man.score) + ' Lives:' + str(man.lives), 1, (0,0,0))
    text2 = font.render('Timer: ' + str(Timer), 1, (0,0,0))
    win.blit(text, (300, 10))
    win.blit(text2, (100, 10))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

# main
font = pygame.font.SysFont('comicsans', 30, True, True)
man = player(300, 410, 64,64)
goblin = enemy(100, 410, 64, 64, 450)
bullets = []
shootloop = 0 
run = True
counter = 0
while run :
    clock.tick(27)
    counter += 1

    if Timer == 0 or man.lives == 0:
        text3 = font.render('--Game Over--', 1, (255,0,0))
        win.blit(text3, (250 - (text3.get_width()/2), 200))
        pygame.display.update()
        pygame.time.delay(2000)
        run = False

    if counter == 27:
        Timer -= 1
        counter = 0

    if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
            man.hit() 
            man.score -= 10*goblin.level
            goblin.health = Health
            man.lives -= 1

    if shootloop > 0:
        shootloop += 1
    if shootloop > 3:
        shootloop = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                goblin.hit() 
                hitsound.play()
                man.score += goblin.level
                bullets.pop(bullets.index(bullet))               

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootloop == 0:
        bulletsound.play()
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + (man.width // 2)), round(man.y + (man.height // 2)), 6, (0,0,0), facing))
        shootloop = 1

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < screenwidth - man.width -man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
    
    if not(man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.walkCount = 0
    else:
        if man.jumpcount >= -10:
            neg = 1
            if man.jumpcount < 0:
                neg = -1
            man.y -= (man.jumpcount ** 2)*0.5*neg
            man.jumpcount -= 1
        else:
            man.isJump = False
            man.jumpcount = 10
    redrawGamewindow()
    
pygame.quit()

