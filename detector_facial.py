import cv2
import numpy as np
import pygame
import random
import time
from jogo_da_cobrinha import JogoSerpente

class DetectorFacial:
    def __init__(self):
        self.jogo = JogoSerpente()
        #Iniciando a câmera
        self.cap = cv2.VideoCapture(0)
        #Carregando modelo de detecção facial pré-treinado
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def capturar_video(self):
        while True:
            #Capturar um frame da câmera 
            ret, frame = self.cap.read()
            if not ret:
                print("Erro ao capturar o frame.")
                break

            #Exibir o frame capturado em uma janela separada
            cv2.imshow('Video da Camera', frame)

            #Aguardar 1 milissegundo e verifica se q foi pressionada
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break            

    def detectar_face(self):
        #Chamar a função para capturar e exibir o vídeo
        ret, frame = self.cap.read()
        x, y = self.jogo.gerar_comida(frame)
        while True:
            ret, frame = self.cap.read()

            current_time = self.jogo.get_time() 

            if self.jogo.is_over():
                frame = self.jogo.show_pontos(frame)
            elif self.jogo.get_time() == 0:
                frame = self.jogo.show_menu(frame)
            elif current_time < 60:
                frame = self.jogo.show_time(frame)
                self.jogo.mostrar_comida(frame, x, y)
            else:
                self.jogo.reset()


            #Converter o frame para tons de cinza para a detecção
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #Detecta as faces na imagem
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor = 1.3, minNeighbors = 5)

            #Determinando retângulos ao redor do rosto detectado
            for(xf, yf, w, h) in faces:
                cv2.rectangle(frame, (xf + int(w/2),yf + int(h/2)), (xf+ int(w/4), yf + int(h/4)), (255, 0, 0), 2)
                if ((xf) < x and (yf) < y and (xf + w) > x and (y + h) > y) and self.jogo.get_time() != 0:
                    self.jogo.inc_pontos()
                    x, y = self.jogo.gerar_comida(frame)
                
            cv2.imshow('Video da Camera', frame)

            if cv2.waitKey(1) == ord('q'):
                self.liberar_camera() 
            if cv2.waitKey(2) == ord('s'):
                self.jogo.set_start()
            if cv2.waitKey(3) == ord('b'):
                self.jogo.voltar_menu()
                 

    def liberar_camera(self):
        # Libera a câmera
        self.cap.release()

