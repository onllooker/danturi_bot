import aiosqlite

# Функция для создания таблицы пользователей
async def create_table():
    async with aiosqlite.connect('twitch_bot.db') as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS users (
                             id INTEGER PRIMARY KEY,
                             username TEXT NOT NULL,
                             points INTEGER DEFAULT 0
                             )''')
        await db.commit()

# Функция для записи никнейма пользователя в базу данных и начисления очков
async def save_to_db(username, points):
    async with aiosqlite.connect('twitch_bot.db') as db:
        # Проверяем, есть ли пользователь в базе данных
        cursor = await db.execute("SELECT points FROM users WHERE username=?", (username,))
        current_points = await cursor.fetchone()

        # Если пользователь найден, обновляем его очки
        if current_points:
            total_points = max(current_points[0] + points, 0)
            await db.execute("UPDATE users SET points=? WHERE username=?", (total_points, username))
        else:
            # Если пользователь не найден, создаем запись в базе данных
            total_points = max(points, 0)  # Убеждаемся, что очки не отрицательны
            await db.execute("INSERT INTO users (username, points) VALUES (?, ?)", (username, total_points))

        await db.commit()

async def get_user_points(username):
    async with aiosqlite.connect('twitch_bot.db') as db:
        cursor = await db.execute("SELECT points FROM users WHERE username=?", (username,))
        total_points = await cursor.fetchone()
        return total_points[0]