import asyncio
import tkinter as tk
from tkinter import ttk, messagebox
from bot import Bot
import threading
import sys
from users_window import users_table
from console import TextRedirector

# Функции для обработки событий кнопок
def start_bot():
    channel = channel_entry.get()
    cooldown_lyt = combo_lyt.get()
    cooldown_casino = combo_casino.get()
    mark_admin = entry_mark_admin.get()

    if not channel:
        messagebox.showwarning("Input Error", "Please enter a channel.")
        return
    if not cooldown_lyt or not cooldown_casino:
        messagebox.showwarning("Input Error", "Please select a cooldown duration.")
        return

    def start_bot_in_thread():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        bot = Bot(channel, lyt_cooldown=int(cooldown_lyt), casino_cooldown=int(cooldown_casino), mark_admin=mark_admin)
        loop.run_until_complete(bot.start())
        loop.run_forever()

    threading.Thread(target=start_bot_in_thread, daemon=True).start()

# Создаем основное окно
root = tk.Tk()
root.title("Danturi Bot")
# root.geometry("260x360")
root.geometry("260x420")
root.resizable(False, False)

# Верхняя часть окна
top_frame = tk.Frame(root)
top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

# Добавляем виджет ввода канала
channel_label = tk.Label(top_frame, text="Enter channel:")
channel_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
channel_entry = ttk.Entry(top_frame)
channel_entry.insert(0, "GodOfDango")
channel_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

# Создаем рамку для секции "Лут"
loot_frame = tk.LabelFrame(top_frame, text="Лут")
loot_frame.grid(row=1, column=0, columnspan=2, pady=4, sticky="ew")

# Добавляем комбо-бокс для выбора кулдауна команды !лут в рамку
cooldown_lyt_label = tk.Label(loot_frame, text="Кулдаун:")
cooldown_lyt_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
cooldowns_lyt = [10, 20, 30, 60]
combo_lyt = ttk.Combobox(loot_frame, values=cooldowns_lyt, state="readonly", width=5)
combo_lyt.grid(row=0, column=1, padx=5, pady=5)

# Создаем рамку для секции "Казино"
casino_frame = tk.LabelFrame(top_frame, text="Казино")
casino_frame.grid(row=2, column=0, columnspan=2, pady=4, sticky="ew")

# Добавляем комбо-бокс для выбора кулдауна и ставки команды !казино в рамку
cooldown_casino_label = tk.Label(casino_frame, text="Кулдаун:")
cooldown_casino_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
cooldowns_casino = [10, 20, 30, 60]
combo_casino = ttk.Combobox(casino_frame, values=cooldowns_casino, state="readonly", width=5)
combo_casino.grid(row=0, column=1, padx=5, pady=5)

# Создаем рамку для секции "Оценка"
mark_frame = tk.LabelFrame(top_frame, text="Оценка")
mark_frame.grid(row=3, column=0, columnspan=2, pady=4, sticky="ew")

# Добавляем комбо-бокс для выбора никнейма админа команды !ОЦЕНКА в рамку
mark_label = tk.Label(mark_frame, text="Никнейм:")
mark_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_mark_admin = ttk.Entry(mark_frame, width=20)
entry_mark_admin.insert(0, "GodOfDango")
entry_mark_admin.grid(row=0, column=1, padx=5, pady=5)

# Кнопки для запуска и остановки бота
button_frame = tk.Frame(top_frame)
button_frame.grid(row=4, column=0, columnspan=2, pady=5)

button_start = ttk.Button(button_frame, text="Start", command=start_bot)
button_start.pack(side=tk.LEFT, padx=10)

button_users = ttk.Button(button_frame, text="Users", command=users_table)
button_users.pack(side=tk.LEFT, padx=10)

# Текстовое поле для вывода консоли
console_output = tk.Text(root, height=10, wrap="word")
console_output.pack(side=tk.BOTTOM, fill=tk.BOTH,expand=False, padx=10, pady=0)
# Перенаправляем вывод консоли в текстовое поле
sys.stdout = TextRedirector(console_output, "stdout")
sys.stderr = TextRedirector(console_output, "stderr")