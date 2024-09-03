class BaseExcelTransformException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class FileIsNotExcel(BaseExcelTransformException):
    def __init__(self):
        super().__init__("Файл не является форматом Excel!")


class FileIsEmpty(BaseExcelTransformException):
    def __init__(self):
        super().__init__("Файл пустой!")


class FileHasNoColumns(BaseExcelTransformException):
    def __init__(self):
        super().__init__("В файле должно быть минимум 2 колонки!")


class NonCompatibleLatitude(BaseExcelTransformException):
    def __init__(self):
        super().__init__("Строки в колонке широты не соотвествуют заданной единице измерения")


class NonCompatibleLongitude(BaseExcelTransformException):
    def __init__(self):
        super().__init__("Строки в колонке долготы не соотвествуют заданной единице измерения")
