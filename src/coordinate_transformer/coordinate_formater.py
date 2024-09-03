from src.coordinate_transformer.enums import OutputMetrics


def format_coordinate(metric, coordinate):
    if metric == OutputMetrics.ANGLE_DM.name:
        coordinate_deg = coordinate // 1
        coordinate_min = (coordinate - coordinate_deg) * 60
        return f'{int(coordinate_deg)}° {round(coordinate_min, ndigits=8)}′'
    if metric == OutputMetrics.ANGLE_DMS.name:
        coordinate_deg = coordinate // 1
        coordinate_min = ((coordinate - coordinate_deg) * 60) // 1
        coordinate_sec = ((coordinate - coordinate_deg) * 60 - coordinate_min) * 60
        return f'{int(coordinate_deg)}° {int(coordinate_min)}′ {round(coordinate_sec, ndigits=4)}″'
    return str(coordinate)


def angle_to_float(degrees: int, minutes: int, seconds: int):
    return degrees + minutes / 60.0 + seconds / 3600.0


def string_angle_to_float(degrees: str, minutes: str, seconds: str = None):
    if seconds:
        return convert_to_float(degrees) + convert_to_float(minutes) / 60.0 + convert_to_float(seconds) / 3600.0
    return convert_to_float(degrees) + convert_to_float(minutes) / 60.0


def convert_to_float(value: str):
    return float(value.replace(',', '.'))
