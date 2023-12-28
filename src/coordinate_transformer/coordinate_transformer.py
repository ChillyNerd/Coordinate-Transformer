from pyproj import CRS, Transformer, transform
from src.coordinate_transformer.transform_exception import NotImplementedYet

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
gskz4 = Transformer.from_crs("epsg:7683",
                             "epsg:20904")  # создаем процедуру расчета метровых координат для 4 зоны ГСК-2011/GSK-2011_GK_Zone_4
gskz8 = Transformer.from_crs("epsg:7683",
                             "epsg:20908")  # создаем процедуру расчета метровых координат для 8 зоны ГСК-2011/GSK-2011_GK_Zone_8
gskz9 = Transformer.from_crs("epsg:7683",
                             "epsg:20909")  # создаем процедуру расчета метровых координат для 9 зоны ГСК-2011/GSK-2011_GK_Zone_9
gskz10 = Transformer.from_crs("epsg:7683",
                              "epsg:20910")  # создаем процедуру расчета метровых координат для 10 зоны ГСК-2011/GSK-2011_GK_Zone_10
gskz11 = Transformer.from_crs("epsg:7683",
                              "epsg:20911")  # создаем процедуру расчета метровых координат для 11 зоны ГСК-2011/GSK-2011_GK_Zone_11
gskz12 = Transformer.from_crs("epsg:7683",
                              "epsg:20912")  # создаем процедуру расчета метровых координат для 12 зоны ГСК-2011/GSK-2011_GK_Zone_12
gskz13 = Transformer.from_crs("epsg:7683",
                              "epsg:20913")  # создаем процедуру расчета метровых координат для 13 зоны ГСК-2011/GSK-2011_GK_Zone_13
gskz14 = Transformer.from_crs("epsg:7683",
                              "epsg:20914")  # создаем процедуру расчета метровых координат для 14 зоны ГСК-2011/GSK-2011_GK_Zone_14
pulkovoz4=Transformer.from_crs("epsg:4284","epsg:28404")    # создаем процедуру расчета метровых координат для Pulkovo_1942_GK_Zone_4
pulkovoz8=Transformer.from_crs("epsg:4284","epsg:28408")    # создаем процедуру расчета метровых координат для Pulkovo_1942_GK_Zone_8
pulkovoz9=Transformer.from_crs("epsg:4284","epsg:28409")    # создаем процедуру расчета метровых координат для Pulkovo_1942_GK_Zone_9
pulkovoz10=Transformer.from_crs("epsg:4284","epsg:28410")    # создаем процедуру расчета метровых координат для Pulkovo_1942_GK_Zone_10
pulkovoz11=Transformer.from_crs("epsg:4284","epsg:28411")    # создаем процедуру расчета метровых координат для Pulkovo_1942_GK_Zone_11
pulkovoz12=Transformer.from_crs("epsg:4284","epsg:28412")    # создаем процедуру расчета метровых координат для Pulkovo_1942_GK_Zone_12
pulkovoz13=Transformer.from_crs("epsg:4284","epsg:28413")    # создаем процедуру расчета метровых координат для Pulkovo_1942_GK_Zone_13
pulkovoz14=Transformer.from_crs("epsg:4284","epsg:28414")    # создаем процедуру расчета метровых координат для Pulkovo_1942_GK_Zone_14
pulkovoz15=Transformer.from_crs("epsg:4284","epsg:28415")    # создаем процедуру расчета метровых координат для Pulkovo_1942_GK_Zone_15


