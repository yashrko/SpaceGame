import pygame as pg
import random
pg.init()
pg.mixer.init()
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
WHITE=(255,255,255)
BLACK=(0,0,0)
fps=30
width=800
height=600
powerTIME=5000
gd=pg.display.set_mode((width,height))
pg.display.set_caption('nothing')
clock=pg.time.Clock()
fontname=pg.font.match_font('arial')
def textdraw(surf,text,size,x,y):
    font=pg.font.Font(fontname,size)
    textsurf=font.render(text,True,BLACK)
    textrect=textsurf.get_rect()
    textrect.midtop=(x,y)
    surf.blit(textsurf,textrect)
def newmob():
    mob=MOB()
    alll.add(mob)
    mobs.add(mob)
def drawshieldbar(surf,x,y,pct):
    if pct<0:
        pct=0
    blength=100
    bheight=10
    fill = (pct/100)*blength
    outrect=pg.Rect(x,y,blength,bheight)
    inrect=pg.Rect(x,y,fill,bheight)
    pg.draw.rect(surf,GREEN,outrect,2)
    pg.draw.rect(surf,GREEN,inrect)
def drawlives(surf,x,y,lives,img):
    for i in range(lives):
        img_rect=img.get_rect()
        img_rect.x=x+30*i
        img_rect.y=y
        surf.blit(img,img_rect)
class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image=pg.transform.scale(plr,(50,38))
        self.image.set_colorkey(BLACK)
        self.radius=20
        self.rect=self.image.get_rect()
        self.rect.bottom=height-20
        self.rect.centerx=width/2
        self.speedx=0
        self.shield=100
        self.lives=3
        self.hidden=False
        self.hidetimer=0
        self.power=1
        self.powertime=pg.time.get_ticks()
    def update(self):
        if self.power>=2 and pg.time.get_ticks()-self.powertime>powerTIME:
            self.power-=1
            self.powertime=pg.time.get_ticks()
        if self.hidden and pg.time.get_ticks()-self.hidetimer>1000:
            self.hidden=False
            self.rect.centerx=width/2
            self.rect.bottom=height-20
        self.speedx=0
        keystate=pg.key.get_pressed()
        if keystate[pg.K_RIGHT]:
            self.speedx=8
        if keystate[pg.K_LEFT]:
            self.speedx=-8    
        self.rect.right+=self.speedx
        if self.rect.right>width:
            self.rect.right=width
        if self.rect.left<0:
            self.rect.left=0
    def shoot(self):
        if self.power ==1:
            bullet=Bullet(self.rect.centerx,self.rect.top)
            alll.add(bullet)
            bullets.add(bullet)
            lsound.play()
        if self.power>=2:
            bullet1=Bullet(self.rect.left,self.rect.centery)
            bullet2=Bullet(self.rect.right,self.rect.centery)
            alll.add(bullet1)
            alll.add(bullet2)
            bullets.add(bullet1)
            bullets.add(bullet2)
            lsound.play()
    def hide(self):
        self.hidden=True
        self.hidetimer=pg.time.get_ticks()
        self.rect.center=(width/2,height+200)
    def twobullet(self):
        self.power+=1
        self.powertime=pg.time.get_ticks()
