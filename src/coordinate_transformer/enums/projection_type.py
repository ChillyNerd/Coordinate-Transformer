from enum import Enum


class ProjectionType(Enum):
    GSK_ZONE = 'Зона ГСК2011'
    GSK = 'ГСК2011'
    PZ = 'ПЗ 90.11'
    PULKOVO = 'Пулково 1942'
    PULKOVO_ZONE = 'Зона Пулково 1942'
    WGS = 'WGS84'