def trans(latitude, longitude, projection_from, projection_to):
    if projection_from == "epsg:4284" and projection_to == "epsg:20904":
        lat2, long2 = pulkovopz_gost2017.transform(latitude, longitude)  # пересчитываем координаты в ПЗ 90-11/PZ90_11
        lat3, long3 = gskpz_gost2017.transform(lat2, long2,
                                               direction='INVERSE')  # пересчитываем координаты в ГСК-2011/GSK-2011 (Zone_id = 64), параметры direction='INVERSE' обязателен
        lat4, long4 = gskz4.transform(lat3, long3)  # пересчитываем координаты в ГСК-2011 зона 4/GSK-2011_GK_Zone_4
    elif projection_from == "epsg:4284" and projection_to == "epsg:20908":
        lat2, long2 = pulkovopz_gost2017.transform(latitude, longitude)  # пересчитываем координаты в ПЗ 90-11/PZ90_11
        lat3, long3 = gskpz_gost2017.transform(lat2, long2,
                                               direction='INVERSE')  # пересчитываем координаты в ГСК-2011/GSK-2011 (Zone_id = 64), параметры direction='INVERSE' обязателен
        lat4, long4 = gskz8.transform(lat3, long3)  # пересчитываем координаты в ГСК-2011 зона 8/GSK-2011_GK_Zone_8
    elif projection_from == "epsg:4284" and projection_to == "epsg:20909":
        lat2, long2 = pulkovopz_gost2017.transform(latitude, longitude)  # пересчитываем координаты в ПЗ 90-11/PZ90_11
        lat3, long3 = gskpz_gost2017.transform(lat2, long2,
                                               direction='INVERSE')  # пересчитываем координаты в ГСК-2011/GSK-2011 (Zone_id = 64), параметры direction='INVERSE' обязателен
        lat4, long4 = gskz9.transform(lat3, long3)  # пересчитываем координаты в ГСК-2011 зона 9/GSK-2011_GK_Zone_9
    elif projection_from == "epsg:4284" and projection_to == "epsg:20910":
        lat2, long2 = pulkovopz_gost2017.transform(latitude, longitude)  # пересчитываем координаты в ПЗ 90-11/PZ90_11
        lat3, long3 = gskpz_gost2017.transform(lat2, long2,
                                               direction='INVERSE')  # пересчитываем координаты в ГСК-2011/GSK-2011 (Zone_id = 64), параметры direction='INVERSE' обязателен
        lat4, long4 = gskz10.transform(lat3, long3)  # пересчитываем координаты в ГСК-2011 зона 10/GSK-2011_GK_Zone_10
    elif projection_from == "epsg:4284" and projection_to == "epsg:20911":
        lat2, long2 = pulkovopz_gost2017.transform(latitude, longitude)  # пересчитываем координаты в ПЗ 90-11/PZ90_11
        lat3, long3 = gskpz_gost2017.transform(lat2, long2,
                                               direction='INVERSE')  # пересчитываем координаты в ГСК-2011/GSK-2011 (Zone_id = 64), параметры direction='INVERSE' обязателен
        lat4, long4 = gskz11.transform(lat3, long3)  # пересчитываем координаты в ГСК-2011 зона 11/GSK-2011_GK_Zone_11
    elif projection_from == "epsg:4284" and projection_to == "epsg:20912":
        lat2, long2 = pulkovopz_gost2017.transform(latitude, longitude)  # пересчитываем координаты в ПЗ 90-11/PZ90_11
        lat3, long3 = gskpz_gost2017.transform(lat2, long2,
                                               direction='INVERSE')  # пересчитываем координаты в ГСК-2011/GSK-2011 (Zone_id = 64), параметры direction='INVERSE' обязателен
        lat4, long4 = gskz12.transform(lat3, long3)  # пересчитываем координаты в ГСК-2011 зона 12/GSK-2011_GK_Zone_12
    elif projection_from == "epsg:4284" and projection_to == "epsg:20913":
        lat2, long2 = pulkovopz_gost2017.transform(latitude, longitude)  # пересчитываем координаты в ПЗ 90-11/PZ90_11
        lat3, long3 = gskpz_gost2017.transform(lat2, long2,
                                               direction='INVERSE')  # пересчитываем координаты в ГСК-2011/GSK-2011 (Zone_id = 64), параметры direction='INVERSE' обязателен
        lat4, long4 = gskz13.transform(lat3, long3)  # пересчитываем координаты в ГСК-2011 зона 13/GSK-2011_GK_Zone_13 
    elif projection_from == "epsg:4284" and projection_to == "epsg:20914":
        lat2, long2 = pulkovopz_gost2017.transform(latitude, longitude)  # пересчитываем координаты в ПЗ 90-11/PZ90_11
        lat3, long3 = gskpz_gost2017.transform(lat2, long2,
                                               direction='INVERSE')  # пересчитываем координаты в ГСК-2011/GSK-2011 (Zone_id = 64), параметры direction='INVERSE' обязателен
        lat4, long4 = gskz14.transform(lat3, long3)  # пересчитываем координаты в ГСК-2011 зона 14/GSK-2011_GK_Zone_14 
    elif projection_from == "epsg:4284" and projection_to == "epsg:7683":
        lat2, long2 = pulkovopz_gost2017.transform(latitude, longitude)  # пересчитываем координаты в ПЗ 90-11/PZ90_11
        lat4, long4 = gskpz_gost2017.transform(lat2, long2,
                                               direction='INVERSE')  # пересчитываем координаты в ГСК-2011/GSK-2011 (Zone_id = 64), параметры direction='INVERSE' обязателен
    elif projection_from == "epsg:7683" and projection_to == "epsg:28404":
        lat2, long2 = gskpz_gost2017.transform(latitude, longitude)   # расчет координат в ПЗ 90-11/PZ90_11 (Добавить зону в справочник wellref.zone)
        lat3, long3 = pulkovopz_gost2017.transform(lat2, long2, direction='INVERSE')    # расчет координат в Пулково 1942/Широта/Долгота (десятичные градусы) (Zone_id = 20), параметры direction='INVERSE' обязателен
        lat4, long4 = gskz4.transform(lat3, long3)   # пересчитываем координаты в ГСК-2011 зона 4/GSK-2011_GK_Zone_4
    elif projection_from == "epsg:7683" and projection_to == "epsg:28408":
        lat2, long2 = pulkovopz_gost2017.transform(latitude, longitude)  # пересчитываем координаты в ПЗ 90-11/PZ90_11
        lat3, long3 = gskpz_gost2017.transform(lat2, long2,
                                               direction='INVERSE')  # пересчитываем координаты в ГСК-2011/GSK-2011 (Zone_id = 64), параметры direction='INVERSE' обязателен
        lat4, long4 = gskz8.transform(lat3, long3)  # пересчитываем координаты в ГСК-2011 зона 8/GSK-2011_GK_Zone_8
    elif projection_from == "epsg:7683" and projection_to == "epsg:28409":
        lat2, long2 = pulkovopz_gost2017.transform(latitude, longitude)  # пересчитываем координаты в ПЗ 90-11/PZ90_11
        lat3, long3 = gskpz_gost2017.transform(lat2, long2,
                                               direction='INVERSE')  # пересчитываем координаты в ГСК-2011/GSK-2011 (Zone_id = 64), параметры direction='INVERSE' обязателен
        lat4, long4 = gskz9.transform(lat3, long3)  # пересчитываем координаты в ГСК-2011 зона 9/GSK-2011_GK_Zone_9
    elif projection_from == "epsg:7683" and projection_to == "epsg:28410":
        lat2, long2 = pulkovopz_gost2017.transform(latitude, longitude)  # пересчитываем координаты в ПЗ 90-11/PZ90_11
        lat3, long3 = gskpz_gost2017.transform(lat2, long2,
                                               direction='INVERSE')  # пересчитываем координаты в ГСК-2011/GSK-2011 (Zone_id = 64), параметры direction='INVERSE' обязателен
        lat4, long4 = gskz10.transform(lat3, long3)  # пересчитываем координаты в ГСК-2011 зона 10/GSK-2011_GK_Zone_10
    elif projection_from == "epsg:7683" and projection_to == "epsg:28411":
        lat2, long2 = pulkovopz_gost2017.transform(latitude, longitude)  # пересчитываем координаты в ПЗ 90-11/PZ90_11
        lat3, long3 = gskpz_gost2017.transform(lat2, long2,
                                               direction='INVERSE')  # пересчитываем координаты в ГСК-2011/GSK-2011 (Zone_id = 64), параметры direction='INVERSE' обязателен
        lat4, long4 = gskz11.transform(lat3, long3)  # пересчитываем координаты в ГСК-2011 зона 11/GSK-2011_GK_Zone_11
    elif projection_from == "epsg:7683" and projection_to == "epsg:28412":
        lat2, long2 = pulkovopz_gost2017.transform(latitude, longitude)  # пересчитываем координаты в ПЗ 90-11/PZ90_11
        lat3, long3 = gskpz_gost2017.transform(lat2, long2,
                                               direction='INVERSE')  # пересчитываем координаты в ГСК-2011/GSK-2011 (Zone_id = 64), параметры direction='INVERSE' обязателен
        lat4, long4 = gskz12.transform(lat3, long3)  # пересчитываем координаты в ГСК-2011 зона 12/GSK-2011_GK_Zone_12
    elif projection_from == "epsg:7683" and projection_to == "epsg:28413":
        lat2, long2 = pulkovopz_gost2017.transform(latitude, longitude)  # пересчитываем координаты в ПЗ 90-11/PZ90_11
        lat3, long3 = gskpz_gost2017.transform(lat2, long2,
                                               direction='INVERSE')  # пересчитываем координаты в ГСК-2011/GSK-2011 (Zone_id = 64), параметры direction='INVERSE' обязателен
        lat4, long4 = gskz13.transform(lat3, long3)  # пересчитываем координаты в ГСК-2011 зона 13/GSK-2011_GK_Zone_13
    elif projection_from == "epsg:7683" and projection_to == "epsg:28414":
        lat2, long2 = pulkovopz_gost2017.transform(latitude, longitude)  # пересчитываем координаты в ПЗ 90-11/PZ90_11
        lat3, long3 = gskpz_gost2017.transform(lat2, long2,
                                               direction='INVERSE')  # пересчитываем координаты в ГСК-2011/GSK-2011 (Zone_id = 64), параметры direction='INVERSE' обязателен
        lat4, long4 = gskz14.transform(lat3, long3)  # пересчитываем координаты в ГСК-2011 зона 14/GSK-2011_GK_Zone_14
    elif (projection_from in ["epsg:28414","epsg:28413","epsg:28412","epsg:28411","epsg:28410","epsg:28409","epsg:28408","epsg:28404", "epsg:4284"] and
          projection_to in ["epsg:28414","epsg:28413","epsg:28412","epsg:28411","epsg:28410","epsg:28409","epsg:28408","epsg:28404", "epsg:4284"]):
        lat4, long4 = transform(projection_from, projection_to, latitude, longitude)
    elif (projection_from in ["epsg:20914","epsg:20913","epsg:20912","epsg:20911","epsg:20910","epsg:20909","epsg:20908","epsg:20904", "epsg:7683"] and
          projection_to in ["epsg:20914","epsg:20913","epsg:20912","epsg:20911","epsg:20910","epsg:20909","epsg:20908","epsg:20904", "epsg:7683"]):
        lat4, long4 = transform(projection_from, projection_to, latitude, longitude)
    elif (projection_from in ["epsg:20914","epsg:20913","epsg:20912","epsg:20911","epsg:20910","epsg:20909","epsg:20908", "epsg:20904"] and
          projection_to in ["epsg:28414","epsg:28413","epsg:28412","epsg:28411","epsg:28410","epsg:28409","epsg:28408","epsg:28404"]):
        lat2, long2 = transform(projection_from, "epsg:7683", latitude, longitude)
        lat4, long4 = trans(lat2, long2, "epsg:7683", projection_to)
    else:
        raise NotImplementedYet()
    return lat4, long4
