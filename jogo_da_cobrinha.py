import pygame
import random
import cv2
import time

pygame.mixer.init()

pygame.mixer.music.load("sound/pontos.mp3")

class JogoSerpente:
    start = 0
    comiday = 0
    comidax = 0
    pontos = 0
    corB = random.randint(0, 255)
    corG = random.randint(0, 255)
    corR = random.randint(0, 255)
    over = False
    record = 0

    def __init__(self):
        with open('banco.txt', 'r') as arquivo:
            self.record = int(arquivo.read());

    def inc_pontos(self):
        self.pontos += 1
        pygame.mixer.music.play()

    def show_menu(self, frame):
        height, width, _ = frame.shape
        cv2.putText(frame, "Para iniciar tecle 's'", [int(width / 4), int(height / 4)], cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.putText(frame, "Para sair tecle 'q'", [int(width / 4), int(height / 2)], cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.putText(frame, f"RECORDE: {self.record}", [int(width / 4), int(height - 100)], cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        return frame
    
    def show_pontos(self, frame):
        height, width, _ = frame.shape
        cv2.putText(frame, "Game Over", [int(width / 4), int(height / 4)], cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
        cv2.putText(frame, f"Pontos: {self.pontos}", [int(width / 4), int(height / 2)], cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.putText(frame, "Voltar tecle 'b'", [int(width / 4), int(height - 100)], cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        return frame

    def is_over(self):
        return self.over
    
    def voltar_menu(self):
        self.over = False
        if (self.record < self.pontos):
            with open('banco.txt', 'w') as arquivo:
                arquivo.write(str(self.pontos))
            self.record = self.pontos
        self.pontos = 0

    def mostrar_comida(self, frame, x, y):
        cv2.rectangle(frame, (x, y), (x + 10, y + 10), (self.corB, self.corG, self.corR), -1)

    def gerar_comida(self, frame):
        self.corB = random.randint(0, 255)
        self.corG = random.randint(0, 255)
        self.corR = random.randint(0, 255)
        self.comiday = random.randint(50, frame.shape[0]- 150)
        self.comidax = random.randint(50, frame.shape[1] - 150)
        # cv2.rectangle(frame, (comidax, comiday), (comidax + 10, comiday + 10), (0, 255, 0), -1)
        return self.comidax, self.comiday

    def reset(self):
        self.start = 0
        self.over = True
    
    def set_start(self):
        self.start = time.time()

    def get_time(self):
        if self.start == 0:
            return 0
        return time.time() - self.start
    
    def show_time(self, frame):
        height, width, _ = frame.shape
        cv2.putText(frame, f"Pontos: {self.pontos}", [10, 50], cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.putText(frame, f"Tempo: {self.get_time():.2f}", [int(width - 300), 50], cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        return frame