class MOB(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.orgimage=random.choice(metimage)
        self.orgimage.set_colorkey(BLACK)
        self.image=self.orgimage.copy()
        self.rect=self.image.get_rect()
        self.radius=int(self.rect.width*.85/2)
        self.rect.x=random.randrange(0,width-self.rect.width)
        self.rect.y=random.randrange(-60,-40)
        self.speedy=random.randrange(4,8)
        self.speedx=random.randrange(-3,3)
        self.rot=0
        self.rotspeed=random.randrange(-8,8)
        self.lastupdate=pg.time.get_ticks()
    def rotate(self):
        now=pg.time.get_ticks()
        if now-self.lastupdate>50:
            self.lastupdate=now
            self.rot=(self.rot +self.rotspeed)%360
            newimage = pg.transform.rotate(self.orgimage,self.rot)
            oldcenter=self.rect.center
            self.image=newimage
            self.rect=self.image.get_rect()
            self.rect.center=oldcenter
        
    def update(self):
        self.rotate()
        self.rect.y+=self.speedy
        self.rect.x+=self.speedx
        if self.rect.top>height+10 or self.rect.left<-10 or self.rect.right>810:
            self.rect.x=random.randrange(0,width-self.rect.width)
            self.rect.y=random.randrange(-100,-70)
            self.speedy=random.randrange(2,8)
class Bullet(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.image=pg.transform.scale(blt,(5,12))
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()
        self.rect.bottom=y
        self.rect.centerx=x
        self.speedy=-15
    def update(self):
         self.rect.y+=self.speedy
         if self.rect.bottom<0:
             self.kill()
class POW(pg.sprite.Sprite):
    def __init__(self,center):
        pg.sprite.Sprite.__init__(self)
        self.rand=random.choice(['shield','bolt'])
        self.image=pg.transform.scale(powerup[self.rand],(12,20))
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()
        self.rect.center=center
        self.speedy=2
    def update(self):
         self.rect.y+=self.speedy
         if self.rect.top>height:
             self.kill()             
class explosion(pg.sprite.Sprite):
     def __init__(self,center,size):
        pg.sprite.Sprite.__init__(self)
        self.size=size
        self.image=explosionanim[self.size][0]
        self.rect=self.image.get_rect()
        self.rect.center=center
        self.frame=0
        self.lastupdate=pg.time.get_ticks()
        self.framerate=75
     def update(self):
         now=pg.time.get_ticks()
         if now-self.lastupdate>self.framerate:
             self.lastupdate=now
             self.frame += 1
             if self.frame==len(explosionanim[self.size]):
                 self.kill()
             else: 
                center=self.rect.center
                self.image = explosionanim[self.size][self.frame]
                self.rect=self.image.get_rect()
                self.rect.center=center
def gameoverscreen():
    gd.blit(backg,backgrect)
    textdraw(gd,'MY GAME!',70,width/2,height/4)
    textdraw(gd,'arrow key to control, space to shoot',24,width/2,height/2)
    textdraw(gd,'press any key to start',40,width/2,height*3/4)
    pg.display.flip()
    waiting=True
    while waiting:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type==pg.QUIT:
                pg.quit()
            if event.type==pg.KEYUP:
                waiting=False                
backg=pg.image.load('space.png').convert()
backgrect=backg.get_rect()
plr=pg.image.load('playerShip1_green.png').convert()
plrrect=plr.get_rect()
plrminiimage=pg.transform.scale(plr,(25,25))
plrminiimage.set_colorkey(BLACK)
#mtr=pg.image.load('meteorBrown_med3.png').convert()
powerup={}
powerup['shield']=pg.image.load('shield.png').convert()
powerup['bolt']=pg.image.load('bolt.png').convert()
metimage=[]
metlist=['meteorBrown_big1.png','meteorBrown_big2.png','meteorBrown_med1.png',
         'meteorBrown_med3.png','meteorBrown_small1.png','meteorBrown_small2.png',
         'meteorBrown_tiny1.png']
for img in metlist:
    metimage.append(pg.image.load(img).convert())
blt=pg.image.load('laserBlue06.png').convert()
explosionanim={}
explosionanim['lg']=[]
explosionanim['sm']=[]
explosionanim['player']=[]
for i in range(9):
    fname='regularExplosion0{}.png'.format(i)
    img=pg.image.load(fname).convert()
    img.set_colorkey(BLACK)
    imglg=pg.transform.scale(img,(75,75))
    explosionanim['lg'].append(imglg)
    imgsm=pg.transform.scale(img,(35,35))
    explosionanim['sm'].append(imgsm)
    fname1='sonicExplosion0{}.png'.format(i)
    img1=pg.image.load(fname1).convert()
    img1.set_colorkey(BLACK)
    #imgpl=pg.transform.scale(img1,(80,80))
    explosionanim['player'].append(img1)
lsound=pg.mixer.Sound('lsound.wav')
msound=pg.mixer.Sound('Explosion3.wav')

gamerun=True
gameover=True
while gamerun:
    if gameover:
       gameoverscreen()
       gameover=False
       alll=pg.sprite.Group()
       mobs=pg.sprite.Group()
       bullets=pg.sprite.Group()
       pups=pg.sprite.Group()
       player=Player()        
       alll.add(player)
       for i in range(20):
         newmob()
       score=0 
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gamerun=False
        elif event.type ==pg.KEYDOWN:
            if event.key== pg.K_SPACE:
                player.shoot()
    gd.fill(WHITE)
    alll.update()
    hits=pg.sprite.spritecollide(player,mobs,True,pg.sprite.collide_circle)
    for hit in hits:
        newmob()
        exp=explosion(hit.rect.center,'sm')
        alll.add(exp)
        player.shield-=hit.radius
        if player.shield<=0:
            msound.play()
            deathexplosion=explosion(player.rect.center,'player')
            alll.add(deathexplosion)
            player.hide()
            player.shield=100
            player.lives-=1
    if player.lives==0 and not deathexplosion.alive():
        gameover=True
    hiti=pg.sprite.groupcollide(mobs,bullets,True,True)
    for hit in hiti:
        if random.random()>.9:
           pup=POW(hit.rect.center)
           alll.add(pup)
           pups.add(pup)
        msound.play()
        score+=50-hit.radius
        exp=explosion(hit.rect.center,'lg')
        alll.add(exp)
        newmob()
    hity=pg.sprite.spritecollide(player,pups,True)
    for hit in hity:
        if hit.rand=='shield':
            player.shield+=20
            if player.shield>100:
                player.shield=100
        if hit.rand=='bolt':
            player.twobullet()
    gd.blit(backg,backgrect)
    alll.draw(gd)
    textdraw(gd,str(score),20,width/2,10)
    drawshieldbar(gd,5,5,player.shield)
    drawlives(gd,width-100,5,player.lives,plrminiimage)
    pg.display.flip()
    clock.tick(fps)
pg.quit()

