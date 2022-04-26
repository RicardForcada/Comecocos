
import pygame

BLACK    = (   0,   0,   0) 
WHITE    = ( 255, 255, 255) 
BLUE     = (   0,   0, 255)
MAGENTA  = ( 255,   0, 255)
CYAN     = (   0, 255, 255)
YELLOW   = ( 255, 255,   0)

# Screen dimensions
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600

class Player():
    """ Definicio """
    def __init__(self,x,y,mapa):
        self.x = x
        self.y = y
        self.tx = x
        self.ty = y
        self.dx = 0
        self.dy = 0
        self.score = 0
        mapa.set(x,y,'<')
    
    def updateDir(self,key):
        if key == pygame.K_LEFT:
            [self.dx,self.dy] = [-1,0]
        elif key == pygame.K_RIGHT:
            self.dx = 1
            self.dy = 0
        elif key == pygame.K_UP:
            self.dx = 0
            self.dy = -1
        elif key == pygame.K_DOWN:
            self.dx = 0
            self.dy = 1
        else:
            self.dx = 0
            self.dy = 0
    
    def updateMap(self, mapa):
        
        self.tx += self.dx
        if self.tx > mapa.cols:
            self.tx = 0
        elif self.tx < 0:
            self.tx = mapa.cols
        self.ty += self.dy

        desti = mapa.check(self.tx,self.ty)
        
        if desti == '<':
            pass
        elif desti == 'W':
            [self.dx, self.dy] = [0,0]
            [self.tx, self.ty] = [self.x,self.y]
        elif desti == '.':
            mapa.set(self.tx, self.ty, '<')
            mapa.set(self.x, self.y, ' ')
            [self.x, self.y] = [self.tx,self.ty]
            self.score += 1
        else:
            mapa.set(self.tx, self.ty, '<')
            mapa.set(self.x, self.y, ' ')
            [self.x, self.y] = [self.tx,self.ty]

    def draw(self):
        pass

class Map():
    """ Definicio """
 
    def __init__(self):
        self.map = ['WWWWWWWWWWWWWWWWWWW',
                    'W .............   W',
                    'W  W   W   W  ... W',
                    'WW     .  .   .  WW',
                    '  .    W  .   .    ',
                    'WW  .  .  WWWW WWWW',
                    'W      .  .   .   W',
                    'WWWWWWWWWWWWWWWWWWW',
                    ]
        self.rows = len(self.map)
        self.cols = len(self.map[0])
        self.size = 20
 
    def check(self,x,y):
        """ Consulta una casella del mapa. Serveix per mirar la casella desti del player"""
        return self.map[y][x]

    def set(self,x,y,item):
        """ Posa el valor de item en una casella del mapa. Serveix per actualitzar el mapa amb el moviment del player"""
        string_list = list(self.map[y])
        string_list[x] = item
        self.map[y] = "".join(string_list)
 
    def draw(self):
        """ Draw everything """
        y = 50
        for row in self.map:
            [x, y] = [0, y + self.size]
            for item in row:
                x += self.size
                if item == 'W':
                    pygame.draw.rect(screen, BLUE, pygame.Rect(x, y, self.size, self.size))
                elif item == '.':
                    pygame.draw.circle(screen, WHITE, [x+int(self.size/2),y+int(self.size/2)],int(self.size/5))
                elif item == '<':
                    pygame.draw.circle(screen, YELLOW, [x+int(self.size/2),y+int(self.size/2)],int(self.size/2))
                

class Game:
    def __init__(self):
        self.status = 1
        self.map = Map()
        self.player = Player(1,2,self.map)
        
        self.keyPressed = ' '
        

    def mainloop(self):
        while self.status==1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.status = 99
                if event.type == pygame.KEYDOWN:
                    self.player.updateDir(event.key)
                elif event.type == pygame.KEYUP:
                    self.keyPressed = ' '

            self.update()
            self.draw()

            clock.tick(5)
            pygame.display.update()
    
    def update(self):
        self.player.updateMap(self.map)


    def draw(self):
        screen.fill(BLACK)
        textsurface = myFont24.render('Score: {0}'.format(self.player.score),False,WHITE)
        screen.blit(textsurface,pygame.Rect(100, 40, 500, 24))
        self.map.draw()

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Comecocos")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    myFont16 = pygame.font.SysFont('calibri', 16)
    myFont24 = pygame.font.SysFont('calibri', 24)
    joc = Game()
    joc.mainloop()
    pygame.quit()
        
