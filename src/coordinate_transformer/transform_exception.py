class BaseTransformException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class NotImplementedYet(BaseTransformException):
    def __init__(self):
        super().__init__("Пересчет координат в данную проекцию находится на стадии разработки")


class FileIsNotExcel(BaseTransformException):
    def __init__(self):
        super().__init__("Файл не является форматом Excel!")
