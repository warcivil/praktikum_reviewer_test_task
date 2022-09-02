import datetime as dt

# лучше конкретно импортировать класс datetime,
# так как тебе кроме datetime ничего не надо из dt
# используй аннотации типов
# используй flake8 когда пишешь код

class Record:
    # лучше написать date=None, если хочешь явно указать, что дату можно не передавать
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment

# это не по заданию, но на будущее:
# лучше бы сделать это класс сделать абстрактным и
# создать какой-то абстрактный метод, например calculate
# и уже его реализовать в классах потомках вместо, например get_calories_remained и
# get_today_cash_remained
class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # названия переменных нужно писать с маленькой буквы,
        # в питоне принято использовать стиль написания snake_case, прочти что это
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                # лучше используй сокращенную запись today_stats+=..
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if ( # лишние скобки
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # Желательно не оставлять комментариев в коде, это говорит о том,
    # что ты с помощью кода не можешь объяснить что он делает,
    # а значит алгоритм запутан или же комментарий бессмыслен
    # вместо комментария лучше добавить Docstring к методу
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # для get_calories_remained и get_today_cash_remained лучше создать базовый метод,
        # и вынести туда базовые сходства, далее уже получать результат базового метода
        # и переопределять различия в методах
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            return('Хватит есть!') # лишние скобки


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # плохо названы переменные, не
    # стоит в параметрах метода создавать константные переменные(они на то и
    # константные что их нельзя менять)
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):

        # лучше использовать здесь другую структуру данных,
        # например dict(currency: (cash_remained, currency_type))
        # тогда можно было бы избавиться от ветвления

        currency_type = currency # ненужное присвоение
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd': # здесь ты используешь currency, а внизу уже почему-то currency_type
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        # тут лучше else, избыточно здесь писать elif
        elif currency_type == 'rub':
            # лучше вынести в константы числа, например, RUB_RATE=1,
            # здесь сравнение, вместо присваивания
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            # лишние скобки
            # здесь ты используешь f строки, а ниже уже .format
            # старайся использовать что-то одно
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # тут можно либо написать else, либо вообще не писать ничего, а просто return
        elif cash_remained < 0:
            # вместо -cash_remained лучше взять модуль от него
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # 1) не стоит переопределять метод просто
    # так, если ты не хочешь писать дополнительную логику
    # 2) тут так же ошибка,
    # теперь данный метод не будет работать(забыл написать return)
    # почитай про оператор super() и полиморфизм в питоне
    def get_week_stats(self):
        super().get_week_stats()

# это main файл, хорошо бы тут разметить точку входа в программу
# if __name__=='__main__': например