from typing import Dict

from src.coordinate_transformer.enums import MetricType, ProjectionType, ProjectionGroup
from src.coordinate_transformer.impl import Projection, Graph

LUK_CRS = {
    "epsg:920904": ["Зона 4N ГСК-2011/GSK-2011_GK_Zone_4N",
                    "+proj=tmerc +lat_0=0 +lon_0=21 +k=1 +x_0=500000 +y_0=0 +ellps=GSK2011 +units=m +no_defs +type=crs",
                    "proj=pipeline step proj=axisswap order=2,1 step inv proj=tmerc lat_0=0 lon_0=21 k=1 x_0=500000 y_0=0 ellps=GSK2011 step proj=unitconvert xy_in=rad xy_out=deg step proj=axisswap order=2,1",
                    "proj=pipeline step proj=axisswap order=2,1 step proj=unitconvert xy_in=deg xy_out=rad step proj=tmerc lat_0=0 lon_0=21 k=1 x_0=500000 y_0=0 ellps=GSK2011 step proj=axisswap order=2,1"],
    "epsg:920908": ["Зона 8N ГСК-2011/GSK-2011_GK_Zone_8N",
                    "+proj=tmerc +lat_0=0 +lon_0=45 +k=1 +x_0=500000 +y_0=0 +ellps=GSK2011 +units=m +no_defs +type=crs",
                    "proj=pipeline step proj=axisswap order=2,1 step inv proj=tmerc lat_0=0 lon_0=45 k=1 x_0=500000 y_0=0 ellps=GSK2011 step proj=unitconvert xy_in=rad xy_out=deg step proj=axisswap order=2,1",
                    "proj=pipeline step proj=axisswap order=2,1 step proj=unitconvert xy_in=deg xy_out=rad step proj=tmerc lat_0=0 lon_0=45 k=1 x_0=500000 y_0=0 ellps=GSK2011 step proj=axisswap order=2,1"],
    "epsg:920909": ["Зона 9N ГСК-2011/GSK-2011_GK_Zone_9N",
                    "+proj=tmerc +lat_0=0 +lon_0=51 +k=1 +x_0=500000 +y_0=0 +ellps=GSK2011 +units=m +no_defs +type=crs",
                    "proj=pipeline step proj=axisswap order=2,1 step inv proj=tmerc lat_0=0 lon_0=51 k=1 x_0=500000 y_0=0 ellps=GSK2011 step proj=unitconvert xy_in=rad xy_out=deg step proj=axisswap order=2,1",
                    "proj=pipeline step proj=axisswap order=2,1 step proj=unitconvert xy_in=deg xy_out=rad step proj=tmerc lat_0=0 lon_0=51 k=1 x_0=500000 y_0=0 ellps=GSK2011 step proj=axisswap order=2,1"],
    "epsg:920910": ["Зона 10N ГСК-2011/GSK-2011_GK_Zone_10N",
                    "+proj=tmerc +lat_0=0 +lon_0=57 +k=1 +x_0=500000 +y_0=0 +ellps=GSK2011 +units=m +no_defs +type=crs",
                    "proj=pipeline step proj=axisswap order=2,1 step inv proj=tmerc lat_0=0 lon_0=57 k=1 x_0=500000 y_0=0 ellps=GSK2011 step proj=unitconvert xy_in=rad xy_out=deg step proj=axisswap order=2,1",
                    "proj=pipeline step proj=axisswap order=2,1 step proj=unitconvert xy_in=deg xy_out=rad step proj=tmerc lat_0=0 lon_0=57 k=1 x_0=500000 y_0=0 ellps=GSK2011 step proj=axisswap order=2,1"],
    "epsg:920911": ["Зона 11N ГСК-2011/GSK-2011_GK_Zone_11N",
                    "+proj=tmerc +lat_0=0 +lon_0=63 +k=1 +x_0=500000 +y_0=0 +ellps=GSK2011 +units=m +no_defs +type=crs",
                    "proj=pipeline step proj=axisswap order=2,1 step inv proj=tmerc lat_0=0 lon_0=63 k=1 x_0=500000 y_0=0 ellps=GSK2011 step proj=unitconvert xy_in=rad xy_out=deg step proj=axisswap order=2,1",
                    "proj=pipeline step proj=axisswap order=2,1 step proj=unitconvert xy_in=deg xy_out=rad step proj=tmerc lat_0=0 lon_0=63 k=1 x_0=500000 y_0=0 ellps=GSK2011 step proj=axisswap order=2,1"],
    "epsg:920912": ["Зона 12N ГСК-2011/GSK-2011_GK_Zone_12N",
                    "+proj=tmerc +lat_0=0 +lon_0=69 +k=1 +x_0=500000 +y_0=0 +ellps=GSK2011 +units=m +no_defs +type=crs",
                    "proj=pipeline step proj=axisswap order=2,1 step inv proj=tmerc lat_0=0 lon_0=69 k=1 x_0=500000 y_0=0 ellps=GSK2011 step proj=unitconvert xy_in=rad xy_out=deg step proj=axisswap order=2,1",
                    "proj=pipeline step proj=axisswap order=2,1 step proj=unitconvert xy_in=deg xy_out=rad step proj=tmerc lat_0=0 lon_0=69 k=1 x_0=500000 y_0=0 ellps=GSK2011 step proj=axisswap order=2,1"],
    "epsg:920913": ["Зона 13N ГСК-2011/GSK-2011_GK_Zone_13N",
                    "+proj=tmerc +lat_0=0 +lon_0=75 +k=1 +x_0=500000 +y_0=0 +ellps=GSK2011 +units=m +no_defs +type=crs",
                    "proj=pipeline step proj=axisswap order=2,1 step inv proj=tmerc lat_0=0 lon_0=75 k=1 x_0=500000 y_0=0 ellps=GSK2011 step proj=unitconvert xy_in=rad xy_out=deg step proj=axisswap order=2,1",
                    "proj=pipeline step proj=axisswap order=2,1 step proj=unitconvert xy_in=deg xy_out=rad step proj=tmerc lat_0=0 lon_0=75 k=1 x_0=500000 y_0=0 ellps=GSK2011 step proj=axisswap order=2,1"],
    "epsg:920914": ["Зона 14N ГСК-2011/GSK-2011_GK_Zone_14N",
                    "+proj=tmerc +lat_0=0 +lon_0=81 +k=1 +x_0=500000 +y_0=0 +ellps=GSK2011 +units=m +no_defs +type=crs",
                    "proj=pipeline step proj=axisswap order=2,1 step inv proj=tmerc lat_0=0 lon_0=81 k=1 x_0=500000 y_0=0 ellps=GSK2011 step proj=unitconvert xy_in=rad xy_out=deg step proj=axisswap order=2,1",
                    "proj=pipeline step proj=axisswap order=2,1 step proj=unitconvert xy_in=deg xy_out=rad step proj=tmerc lat_0=0 lon_0=81 k=1 x_0=500000 y_0=0 ellps=GSK2011 step proj=axisswap order=2,1"],
    "epsg:928404": ["Зона 4N Pulkovo_1942_GK_Zone_4N",
                    "+proj=tmerc +lat_0=0 +lon_0=21 +k=1 +x_0=500000 +y_0=0 +ellps=krass +units=m +no_defs +type=crs",
                    "proj=pipeline step proj=axisswap order=2,1 step inv proj=tmerc lat_0=0 lon_0=21 k=1 x_0=500000 y_0=0 ellps=krass step proj=unitconvert xy_in=rad xy_out=deg step proj=axisswap order=2,1",
                    "proj=pipeline step proj=axisswap order=2,1 step proj=unitconvert xy_in=deg xy_out=rad step proj=tmerc lat_0=0 lon_0=21 k=1 x_0=500000 y_0=0 ellps=krass step proj=axisswap order=2,1"],
    "epsg:928408": ["Зона 8N Pulkovo_1942_GK_Zone_8N",
                    "+proj=tmerc +lat_0=0 +lon_0=45 +k=1 +x_0=500000 +y_0=0 +ellps=krass +units=m +no_defs +type=crs",
                    "proj=pipeline step proj=axisswap order=2,1 step inv proj=tmerc lat_0=0 lon_0=45 k=1 x_0=500000 y_0=0 ellps=krass step proj=unitconvert xy_in=rad xy_out=deg step proj=axisswap order=2,1",
                    "proj=pipeline step proj=axisswap order=2,1 step proj=unitconvert xy_in=deg xy_out=rad step proj=tmerc lat_0=0 lon_0=45 k=1 x_0=500000 y_0=0 ellps=krass step proj=axisswap order=2,1"],
    "epsg:928409": ["Зона 9N Pulkovo_1942_GK_Zone_9N",
                    "+proj=tmerc +lat_0=0 +lon_0=51 +k=1 +x_0=500000 +y_0=0 +ellps=krass +units=m +no_defs +type=crs",
                    "proj=pipeline step proj=axisswap order=2,1 step inv proj=tmerc lat_0=0 lon_0=51 k=1 x_0=500000 y_0=0 ellps=krass step proj=unitconvert xy_in=rad xy_out=deg step proj=axisswap order=2,1",
                    "proj=pipeline step proj=axisswap order=2,1 step proj=unitconvert xy_in=deg xy_out=rad step proj=tmerc lat_0=0 lon_0=51 k=1 x_0=500000 y_0=0 ellps=krass step proj=axisswap order=2,1"],
    "epsg:928410": ["Зона 10N Pulkovo_1942_GK_Zone_10N",
                    "+proj=tmerc +lat_0=0 +lon_0=57 +k=1 +x_0=500000 +y_0=0 +ellps=krass +units=m +no_defs +type=crs",
                    "proj=pipeline step proj=axisswap order=2,1 step inv proj=tmerc lat_0=0 lon_0=57 k=1 x_0=500000 y_0=0 ellps=krass step proj=unitconvert xy_in=rad xy_out=deg step proj=axisswap order=2,1",
                    "proj=pipeline step proj=axisswap order=2,1 step proj=unitconvert xy_in=deg xy_out=rad step proj=tmerc lat_0=0 lon_0=57 k=1 x_0=500000 y_0=0 ellps=krass step proj=axisswap order=2,1"],
    "epsg:928411": ["Зона 11N Pulkovo_1942_GK_Zone_11N",
                    "+proj=tmerc +lat_0=0 +lon_0=63 +k=1 +x_0=500000 +y_0=0 +ellps=krass +units=m +no_defs +type=crs",
                    "proj=pipeline step proj=axisswap order=2,1 step inv proj=tmerc lat_0=0 lon_0=63 k=1 x_0=500000 y_0=0 ellps=krass step proj=unitconvert xy_in=rad xy_out=deg step proj=axisswap order=2,1",
                    "proj=pipeline step proj=axisswap order=2,1 step proj=unitconvert xy_in=deg xy_out=rad step proj=tmerc lat_0=0 lon_0=63 k=1 x_0=500000 y_0=0 ellps=krass step proj=axisswap order=2,1"],
    "epsg:928412": ["Зона 12N Pulkovo_1942_GK_Zone_12N",
                    "+proj=tmerc +lat_0=0 +lon_0=69 +k=1 +x_0=500000 +y_0=0 +ellps=krass +units=m +no_defs +type=crs",
                    "proj=pipeline step proj=axisswap order=2,1 step inv proj=tmerc lat_0=0 lon_0=69 k=1 x_0=500000 y_0=0 ellps=krass step proj=unitconvert xy_in=rad xy_out=deg step proj=axisswap order=2,1",
                    "proj=pipeline step proj=axisswap order=2,1 step proj=unitconvert xy_in=deg xy_out=rad step proj=tmerc lat_0=0 lon_0=69 k=1 x_0=500000 y_0=0 ellps=krass step proj=axisswap order=2,1"],
    "epsg:928413": ["Зона 13N Pulkovo_1942_GK_Zone_13N",
                    "+proj=tmerc +lat_0=0 +lon_0=75 +k=1 +x_0=500000 +y_0=0 +ellps=krass +units=m +no_defs +type=crs",
                    "proj=pipeline step proj=axisswap order=2,1 step inv proj=tmerc lat_0=0 lon_0=75 k=1 x_0=500000 y_0=0 ellps=krass step proj=unitconvert xy_in=rad xy_out=deg step proj=axisswap order=2,1",
                    "proj=pipeline step proj=axisswap order=2,1 step proj=unitconvert xy_in=deg xy_out=rad step proj=tmerc lat_0=0 lon_0=75 k=1 x_0=500000 y_0=0 ellps=krass step proj=axisswap order=2,1"],
    "epsg:928414": ["Зона 14N Pulkovo_1942_GK_Zone_14N",
                    "+proj=tmerc +lat_0=0 +lon_0=81 +k=1 +x_0=500000 +y_0=0 +ellps=krass +units=m +no_defs +type=crs",
                    "proj=pipeline step proj=axisswap order=2,1 step inv proj=tmerc lat_0=0 lon_0=81 k=1 x_0=500000 y_0=0 ellps=krass step proj=unitconvert xy_in=rad xy_out=deg step proj=axisswap order=2,1",
                    "proj=pipeline step proj=axisswap order=2,1 step proj=unitconvert xy_in=deg xy_out=rad step proj=tmerc lat_0=0 lon_0=81 k=1 x_0=500000 y_0=0 ellps=krass step proj=axisswap order=2,1"],
    "epsg:928415": ["Зона 15N Pulkovo_1942_GK_Zone_15N",
                    "+proj=tmerc +lat_0=0 +lon_0=87 +k=1 +x_0=500000 +y_0=0 +ellps=krass +units=m +no_defs +type=crs",
                    "proj=pipeline step proj=axisswap order=2,1 step inv proj=tmerc lat_0=0 lon_0=87 k=1 x_0=500000 y_0=0 ellps=krass step proj=unitconvert xy_in=rad xy_out=deg step proj=axisswap order=2,1",
                    "proj=pipeline step proj=axisswap order=2,1 step proj=unitconvert xy_in=deg xy_out=rad step proj=tmerc lat_0=0 lon_0=87 k=1 x_0=500000 y_0=0 ellps=krass step proj=axisswap order=2,1"],
    "epsg:999001": ["W-2 (УНГ- 63год)",
                    "+proj=tmerc +lat_0=0 +lon_0=66.05 +k=1 +x_0=500000 +y_0=6011057.625 +ellps=krass +units=m +no_defs +type=crs",
                    "proj=pipeline step proj=axisswap order=2,1 step inv proj=tmerc lat_0=0 lon_0=66.05 k=1 x_0=500000 y_0=-6011057.625 ellps=krass step proj=unitconvert xy_in=rad xy_out=deg step proj=axisswap order=2,1",
                    "proj=pipeline step proj=axisswap order=2,1 step proj=unitconvert xy_in=deg xy_out=rad step proj=tmerc lat_0=0 lon_0=66.05 k=1 x_0=500000 y_0=-6011057.625 ellps=krass step proj=axisswap order=2,1"],
    "epsg:999002": ["W-3 (КНГ+ПовхНГ- 63год)",
                    "+proj=tmerc +lat_0=0 +lon_0=72.05 +k=1 +x_0=500000 +y_0=6011057.625 +ellps=krass +units=m +no_defs +type=crs",
                    "proj=pipeline step proj=axisswap order=2,1 step inv proj=tmerc lat_0=0 lon_0=72.05 k=1 x_0=500000 y_0=-6011057.625 ellps=krass step proj=unitconvert xy_in=rad xy_out=deg step proj=axisswap order=2,1",
                    "proj=pipeline step proj=axisswap order=2,1 step proj=unitconvert xy_in=deg xy_out=rad step proj=tmerc lat_0=0 lon_0=72.05 k=1 x_0=500000 y_0=-6011057.625 ellps=krass step proj=axisswap order=2,1"],
    "epsg:999003": ["W-4 (ПНГ+ЛНГ- 63год)",
                    "+proj=tmerc +lat_0=0 +lon_0=78.05 +k=1 +x_0=500000 +y_0=6011057.625 +ellps=krass +units=m +no_defs +type=crs",
                    "proj=pipeline step proj=axisswap order=2,1 step inv proj=tmerc lat_0=0 lon_0=78.05 k=1 x_0=500000 y_0=-6011057.625 ellps=krass step proj=unitconvert xy_in=rad xy_out=deg step proj=axisswap order=2,1",
                    "proj=pipeline step proj=axisswap order=2,1 step proj=unitconvert xy_in=deg xy_out=rad step proj=tmerc lat_0=0 lon_0=78.05 k=1 x_0=500000 y_0=-6011057,625 ellps=krass step proj=axisswap order=2,1"],
    "epsg:999004": ["W-4-L (ЯНГ- 63год)",
                    "+proj=tmerc +lat_0=0 +lon_0=78.05 +k=1 +x_0=500000 +y_0=-70117057.625 +ellps=krass +units=m +no_defs +type=crs",
                    "proj=pipeline step proj=axisswap order=2,1 step inv proj=tmerc lat_0=0 lon_0=78.05 k=1 x_0=500000 y_0=-7011057.625 ellps=krass step proj=unitconvert xy_in=rad xy_out=deg step proj=axisswap order=2,1",
                    "proj=pipeline step proj=axisswap order=2,1 step proj=unitconvert xy_in=deg xy_out=rad step proj=tmerc lat_0=0 lon_0=78.05 k=1 x_0=500000 y_0=-7011057.625 ellps=krass step proj=axisswap order=2,1"]
}

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

