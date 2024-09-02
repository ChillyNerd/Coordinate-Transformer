from enum import Enum

class ProjectionType(Enum):
    GSK_ZONE = 'Зона ГСК2011'
    GSK_NZONE = 'Зона N ГСК2011'
    GSK = 'ГСК2011'
    PZ = 'ПЗ 90.11'
    PULKOVO = 'Пулково 1942'
    PULKOVO_ZONE = 'Зона Пулково 1942'
    PULKOVO_NZONE = 'Зона N Пулково 1942'
    PULKOVO63_ZONE = 'Зона Пулково 1963'
    WGS = 'WGS84'

class ProjectionGroup(Enum):
    GSK_SK = 'ГСК-2011'
    SK42_SK = 'Пулково 1942г.'
    SK63_SK = 'Пулково 1963г.'
    PZ_SK = 'ПЗ 90.11'
    WGS84_SK = 'WGS84'