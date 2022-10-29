import pygame
from pygame.locals import *
import time
import random

SIZE=40
BACKGROUND_COLOR=(61, 54, 135)
RACE_TIME=0.25

class Apple:
    def __init__(self,parent_screen):
        self.image=pygame.image.load("resources/apple1.jpg").convert()
        self.parent_screen=parent_screen
        self.x=SIZE*3
        self.y=SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image,(self.x,self.y))
        pygame.display.flip()

    def move(self):
        self.x=random.randint(1,24)*SIZE
        self.y=random.randint(1,14)*SIZE



class Snake:
    def __init__(self,parent_screen,length):
        self.length=length
        self.parent_screen=parent_screen
        self.block=pygame.image.load("resources/block_x.jpg").convert()
        self.x=[SIZE]*length
        self.y=[SIZE]*length
        self.direction="right"

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length+=1
        self.x.append(SIZE)
        self.y.append(SIZE)

    def move_left(self):
        self.direction="left"

    def move_right(self):
        self.direction="right"

    def move_up(self):
        self.direction="up"

    def move_down(self):
        self.direction="down"

    def walk(self):
        #moving the body
        for i in range(self.length-1,0,-1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]

        #moving the head
        if self.direction=="left":
            self.x[0]-=SIZE
        if self.direction=="right":
            self.x[0]+=SIZE
        if self.direction=="up":
            self.y[0]-=SIZE
        if self.direction=="down":
            self.y[0]+=SIZE

        self.draw()



class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Apple and Snake Game")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((1000,600))
        # self.surface.fill((61, 54, 135))
        self.snake=Snake(self.surface,1)
        self.snake.draw()
        self.apple=Apple(self.surface)
        self.apple.draw()

    def render_background(self):
        bg=pygame.image.load("resources/Grassy_background.jpg")
        self.surface.blit(bg,(0,0))

    def is_collision(self,x1,y1,x2,y2):
        if x1>=x2 and x1<x2+SIZE:
            if y1>=y2 and y1<y2+SIZE:
                return True
        return False

    def display_score(self):
        font=pygame.font.SysFont("arial",30)
        score=font.render(f"Score: {self.snake.length}",True,(255,255,255))
        self.surface.blit(score,(800,10))

    def play_background_music(self):
         pygame.mixer.music.load("resources/joy_music.mp3")
         pygame.mixer.music.play(-1,0)

    def play_sound(self,sound_name):
        sound = pygame.mixer.Sound(f"resources/{sound_name}.mp3")
        pygame.mixer.Sound.play(sound)

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        #snake collion with apple
        #for i in range(self.snake.length):
        #if self.is_collision(self.snake.x[i],self.snake.y[i],self.apple.x,self.apple.y)
        if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            global RACE_TIME
            if RACE_TIME>0.02:
                RACE_TIME=RACE_TIME-0.01
            self.apple.move()

        #snake collision with itself
        for i in range(1,self.snake.length):
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                self.play_sound("crash_buzzer")
                raise "Collision Occured"


        #snake colliding with boundaries of the window
        if not(0<=self.snake.x[0]<=1000 and 0<=self.snake.y[0]<600):
            self.play_sound('crash_buzzer')
            raise "hit boundaru error"

    def show_game_over(self):
        self.render_background()
        font=pygame.font.SysFont("arial",30)
        line1=font.render(f"Game is over: Your score is {self.snake.length}",True,(255,255,255))
        self.surface.blit(line1,(200,300))
        line2=font.render("To play again press Enter. To exit press Escape",True,(255,255,255))
        self.surface.blit(line2,(200,350))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        self.apple=Apple(self.surface)
        self.snake = Snake(self.surface, 1)
        global RACE_TIME
        RACE_TIME=0.25

    def run(self):
        running = True
        pause=False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:       #K_KEYDOWN means any key pressed on keyboard
                    if event.key == K_ESCAPE:   #K_ESCAPE is esc Key
                        running = False
                    if event.key==K_RETURN:     #K_RETURN means enter key is pressed
                        pause=False
                        pygame.mixer.music.unpause()

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause=True
                self.reset()

            time.sleep(RACE_TIME)



if __name__=="__main__":
    game=Game()
    game.run()