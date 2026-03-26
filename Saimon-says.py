import tkinter as tk

# ===== ФУНКЦИИ =====
def start_game():
    name = name_entry.get()
    print(f"Игрок: {name}, сложность: {difficulty.get()}")

def show_rules():
    rules_win = tk.Toplevel(root)
    rules_win.title("Правила")

    tk.Label(rules_win, text="""
Повторяйте последовательность цветов.
Каждый уровень добавляется новый цвет.
Ошибка — проигрыш.
""", font=("Arial", 12)).pack(padx=20, pady=20)

def exit_app():
    root.quit()


def set_difficulty(level):
    difficulty.set(level)
    label_diff.config(text=f"Сложность: {level}")


# ===== ОСНОВНОЕ ОКНО =====
root = tk.Tk()
root.title("Simon Says")
root.geometry("400x500")
root.configure(bg="#1f2a30")

difficulty = tk.StringVar(value="Легко")

# ===== ЗАГОЛОВОК =====
tk.Label(root, text="Saimon says",
         font=("Arial", 24),
         fg="white", bg="#1f2a30").pack(pady=20)

# ===== ВВОД ИМЕНИ =====
tk.Label(root, text="Введите имя",
         font=("Arial", 12),
         fg="gray", bg="#1f2a30").pack()

name_entry = tk.Entry(root, font=("Arial", 14), justify="center")
name_entry.pack(pady=10, ipadx=50, ipady=8)

# ===== СЛОЖНОСТЬ =====
tk.Label(root, text="Сложность",
         font=("Arial", 12),
         fg="gray", bg="#1f2a30").pack(pady=10)

frame_diff = tk.Frame(root, bg="#1f2a30")
frame_diff.pack()

btn_easy = tk.Button(frame_diff, bg="#4CAF6A", width=8, height=2,
                     command=lambda: set_difficulty("Легко"))
btn_easy.pack(side=tk.LEFT, padx=10)

btn_mid = tk.Button(frame_diff, bg="#F4B942", width=8, height=2,
                    command=lambda: set_difficulty("Средне"))
btn_mid.pack(side=tk.LEFT, padx=10)

btn_hard = tk.Button(frame_diff, bg="#E03A3E", width=8, height=2,
                     command=lambda: set_difficulty("Сложно"))
btn_hard.pack(side=tk.LEFT, padx=10)

label_diff = tk.Label(root, text="Сложность: Легко",
                      fg="white", bg="#1f2a30")
label_diff.pack(pady=5)

# ===== КНОПКИ =====
def styled_button(text, command):
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

styled_button("Играть", start_game).pack(pady=10)
styled_button("Правила", show_rules).pack(pady=10)
styled_button("Выход", exit_app).pack(pady=10)

root.mainloop()