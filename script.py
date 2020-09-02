import pygame
import pygame.locals
import random

pygame.mixer.init()
fire = pygame.mixer.Sound('gun2.WAV')
fire.set_volume(0.1)
boom_sound = pygame.mixer.Sound('boom.WAV')
reload_sound = pygame.mixer.Sound('reload.WAV')

class Screen(object):

    def __init__(self, width, height):
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption("GOBLINS IN THE WILD WEST @Szczotar")

class Background(object):
    def __init__(self, width, height, x, y):
        self.width = width
        self.heigth = height
        self.x = x
        self.y = y
        self.surface = pygame.image.load('west2.jpg')
        self.rect = self.surface.get_rect(x=x, y=y)

    def draw(self, surface):
        surface.blit(self.surface, self.rect)

class Target(pygame.sprite.Sprite):
    def __init__(self, width, height, speed_x, speed_y, x, y,color = (0,0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.x = x
        self.y = y
        self.color = color
        self.move_counter = 0
        self.images = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'),
                         pygame.image.load('R3E.png'), pygame.image.load('R4E.png'),
                         pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                         pygame.image.load('R7E.png'), pygame.image.load('R8E.png'),
                         pygame.image.load('R9E.png'), pygame.image.load('R10E.png'),
                         pygame.image.load('R11E.png')]
        self.image = pygame.Surface.copy(self.images[0])
        self.rect = self.image.get_rect(x=x,y=y)

    def update_image(self):
        self.image = pygame.Surface.copy(self.images[self.move_counter])

class Explosion(object):
    def __init__(self,x,y):
        self.images = [pygame.image.load('boom1.png'), pygame.image.load('boom2.png'),
                       pygame.image.load('boom3.png'),pygame.image.load('boom4.png'),
                       pygame.image.load('boom5.png'),pygame.image.load('boom6.png'),
                       pygame.image.load('boom7.png'),pygame.image.load('boom8.png')]
        self.image = pygame.Surface.copy(self.images[0])
        self.re = self.image.get_rect(x=x,y=y)
        self.x = x
        self.y = y
        self.counter = 0

    def get_position(self,pos):
        self.re.x = pos[0] - 50
        self.re.y= pos[1] - 50

    def draw(self,surface):
        if  self.counter > 0:
            self.image = pygame.Surface.copy(self.images[self.counter -1])
            surface.blit(self.image,self.re)
            self.counter += 1
            if self.counter == 8:
                self.counter = 0

class Tank(Explosion):
    def __init__(self,x,y):
        super(Tank,self).__init__(x,y)
        self.group = pygame.sprite.Group()
        self.counter = 0
        self.t2 = 0

    def create_sprite(self):
        time = pygame.time.get_ticks()/1000 - self.t2

        if time//5 == self.counter:
            self.counter += 1

            if time < 10:
                for x in range(0,2):
                    z = (random.randint(19, 35)) * 10
                    w = (random.randint(-20,-1))*10
                    creature = Target(30,30,3,3,w,z)
                    self.group.add(creature)

            if 10 <= time <= 30:
                for x in range(0, 4):
                    z = (random.randint(19, 35)) * 10
                    w = (random.randint(-30, -1)) * 10
                    creature = Target(30, 30, 3, 3, w, z)
                    self.group.add(creature)

            if 30 < time <= 50:
                for x in range(0, 8):
                    z = (random.randint(19, 35)) * 10
                    w = (random.randint(-50, -1)) * 10
                    creature = Target(30, 30, 3, 3, w, z)
                    self.group.add(creature)

            if 50 < time <= 70:
                for x in range(0, 10):
                    z = (random.randint(19, 35)) * 10
                    w = (random.randint(-60, -1)) * 10
                    creature = Target(30, 30, 3, 3, w, z)
                    self.group.add(creature)

            if 70 < time:
                for x in range(0, 12):
                    z = (random.randint(19, 35)) * 10
                    w = (random.randint(-70, -1)) * 10
                    creature = Target(30, 30, 3, 3, w, z)
                    self.group.add(creature)

    def get_position(self, pos):
        self.re.x = pos[0] - 50
        self.re.y = pos[1] - 50

    def kill_sprite(self):
        z, w = pygame.mouse.get_pos()
        for monster in self.group:
            z, w = pygame.mouse.get_pos()
            if monster.rect.collidepoint((z,w)) and \
                    z in range(monster.rect.x +10, monster.rect.x + 30) and \
                    w in range(monster.rect.y + 10,monster.rect.y + 40):
                monster.rect.x = 2000
                newgame.score.update_score()

    def explode_sprite(self):
        print(self.re)
        for monster in self.group:
            if monster.rect.colliderect(self.re):
                monster.rect.x = 2000
                newgame.score.update_score()

    def move(self,surface):

        for sprite in self.group:
            sprite.update_image()
            surface.blit(sprite.image,sprite.rect)
            sprite.move_counter +=1
            sprite.rect.x += sprite.speed_x

            if sprite.move_counter >= 8:
                sprite.move_counter = 0

            if 1065 < sprite.rect.x < 1200:
                newgame.score.game_over(surface)
                pygame.time.delay(1000)

    def pick_up_boomb(self,pos):

        if newgame.boombs.rect_boom.collidepoint(pos):
            newgame.boombs.rect_boom.x = - 100
            newgame.score.update_ammo()
            reload_sound.play()

class Boomb_sprite(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.image_boom = pygame.image.load('bomba.png')
        self.rect_boom = self.image_boom.get_rect(x=x,y=y)
        self.timer = 0

    def boombs_pos_reset(self):
        self.rect_boom.x = random.randint(50,800)
        self.rect_boom.y = random.randint(50,300)

    def draw(self,surface):
        time = pygame.time.get_ticks()/1000

        if  10 < time - 20 * self.timer  <15:
            surface.blit(self.image_boom, self.rect_boom)
        if time - 20 * self.timer >= 20:
            self.rect_boom.x = random.randint(50, 800)
            self.rect_boom.y = random.randint(50, 300)
            self.timer += 1

class Gun_point(object):
    def __init__(self, width, height, speed_x, speed_y, x, y, color=(0, 0, 0)):
        self.width = width
        self.height = height
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.x = x
        self.y = y
        self.color = color
        self.surface = pygame.image.load("celownik.png").convert()
        self.rect = self.surface.get_rect(x=x, y=y)

    def draw(self, surface):
        self.surface.set_colorkey((0, 0, 0))
        surface.blit(self.surface, self.rect)

    def move(self):
        up, down = pygame.mouse.get_pos()
        self.rect.x = up - 17
        self.rect.y = down - 17

class Score(object):
    def __init__(self,ammo):
        self.ammo = ammo
        self.score = 0
        pygame.font.init()
        font_path = pygame.font.match_font('arial',bold=True)
        self.font = pygame.font.Font(font_path,20)
        self.font2 = pygame.font.Font(font_path, 100)
        self.font3 = pygame.font.Font(font_path, 50)
        self.font4 = pygame.font.Font(font_path,40)
        self.goblin = pygame.image.load('R6E.png')
        self.boomb_point = pygame.image.load('bomba.png')

    def update_score(self):
        self.score += 1

    def update_ammo(self):
        self.ammo += 1

    def draw_text(self,surface):
        text = self.font.render(f'{self.score}',True,(255,0,0))
        text2 = self.font.render(f'{self.ammo}',True,(255,0,0))
        rect = text.get_rect(x = 873, y = 25)
        rect2 = text2.get_rect(x=950,y =25)
        surface.blit(text,rect)
        surface.blit(text2,rect2)
        surface.blit(self.goblin,(820,0))
        surface.blit(self.boomb_point,(910,10))

    def game_over(self,surface):
        text3 = self.font2.render(f'GAME OVER',True,(0,255,0))
        text4 = self.font3.render(f'Your total score is {self.score}',True,(0,255,0))
        text5 = self.font4.render('Press SPACE to play again',True,(0,255,0))
        rect3  = text3.get_rect(x = 200, y = 100)
        rect4 = text4.get_rect(x = 250, y = 220)
        rect5 = text5.get_rect(x = 250,y = 300)
        surface.blit(text3,rect3)
        surface.blit(text4,rect4)
        surface.blit(text5,rect5)

class Game(object):
    def __init__(self, width, heigth):
        pygame.init()
        self.fps_clock = pygame.time.Clock()
        self.screen = Screen(width, heigth)
        self.background = Background(width, heigth, 0, 0)
        self.gun = Gun_point(35, 35, 500, 500, 0, 0)
        self.monster = Target(30, 30, 3, 3, 100,200)
        self.explosion = Explosion(100,100)
        self.tank = Tank(100, 100)
        self.boombs = Boomb_sprite(300,300)
        self.score = Score(0)
        self.game_on = True

    def run(self):
        while self.game_on:
            pygame.mouse.set_visible(False)
            pygame.init()
            self.fps_clock.tick(30)
            self.handle_events()
            self.background.draw(self.screen.surface)
            self.boombs.draw(self.screen.surface)
            self.tank.create_sprite()
            self.tank.move(self.screen.surface)
            self.gun.draw(self.screen.surface)
            self.gun.move()
            self.explosion.draw(self.screen.surface)
            self.score.draw_text(self.screen.surface)
            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.locals.QUIT:
                pygame.quit()
                return False

            if event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.score.ammo = 0
                    self.score.score = 0
                    self.tank.group.empty()
                    self.tank.t2 = pygame.time.get_ticks()//1000
                    self.tank.counter = 0

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                point_pos = event.pos
                self.tank.kill_sprite()
                self.tank.pick_up_boomb(point_pos)
                fire.play(0)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                pos = event.pos
                self.explosion.get_position(pos)
                self.tank.get_position(pos)
                if self.score.ammo > 0:
                    self.explosion.counter = 1
                    self.tank.explode_sprite()
                    boom_sound.play(0)
                    self.score.ammo -= 1

newgame = Game(1065, 420)
newgame.run()
