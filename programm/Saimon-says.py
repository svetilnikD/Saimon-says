import os
import tkinter as tk
import random
import time
import logging 

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #Получаем расположение папки с игрой
LOG_FILE = os.path.join(BASE_DIR, "log.txt") #Путь к файлу логов


with open(LOG_FILE, "a", encoding="utf-8"): #Создаём файл логов, если его нет
    pass #Файл создан, ничего не делаем


logging.basicConfig( #Настройка логирования
    filename=LOG_FILE,
    level=logging.INFO, #Уровень логов — INFO (обычные события).
    format="%(asctime)s - %(message)s", #Формат логов: время - сообщение.
    encoding="utf-8" #Указываем кодировку для логов
)
#Глобальеые переменные
sequence = [] #Последовательность цветов
user_sequence = [] #Последовательность, которую вводит пользователь
level = 0 #Счетчик уровней
player_name = "" #Ник
selected_colors = [] #Цвета, которые будут использоваться в игре в зависимости от сложности

ALL_COLORS = ["red", "blue", "green", "yellow", "purple", "orange"] #Все цвета, которые могут быть в игре

# Менюшка
def start_menu(): 
    global root, name_entry, difficulty, label_diff #Переменные элементов меню, которые нужно будет использовать в других функциях

    root = tk.Tk() #Создаём главное окно
    root.title("Simon Says") #Заголовок окна
    root.geometry("400x650") #Размер окна
    root.configure(bg="#1f2a30") #Цвет фона

    difficulty = tk.StringVar(value="Легко") #Переменная для выбранной сложности 

    # Заголовок
    tk.Label(root, text="Simon says", #Текст, который будет отображаться
             font=("Arial", 24), #Шрифт и размер текста
             fg="white", bg="#1f2a30").pack(pady=20) #Цвет текста, цвет фона и отступы

    #Надпись
    tk.Label(root, text="Введите имя",
             font=("Arial", 12),
             fg="gray", bg="#1f2a30").pack()
    
    #Текстбокс для ввода имени
    name_entry = tk.Entry(root, font=("Arial", 14), justify="center")
    name_entry.pack(pady=10, ipadx=50, ipady=8)

    #Надпись для выбора сложности
    tk.Label(root, text="Сложность",
             font=("Arial", 12),
             fg="gray", bg="#1f2a30").pack(pady=10)

    frame_diff = tk.Frame(root, bg="#1f2a30") #Создаём фрейм для кнопок выбора сложности, чтобы они были в одной строке
    frame_diff.pack() #Размещаем фрейм в окне
    #Установки сложности и обновление надписи
    def set_difficulty(level_name): 
        difficulty.set(level_name)
        label_diff.config(text=f"Сложность: {level_name}")

  
    tk.Button(frame_diff, bg="#4CAF6A", width=8, height=2, #Легко
              command=lambda: set_difficulty("Легко")).pack(side=tk.LEFT, padx=10)

    tk.Button(frame_diff, bg="#F4B942", width=8, height=2,#Средне
              command=lambda: set_difficulty("Средне")).pack(side=tk.LEFT, padx=10)

    tk.Button(frame_diff, bg="#E03A3E", width=8, height=2, #Сложно
              command=lambda: set_difficulty("Сложно")).pack(side=tk.LEFT, padx=10)

    label_diff = tk.Label(root, text="Сложность: Легко", #Выбранная сложность
                          fg="white", bg="#1f2a30")
    label_diff.pack(pady=5)

   #Старт
    def start_game():
        global player_name, selected_colors

        player_name = name_entry.get()

        diff = difficulty.get()
        #Проверка сложности
        if diff == "Легко":
            selected_colors = ALL_COLORS[:3]
        elif diff == "Средне":
            selected_colors = ALL_COLORS[:4]
        else:
            selected_colors = ALL_COLORS[:6]

        logging.info(f"Игрок {player_name}, сложность: {diff}") #Логируем имя игрока и выбранную сложность

        root.destroy()
        game_window()

    def show_rules(): #Показать правила игры
        rules_win = tk.Toplevel() #Создаём новое окно поверх главного
        rules_win.title("Правила") #Заголовок окна с правилами
        rules_win.configure(bg="#1f2a30") #Цвет фона окна с правилами
        logging.info(f"Пользователь  открыл правила") #Логируем открытие правил
        tk.Label(rules_win, text=""" 
Повторяйте последовательность цветов.
Каждый уровень добавляется новый цвет.
Ошибка — проигрыш.
""", font=("Arial", 12), fg="white", bg="#1f2a30").pack(padx=20, pady=20) #Текст с правилами, шрифт, цвет текста, цвет фона и отступы

    def exit_app(): #Выход из приложения
        root.quit() 

    def styled_button(text, command): #Функция для создания стилизованных кнопок
        return tk.Button(root,
                         text=text,
                         command=command,
                         font=("Arial", 14),
                         bg="#1976D2",
                         fg="white",
                         activebackground="#1565C0",
                         relief="flat",
                         width=25,
                         height=2)

    styled_button("Играть", start_game).pack(pady=10) #кнопка Играть
    styled_button("Правила", show_rules).pack(pady=10) #кнопка Правила
    styled_button("Выход", exit_app).pack(pady=10) #кнопка Выход

    root.mainloop() #Запуск главного окна
