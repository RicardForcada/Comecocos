
import pygame

BLACK    = (   0,   0,   0) 
WHITE    = ( 255, 255, 255) 
BLUE     = (   0,   0, 255)
MAGENTA  = ( 255,   0, 255)
CYAN     = (   0, 255, 255)
YELLOW   = ( 255, 255,   0)
RED      = ( 255,   0,   0)
ORANGE   = ( 255, 128,   0)

# Screen dimensions
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 800
SIZE = 20

class Coco():
    """ Definicio """
    def __init__(self,x,y,sprite):
        self.x = x
        self.y = y
        self.sprite = sprite
    
    def draw(self,s):
        if self.sprite == '.':
            pygame.draw.circle(s, WHITE, [(self.x*SIZE)+int(SIZE/2),(self.y*SIZE)+int(SIZE/2)],int(SIZE/5))
        elif self.sprite == 'o':
            pygame.draw.circle(s, YELLOW, [(self.x*SIZE)+int(SIZE/2),(self.y*SIZE)+int(SIZE/2)],int(SIZE/4))
        else:
            pass

class Ghost():
    """ Definicio """
    def __init__(self,x,y,sprite):
        self.x = x
        self.y = y
        self.tx = x
        self.ty = y
        self.dx = 0
        self.dy = 0
        self.sprite = sprite
    
    def update(self,key,mapa):
        self.updatedxdy(key)
        self.updatexy(mapa)

    def updatedxdy(self,key):
        """
        L'objectiu es deixar dx i dy correctes tenint en compte el comportament
        del fantasma (aqui no es tenen en compte els obstacles).
        Cada fantasma es mou de manera diferent, per aixo s'executa una
        funcio diferent per cada un d'ells.
        """
        if self.sprite == '#': #Blinky - RED
            self.updateDirBlinky()
        elif self.sprite == '&': #Inky - CYAN
            self.updateDirInky(key)
        elif self.sprite == '$': #Clyde - ORANGE
            self.updateDirClyde(key)
        else:
            pass
    
    def updateDirBlinky(self):
        """
        """
        [self.dx,self.dy] = [0, 0] #pendiente

    def updateDirInky(self,key):
        if key == pygame.K_LEFT:
            [self.dx,self.dy] = [-1, 0]
        elif key == pygame.K_RIGHT:
            [self.dx,self.dy] = [1, 0]
        elif key == pygame.K_UP:
            [self.dx,self.dy] = [0, -1]
        elif key == pygame.K_DOWN:
            [self.dx,self.dy] = [0, 1]
        else:
            [self.dx,self.dy] = [0, 0]
    
    def updateDirClyde(self,key):
        if key == pygame.K_LEFT:
            [self.dx,self.dy] = [1, 0]
        elif key == pygame.K_RIGHT:
            [self.dx,self.dy] = [-1, 0]
        elif key == pygame.K_UP:
            [self.dx,self.dy] = [0, 1]
        elif key == pygame.K_DOWN:
            [self.dx,self.dy] = [0, -1]
        else:
            [self.dx,self.dy] = [0, 0]
    
    def updatexy(self, mapa):
        """
        Es deixen actualitzades les posicions tenint en compte els obstacles
        """
        self.tx += self.dx
        # Tractamente de la posicio del fantasma pq quan surti per l'esquerra
        # apareixi per la dreta i a l'inreves
        if self.tx > mapa.cols - 1:
            self.tx = 0
        elif self.tx < 0:
            self.tx = mapa.cols - 1
        self.ty += self.dy

        desti = mapa.check(self.tx,self.ty)
        
        if desti == 'W':
            [self.dx, self.dy] = [0,0]
            [self.tx, self.ty] = [self.x,self.y]
        else:
            [self.x, self.y] = [self.tx,self.ty]

    def draw(self,s):
        if self.sprite == '#':
            pygame.draw.polygon(s, RED, [((SIZE*self.x)+int(SIZE/2),(SIZE*self.y)),((SIZE*self.x)+SIZE,(SIZE*self.y)+SIZE),((SIZE*self.x),(SIZE*self.y)+SIZE)])
        elif self.sprite == '$':
            pygame.draw.polygon(s, ORANGE, [((SIZE*self.x)+int(SIZE/2),(SIZE*self.y)),((SIZE*self.x)+SIZE,(SIZE*self.y)+SIZE),((SIZE*self.x),(SIZE*self.y)+SIZE)]) 
        elif self.sprite == '&':
            pygame.draw.polygon(s, CYAN, [((SIZE*self.x)+int(SIZE/2),(SIZE*self.y)),((SIZE*self.x)+SIZE,(SIZE*self.y)+SIZE),((SIZE*self.x),(SIZE*self.y)+SIZE)]) 
        else:
            pass



