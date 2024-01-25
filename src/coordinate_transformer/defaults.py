from src.coordinate_transformer.impl import *
from src.coordinate_transformer.enums import *


pulkovo_to_pz = (
    "proj=pipeline "
    "step proj=axisswap order=2,1 "
    "step proj=unitconvert xy_in=deg xy_out=rad "
    "step proj=push v_3 step proj=cart ellps=krass "
    "step proj=helmert x=23.557 y=-140.844 z=-79.778 rx=-0.0023 ry=-0.34646 rz=-0.79421 s=-0.228"
    " convention=coordinate_frame "
    "step inv proj=cart a=6378136 rf=298.25784 "
    "step proj=pop v_3 step proj=longlat a=6378136 rf=298.25784 "
    "step proj=unitconvert xy_in=rad xy_out=deg step proj=axisswap order=2,1"
)

gsk_to_pz = (
    "proj=pipeline "
    "step proj=axisswap order=2,1 "
    "step proj=unitconvert xy_in=deg xy_out=rad "
    "step proj=push v_3 step proj=cart ellps=GSK2011 "
    "step proj=helmert x=0 y=0.014 z=-0.008 rx=-0.000562 ry=-0.000019 rz=0.000053 s=-0.0006"
    " convention=coordinate_frame "
    "step inv proj=cart a=6378136 rf=298.25784 "
    "step proj=pop v_3 step proj=longlat a=6378136 rf=298.25784 "
    "step proj=unitconvert xy_in=rad xy_out=deg step proj=axisswap order=2,1"
)

angle_metrics = [Metrics.ANGLE, Metrics.FLOAT_ANGLE]
meter_metrics = [Metrics.METER]

intermediate_projections = [
    Projection("epsg:4326", "WGS84", ProjectionType.WGS, angle_metrics),
    Projection("epsg:9475", "ПЗ 90.11", ProjectionType.PZ, angle_metrics, disabled=True),
    Projection("epsg:4284", "Пулково 1942/Широта/Долгота", ProjectionType.PULKOVO, angle_metrics),
    Projection("epsg:7683", "ГСК-2011/GSK-2011", ProjectionType.GSK, angle_metrics),
]
intermediate_projections_dict = {
    projection.projection_type: projection.mnemonic for projection in intermediate_projections
}
zone_projections = [
    Projection("epsg:20904", "Зона 4 ГСК-2011/GSK-2011_GK_Zone_4", ProjectionType.GSK_ZONE, meter_metrics),
    Projection("epsg:20908", "Зона 8 ГСК-2011/GSK-2011_GK_Zone_8", ProjectionType.GSK_ZONE, meter_metrics),
    Projection("epsg:20909", "Зона 9 ГСК-2011/GSK-2011_GK_Zone_9", ProjectionType.GSK_ZONE, meter_metrics),
    Projection("epsg:20910", "Зона 10 ГСК-2011/GSK-2011_GK_Zone_10", ProjectionType.GSK_ZONE, meter_metrics),
    Projection("epsg:20911", "Зона 11 ГСК-2011/GSK-2011_GK_Zone_11", ProjectionType.GSK_ZONE, meter_metrics),
    Projection("epsg:20912", "Зона 12 ГСК-2011/GSK-2011_GK_Zone_12", ProjectionType.GSK_ZONE, meter_metrics),
    Projection("epsg:20913", "Зона 13 ГСК-2011/GSK-2011_GK_Zone_13", ProjectionType.GSK_ZONE, meter_metrics),
    Projection("epsg:20914", "Зона 14 ГСК-2011/GSK-2011_GK_Zone_14", ProjectionType.GSK_ZONE, meter_metrics),
    Projection("epsg:28404", "Зона 4 Pulkovo_1942_GK_Zone_4", ProjectionType.PULKOVO_ZONE, meter_metrics),
    Projection("epsg:28408", "Зона 8 Pulkovo_1942_GK_Zone_8", ProjectionType.PULKOVO_ZONE, meter_metrics),
    Projection("epsg:28409", "Зона 9 Pulkovo_1942_GK_Zone_9", ProjectionType.PULKOVO_ZONE, meter_metrics),
    Projection("epsg:28410", "Зона 10 Pulkovo_1942_GK_Zone_10", ProjectionType.PULKOVO_ZONE, meter_metrics),
    Projection("epsg:28411", "Зона 11 Pulkovo_1942_GK_Zone_11", ProjectionType.PULKOVO_ZONE, meter_metrics),
    Projection("epsg:28412", "Зона 12 Pulkovo_1942_GK_Zone_12", ProjectionType.PULKOVO_ZONE, meter_metrics),
    Projection("epsg:28413", "Зона 13 Pulkovo_1942_GK_Zone_13", ProjectionType.PULKOVO_ZONE, meter_metrics),
    Projection("epsg:28414", "Зона 14 Pulkovo_1942_GK_Zone_14", ProjectionType.PULKOVO_ZONE, meter_metrics),
    Projection("epsg:28415", "Зона 15 Pulkovo_1942_GK_Zone_15", ProjectionType.PULKOVO_ZONE, meter_metrics),
]
projections = [
    *intermediate_projections,
    *zone_projections,
]
projections_dict = {projection.mnemonic: projection for projection in projections}

dependencies = Graph({
    ProjectionType.GSK_ZONE: [ProjectionType.GSK],
    ProjectionType.GSK: [ProjectionType.GSK_ZONE, ProjectionType.PZ],
    ProjectionType.PZ: [ProjectionType.GSK, ProjectionType.PULKOVO],
    ProjectionType.PULKOVO: [ProjectionType.PZ, ProjectionType.PULKOVO_ZONE, ProjectionType.WGS],
    ProjectionType.PULKOVO_ZONE: [ProjectionType.PULKOVO],
    ProjectionType.WGS: [ProjectionType.PULKOVO],
})
