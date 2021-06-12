import pygame
from pygame.locals import *
import sys
import time
import random


# 750 x 500

class Game:

    def __init__(self):
        self.w = 750
        self.h = 500
        self.reset = True
        self.active = False
        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.accuracy = '0%'
        self.results = 'Time :0 Accuracy :0 % Wpm :0 '
        self.wpm = 0
        self.end = False
        self.HEAD_C = (255, 255, 255)
        self.TEXT_C = (255, 255, 204)
        self.RESULT_C = (255, 255, 51)

        pygame.init()
        self.open_img = pygame.image.load('home.jpg')
        self.open_img = pygame.transform.scale(self.open_img, (self.w, self.h))

        self.bg = pygame.image.load('bg.jpg')
        self.bg = pygame.transform.scale(self.bg, (900, 750))

        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Speed test')

    def draw_text(self, screen, msg, y, x, fsize, color):
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, 1, color)
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)
        pygame.display.update()

    def get_sentence(self):
        f = open('sentences1.txt').read()
        sentences = f.split('\n')
        sentence = random.choice(sentences)
        return sentence

    def show_results(self, screen):
        if (not self.end):
            # Calculate time
            self.total_time = time.time() - self.time_start

            # Calculate accuracy
            count = 0
            for i, c in enumerate(self.word):
                try:
                    if self.input_text[i] == c:
                        count += 1
                except:
                    pass
            self.accuracy = count / len(self.word) * 100

            # Calculate words per minute
            self.wpm = len(self.input_text) * 60 / (5 * self.total_time)
            self.end = True
            print(self.total_time)

            self.results = 'Time:' + str(round(self.total_time)) + " secs   Accuracy:" + str(
                round(self.accuracy)) + "%" + '   Wpm: ' + str(round(self.wpm))

            # draw icon image
            self.time_img = pygame.image.load('RESET.png')
            self.time_img = pygame.transform.scale(self.time_img, (170, 50))
            # screen.blit(self.time_img, (80,320))
            screen.blit(self.time_img, (self.w / 2 - 75, self.h - 140))
            self.draw_text(screen, "", self.h - 70, self.w / 2, 26, (100, 100, 100))

            print(self.results)
            pygame.display.update()

    def run(self):
        self.reset_game(self.screen)

        self.running = True
        while self.running:
            clock = pygame.time.Clock()
            self.screen.fill((0, 0, 0), (50, 250, 650, 50))
            pygame.draw.rect(self.screen, self.HEAD_C, (50, 250, 650, 50), 2)
            # update the text of user input
            self.draw_text(self.screen, self.input_text, 274, self.w / 2, 26, (0, 250, 255))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    # position of input box
                    if x >= 50 and x <= 650 and y >= 250 and y <= 300:
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time()
                        # position of reset box
                    if 300 <= x <= 470 and y >= 360 and y <= 410:
                        self.reset_game(self.screen)
                        x, y = pygame.mouse.get_pos()

                    if 130 <= y <= 160 and 240 <= x <= 260:
                        self.draw_text(self.screen, self.word, 200, self.w / 2, 28, self.TEXT_C)





                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            self.show_results(self.screen)
                            print(self.results)
                            self.draw_text(self.screen, self.results, 350, self.w / 2, 28, self.RESULT_C)
                            self.end = True

                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass

            pygame.display.update()

        clock.tick(60)

    def reset_game(self, screen):
        self.screen.blit(self.open_img, (0, 0))

        pygame.display.update()
        pygame.time.wait(1000)

        self.reset = False
        self.end = False

        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0

        x, y = pygame.mouse.get_pos()

        # Get random sentence
        self.word = self.get_sentence()
        if not self.word:
            self.reset_game(self.screen)
        # drawing heading
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        msg = "Type it Up!"
        self.draw_text(self.screen, msg, 80, self.w / 2, 80, self.HEAD_C)
        '''
        for event in pygame.event.get():
            if event.type==pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                if 130 <= y <= 160 and 240 <= x <= 260:
                    self.draw_text(self.screen, 'Sentence', 150, 240, 30, (0, 204, 0))
                else:
                    self.draw_text(self.screen, 'Sentence', 150, 240, 30, (255, 245, 224))
        '''

        sent = 'Sentence'
        self.draw_text(self.screen, sent, 150, 240, 30, (255, 245, 224))
        sent = 'Paragraph'
        self.draw_text(self.screen, sent, 150, self.w - 240, 30, (255, 245, 224))

        # draw the rectangle for input box
        pygame.draw.rect(self.screen, (0, 0, 0), (50, 250, 650, 50), 2)

        # draw the sentence string
        #self.draw_text(self.screen, self.word, 200, self.w / 2, 28, self.TEXT_C)

        pygame.display.update()


Game().run()
