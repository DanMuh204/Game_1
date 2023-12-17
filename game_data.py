"""Этот модуль отвечает за переход на уровни и карты этих уровней"""
# X - плитки, состовляющие поверхность ; T - телепорт в overworld ; E - начальная позиция врагов; I - невидимые стены
level_1_map = [
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ',
'                                     ',
'X        B                         X ',
'XXX     XXX                    XXXXX ',
'XXXX           I  E I          XXXXX ',
'XXXXX           XXXX   X  I  E     TI',
'XXXXX  X                   XXXXXXXXX ',
'XXX           XXX     XXX         XX ',
'XX         X  X XXXXX             XX ',
'XX       XXX  XXXXXXXX      XXX   XX ',
'XXP     XXX   XXXXXXXXXXXX  XXX   XX ',
'XXXXXXXXXXX   XXXXXXXXXXX  XXX   XXX ',
'                                     ']
"""Этот список является картой уровня 1"""
level_2_map = [
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
'                                     ',
'                                     ',
'X      B                             ',
'X     XXX   X  X   X               XX',
'XXX                X            XXXXX',
'XXXX               X            XXXXX',
'XXXXXIE   I  X     XI  E I         T',
'XXXXXXXXXX      XXXXXXXXX     XXXXXXX',
'XXX           XXX          XX    XXXX',
'XX         X   XXXXXIE  I  XX      XX',
'XX      XXXX  XXXXXXXXXX    XXX   XXX',
'XXP    XXXX              X  XXX   XXX',
'XXXXXXXXXXX   XXXXXXXXXXX  XXX   XXXX',
'                                     '
]
"""Этот список является картой уровня 2"""
level_3_map = [
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
'XXXXXXXXXX                      XXXX',
'XXXXXXX            B               T',
'XXXXX        XI  E  IXXXXXXXXXXXXXXX',
'XXXX       XX  XXXXXXXXXXXXXXXXXXXXX',
'XXXX      XX  XXXXXXXXXXXXXXXXXXXXXX',
'XXXX     XX  XXXXXXXXXXXXXXXXXXXXXXX',
'XXXX           XXXXXXXXXXXXXXXXXXXXX',
'XXXXXXXX                      XXXXXX',
'XXXXXXXIE      P  I           XXXXXX',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
'                                    '
]
"""Этот список является картой уровня 3"""
level_4_map = [
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'                                        ',
'X                                      X',
'XP  BI     EE   E  EE   E   E     E  ITX',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
]
"""Этот список является картой уровня 4"""

level_0 = {'content': level_1_map, 'node_pos': (100, 400), 'unlock': 1}
"""
Этот словарь отвечает за подключение карты уровня 1, позиции его представления в overworld и открытии следующего уровня
"""
level_1 = {'content': level_2_map, 'node_pos': (400, 200), 'unlock': 2}
"""
Этот словарь отвечает за подключение карты уровня 2, позиции его представления в overworld и открытии следующего уровня
"""
level_2 = {'content': level_3_map, 'node_pos': (700, 400), 'unlock': 3}
"""
Этот словарь отвечает за подключение карты уровня 3, позиции его представления в overworld и открытии следующего уровня
"""
level_3 = {'content': level_4_map, 'node_pos': (1000, 200), 'unlock': 3}
"""
Этот словарь отвечает за подключение карты уровня 4, позиции его представления в overworld и открытии следующего уровня
"""

levels = {
	0: level_0,
	1: level_1,
	2: level_2,
	3: level_3
	}
"""Этот словарь отвечает за хранения информации об уровнях"""
