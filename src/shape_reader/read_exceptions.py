class BaseShapeReadException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class FileIsNotArchive(BaseShapeReadException):
    def __init__(self):
        super().__init__("Файл не является архивом!")


class FilesAreCorrelating(BaseShapeReadException):
    def __init__(self):
        super().__init__("В архиве найдены файлы с одинаковыми именами!")


class ThereIsNoShapeFiles(BaseShapeReadException):
    def __init__(self):
        super().__init__("Shape файл не найден!")