intermediate_projections = [
    Projection("epsg:4326", "WGS84", ProjectionType.WGS, ProjectionGroup.WGS84_SK, metric_type=MetricType.ANGLE),
    Projection("epsg:9475", "ПЗ 90.11", ProjectionType.PZ, ProjectionGroup.PZ_SK, metric_type=MetricType.ANGLE,
               disabled=True),
    Projection("epsg:4284", "Пулково 1942/Широта/Долгота", ProjectionType.PULKOVO, ProjectionGroup.SK42_SK,
               metric_type=MetricType.ANGLE),
    Projection("epsg:7683", "ГСК-2011/GSK-2011", ProjectionType.GSK, ProjectionGroup.GSK_SK,
               metric_type=MetricType.ANGLE),
]
intermediate_projections_dict = {
    projection.projection_type: projection.mnemonic for projection in intermediate_projections
}
zone_projections = [
    Projection("epsg:20904", "Зона 4 ГСК-2011/GSK-2011_GK_Zone_4", ProjectionType.GSK_ZONE, ProjectionGroup.GSK_SK,
               metric_type=MetricType.METER),
    Projection("epsg:20908", "Зона 8 ГСК-2011/GSK-2011_GK_Zone_8", ProjectionType.GSK_ZONE, ProjectionGroup.GSK_SK,
               metric_type=MetricType.METER),
    Projection("epsg:20909", "Зона 9 ГСК-2011/GSK-2011_GK_Zone_9", ProjectionType.GSK_ZONE, ProjectionGroup.GSK_SK,
               metric_type=MetricType.METER),
    Projection("epsg:20910", "Зона 10 ГСК-2011/GSK-2011_GK_Zone_10", ProjectionType.GSK_ZONE, ProjectionGroup.GSK_SK,
               metric_type=MetricType.METER),
    Projection("epsg:20911", "Зона 11 ГСК-2011/GSK-2011_GK_Zone_11", ProjectionType.GSK_ZONE, ProjectionGroup.GSK_SK,
               metric_type=MetricType.METER),
    Projection("epsg:20912", "Зона 12 ГСК-2011/GSK-2011_GK_Zone_12", ProjectionType.GSK_ZONE, ProjectionGroup.GSK_SK,
               metric_type=MetricType.METER),
    Projection("epsg:20913", "Зона 13 ГСК-2011/GSK-2011_GK_Zone_13", ProjectionType.GSK_ZONE, ProjectionGroup.GSK_SK,
               metric_type=MetricType.METER),
    Projection("epsg:20914", "Зона 14 ГСК-2011/GSK-2011_GK_Zone_14", ProjectionType.GSK_ZONE, ProjectionGroup.GSK_SK,
               metric_type=MetricType.METER),
    Projection("epsg:920904", "Зона 4N ГСК-2011/GSK-2011_GK_Zone_4N", ProjectionType.GSK_NZONE, ProjectionGroup.GSK_SK,
               metric_type=MetricType.METER),
    Projection("epsg:920908", "Зона 8N ГСК-2011/GSK-2011_GK_Zone_8N", ProjectionType.GSK_NZONE, ProjectionGroup.GSK_SK,
               metric_type=MetricType.METER),
    Projection("epsg:920909", "Зона 9N ГСК-2011/GSK-2011_GK_Zone_9N", ProjectionType.GSK_NZONE, ProjectionGroup.GSK_SK,
               metric_type=MetricType.METER),
    Projection("epsg:920910", "Зона 10N ГСК-2011/GSK-2011_GK_Zone_10N", ProjectionType.GSK_NZONE,
               ProjectionGroup.GSK_SK, metric_type=MetricType.METER),
    Projection("epsg:920911", "Зона 11N ГСК-2011/GSK-2011_GK_Zone_11N", ProjectionType.GSK_NZONE,
               ProjectionGroup.GSK_SK, metric_type=MetricType.METER),
    Projection("epsg:920912", "Зона 12N ГСК-2011/GSK-2011_GK_Zone_12N", ProjectionType.GSK_NZONE,
               ProjectionGroup.GSK_SK, metric_type=MetricType.METER),
    Projection("epsg:920913", "Зона 13N ГСК-2011/GSK-2011_GK_Zone_13N", ProjectionType.GSK_NZONE,
               ProjectionGroup.GSK_SK, metric_type=MetricType.METER),
    Projection("epsg:920914", "Зона 14N ГСК-2011/GSK-2011_GK_Zone_14N", ProjectionType.GSK_NZONE,
               ProjectionGroup.GSK_SK, metric_type=MetricType.METER),
    Projection("epsg:28404", "Зона 4 Pulkovo_1942_GK_Zone_4", ProjectionType.PULKOVO_ZONE, ProjectionGroup.SK42_SK,
               metric_type=MetricType.METER),
    Projection("epsg:28408", "Зона 8 Pulkovo_1942_GK_Zone_8", ProjectionType.PULKOVO_ZONE, ProjectionGroup.SK42_SK,
               metric_type=MetricType.METER),
    Projection("epsg:28409", "Зона 9 Pulkovo_1942_GK_Zone_9", ProjectionType.PULKOVO_ZONE, ProjectionGroup.SK42_SK,
               metric_type=MetricType.METER),
    Projection("epsg:28410", "Зона 10 Pulkovo_1942_GK_Zone_10", ProjectionType.PULKOVO_ZONE, ProjectionGroup.SK42_SK,
               metric_type=MetricType.METER),
    Projection("epsg:28411", "Зона 11 Pulkovo_1942_GK_Zone_11", ProjectionType.PULKOVO_ZONE, ProjectionGroup.SK42_SK,
               metric_type=MetricType.METER),
    Projection("epsg:28412", "Зона 12 Pulkovo_1942_GK_Zone_12", ProjectionType.PULKOVO_ZONE, ProjectionGroup.SK42_SK,
               metric_type=MetricType.METER),
    Projection("epsg:28413", "Зона 13 Pulkovo_1942_GK_Zone_13", ProjectionType.PULKOVO_ZONE, ProjectionGroup.SK42_SK,
               metric_type=MetricType.METER),
    Projection("epsg:28414", "Зона 14 Pulkovo_1942_GK_Zone_14", ProjectionType.PULKOVO_ZONE, ProjectionGroup.SK42_SK,
               metric_type=MetricType.METER),
    Projection("epsg:28415", "Зона 15 Pulkovo_1942_GK_Zone_15", ProjectionType.PULKOVO_ZONE, ProjectionGroup.SK42_SK,
               metric_type=MetricType.METER),
    Projection("epsg:928404", "Зона 4N Pulkovo_1942_GK_Zone_4N", ProjectionType.PULKOVO_NZONE, ProjectionGroup.SK42_SK,
               metric_type=MetricType.METER),
    Projection("epsg:928408", "Зона 8N Pulkovo_1942_GK_Zone_8N", ProjectionType.PULKOVO_NZONE, ProjectionGroup.SK42_SK,
               metric_type=MetricType.METER),
    Projection("epsg:928409", "Зона 9N Pulkovo_1942_GK_Zone_9N", ProjectionType.PULKOVO_NZONE, ProjectionGroup.SK42_SK,
               metric_type=MetricType.METER),
    Projection("epsg:928410", "Зона 10N Pulkovo_1942_GK_Zone_10N", ProjectionType.PULKOVO_NZONE,
               ProjectionGroup.SK42_SK, metric_type=MetricType.METER),
    Projection("epsg:928411", "Зона 11N Pulkovo_1942_GK_Zone_11N", ProjectionType.PULKOVO_NZONE,
               ProjectionGroup.SK42_SK, metric_type=MetricType.METER),
    Projection("epsg:928412", "Зона 12N Pulkovo_1942_GK_Zone_12N", ProjectionType.PULKOVO_NZONE,
               ProjectionGroup.SK42_SK, metric_type=MetricType.METER),
    Projection("epsg:928413", "Зона 13N Pulkovo_1942_GK_Zone_13N", ProjectionType.PULKOVO_NZONE,
               ProjectionGroup.SK42_SK, metric_type=MetricType.METER),
    Projection("epsg:928414", "Зона 14N Pulkovo_1942_GK_Zone_14N", ProjectionType.PULKOVO_NZONE,
               ProjectionGroup.SK42_SK, metric_type=MetricType.METER),
    Projection("epsg:928415", "Зона 15N Pulkovo_1942_GK_Zone_15N", ProjectionType.PULKOVO_NZONE,
               ProjectionGroup.SK42_SK, metric_type=MetricType.METER),
    Projection("epsg:999001", "W-2 (УНГ- 63год)", ProjectionType.PULKOVO_NZONE, ProjectionGroup.SK63_SK,
               metric_type=MetricType.METER),
    Projection("epsg:999002", "W-3 (КНГ+ПовхНГ- 63год)", ProjectionType.PULKOVO_NZONE, ProjectionGroup.SK63_SK,
               metric_type=MetricType.METER),
    Projection("epsg:999003", "W-4 (ПНГ+ЛНГ- 63год)", ProjectionType.PULKOVO_NZONE, ProjectionGroup.SK63_SK,
               metric_type=MetricType.METER),
    Projection("epsg:999004", "W-4-L (ЯНГ- 63год)", ProjectionType.PULKOVO_NZONE, ProjectionGroup.SK63_SK,
               metric_type=MetricType.METER),
]
projections = [
    *intermediate_projections,
    *zone_projections,
]
projections_dict: Dict[str, Projection] = {projection.mnemonic: projection for projection in projections}

dependencies = Graph({
    ProjectionType.GSK_ZONE: [ProjectionType.GSK],
    ProjectionType.GSK_NZONE: [ProjectionType.GSK],
    ProjectionType.GSK: [ProjectionType.GSK_ZONE, ProjectionType.PZ, ProjectionType.GSK_NZONE],
    ProjectionType.PZ: [ProjectionType.GSK, ProjectionType.PULKOVO],
    ProjectionType.PULKOVO: [ProjectionType.PZ, ProjectionType.PULKOVO_ZONE, ProjectionType.WGS,
                             ProjectionType.PULKOVO63_ZONE, ProjectionType.PULKOVO_NZONE],
    ProjectionType.PULKOVO_ZONE: [ProjectionType.PULKOVO],
    ProjectionType.PULKOVO_NZONE: [ProjectionType.PULKOVO],
    ProjectionType.WGS: [ProjectionType.PULKOVO],
    ProjectionType.PULKOVO63_ZONE: [ProjectionType.PULKOVO],
})