class Player():
    """ Definicio """
    def __init__(self,x,y):
        [self.x, self.y] = [x, y]
        [self.tx, self.ty] = [x, y]
        [self.initx, self.inity] = [x, y]
        [self.dx, self.dy] = [0, 0]
        self.score = 0
        self.lives = 3
    
    def update(self,key,mapa):
        self.updatedxdy(key)
        self.updatexy(mapa)

    def restoreXY(self):
        self.lives -= 1
        [self.x,self.y] = [self.initx,self.inity]
        [self.tx,self.ty] = [self.initx,self.inity]

    def updatedxdy(self,key):
        if key == pygame.K_LEFT:
            [self.dx,self.dy] = [-1, 0]
        elif key == pygame.K_RIGHT:
            [self.dx,self.dy] = [1, 0]
        elif key == pygame.K_UP:
            [self.dx,self.dy] = [0, -1]
        elif key == pygame.K_DOWN:
            [self.dx,self.dy] = [0, 1]
        else:
            [self.dx,self.dy] = [0, 0]
    
    def updatexy(self, mapa):
        self.tx += self.dx
        # Tractamente de la posicio del jugador pq quan surti per l'esquerra
        # apareixi per la dreta i a l'inreves
        if self.tx > mapa.cols - 1:
            self.tx = 0
        elif self.tx < 0:
            self.tx = mapa.cols - 1
        self.ty += self.dy

        # Es comprova si es pot anar en la direccio triada. Si no es pot,
        # es posa la velocitat a 0
        if mapa.check(self.tx,self.ty) == 'W':
            [self.dx, self.dy] = [0,0]
            [self.tx, self.ty] = [self.x,self.y] # no em moc
        else:
            [self.x, self.y] = [self.tx,self.ty] # me muevo

    def draw(self,s):
        pygame.draw.circle(s, YELLOW, [(self.x*SIZE)+int(SIZE/2),(self.y*SIZE)+int(SIZE/2)],int(SIZE/2))

class Map():
    """ Definicio del mapa. Significat de cada Item
      W - Pared
      . - Coco normal
      o - Coco Energia
      < - Jugador
      $&# - Fantasme
    """
    def __init__(self):
        self.map = ['WWWWWWWWWWWWWWWWWWWWWWWWWWWW',
                    'W............WW............W',
                    'W.WWWW.WWWWW.WW.WWWWW.WWWW.W',
                    'WoWWWW.WWWWW.WW.WWWWW.WWWWoW',
                    'W.WWWW.WWWWW.WW.WWWWW.WWWW.W',
                    'W............&.............W',
                    'W.WWWW.WW.WWWWWWWW.WW.WWWW.W',
                    'W.WWWW.WW.WWWWWWWW.WW.WWWW.W',
                    'W......WW....WW....WW......W',
                    'WWWWWW.WWWWW WW WWWWW.WWWWWW',
                    '     W.WWWWW WW WWWWW.W     ',
                    '     W.WW    #     WW.W     ',
                    '     W.WW WWWWWWWW WW.W     ',
                    'WWWWWW.WW W      W WW.WWWWWW',
                    '      .   W      W   .      ',
                    'WWWWWW.WW W      W WW.WWWWWW',
                    '     W.WW WWWWWWWW WW.W     ',
                    '     W.WW     <    WW.W     ',
                    'WWWWWW.WW WWWWWWWW WW.WWWWWW',
                    'W............WW............W',
                    'W.WWWW.WWWWW.WW.WWWWW.WWWW.W',
                    'W.WWWW.WWWWW.WW.WWWWW.WWWW.W',
                    'Wo..WW....... $.......WW..oW',
                    'WWW.WW.WW.WWWWWWWW.WW.WW.WWW',
                    'WWW.WW.WW.WWWWWWWW.WW.WW.WWW',
                    'W......WW....WW....WW......W',
                    'W.WWWWWWWWWW.WW.WWWWWWWWWW.W',
                    'W.WWWWWWWWWW.WW.WWWWWWWWWW.W',
                    'W..........................W',
                    'WWWWWWWWWWWWWWWWWWWWWWWWWWWW'
                    ]
        self.rows = len(self.map)
        self.cols = len(self.map[0])

    def mapDims(self):
        return [(self.cols + 1) * SIZE,(self.rows + 1) * SIZE]

    def check(self,x,y):
        """ Consulta una casella del mapa. Serveix per mirar la casella desti del player"""
        return self.map[y][x]

    def extract(self):
        cocos = []
        fantasmes = []
        [x, y] = [0, 0]
        for row in self.map:      
            for item in row:
                if item == '<':
                    player = Player(x,y)
                    self.set(x,y,' ')
                elif item in ['o','.']:
                    cocos.append(Coco(x,y,item))
                    self.set(x,y,' ')
                elif item in ['#','$','&']:
                    fantasmes.append(Ghost(x,y,item))
                    self.set(x,y,' ')
                x += 1
            [x, y] = [0, y + 1]
              #  print('x={0} y={1}'.format(x,y))

        return [player,fantasmes,cocos]

    def set(self,x,y,item):
        """ Posa el valor de item en una casella del mapa."""
        string_list = list(self.map[y])
        string_list[x] = item
        self.map[y] = "".join(string_list)
 
    def draw(self,s):
        """ Dibuixa les parets """
        [x, y] = [0, 0]
        for row in self.map:
            for item in row:
                if item == 'W':
                    pygame.draw.rect(s, BLUE, pygame.Rect(x, y, SIZE, SIZE))
                x += SIZE
            [x, y] = [0, y + SIZE]

