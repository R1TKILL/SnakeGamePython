import pygame

from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

music_defeats = pygame.mixer.Sound('defeat.wav')
music_points = pygame.mixer.Sound('points.wav')

def startGame():
    largura = 640
    altura = 480

    #Para o movimento definido.
    velocidade = 3
    x_control = velocidade
    y_control = 0

    x_cobra = int(largura/2)
    y_cobra = int(altura/2)
    x_maca = randint(40,600)
    y_maca = randint(50, 430)

    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Colisões")
    relogio = pygame.time.Clock()

    # Lista que vai armazenar as posiçõoes que a cobra já passou, tem que ficar fora para não ser redefinida no loop.
    lista_corpo = []
    comprimento_inicial = 7

    textFormat = pygame.font.SysFont('arial', 40, True, True)
    textFormat2 = pygame.font.SysFont('calibri', 70, True, True)
    textFormat3 = pygame.font.SysFont('calibri', 20, True, True)

    defeat = False
    pontos = 0

    def draw_snake(corpo_cobra):
        #Toda vez que comer a maçã essa função desenha um corpo para cobra.
        for xy in corpo_cobra:
            pygame.draw.rect(tela,(0,155,0), (xy[0], xy[1], 30, 30))


    while True:
        relogio.tick(60)
        tela.fill((255,255,255))

        labelPontos = f"Pontos: {pontos}"
        formatacao = textFormat.render(labelPontos, True, (0,0,0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            # Movimento só para os lados e não diagonais.
            if event.type == KEYDOWN:
                #Para evitar de estar indo para direita e voltar derrepente para esqueda.
                if event.key == K_a:
                    if x_control == velocidade:
                        pass
                    else:
                        x_control = -velocidade
                        y_control = 0
                if event.key == K_d:
                    if x_control == -velocidade:
                        pass
                    else:
                        x_control = velocidade
                        y_control = 0
                if event.key == K_w:
                    if y_control == velocidade:
                        pass
                    else:
                        y_control = -velocidade
                        x_control = 0
                if event.key == K_s:
                    if y_control == -velocidade:
                        pass
                    else:
                        y_control = velocidade
                        x_control = 0

        x_cobra += x_control
        y_cobra += y_control

        draw_snake(lista_corpo)

        cobra = pygame.draw.rect(tela,(0,255,0),(x_cobra,y_cobra,30,30))
        maca = pygame.draw.rect(tela, (255, 0, 0), (x_maca, y_maca, 30, 30))

        #Lista que vai armazenar as posiçãoes atuais da cabeça da cobra.
        lista_cabeca = []
        lista_cabeca.append(x_cobra)
        lista_cabeca.append(y_cobra)

        lista_corpo.append(lista_cabeca)

        #Se houver mais de uma posição da cabeça no corpo, a cobra encostou em sí mesma.
        if lista_corpo.count(lista_cabeca) > 1 or defeat == True:
            defeat = True
            while defeat:
                tela.fill((255,255,255))
                music_defeats.play()
                music_defeats.set_volume(0.3)
                labelDefeat = "Game Over"
                formatacaoDefeat = textFormat2.render(labelDefeat, True, (255,0,0))
                tela.blit(formatacaoDefeat, (140, 150))

                labelReset = "Pressione R para continuar..."
                formatacaoReset = textFormat3.render(labelReset, True, (0,0,0))
                tela.blit(formatacaoReset, (190, 250))

                for event in pygame.event.get():

                    if event.type == QUIT:
                        music_defeats.stop()
                        pygame.quit()
                        exit()

                    if event.type == KEYDOWN:
                        if event.key == K_r:
                            music_defeats.stop()
                            startGame()
                pygame.display.update()


        #Para a cobra não crescer indefinidamente, apaga a ultima posição..
        if len(lista_corpo) > comprimento_inicial:
            del lista_corpo[0]

        #Se a cobra colidir com a maçã
        if cobra.colliderect(maca):
            x_maca = randint(40, 600)
            y_maca = randint(50, 430)
            pontos += 1
            comprimento_inicial+=1
            music_points.play()
            velocidade+=0.05

        #Para não sair da tela.
        if x_cobra < 0:
            x_cobra = 0
            defeat = True
        if x_cobra > 610:
            x_cobra = 610
            defeat = True
        if y_cobra < 0:
            y_cobra = 0
            defeat = True
        if y_cobra > 450:
            y_cobra = 450
            defeat = True

        #Fica por cima se aplicado depois
        tela.blit(formatacao, (400,40))
        pygame.display.update()

startGame()