import pygame
from random import randint
pygame.init()

W, H = 800, 700
FPS = 60
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

pygame.display.set_caption('Flappy Bird')
pygame.display.set_icon(pygame.image.load('images/Fluppy Bird.png'))

font1 = pygame.font.Font(None, 35)
font2 = pygame.font.Font(None, 80)

fon = pygame.image.load('images/Fluppy font.png')
truba = pygame.image.load('images/Pipe.png')
truba2 = pygame.image.load('images/Pipe2.png')
Bird = pygame.image.load('images/Bird.png')

pygame.mixer.music.load('sounds/veselaya-muz-rf43432.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

soundFall = pygame.mixer.Sound('sounds/spongebob-fail.wav')
pygame.mixer.music.set_volume(0.1)
py, s, a = H // 2, 0, 0
character = pygame.Rect(W // 3, py, 75, 65)
frame = 0
state = 'start'
time = 10
pipes = []
fon2 = []
pipeScores = []
pipeSpeed = 3
pipeGateSize = 200
pipeGatePos = H // 2
fon2.append(pygame.Rect(0, 0, 1000, 704))
lives = 3
scores = 0
p = True
while p:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            p = False
    press = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    click = press[0] or keys[pygame.K_SPACE]

    if time:
        time -= 1

    frame = (frame + 0.2) % 4

    for i in range(len(fon2)-1, -1, -1):
        bg = fon2[i]
        bg.x -= pipeSpeed // 2

        if bg.right < 0:
            fon2.remove(bg)

        if fon2[len(fon2)-1].right <= W:
            fon2.append(pygame.Rect(fon2[len(fon2)-1].right, 0, 1000, 704))
    for i in range(len(pipes)-1, -1, -1):
        pipe = pipes[i]
        pipe.x -= pipeSpeed

        if pipe.right < 0:
            pipes.remove(pipe)
            if pipe in pipeScores:
                 pipeScores.remove(pipe)
    if state == 'start':
        if click and not time and not len(pipes):
            state = 'play'

        py += (H // 2 - py) * 0.1
        character.y = py
    elif state == 'play':
        if click: a = -2
        else: a = 0
        py += s
        s = (s + a + 1) * 0.98
        character.y = py

        if not len(pipes) or pipes[len(pipes)-1].x < W - 200:
            pipes.append(pygame.Rect(W, 0, 52, pipeGatePos - pipeGateSize // 2))
            pipes.append(pygame.Rect(W, pipeGatePos + pipeGateSize // 2, 52, H - pipeGatePos + pipeGateSize // 2))

            pipeGatePos += randint(-100, 100)
            if pipeGatePos < pipeGateSize:
                pipeGatePos = pipeGateSize
            elif pipeGatePos > H - pipeGateSize:
                pipeGatePos = H - pipeGateSize

        if character.top < 0 or character.bottom > H:
            state = 'fall'

        for pipe in pipes:
            if character.colliderect(pipe):
                state = 'fall'
            if pipe.right < character.left and pipe not in pipeScores:
                pipeScores.append(pipe)
                scores += 5
                pipeSpeed = 3 + scores // 100
    elif state == 'fall':
        soundFall.play()
        s, a = 0, 0
        pipeGatePos = H // 2


        lives -= 1
        if lives:
            state = 'start'
            time = 60
        else:
            state = 'game over'
            time = 180

    else:
        py += s
        s = (s + a + 1) * 0.98
        character.y = py

        if not time:
           p == False

    for bg in fon2:
        screen.blit(fon, bg)
    for pipe in pipes:
        if not pipe.y:
            rect = truba.get_rect(bottomleft = pipe.bottomleft)
            screen.blit(truba, rect)
        else:
            rect = truba2.get_rect(topleft = pipe.topleft)
            screen.blit(truba2, rect)


    image = pygame.transform.rotate(Bird, -s * 2)
    screen.blit(image, character)

    text = font1.render('Scores: ' + str(scores), 1, pygame.Color('white'))
    screen.blit(text, (10, 10))

    text = font1.render('Lives: ' + str(lives), 1, pygame.Color('white'))
    screen.blit(text, (10, H - 30))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()