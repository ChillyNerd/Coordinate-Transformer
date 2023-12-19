from pyproj import CRS, Transformer


pulkovopz_str = (
    "proj=pipeline "
    "step proj=axisswap order=2,1 "
    "step proj=unitconvert xy_in=deg xy_out=rad "
    "step proj=push v_3 step proj=cart ellps=krass "
    "step proj=helmert x=23.557 y=-140.844 z=-79.778 rx=-0.0023 ry=-0.34646 rz=-0.79421 s=-0.228"
    " convention=coordinate_frame "
    "step inv proj=cart a=6378136 rf=298.25784 step proj=pop v_3 step proj=longlat a=6378136 rf=298.25784 "
    "step proj=unitconvert xy_in=rad xy_out=deg step proj=axisswap order=2,1"
)
pulkovopz_gost2017 = Transformer.from_pipeline(pulkovopz_str)

pulkovopz_str3 = (
    "proj=pipeline "
    "step proj=axisswap order=2,1 step proj=unitconvert xy_in=deg xy_out=rad "
    "step proj=push v_3 step proj=cart ellps=GSK2011 "
    "step proj=helmert x=0 y=0.014 z=-0.008 rx=-0.000562 ry=-0.000019 rz=0.000053 s=-0.0006"
    " convention=coordinate_frame "
    "step inv proj=cart a=6378136 rf=298.25784 "
    "step proj=pop v_3 step proj=longlat a=6378136 rf=298.25784 "
    "step proj=unitconvert xy_in=rad xy_out=deg step proj=axisswap order=2,1"
)
gskpz_gost2017 = Transformer.from_pipeline(pulkovopz_str3)


def transform(latitude, longitude, projection_from, projection_to):
    transformer = Transformer.from_crs(CRS(projection_from), CRS(projection_to))
    lat2, long2 = pulkovopz_gost2017.transform(latitude, longitude)
    lat3, long3 = gskpz_gost2017.transform(lat2, long2, direction='INVERSE')
    lat4, long4 = transformer.transform(lat3, long3)
    return {'lat3': lat3, 'long3': long3, 'lat4': lat4, 'long4': long4}
