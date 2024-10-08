import logging

from pyproj import Transformer
from pyproj.enums import TransformDirection

from src.config import Config
from src.coordinate_transformer.defaults import dependencies, intermediate_projections_dict, pulkovo_to_pz, gsk_to_pz, \
    LUK_CRS
from src.coordinate_transformer.enums import ProjectionType
from src.coordinate_transformer.impl import Projection
from src.coordinate_transformer.transform_exception import NotImplementedYet


class TransformNode:
    def __init__(self, projection_type: ProjectionType, mnemonic: str):
        self.type: ProjectionType = projection_type
        self.mnemonic: str = mnemonic


class StepTransformer:
    def __init__(self, projection_from: TransformNode, projection_to: TransformNode):
        self.from_: TransformNode = projection_from
        self.to_: TransformNode = projection_to
        self.log = logging.getLogger(Config.coordinate_transformer)

    def transform(self, latitude, longitude):
        direction = TransformDirection.FORWARD
        if self.from_.type == ProjectionType.PULKOVO and self.to_.type == ProjectionType.PZ:
            transformer = Transformer.from_pipeline(pulkovo_to_pz)
            pipeline = f'Using PULKOVO to PZ pipeline'
        elif self.from_.type == ProjectionType.PZ and self.to_.type == ProjectionType.PULKOVO:
            transformer = Transformer.from_pipeline(pulkovo_to_pz)
            direction = TransformDirection.INVERSE
            pipeline = f'Using inversed PULKOVO to PZ pipeline'
        elif self.from_.type == ProjectionType.GSK and self.to_.type == ProjectionType.PZ:
            transformer = Transformer.from_pipeline(gsk_to_pz)
            pipeline = f'Using GSK to PZ pipeline'
        elif self.from_.type == ProjectionType.PZ and self.to_.type == ProjectionType.GSK:
            transformer = Transformer.from_pipeline(gsk_to_pz)
            direction = TransformDirection.INVERSE
            pipeline = f'Using inversed GSK to PZ pipeline'
        elif self.from_.type == ProjectionType.PULKOVO_NZONE and self.to_.type == ProjectionType.PULKOVO:
            transformer = Transformer.from_pipeline(LUK_CRS[self.from_.mnemonic][2])
            pipeline = f'Using PULKOVO_NZONE to PULKOVO pipeline'
        elif self.from_.type == ProjectionType.PULKOVO and self.to_.type == ProjectionType.PULKOVO_NZONE:
            transformer = Transformer.from_pipeline(LUK_CRS[self.to_.mnemonic][3])
            pipeline = f'Using PULKOVO to PULKOVO_NZONE pipeline'
        elif self.from_.type == ProjectionType.GSK_NZONE and self.to_.type == ProjectionType.GSK:
            transformer = Transformer.from_pipeline(LUK_CRS[self.from_.mnemonic][2])
            pipeline = f'Using GSK_NZONE to GSK pipeline'
        elif self.from_.type == ProjectionType.GSK and self.to_.type == ProjectionType.GSK_NZONE:
            transformer = Transformer.from_pipeline(LUK_CRS[self.to_.mnemonic][3])
            pipeline = f'Using GSK to GSK_NZONE pipeline'
        else:
            transformer = Transformer.from_crs(self.from_.mnemonic, self.to_.mnemonic)
            pipeline = f'Using common transformer'
        transformed_from = f'{latitude, longitude} {self.from_.type.name} ({self.from_.mnemonic})'
        result_latitude, result_longitude = transformer.transform(latitude, longitude, direction=direction)
        transformed_to = f'{result_latitude, result_longitude} {self.to_.type.name} ({self.to_.mnemonic})'
        self.log.debug(f'{pipeline} transformed from {transformed_from} to {transformed_to}')
        return result_latitude, result_longitude


class CoordinateTransformer:
    def __init__(self, projection_from: Projection, projection_to: Projection):
        self.from_: TransformNode = TransformNode(projection_from.projection_type, projection_from.mnemonic)
        self.to_: TransformNode = TransformNode(projection_to.projection_type, projection_to.mnemonic)
        self.transform_path = dependencies.find_path(
            self.from_.type,
            self.to_.type
        )
        if self.transform_path is None:
            raise NotImplementedYet()

    def transform(self, latitude, longitude):
        current_latitude, current_longitude = latitude, longitude
        steps = len(self.transform_path) - 1
        for i in range(steps):
            if i == 0:
                projection_from = self.from_
            else:
                from_ = self.transform_path[i]
                projection_from = TransformNode(from_, intermediate_projections_dict[from_])
            if i == steps - 1:
                projection_to = self.to_
            else:
                to_ = self.transform_path[i + 1]
                projection_to = TransformNode(to_, intermediate_projections_dict[to_])
            transform_step = StepTransformer(projection_from, projection_to)
            current_latitude, current_longitude = transform_step.transform(current_latitude, current_longitude)
        return current_latitude, current_longitude
