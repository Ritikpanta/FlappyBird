#Thank you clear code
import random
from pip import main #To generate random numbers and stuff
import pygame
from pygame.locals import * #pygame imports
import sys #To stop game when cross or sth to stop game is clicked (sys.exit to exit the game)
from PIL import Image

#Resizing the Sprite images for the game

#Resizing background image
image = Image.open('images/background.png')
new = image.resize((800,400))
new.save("recreated_image/NewBackground.png")

#resizing Bird image
image = Image.open('Images/midflap.png')
new = image.resize((30,25))
new.save("recreated_image/NewMidflap.png")

image = Image.open('Images/downflap.png')
new = image.resize((30,25))
new.save("recreated_image/NewDownflap.png")

image = Image.open('Images/upflap.png')
new = image.resize((30,25))
new.save("recreated_image/NewUpflap.png")

#Resizing home image
image = Image.open('images/Home.png')
new = image.resize((500,100))
new.save("recreated_image/NewHome.png")

#Rezining pipe image
image = Image.open('images/pipe.png')
new = image.resize((70,330))
new.save('recreated_image/NewPipe.png')


image = Image.open("Images/base.png")
new = image.resize((800,80))
new.save('recreated_image/NewBase.png')


#Initializing pygame 
pygame.init()

#Sounds
Flap_sound =pygame.mixer.Sound('sound/wing.wav')
Die_sound =pygame.mixer.Sound('sound/die.wav')
hit_sound = pygame.mixer.Sound('sound/hit.wav')
swooshing_sound = pygame.mixer.Sound('sound/swooshing.wav')
point_sound = pygame.mixer.Sound('sound/point.wav')

#Variables in games
X = 0
FPS = 120
floorx = 0
ScreenWidth = 800
ScreenHeight = 400
SpeedOfFloor = 1.5

PipeHeight = [190,200,220,250,230]
#Game variables 
gravity = 0.2
player_movement = 0 
Game_Active = True #for game restart
PipeList = []
clock = pygame.time.Clock() 
index = 0

#for scores
Font = pygame.font.Font('font/FlappyBirdy.ttf',20)
Score = 0
high_score = 0
scoresound = 100

#Setting screen for the game
Screen = pygame.display.set_mode((800,400))
background = pygame.image.load('recreated_image/NewBackground.png').convert() 
base = pygame.image.load('recreated_image/NewBase.png')
home = pygame.image.load('recreated_image/NewHome.png').convert_alpha()


player_up = pygame.image.load('recreated_image/NewUpFlap.png').convert_alpha()
player_mid = pygame.image.load('recreated_image/NewMidflap.png').convert_alpha()
player_down = pygame.image.load('recreated_image/NewDownFlap.png').convert_alpha()
player_list = [player_up,player_mid,player_down]
player = player_list[index]
player_rect = player.get_rect(center=(400,200))
UpPipe = pygame.image.load('recreated_image/NewPipe.png')
BirdFlap = pygame.USEREVENT + 1 
pygame.time.set_timer(BirdFlap,150)
ComingPipe = pygame.USEREVENT
#Creating timer
pygame.time.set_timer(ComingPipe,1200)

#for fixin sound 
pygame.mixer.pre_init(frequency = 44100, size = 12, channels = 1, buffer = 256 )


def NewPipe():
    randompipe = random.choice(PipeHeight)
    Up_pipe = UpPipe.get_rect(midtop = (850,randompipe))
    top_pipe = UpPipe.get_rect(midbottom = (850,randompipe-130))
    return Up_pipe , top_pipe
    


def MovePipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 2  #To move -5 component to the left
    return pipes

def DrawPipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 400:
            Screen.blit(UpPipe,pipe)
        else:
            down_pipe = pygame.transform.flip(UpPipe,False,True)
            Screen.blit(down_pipe,pipe)

#for making extra floor 
def NewFloor():
    Screen.blit(base,(floorx,340))
    Screen.blit(base,(floorx+800,340))

def Collision(pipes):  #for collision between bird and traps and others
    for pipe in pipes:
        if player_rect.colliderect(pipe):
            hit_sound.play()
            return False
            
    if player_rect.top <= -50 or player_rect.bottom >= 340:
        Die_sound.play()
        return False
    return True
    

def rotate_player(player):   #for the look of the bird
    rotation = pygame.transform.rotozoom(player, -player_movement * 2.5,1 )
    return rotation

def Player_animation():
    frames = player_list[index]
    new_player_rect = frames.get_rect(center = (100,player_rect.centery))
    return frames,new_player_rect

def score(compare):
    if compare == 'main game':
        score_display = Font.render((f'Score : {int(Score)}'),True,(255,255,255))
        score_rect = score_display.get_rect(center= (400,30))
        Screen.blit(score_display,score_rect)
    else: 
        score_display = Font.render((f'Score : {int(Score)}'),True,(255,255,255))
        score_rect = score_display.get_rect(center= (400,30))
        Screen.blit(score_display,score_rect)

        Highscore_display = Font.render((f'High Score : {int(high_score)}'),True,(0,0,0))
        Highscore_rect = score_display.get_rect(center= (385,320))
        Screen.blit(Highscore_display,Highscore_rect)

def Score_change(Score , high_score):
    if Score > high_score:
        high_score = Score
    return high_score

while True:
        for event in pygame.event.get(): #Talks about the event running in the code
            if event.type == pygame.QUIT:
                pygame.quit() #Quit the screen note: this doesn't end full program so we have sys
                sys.exit()   #End the system i.e full program
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE or event.key == pygame.K_RIGHT and Game_Active:
                    player_movement = 0
                    player_movement -= 5
                    Flap_sound.play()

                if event.key == K_UP or event.key == pygame.K_SPACE and Game_Active == False:
                    swooshing_sound.play()
                    Game_Active = True
                    PipeList.clear()
                    player_rect.center = (100,170)
                    Score = 0

            if event.type == ComingPipe:
                PipeList.extend(NewPipe())
                
            if event.type == BirdFlap:
                if index < 2:
                    index += 1
                else:
                    index = 0
                
                player,player_rect = Player_animation()

        #background
        Screen.blit(background,(0,0))

        #collision
        
        
        if Game_Active:
            #Player/Bird 
            rotated_player = rotate_player(player)
            player_movement += gravity
            player_rect.centery += player_movement
            Screen.blit(rotated_player,player_rect)
            Game_Active = Collision(PipeList)
            
            #Pipes
            PipeList = MovePipe(PipeList)
            DrawPipes(PipeList)
            Score += 0.01
            score('main game')
            scoresound -= 1
            if scoresound <= 0:
                point_sound.play()
                scoresound = 100
            
        else:
            high_score = Score_change(Score,high_score)
            Screen.blit(home,(150,118))
            score('game over')


        
        #Base image
        floorx -= SpeedOfFloor
        NewFloor()
        if floorx <= -800:
            floorx = 0

        #Screen Name
        pygame.display.set_caption("Flappy Bird by Ritik")     
        pygame.display.update() #Display the things in the loop
        clock.tick(FPS)  #Game frames per sec






