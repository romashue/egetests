import pygame
import sys
from PIL import Image, ImageSequence
import time
from buttons import ImageButton

#Инициализация pygame
pygame.init()

#Параметры экрана
WIDTH, HEIGHT = 1240, 950
MAX_FPS = 60

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Обучалочка от Матти")
main_background = pygame.image.load("images/background.png")
timer_background = pygame.image.load("images/timer_background.png")
FONT = pygame.font.Font("fonts/ArialRoundedMTBold.ttf", 120)
timer_text = FONT.render("40:00", True, "white")
timer_text_rect = timer_text.get_rect(center=(WIDTH/2, HEIGHT/2-25))
clock = pygame.time.Clock()

#Загрузка и установка курсора
cursor = pygame.image.load("images/mouse.png")
pygame.mouse.set_visible(False) #Скрываем стандартный курсор

def start_menu():
    # Загрузка GIF-файлов
    gif_image1 = Image.open("images/gif1.gif")
    frames1 = []
    for frame in ImageSequence.Iterator(gif_image1):
        frames1.append(pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode))

    gif_image2 = Image.open("images/gif2.gif")
    frames2 = []
    for frame in ImageSequence.Iterator(gif_image2):
        frames2.append(pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode))


    # Счетчики кадров
    current_frame1 = 0
    current_frame2 = 0

    # Создание кнопки с книжкой
    book_button = ImageButton((WIDTH-100)-(100/2),40,100,100,"","images/menu_image.png","images/menu_image_hover.png","sounds/click.mp3")

    running = True
    while running:

        screen.fill((0, 0, 0))  # Очистка экрана 
        # Отображение кадров
        screen.blit(frames1[current_frame1], (0, 0))
        screen.blit(frames2[current_frame2], (0, 0))

        # Обновление счетчиков кадров
        current_frame1 = (current_frame1 + 1) % len(frames1)
        current_frame2 = (current_frame2 + 1) % len(frames2)

        if current_frame1 == 0:
            current_frame1 = 1
        if current_frame2 == 0:
            current_frame2 = 1

        pygame.time.delay(80)

        # Получение позиции мыши
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running == False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == book_button:
                print("Кнопка 'Книжка' была нажата!")
                fade()
                main_menu()

            for btn in [book_button]:
                btn.handle_event(event)
        
        for btn in [book_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        #Отображение курсора в текущей позиции мыши
        screen.blit(cursor,(mouse_x, mouse_y))

        pygame.display.flip()

def main_menu():
    #Создание кнопок
    start_button = ImageButton(WIDTH/4-(452/2),150,452,74,"Самостоятельное обучение","images/button.png","images/button_hover.png","sounds/click.mp3")
    material_button = ImageButton(WIDTH/4-(452/2),250,452,74,"Материалы","images/button.png","images/button_hover.png","sounds/click.mp3")
    test_button = ImageButton(WIDTH/4-(452/2),350,452,74,"Тесты","images/button.png","images/button_hover.png","sounds/click.mp3")
    exit_button = ImageButton(WIDTH/4-(452/2),450,452,74,"Выход","images/button.png","images/button_hover.png","sounds/click.mp3")

    running = True
    while running:
        screen.fill((0,0,0))
        screen.blit(main_background,(-165,-65))

        font = pygame.font.Font(None,72)
        text_surface = font.render("ОБУЧАЛОЧКА ОТ МАТТИ",True,(255,255,255))
        text_rect = text_surface.get_rect(center=(WIDTH/4,100))
        screen.blit(text_surface,text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running == False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == start_button:
                print("Кнопка 'Самостоятельное обучение' была нажата!")
                fade()
                timer()

            if event.type == pygame.USEREVENT and event.button == material_button:
                print("Кнопка 'Материалы' была нажата!")
                fade()
                materials_menu()

            if event.type == pygame.USEREVENT and event.button == exit_button:
                running = False
                pygame.quit()
                sys.exit()

            for btn in [start_button,material_button, test_button,exit_button]:
                btn.handle_event(event)
        
        for btn in [start_button,material_button, test_button,exit_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        #Отображение курсора в текущей позиции мыши
        x, y = pygame.mouse.get_pos()
        screen.blit(cursor,(x, y))
            

        pygame.display.flip()

def materials_menu():
    #Создание кнопок
    matan_button = ImageButton(WIDTH/2-(452/2),150,452,74,"Матан","images/button.png","images/button_hover.png","sounds/click.mp3")
    info_button = ImageButton(WIDTH/2-(452/2),250,452,74,"Инфа","images/button.png","images/button_hover.png","sounds/click.mp3")
    back_button = ImageButton(WIDTH/2-(452/2),350,452,74,"Назад","images/button.png","images/button_hover.png","sounds/click.mp3")

    running = True
    while running:
        screen.fill((0,0,0))
        screen.blit(main_background,(0,0))

        font = pygame.font.Font(None,72)
        text_surface = font.render("МАТЕРИАЛЫ",True,(255,255,255))
        text_rect = text_surface.get_rect(center=(WIDTH/2,100))
        screen.blit(text_surface,text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running == False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                #Возврат в меню
                if event.key == pygame.K_ESCAPE:
                    fade()
                    running = False

            if event.type == pygame.USEREVENT and event.button == back_button:
                fade()
                running = False

            for btn in [matan_button,info_button,back_button]:
                btn.handle_event(event)

        for btn in [matan_button,info_button,back_button]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(screen) 

        #Отображение курсора в текущей позиции мыши
        x, y = pygame.mouse.get_pos()
        screen.blit(cursor,(x, y))

        pygame.display.flip()

    

def timer():
    
    input_time = ""
    timer_started = False
    start_time = 0

    start_stop_button = ImageButton(WIDTH/4-(452/2),HEIGHT*3/4,452,74,"Старт","images/button.png","images/button_hover.png","sounds/click.mp3")
    back_button = ImageButton(3*WIDTH/4-(452/2),HEIGHT*3/4,452,74,"Назад","images/button.png","images/button_hover.png","sounds/click.mp3")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running == False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                #Возврат в меню
                if event.key == pygame.K_ESCAPE:
                    fade()
                    running = False

            if event.type == pygame.USEREVENT and event.button == back_button:
                fade()
                running = False

            if event.type == pygame.USEREVENT and event.button == start_stop_button:
                ftimer_started = not timer_started  # Переключение состояния таймера

            for btn in [start_stop_button,back_button]:
                btn.handle_event(event)

            # Обработка нажатий клавиш
            if event.type == pygame.KEYDOWN or (event.type == pygame.USEREVENT and event.button == start_stop_button):
                if event.key == pygame.K_RETURN or (event.type == pygame.USEREVENT and event.button == start_stop_button):
                    # Нажата Enter - обрабатываем ввод
                    if input_time:
                        minutes = int(input_time[:2])  # Первые две цифры - минуты
                        seconds = int(input_time[2:])  # Последние две цифры - секунды
                        total_seconds = minutes * 60 + seconds
                        timer_started = True
                        start_time = time.time() + total_seconds  #  Запоминаем момент окончания таймера
                    input_time = "" 
                elif event.key == pygame.K_BACKSPACE:
                    # Backspace - удаляем последний символ
                    input_time = input_time[:-1]
                elif event.unicode.isdigit():
                    # Ввод цифры - добавляем ее к строке
                    input_time += event.unicode

        # Очистка экрана
        screen.fill((0, 0, 0))

        # Отображение фона
        screen.blit(timer_background, (0, 0))


        # Отображение введенного времени
        font = pygame.font.Font(None, 200)  #  Шрифт 
        text = font.render(input_time, True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Центрируем по горизонтали и выше таймера
        screen.blit(text, text_rect)

        if timer_started:
            remaining_time = start_time - time.time()
            if remaining_time <= 0:
                timer_started = False  # Таймер закончился
                #  Добавьте здесь действия при окончании таймера (звуковой сигнал, анимация и т. д.)
            else:
                minutes = int(remaining_time // 60)
                seconds = int(remaining_time % 60)
                timer_text = f"{minutes:02}:{seconds:02}"
                timer_font = pygame.font.Font(None, 200)  # Шрифт
                timer_surface = timer_font.render(timer_text, True, (255, 255, 255))
                timer_rect = timer_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Центрируем по центру экрана
                screen.blit(timer_surface, timer_rect)

        for btn in [start_stop_button,back_button]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(screen)  

        #Отображение курсора в текущей позиции мыши
        x, y = pygame.mouse.get_pos()
        screen.blit(cursor,(x, y))

        # Обновление экрана
        pygame.display.flip()

def fade():
    running = True
    fade_alpha = 0 #Уровень прозрачности для анимации

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #Анимация затухания текущего экрана
        fade_surface = pygame.Surface((WIDTH,HEIGHT))
        fade_surface.fill((0,0,0))
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface,(0,0))

        #Увеличение уровня прозрачности
        fade_alpha += 5
        if fade_alpha >= 105:
            fade_alpha = 255
            running = False

        pygame.display.flip()
        clock.tick(MAX_FPS) #Ограничение FPS

if __name__ == "__main__":
    start_menu()