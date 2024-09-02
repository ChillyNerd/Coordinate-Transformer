from enum import Enum


class Metrics(Enum):
    METER = "Метры"
    ANGLE = "Градусы минуты секунды"
    ANGLESEP = "Градусы минуты секунды через пробел"
    FLOAT_ANGLE = "Градусы (десятичная дробь)"
