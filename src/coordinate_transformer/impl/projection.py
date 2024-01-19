from src.coordinate_transformer.enums import Metrics, ProjectionType
from typing import List


class Projection:
    def __init__(self, mnemonic: str, comment: str, projection_type: ProjectionType, metrics: List[Metrics] = None,
                 disabled: bool = False):
        if metrics is None:
            metrics = []
        self.mnemonic: str = mnemonic
        self.comment: str = comment
        self.projection_type: ProjectionType = projection_type
        self.allowed_metrics: List[Metrics] = list(map(lambda metric: metric.name, metrics))
        self.disabled: bool = disabled
