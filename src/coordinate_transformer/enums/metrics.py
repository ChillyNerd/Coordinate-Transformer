from enum import Enum


class MetricType(Enum):
    METER = "Метровая"
    ANGLE = "Градусная"


class Metric:
    def __init__(self, label: str, metric_type: MetricType):
        self.label = label
        self.metric_type = metric_type


class Metrics(Enum):
    METER = Metric("Метры", MetricType.METER)
    ANGLE = Metric("Градусы минуты секунды", MetricType.ANGLE)
    FLOAT_ANGLE = Metric("Градусы (десятичная дробь)", MetricType.ANGLE)


class OutputMetrics(Enum):
    METER = Metric("Метры", MetricType.METER)
    ANGLE_DM = Metric("Градусы минуты", MetricType.ANGLE)
    ANGLE_DMS = Metric("Градусы минуты секунды", MetricType.ANGLE)
    FLOAT_ANGLE = Metric("Градусы (десятичная дробь)", MetricType.ANGLE)
