import tkinter as tk
from tkinter import ttk
import asyncio
import aiosqlite

async def fetch_users():
    async with aiosqlite.connect('twitch_bot.db') as db:
        cursor = await db.execute("SELECT username, points FROM users")
        rows = await cursor.fetchall()
        return rows

def users_table():
    # Создаем новое окно
    window = tk.Toplevel()
    window.title("Users Table")
    window.geometry("400x400")
    window.resizable(False, False)
    # root.iconbitmap("temp.ico")

    # Создаем виджет Treeview
    tree = ttk.Treeview(window, columns=("Username", "Points"), show="headings")
    tree.heading("Username", text="Username")
    tree.heading("Points", text="Points")
    tree.pack(fill=tk.BOTH, expand=True)

    # Создаем строку поиска
    control_frame = tk.Frame(window)
    control_frame.pack(pady=5, fill=tk.X)

    search_label = tk.Label(control_frame, text="Search:")
    search_label.pack(side=tk.LEFT, padx=5)

    search_entry = tk.Entry(control_frame)
    search_entry.pack(side=tk.LEFT, padx=5)

    def filter_data():
        search_term = search_entry.get().lower()
        for item in tree.get_children():
            tree.delete(item)
        for user in all_users:
            if search_term in user[0].lower():
                tree.insert("", "end", values=user)

    search_entry.bind("<KeyRelease>", lambda event: filter_data())


    async def load_data():
        global all_users
        all_users = await fetch_users()
        for user in all_users:
            tree.insert("", "end", values=user)

    # Кнопка для обновления таблицы
    def refresh_data():
        tree.delete(*tree.get_children())
        asyncio.run(load_data())

    refresh_button = ttk.Button(control_frame, text="Refresh", command=refresh_data)
    refresh_button.pack(side=tk.RIGHT, padx=5)

    # Запускаем загрузку данных
    asyncio.run(load_data())
