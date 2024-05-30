from twitchio.ext import commands
from database import create_table, save_to_db, get_user_points
from cogs import MyCog
import random

class Bot(commands.Bot):
    def __init__(self, channel, lyt_cooldown, casino_cooldown, mark_admin):
        super().__init__(token='8fn77ck34t909kw3rtac8xi91vzxoq', prefix='!', initial_channels=[channel])
        self.channel = channel
        self.add_cog(MyCog(self, lyt_cooldown, casino_cooldown, mark_admin))

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        await create_table()

    async def event_command_error(self, context: commands.Context, error: Exception):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.ArgumentParsingFailed):
            await context.send(error.message)
        else:
            print(error)

    @commands.command(name="ДО", aliases=["до"])
    async def check_do(self,ctx:commands.Context):
        total_points = await get_user_points(ctx.author.name)
        await ctx.send('@'+ctx.author.name+', '+'у тебя '+str(total_points)+"ДО")

    @commands.command(name="ЛУТ", aliases=['лут'])
    async def lyt(self, ctx: commands.Context):
        try:
            voting_cog = self.get_cog('MyCog')
            await voting_cog.check_cooldown(ctx.message, 'loot')
        except commands.CommandOnCooldown as e:
            remaining_time = e.retry_after
            await ctx.send(f'ПЩ. ПЩ. Перезарядка: {remaining_time} секунд!')
            return
        events = [
            (random.choice(["Здесь пусто! Поищи в следующий раз :)", "Похоже, невезение преследует тебя... Как жаль :(", "ВАУ, НЕУЖЕЛИ? А, нет. Извини, тут ничего нет! :D"]), 0),
            ("Что ж, продуктивный день встретил продуктивный день!", 5),
            ("Проскользнув сквозь пещеру, ты находишь что-то в области таза!", 10),
            ("ОГО! Целый данго! Может, съесть?", 1),
            ("Это же?! Преодолев самые сложные испытания, ты находишь достойную награду!", 20),
            ("Тебя окружают три авантюриста, ловят и приставляют к тебе свои данго. Что ж. У всего есть плюсы!", 3),
            ("Спрячешь ствол - будет разговор. Ты теряешь часть экипировки", 2),
            ("ДАНГОПОТ! Может, пора сходить в лотерею?!", 30)
        ]

        probabilities = [0.50, 0.20, 0.10, 0.10, 0.05, 0.03, 0.01, 0.01]
        event_func = random.choices(events, probabilities, k=1)
        await save_to_db(ctx.author.name, event_func[0][1])
        total_points = await get_user_points(ctx.author.name)
        await ctx.send('@'+ctx.author.name+', '+event_func[0][0]+f' ({"+" + str(event_func[0][1]) if event_func[0][1] >= 0 else str(event_func[0][1])}ДО / {total_points}ДО)')

    def stop(self):
        self.loop.stop()

    @commands.command(name="КАЗИНО", aliases=["казино"])
    async def casino(self, ctx: commands.Context):
        args = ctx.message.content.split()
        if len(args) != 2 or not args[1].isdigit() or not (1 <= int(args[1]) <= 10):
            await ctx.send(f'@{ctx.author.name}, ставка должна быть числом от 1 до 10.')
            return

        try:
            my_cog = self.get_cog('MyCog')
            await my_cog.check_cooldown(ctx.message, 'casino')
        except commands.CommandOnCooldown as e:
            remaining_time = e.retry_after
            await ctx.send(f'Казино на перезарядке: {remaining_time} секунд!')
            return
        casino_bet = int(args[1])
        user_points = await get_user_points(ctx.author.name)

        if user_points < casino_bet:
            await ctx.send(f'@{ctx.author.name}, у тебя недостаточно ДО для ставки. Текущий баланс: {user_points} ДО.')
            return

        symbols = ["🍡", "🪵", "🍓", "🍒", "🍋", "🍌", "🍉", "🥝", "🥥", "🍏", "🍑"]
        result = [random.choice(symbols) for _ in range(3)]
        result_str = ''.join(result)

        if result_str == "🍡🍡🍡":
            points = 50
            response = "ДАНГОПОТ! Вы выигрываете 50 ДО!"
        elif result_str == "🪵🪵🪵":
            points = 30
            response = "БРЕВНА! Ваша ставка утраивается — вы получаете 30 ДО!"
        elif result_str == "🍉🍉🍉":
            points = 5
            response = "АРБУЗНЫЙ ЛОРД! Ваша ставка возвращается + 5 ДО сверху!"
        elif result[0] == result[1] == result[2]:
            points = 0  # если 3 любых одинаковых символа, кроме описанных выше, это случай с "ТРИ В РЯД"
            response = "ТРИ В РЯД! Вы возвращаете свою ставку!"
        else:
            points = -casino_bet
            response = "... Увы, казино обыграло вас!"

        await save_to_db(ctx.author.name, points)
        total_points = await get_user_points(ctx.author.name)
        await ctx.send(f'Результат: [{result_str}] — {response} ({total_points} ДО)')

    @commands.command(name="ОЦЕНКА", aliases=["оценка"])
    async def start_voting(self, ctx: commands.Context):
        if ctx.author.name.lower() == 'danturi_i':  # Проверяем имя на стримера
            self.get_cog('MyCog').voting_active = True
            self.get_cog('MyCog').votes = {}  # Очищаем предыдущие голоса
            await ctx.send('Голосование началось! Пожалуйста, отправьте свою оценку от 0 до 10.')

    @commands.command(name="ОЦЕНКАСТОП", aliases=["оценкастоп"])
    async def stop_voting(self, ctx: commands.Context):
        if ctx.author.name.lower() == 'danturi_i':  # Проверяем имя на стримера
            self.get_cog('MyCog').voting_active = False

            if self.get_cog('MyCog').votes:
                average_score = sum(self.get_cog('MyCog').votes.values()) / len(self.get_cog('MyCog').votes)
                await ctx.send(f'ГОЛОСОВАНИЕ ОКОНЧЕНО! Средняя оценка: {average_score:.2f}')
            else:
                await ctx.send('ГОЛОСОВАНИЕ ОКОНЧЕНО! Оценок не поступило.')