class Game:
    def __init__(self):
        self.status = 'Init'
        self.map = Map()
        self.surface = pygame.Surface(self.map.mapDims())
        [self.player, self.fantasmesList, self.cocosList] = self.map.extract()
        self.keyPressed = ' '

    def mainloop(self):
        while self.status != 'Quit':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.status = 'Quit'
                if event.type == pygame.KEYDOWN:
                    self.keyPressed = event.key
                elif event.type == pygame.KEYUP:
                    self.keyPressed = ' '
            
            self.updateStatus()

            if self.status == 'Play': 
                self.update()
    
            self.draw()

            clock.tick(5)
            pygame.display.update()
    
    def updateStatus(self):
            if self.keyPressed == pygame.K_p:
                if self.status == 'Play':
                    self.status = 'Paused'
            elif self.keyPressed == pygame.K_SPACE:
                if self.status == 'Init' or self.status == 'Paused' or self.status == 'GameOver':
                    self.status = 'Play'
            elif self.keyPressed == pygame.K_ESCAPE:
                self.status = 'Quit'
            elif self.player.lives < 1 or self.cocosList == []:
                self.status = 'GameOver'
        
    def update(self):
        self.player.update(self.keyPressed,self.map)
        
        for fantasma in self.fantasmesList:
            fantasma.update(self.keyPressed,self.map)

        for fantasma in self.fantasmesList:
            if fantasma.x == self.player.x and fantasma.y == self.player.y:
                self.player.restoreXY()
                break
            
        for coco in self.cocosList:
            if coco.x == self.player.x and coco.y == self.player.y:
                self.player.score += 1
                self.cocosList.remove(coco)
                break


    def draw(self):
        screen.fill(BLACK)
        # Missatge a l'inici de la pantalla
        if self.status == 'Init':
            textsurface = myFont20.render('Press space to start game, ESC to exit. [{0}]'.format(self.status),False,WHITE)
        elif self.status == 'Paused':
            textsurface = myFont20.render('Game paused. Press SPACE to continue, ESC to exit.  [{0}]'.format(self.status),False,WHITE)
        elif self.status == 'GameOver':
            textsurface = myFont20.render('Game Over. Press SPACE to start, ESC to exit.  [{0}]'.format(self.status),False,RED)
        else:
            textsurface = myFont20.render('Enjoy playing, ESC to exit.  [{0}]'.format(self.status),False,WHITE)
        screen.blit(textsurface,pygame.Rect(SIZE, 0, 500, SIZE))    
        
        self.surface.fill(BLACK)
        self.map.draw(self.surface)

        for coco in self.cocosList:
            coco.draw(self.surface)

        for fantasma in self.fantasmesList:
            fantasma.draw(self.surface)

        self.player.draw(self.surface)
        screen.blit(self.surface,(SIZE,SIZE))

        # Missatge al final de la pantalla
        textsurface = myFont20.render('Score: {0}  Lives: {1}'.format(self.player.score, self.player.lives),False,WHITE)
        screen.blit(textsurface,pygame.Rect(SIZE, SIZE * (self.map.rows + 1), 500, SIZE))

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Comecocos")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    clock = pygame.time.Clock()
    myFont20 = pygame.font.SysFont('calibri', 20)

    joc = Game()
    joc.mainloop()

    pygame.quit()
        