#Игровое окно
def game_window():
    global sequence, user_sequence, level #Переменные для игры

    sequence = []
    user_sequence = []
    level = 0
  
    game = tk.Tk() #Создаём новое окно 
    game.title("Simon Says - Игра")
    game.geometry("300x650")
    game.configure(bg="#1f2a30")


    tk.Label(game, #Надпись
             text="Нажми 'Старт'", fg="white", bg="#1f2a30").pack(pady=10) 

    level_label = tk.Label(game, text="Уровень: 0", fg="white", bg="#1f2a30")
    level_label.pack()

    buttons_frame = tk.Frame(game, bg="#1f2a30") #Фрейм для цветных кнопок
    buttons_frame.pack(pady=20)

    buttons = {} #Словарь для хранения цветных кнопок

    def flash(color): #Подсветка кнопки
        buttons[color].config(bg="white")
        game.update()
        time.sleep(0.3)
        buttons[color].config(bg=color)
        game.update()
        time.sleep(0.2)

    def show_sequence(): #Показать последовательность 
        for color in sequence:
            flash(color)

    def next_round():
        global level
        user_sequence.clear()
        sequence.append(random.choice(selected_colors))
        level += 1
        level_label.config(text=f"Уровень: {level}")
        logging.info(f"Уровень {level}") #Логируем начало нового уровня
        game.after(500, show_sequence)

    def check_input(color):
        user_sequence.append(color)
        logging.info(f"Нажата кнопка: {color}") #Логируем нажатия кнопок пользователем

        for i in range(len(user_sequence)):
            if user_sequence[i] != sequence[i]:
                logging.info("Ошибка") #Логируем ошибку
                game.destroy()
                result_window()
                return

        if len(user_sequence) == len(sequence): #Если пользователь правильно повторил последовательность, переходим к следующему уровню
            game.after(1000, next_round) #Задержка 

    for color in selected_colors: #Создаём кнопки для каждого цвета в зависимости от выбранной сложности
        btn = tk.Button(buttons_frame, bg=color, width=10, height=3,
                        command=lambda c=color: check_input(c))
        btn.pack(pady=5)
        buttons[color] = btn
  
    #Кнопка для запуска первого уровня
    tk.Button(game, 
              text="Старт", 
              bg="#1976D2",
             fg="white",
             activebackground="#1565C0",
              command=next_round).pack(pady=10)

    game.mainloop() #Запуск игрового окна


# Окно с результатами
def result_window():
    result = tk.Tk() 
    result.title("Результат")
    result.geometry("300x650")
    result.configure(bg="#1f2a30")
    tk.Label(result, #Надпись с именем игрока
             text=f"Игрок: {player_name}", 
             fg="white", 
             bg="#1f2a30").pack(pady=5)
    tk.Label(result, #Надпись с уровнем
             text=f"Уровень: {level}", 
             fg="white", 
             bg="#1f2a30").pack(pady=5)

    logging.info(f"Игра окончена. Уровень {level}") #Логируем окончание игры и достигнутый уровень
    #Кнопка для перезапуска игры
    tk.Button(result, 
              text="Сыграть снова",
              bg="#1976D2",
              fg="white",
              activebackground="#1565C0",
              relief="flat",
              width=25,
              height=2, 
              command=lambda: restart(result)).pack(pady=5)
    #Кнопка для выхода из приложения
    tk.Button(result, 
              text="Выход", 
              bg="#1976D2",
              fg="white",
              activebackground="#1565C0",
              relief="flat",
              width=25,
              height=2,
              command=result.destroy).pack(pady=5)

    result.mainloop()


def restart(window): #Перезапуск игры
    window.destroy()
    start_menu()


# Запуск программы
if __name__ == "__main__":
    logging.info("Программа запущена") #Логируем запуск программы
    start_menu() 