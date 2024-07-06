import os
import random
import re
import time
import urllib.request
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import requests
import shutil
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pygame
import textwrap

pygame.init()

WIDTH, HEIGHT = 1240, 1000  # Ширина и высота экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Тест по математике")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Шрифты
font_title = pygame.font.Font(None, 48)
font_question = pygame.font.Font(None, 32)
font_answer = pygame.font.Font(None, 24)

# Основной URL
base_url = "https://math-ege.sdamgia.ru"

# Настройка веб-драйвера Chrome с использованием webdriver_manager
options = Options()
options.add_argument("--headless")  # Запуск браузера в фоновом режиме
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Установка времени ожидания
driver.set_page_load_timeout(30)

# Папка для сохранения изображений
image_folder = "problem_images"

# Создаем папку для изображений, если ее нет
os.makedirs(image_folder, exist_ok=True)

# Функция для скачивания изображений
def download_image(url, folder):
    try:
        file_name = os.path.basename(url)
        file_path = os.path.join(folder, file_name)
        
        # Добавление заголовка User-Agent
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response, open(file_path, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print(f"Downloaded {url} to {file_path}")
        return file_path
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

# Функция для вывода данных на экран с учетом последовательности текста и изображений
def display_data(problem_num, url, task_content, solution_content, answer_text):
    print(f"Problem {problem_num} on {url} (Задача):")
    print(task_content)
    
    print(f"Problem {problem_num} on {url} (Решение):")
    print(solution_content)
    
    print(f"Problem {problem_num} on {url} (Ответ):")
    print(answer_text)
    print("-----------------------")

def delete_images(folder):
       try:
           for filename in os.listdir(folder):
               file_path = os.path.join(folder, filename)
               if os.path.isfile(file_path):
                   os.remove(file_path)
                   print(f"Deleted {filename}")
           print(f"All files deleted from {folder}")
       except Exception as e:
           print(f"Error deleting files: {e}")

# Удаление всех файлов из папки с изображениями перед началом работы
delete_images(image_folder)

# Переменные для теста
current_question = 0
user_answers = []
score = 0
running = True
input_text = ''  # Переменная для хранения текста ввода
show_answer = False
show_solution = False
questions = []
answers = []
solutions = []

# Переход на основную страницу
driver.get(base_url + "/?redir=1")

# Список для хранения URL задач
task_urls = []
# Переход по каждому data-topic-i от 0 до 11 и извлечение ссылок на задачи
for topic_i in range(12):  # от 0 до 11 включительно
    # Переход на страницу с соответствующим data-topic-i
    driver.get(f"{base_url}/?redir=1&data-topic-i={topic_i}")
    time.sleep(2)  # Ждем некоторое время для загрузки контента (можно настроить под вашу ситуацию)
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, "lxml")
    # Поиск всех меток с интересующими нас классами
    label_tags = soup.find_all('label', class_=['Link_wrap', 'ConstructorForm-TopicName', 'Label'])
    
    # Поиск нужных типов задания и извлечение их ссылок
    for label_tag in label_tags:
        input_tag = label_tag.find('input', {'class': 'Checkbox', 'data-topic-i': str(topic_i)})
        if input_tag:
            a_tag = label_tag.find('a')
            if a_tag and 'href' in a_tag.attrs:
                task_url = base_url + a_tag['href']
                task_urls.append(task_url)

# Выбираем случайные 5 задач без повторений
random_task_urls = random.sample(task_urls, k=min(5, len(task_urls)))

# Переход по каждой случайной ссылке и извлечение данных
questions = []
answers = []
solutions = []
for url in random_task_urls:
    driver.get(url)
    time.sleep(2)  # Ждем некоторое время для загрузки контента (можно настроить под вашу ситуацию)
    
    # Ожидание до тех пор, пока не загрузятся необходимые элементы задачи
    try:
        task_elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'task_problem_text'))
        )
    except TimeoutException:
        print(f"Не удалось загрузить элементы задачи по URL: {url}")
        continue  # Переход к следующей задаче

    # Извлекаем текст условия задачи
    task_content = ''
    for element in task_elements:
        task_content += element.text.strip() + ' '

    # Останавливаем добавление текста, если встретили слово "Решение"
    if "Решение" in task_content:
        task_content = task_content.split("Решение")[0].strip()  # Берем часть до слова "Решение"

    # Создаем список для хранения изображений и их координат
    task_images = []

    # Добавляем изображения в текст задачи
    task_images_elements = driver.find_elements(By.XPATH, "//div[@class='task_problem_text']//img")
    for image_element in task_images_elements:
        img_src = image_element.get_attribute("src")
        if img_src.startswith('/'):
            img_src = base_url + img_src
        img_filename = os.path.basename(img_src)
        img_path = os.path.join(image_folder, img_filename)
        if not os.path.exists(img_path):
            try:
                response = requests.get(img_src, stream=True)
                with open(img_path, 'wb') as out_file:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, out_file)
                # Добавляем изображение в список
                task_images.append((img_path, image_element.location['x'], image_element.location['y']))
            except Exception as e:
                print(f"Ошибка при загрузке изображения: {e}")
        
        # Поиск абзаца с ответом в разделе "Решение"
        answer_paragraph = solution_parts.find(lambda tag: tag.name == 'p' and "Ответ" in tag.get_text())
        if answer_paragraph:
            answer_text = answer_paragraph.get_text(separator=' ', strip=True)
            # Удаление префикса "Ответ: " из текста "Ответа"
            answer_text = re.sub(r'^Ответ:\s*', '', answer_text)
        else:
            answer_text = ""

    # Извлекаем текст решения и добавляем изображения
    try:
        solution_elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'task_solution_text'))
        )
    except TimeoutException:
        print(f"Не удалось загрузить элементы решения по URL: {url}")
        continue  # Переход к следующей задаче

    solution_content = ''
    for element in solution_elements:
        solution_content += element.text.strip() + ' '

    # Проверяем, есть ли слово "Решение" в тексте решения
    if "Решение" in solution_content:
        # Разделяем текст решения на две части по слову "Решение"
        solution_parts = solution_content.split("Решение")
        # Берем вторую часть (решение)
        solution_content = solution_parts[1].strip()

    # Добавление задачи, решения и ответа в списки
    questions.append(task_content.strip())
    solutions.append(solution_content.strip())
    answers.append(answer_text.strip())

