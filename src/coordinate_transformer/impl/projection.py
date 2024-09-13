from src.coordinate_transformer.enums import ProjectionType, ProjectionGroup, MetricType


class Projection:
    def __init__(self, mnemonic: str, comment: str, projection_type: ProjectionType, projection_group: ProjectionGroup,
                 metric_type: MetricType = MetricType.METER, disabled: bool = False):
        self.mnemonic: str = mnemonic
        self.comment: str = comment
        self.projection_type: ProjectionType = projection_type
        self.metric_type: MetricType = metric_type
        self.projection_group: str = projection_group.name
        self.disabled: bool = disabled
