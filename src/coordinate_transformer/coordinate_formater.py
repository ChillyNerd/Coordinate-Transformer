from src.coordinate_transformer.enums import OutputMetrics


def format_coordinate(metric, coordinate):
    if metric == OutputMetrics.ANGLE_DM.name:
        coordinate_deg = coordinate // 1
        coordinate_decmin = (coordinate - coordinate_deg) * 60
        return f'{int(coordinate_deg)}° {round(coordinate_decmin, ndigits=8)}\''
    if metric == OutputMetrics.ANGLE_DMS.name:
        coordinate_deg = coordinate // 1
        coordinate_min = ((coordinate - coordinate_deg) * 60) // 1
        coordinate_sec = ((coordinate - coordinate_deg) * 60 - coordinate_min) * 60
        return f'{int(coordinate_deg)}° {int(coordinate_min)}\' {round(coordinate_sec, ndigits=4)}"'
    return str(coordinate)
