from pyproj import Transformer
from pyproj.enums import TransformDirection
from typing import List
from src.coordinate_transformer.transform_exception import NotImplementedYet
from src.coordinate_transformer.impl import Projection
from src.coordinate_transformer.enums import ProjectionType
from src.coordinate_transformer.defaults import dependencies, intermediate_projections_dict, pulkovo_to_pz, gsk_to_pz
from src.logger import log


class TransformNode:
    def __init__(self, projection_type: ProjectionType, mnemonic: str):
        self.type: ProjectionType = projection_type
        self.mnemonic: str = mnemonic


class TransformStep:
    def __init__(self, projection_from: TransformNode, projection_to: TransformNode):
        self.projection_from: TransformNode = projection_from
        self.projection_to: TransformNode = projection_to

    def transform(self, latitude, longitude):
        direction = TransformDirection.FORWARD
        if self.projection_from.type == ProjectionType.PULKOVO and self.projection_to.type == ProjectionType.PZ:
            transformer = Transformer.from_pipeline(pulkovo_to_pz)
        elif self.projection_from.type == ProjectionType.PZ and self.projection_to.type == ProjectionType.PULKOVO:
            transformer = Transformer.from_pipeline(pulkovo_to_pz)
            direction = TransformDirection.INVERSE
        elif self.projection_from.type == ProjectionType.GSK and self.projection_to.type == ProjectionType.PZ:
            transformer = Transformer.from_pipeline(gsk_to_pz)
        elif self.projection_from.type == ProjectionType.PZ and self.projection_to.type == ProjectionType.GSK:
            transformer = Transformer.from_pipeline(gsk_to_pz)
            direction = TransformDirection.INVERSE
        else:
            transformer = Transformer.from_crs(self.projection_from.mnemonic, self.projection_to.mnemonic)
        return transformer.transform(latitude, longitude, direction=direction)


class CoordinateTransformer:
    def __init__(self, projection_from: Projection, projection_to: Projection):
        self.projection_from: TransformNode = TransformNode(projection_from.projection_type, projection_from.mnemonic)
        self.projection_to: TransformNode = TransformNode(projection_to.projection_type, projection_to.mnemonic)

    def transform(self, latitude, longitude):
        transform_path = dependencies.find_path(
            self.projection_from.type,
            self.projection_to.type
        )
        if transform_path is None:
            raise NotImplementedYet()
        log.debug(f'Transform path is {"->".join(list(map(lambda node: f"({node.value})", transform_path)))}')
        return self.transform_sequence(transform_path, latitude, longitude)

    def transform_sequence(self, path: List[ProjectionType], latitude, longitude):
        current_latitude, current_longitude = latitude, longitude
        for i in range(len(path) - 1):
            if i == 0:
                projection_from = TransformNode(self.projection_from.type, self.projection_from.mnemonic)
            else:
                projection_from = TransformNode(path[i], intermediate_projections_dict[path[i]])
            if i == len(path) - 2:
                projection_to = TransformNode(self.projection_to.type, self.projection_to.mnemonic)
            else:
                projection_to = TransformNode(path[i + 1], intermediate_projections_dict[path[i + 1]])
            step = TransformStep(projection_from, projection_to)
            current_latitude, current_longitude = step.transform(current_latitude, current_longitude)
        return current_latitude, current_longitude


def trans_excel(file_path: str):
    return file_path