# Закрытие веб-драйвера
driver.quit()

# Основной цикл игры
if len(questions) > 0:  # Проверяем, есть ли задачи
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Проверка ответа
                    if current_question < len(questions):
                        user_answers.append(input_text)
                        current_question += 1
                        input_text = ''
                        show_answer = True
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode  # Добавление символа к строке input_text (строке)

        # Отрисовка экрана
        screen.fill(WHITE)

        # Заголовок
        title_text = font_title.render("Тест по математике", True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))

        # Отображение текущего вопроса
        if current_question < len(questions):
            question_text = questions[current_question]  # Получаем текст вопроса
            
            # Разбиваем текст на строки с учетом ширины экрана
            wrapped_text = textwrap.wrap(question_text, width=WIDTH // 2 - 50)  # 50 - отступ от краёв

            # Вычисляем высоту текста задачи
            y_offset = 100  # Вертикальный отступ от верха экрана
            text_height = 0
            for line in wrapped_text:
                text_surface = font_question.render(line, True, BLACK)
                text_height += text_surface.get_height() + 5  # Добавляем отступ между строками

            # Отрисовываем каждую строку с отступом
            y_offset = 100  # Вертикальный отступ от верха экрана
            for line in wrapped_text:
                text_surface = font_question.render(line, True, BLACK)
                screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, y_offset))
                y_offset += text_surface.get_height() + 5  # Добавляем отступ между строками

            # Корректируем положение поля для ввода ответа
            input_box = pygame.Rect(WIDTH // 2 - 150, 200 + text_height, 300, 50) 
            pygame.draw.rect(screen, GRAY, input_box, 2)

            # Отображение введенного текста
            text_surface = font_answer.render(input_text, True, BLACK)  # Отрисовка текста
            screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

            # Подсказка для ввода ответа
            prompt_text = font_answer.render("Введите ответ...", True, GRAY)
            screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, 260))

        # Отображение результатов
        else:
            # Отображение результата
            result_text = font_title.render(f"Ваш результат: {score}/{len(questions)}", True, BLACK)
            screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, 400))

        # Отображение правильного ответа и решения
        if show_answer:
            if current_question < len(questions):
                answer_text = font_answer.render(f"Правильный ответ: {answers[current_question - 1]}", True, BLACK)
                screen.blit(answer_text, (WIDTH // 2 - answer_text.get_width() // 2, 300))
            
            # Проверка ответа
            if current_question < len(questions) and user_answers[-1].strip() == answers[current_question - 1].strip():
                score += 1

            if show_solution:
                solution_text = font_answer.render(f"Решение: {solutions[current_question - 1]}", True, BLACK)
                screen.blit(solution_text, (WIDTH // 2 - solution_text.get_width() // 2, 350))
        
        # Кнопка "Показать решение"
        button_solution = pygame.Rect(WIDTH // 2 - 100, 450, 200, 50)
        pygame.draw.rect(screen, GRAY, button_solution, 2)
        solution_text = font_answer.render("Показать решение", True, BLACK)
        screen.blit(solution_text, (button_solution.x + 5, button_solution.y + 5))
        
        # Обработка нажатия на кнопку "Показать решение"
        mouse = pygame.mouse.get_pos()
        if button_solution.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            show_solution = True

        # Кнопка "Следующая задача"
        button_next = pygame.Rect(WIDTH // 2 - 100, 510, 200, 50)
        pygame.draw.rect(screen, GRAY, button_next, 2)
        next_text = font_answer.render("Следующая задача", True, BLACK)
        screen.blit(next_text, (button_next.x + 5, button_next.y + 5))
        # Обработка нажатия на кнопку "Следующая задача"
        if button_next.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            show_answer = False
            show_solution = False
            if current_question < len(questions):
                current_question += 1
        
        pygame.display.flip()
        pygame.time.Clock().tick(30)

else:
    print("Не удалось получить список заданий!")

pygame.quit()