from bot.models import TgUser
from bot.tg.client import TgClient
from bot.utils import generator_code_verification
from goals.models.board import BoardParticipant
from goals.models.goal import Goal
from goals.models.goal_category import GoalCategory


class TgBot:
    def __init__(self, tg_client: TgClient):
        self.offset = 0
        self.tg_client = tg_client

    def get_goals_user(self, user_tg: TgUser) -> None:
        """
        Отправка всех целей пользователя в telegram.
        Если целей у пользователя нет, то отправить сообщение, что целей нет.
        Args:
            user_tg: объект TgUser
        Returns:
            None
        """
        goals = (Goal.objects.filter(category__board__participants__user=user_tg.user).
                 exclude(status=Goal.Status.archived))

        if not goals:
            self.tg_client.send_message(
                chat_id=user_tg.chat_id,
                text=f'На сегодня ничего нет')

            return None

        for goal in goals:
            self.tg_client.send_message(
                chat_id=user_tg.chat_id,
                text=f'{goal.title}\n'
                     f'Категория - {goal.category}\n'
                     f'Приоритет - {goal.Priority.choices[goal.priority - 1][1]}\n'
                     f"Дедлайн - {goal.due_date.strftime('%Y-%m-%d') if goal.due_date else 'Не указан'}"
            )

    def check_user(self, user_ud: int, chat_id: int) -> TgUser | bool:
        """
        Проверка, что пользователь есть в базе данных.
        Если пользователя нет в базе, то создание записи в TgUser и ожидание подтверждение верификационного кода на сайте.
        Если TgUser найден, но не закреплен за User, то создаем другой код верификации и просим его подтвердить его.
        Args:
            user_ud: номер пользователя в телеграмме
            chat_id: номер чата пользователя в телеграмме
        Returns:
            TgUser или None
        """
        user_tg, created = TgUser.objects.get_or_create(user_ud=user_ud, chat_id=chat_id)

        ver_cod = generator_code_verification()

        if created:
            user_tg.verification_code = ver_cod
            user_tg.save()
            self.tg_client.send_message(
                chat_id=user_tg.chat_id,
                text=f'Привет новый пользователь\n'
                     f'Код верификации - {ver_cod}'
            )
            return False

        if not user_tg.user:
            user_tg.verification_code = ver_cod
            user_tg.save()
            self.tg_client.send_message(
                chat_id=user_tg.chat_id,
                text=f'Подтвердите свой аккаунт\n'
                     f'Код верификации - {ver_cod}')
            return False

        return user_tg

    def create_goal(self, category: GoalCategory, user_tg: TgUser) -> None:
        """
        Метод создания новой цели в выбранной категории
        Args:
            category: GoalCategory - выбранная категория
            user_tg: TgUser - пользователь который создает цель
        Returns:
            None
        """
        self.tg_client.send_message(chat_id=user_tg.chat_id, text=f'Введите заголовок цели')

        # вход в состояния ожидания названия для создаваемой цели
        flag = True
        while flag:
            response = self.tg_client.get_updates(offset=self.offset)
            for item in response.result:
                self.offset = item.update_id + 1

                if item.message.text == '/cancel':
                    self.tg_client.send_message(chat_id=user_tg.chat_id, text='Операция отменена')
                    flag = False

                else:
                    goal = Goal.objects.create(category=category, user=user_tg.user, title=item.message.text)
                    self.tg_client.send_message(
                        chat_id=user_tg.chat_id,
                        text=f'Цель создана\n'
                             f'{goal.title}\n'
                             f'{goal.category}'
                    )
                    flag = False

    def choice_category(self, user_tg: TgUser) -> None:
        """
        Метод выдает все категории пользователя в telegram и просит выбрать из этого
        списка категорию в которой будет создана новая цель.
        Args:
            user_tg: TgUser
        Returns:
            None
        """
        categories = GoalCategory.objects.filter(
            board__participants__user=user_tg.user,
            board__participants__role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer)
        ).exclude(is_deleted=True)

        if not categories:
            self.tg_client.send_message(chat_id=user_tg.chat_id, text='Категорий нет')
            return None

        categories_dict = {category.title: category for category in categories}

        self.tg_client.send_message(
            chat_id=user_tg.chat_id,
            text=('Выберете категорию:\n' +
                  '-' * 10 + '\n' +
                  '\n'.join([category for category in categories_dict.keys()]) +
                  '\n' + '-' * 10)
        )

        # вход в состояния ожидания категории от пользователя
        flag = True
        while flag:
            response = self.tg_client.get_updates(offset=self.offset)
            for item in response.result:
                self.offset = item.update_id + 1

                if item.message.text in categories_dict:
                    category_user = categories_dict[item.message.text]
                    self.create_goal(category=category_user, user_tg=user_tg)
                    flag = False

                elif item.message.text == '/cancel':
                    self.tg_client.send_message(chat_id=user_tg.chat_id, text=f'Операция отменена')
                    flag = False

                else:
                    self.tg_client.send_message(chat_id=user_tg.chat_id, text=f'Такой категории нет')

    def run(self) -> None:
        """
        Метод запускает бота
        """
        while True:
            response = self.tg_client.get_updates(offset=self.offset)
            for item in response.result:
                self.offset = item.update_id + 1

                user_tg: TgUser | False = self.check_user(user_ud=item.message.from_.id,
                                                          chat_id=item.message.chat.id)

                if not user_tg:
                    continue

                if item.message.text == '/goals':
                    self.get_goals_user(user_tg=user_tg)
                elif item.message.text == '/create':
                    self.choice_category(user_tg=user_tg)
                else:
                    self.tg_client.send_message(
                        chat_id=item.message.chat.id,
                        text='Неизвестная команда'
                    )
