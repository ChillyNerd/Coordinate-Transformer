from enum import Enum
from typing import List


class Metrics(Enum):
    METER = "Метры"
    ANGLE = "Угол (градусы)"
    FLOAT_ANGLE = "Угол (десятичная дробь)"


class Projection:
    def __init__(self, mnemonic, comment, metrics: List[Metrics] = None):
        if metrics is None:
            metrics = []
        self.mnemonic = mnemonic
        self.comment = comment
        self.allowed_metrics = list(map(lambda metric: metric.name, metrics))


angle_metrics = [Metrics.ANGLE, Metrics.FLOAT_ANGLE]
meter_metrics = [Metrics.METER]
projections = [
    Projection("epsg:4284", "Пулково 1942/Широта/Долгота", angle_metrics),
    Projection("epsg:7683", "ГСК-2011/GSK-2011", angle_metrics),
    Projection("epsg:20904", "Зона 4 ГСК-2011/GSK-2011_GK_Zone_4", meter_metrics),
    Projection("epsg:20908", "Зона 8 ГСК-2011/GSK-2011_GK_Zone_8", meter_metrics),
    Projection("epsg:20909", "Зона 9 ГСК-2011/GSK-2011_GK_Zone_9", meter_metrics),
    Projection("epsg:20910", "Зона 10 ГСК-2011/GSK-2011_GK_Zone_10", meter_metrics),
    Projection("epsg:20911", "Зона 11 ГСК-2011/GSK-2011_GK_Zone_11", meter_metrics),
    Projection("epsg:20912", "Зона 12 ГСК-2011/GSK-2011_GK_Zone_12", meter_metrics),
    Projection("epsg:20913", "Зона 13 ГСК-2011/GSK-2011_GK_Zone_13", meter_metrics),
    Projection("epsg:20914", "Зона 14 ГСК-2011/GSK-2011_GK_Zone_14", meter_metrics),
    Projection("epsg:28404", "Зона 4 Pulkovo_1942_GK_Zone_4", meter_metrics),
    Projection("epsg:28408", "Зона 8 Pulkovo_1942_GK_Zone_8", meter_metrics),
    Projection("epsg:28409", "Зона 9 Pulkovo_1942_GK_Zone_9", meter_metrics),
    Projection("epsg:28410", "Зона 10 Pulkovo_1942_GK_Zone_10", meter_metrics),
    Projection("epsg:28411", "Зона 11 Pulkovo_1942_GK_Zone_11", meter_metrics),
    Projection("epsg:28412", "Зона 12 Pulkovo_1942_GK_Zone_12", meter_metrics),
    Projection("epsg:28413", "Зона 13 Pulkovo_1942_GK_Zone_13", meter_metrics),
    Projection("epsg:28414", "Зона 14 Pulkovo_1942_GK_Zone_14", meter_metrics),
    Projection("epsg:28415", "Зона 15 Pulkovo_1942_GK_Zone_15", meter_metrics),
]
