import pygame                                     
from pygame.locals import *
import time
import random

SIZE = 40
HEIGHT = 800
LENGTH_ = 1000
BACKGROUND_COLOR = (118, 163, 122)
highscore = 0
class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = random.randint(0,23)*SIZE
        self.y = random.randint(0,20)*SIZE

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0,23)*SIZE
        self.y = random.randint(0,19)*SIZE
        ##self.parent_screen.blit(self.image,(self.x,self.y))
       ## pygame.display.flip()

class Snake:
    def __init__(self, parent_screen,length):

        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.direction = 'down'

        self.length = length
        self.highscore = highscore
        self.x = [SIZE] * length
        self.y = [SIZE] * length

    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def walk(self):

        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'up':
            self.y[0]-=SIZE
        if self.direction == 'down':
            self.y[0]+=SIZE
        if self.direction == 'left':
            self.x[0]-=SIZE
        if self.direction == 'right':
            self.x[0]+=SIZE
        self.draw()

    def move_up(self):
        self.direction = 'up'
        self.draw()

    def move_down(self):
        self.direction = 'down'
        self.draw()

    def move_left(self):
        self.direction = 'left'
        self.draw()

    def move_right(self):
        self.direction = 'right'
        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.highscore = highscore
        self.surface = pygame.display.set_mode((1000,800))
        self.snake = Snake(self.surface,1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collusion(self, x1, x2, y1, y2):

        if x1 >= x2 and x1< x2+SIZE:
            if y1>=y2 and y1< y2+SIZE:
                return True
        return False

    def exit_boundaries(self,x1,y1):
        if x1<0 or y1<0 or y1>HEIGHT or x1>LENGTH_:
            return True
        return False

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def background_music(self):
        sound = pygame.mixer.Sound("resources/Theme Song.mp3")

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg,(0,0))

    def play(self):
        self.render_background()

        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collusion(self.snake.x[0],self.apple.x,self.snake.y[0],self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        for i in range(3,self.snake.length):
            if self.is_collusion(self.snake.x[0],self.snake.x[i],self.snake.y[0],self.snake.y[i]):
                self.play_sound("crash")
                raise "Game over"


        if self.exit_boundaries(self.snake.x[0],self.snake.y[0]):
            self.play_sound("crash")
            raise "Game over"

    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length-1}", True, (200,200,200))
        self.surface.blit(score, (800,10))

    def game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont("arial", 30)
        FONT = pygame.font.SysFont("bold",50)

        Game_OVER = font.render(f"GAME OVER. Your score is: {self.snake.length-1}.", True, (114,24,24))

        if self.highscore < self.snake.length - 1:
            congrats = FONT.render(f"Congratulations. Your new highscore is: {self.snake.length-1}.",True,(114,24,24))
            self.highscore = self.snake.length-1
        else:
            congrats = FONT.render(f"Your current highscore is: {self.highscore}.", True, (114,24,24))



        self.surface.blit(Game_OVER,(200,300))
        self.surface.blit(congrats,(200,400))
        line  = font.render("To play again press enter. To exit press Escape", True, (205,199,18))
        self.surface.blit(line, (200,600))
        pygame.display.flip()

    def reset(self):
        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def run(self):
        running = True
        pause = False
        self.play_sound("Theme Song") 
        while running:

            #print(running)
            #("89=",pause)

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        #print("$$$")
                        pause = False
                        self.reset()


                    if not pause:

                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        elif event.type == QUIT:
                            running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.game_over()
                pause = True
            time.sleep(0.3)




if __name__ == "__main__":
    game = Game()
    game.run()


