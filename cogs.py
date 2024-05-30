from twitchio.ext import commands
import twitchio
import time

class MyCog(commands.Cog):
    def __init__(self, bot, loot_cooldown, casino_cooldown, mark_admin):
        self.bot = bot
        self.cooldowns = {
            'loot': {},
            'casino': {}
        }
        self.loot_cooldown_duration = loot_cooldown
        self.casino_cooldown_duration = casino_cooldown
        self.mark_admin = mark_admin
        self.voting_active = False
        self.votes = {}
    @commands.Cog.event()
    async def event_message(self, message: twitchio.Message):
        # Проверяем, что автор сообщения существует
        if message.author:
            # Игнорируем сообщения от бота, чтобы избежать рекурсии
            if message.author.name and message.author.name.lower() == self.bot.nick.lower():
                return

            # Если голосование активно, принимаем оценки
            if self.voting_active and message.content.isdigit():
                score = int(message.content)
                if 0 <= score <= 10 and message.author.name not in self.votes:
                    self.votes[message.author.name] = score
                    await message.channel.send(f'{message.author.name}, твоя оценка принята: {score}')
                elif message.author.name in self.votes:
                    await message.channel.send(f'{message.author.name}, ты уже оставил свою оценку.')
                else:
                    await message.channel.send(
                        f'{message.author.name}, оценка должна быть целым числом от 0 до 10.')

    async def check_cooldown(self, message: twitchio.Message, command_name: str):
        cooldowns = self.cooldowns.get(command_name)
        cooldown_duration = getattr(self, f"{command_name}_cooldown_duration")

        cooldown = cooldowns.get(message.author.name)
        if cooldown and time.time() < cooldown:
            remaining_time = int(cooldown - time.time())
            raise commands.CommandOnCooldown(message.author, remaining_time)

        cooldowns[message.author.name] = time.time() + cooldown_duration*60