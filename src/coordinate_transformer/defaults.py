class Projection:
    def __init__(self, mnemonic, comment):
        self.mnemonic = mnemonic
        self.comment = comment


projections_from = [
    Projection("epsg:4284", "Пулково 1942/Широта/Долгота"),
    Projection("epsg:7680", "Промежуточная проекция ПЗ 90-11/PZ90_11 "),
    Projection("epsg:7683", "ГСК-2011/GSK-2011")
]

projections_to = [
    Projection("epsg:20904", "Зона 4 ГСК-2011/GSK-2011_GK_Zone_4"),
    Projection("epsg:20908", "Зона 8 ГСК-2011/GSK-2011_GK_Zone_8"),
    Projection("epsg:20909", "Зона 9 ГСК-2011/GSK-2011_GK_Zone_9"),
    Projection("epsg:20910", "Зона 10 ГСК-2011/GSK-2011_GK_Zone_10"),
    Projection("epsg:20911", "Зона 11 ГСК-2011/GSK-2011_GK_Zone_11"),
    Projection("epsg:20912", "Зона 12 ГСК-2011/GSK-2011_GK_Zone_12"),
    Projection("epsg:20913", "Зона 13 ГСК-2011/GSK-2011_GK_Zone_13"),
    Projection("epsg:20914", "Зона 14 ГСК-2011/GSK-2011_GK_Zone_14"),
    Projection("epsg:28404", "Зона 4 Pulkovo_1942_GK_Zone_4"),
    Projection("epsg:28408", "Зона 8 Pulkovo_1942_GK_Zone_8"),
    Projection("epsg:28409", "Зона 9 Pulkovo_1942_GK_Zone_9"),
    Projection("epsg:28410", "Зона 10 Pulkovo_1942_GK_Zone_10"),
    Projection("epsg:28411", "Зона 11 Pulkovo_1942_GK_Zone_11"),
    Projection("epsg:28412", "Зона 12 Pulkovo_1942_GK_Zone_12"),
    Projection("epsg:28413", "Зона 13 Pulkovo_1942_GK_Zone_13"),
    Projection("epsg:28414", "Зона 14 Pulkovo_1942_GK_Zone_14"),
    Projection("epsg:28415", "Зона 15 Pulkovo_1942_GK_Zone_15")
]
