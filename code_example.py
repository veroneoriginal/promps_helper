# pylint: skip-file
import re

data1 = """
Средство_1 : NATURA ,@#$%^&*:SIBERICA Био. S.O.S ВОССТАНОВЛЕНИЕ и УВЛАЖНЕНИЕ, 19000111815
Средство_2 : VICHY DERCOS DENSI-SOLUTIONS, 19760303700
Средство_3 : («DERMEDIC DERMEDIC CAPILARTE soothing shampoo for sensitive and irritated scalp, 19000023112
Средство_4 : OLLIN PROFESSIONAL BASIC LINE, 19000027320
Средство_5 : ARAVIA PROFESSIONAL Sensitive Skin Shampoo, 19000032946
Средство_6 : DAVINES LOVE CURL shampoo, 28140200002
"""

data2 = """
Набор_1 :
Средство_1 : KEVIN.MURPHY KILLER.CURLS WASH,  19000260883
Средство_2 : KEVIN.MURPHY KILLER.CURLS RINSE,  19000260882
Набор_2 :
Средство_1 : KEVIN.MURPHY PLUMPING, 19760327053
Средство_2 : KEVIN.MURPHY PLUMPING, 19760327054
"""

data3 = """
Набор_1:
Средство_1: KEVIN.MURPHY KILLER.CURLS WASH,  19000260883
Средство_2: KEVIN.MURPHY KILLER.CURLS RINSE,  19000260882
Набор_2:
Средство_1: KEVIN.MURPHY PLUMPING, 19760327053
Средство_2: KEVIN.MURPHY PLUMPING, 19760327054
"""

data4 = """
Средство_1  :  KEVIN.MURPHY KILLER.CURLS WASH,19000260883
Средство_2 :  KEVIN.MURPHY KILLER.CURLS RINSE,19000260882
"""
data5 = """
Исходное_средство : K18 leave-in molecular repair hair mask, 19000041719
Аналог_средство : LIMBA COSMETICS Instant Transformation, 19000279301
"""


def parse_collection_products_data(raw: str) -> dict:
    """
    Парсит средства подборки из строки
    :param raw: строка с средствами
    :return: словарь с средствами и артикулами
    """
    result = {}
    current_group = None
    raw = raw.strip().replace("«", "\"").replace("»", "\"")

    lines = [line.strip() for line in raw.splitlines() if line.strip()]

    group_header_pattern = re.compile(r'^(Набор_\d+)\s*:?\s*$')
    entry_pattern = re.compile(r'^([\wА-Яа-яёЁ_]+)\s*:\s*(.+?),\s*(\d+)$')

    for line in lines:
        group_match = group_header_pattern.match(line)
        entry_match = entry_pattern.match(line)

        if group_match:
            current_group = group_match.group(1)
            result[current_group] = {}
        elif entry_match:
            key, name, code = entry_match.groups()
            item = (name.strip(), code.strip())
            if current_group:
                result[current_group][key] = item
            else:
                result[key] = item
        else:
            message = f"⚠️ Не смог спарсить средство из подборки: {line}"
            print(message)
            raise ValueError(message)

    return result


res_1 = parse_collection_products_data(data1)
print(res_1)
print(type(res_1))

res_2 = parse_collection_products_data(data2)
print(res_2)
print(type(res_2))

res_3 = parse_collection_products_data(data3)
print(res_3)
print(type(res_3))

res_4 = parse_collection_products_data(data4)
print(res_4)
print(type(res_4))

res_5 = parse_collection_products_data(data5)
print(res_5)
print(type(res_5))
