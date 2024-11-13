import os
from datetime import datetime


def logger(path):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __logger(old_function):
        name = old_function.__name__

        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            with open(path, "a") as file:
                file.write(f"{time:12} {name:12} результат = {result:15} args = {args}, kwargs = {
                    kwargs} \n")
            return result

        return new_function

    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()
            print(log_file_content)

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{
                item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()
