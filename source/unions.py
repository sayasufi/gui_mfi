import struct


def dict_to_byte(dcit_name):
    s = ""
    for value in dcit_name.values():
        s += str(value)
    s = s[::-1]
    bit_string = int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')
    return bit_string[::-1]


class Unions:
    def __init__(self):
        self.sds1 = {
            "vpnp_valid": 0x01,  # Исправность ВПНП
            "vpnp_fail": 0,  # Отказ ВПНП
            "data_failure": 0,  # Отказ данных от ВС
            "data_link": 0,  # Нет данных от ВС
            "built_in_test": 0x01,  # Тест начального включения
            "ground_test": 0,  # Наземный контроль
            "wait": 0,  # Ожидание
            "nav": 0,  # Навигация
            "bit9": 0,
            "bit10": 0,
            "bit11": 0,
            "bit12": 0,
            "mfi10_link_fail": 0,  # Нет данных от МФИ-10
            "mfi12l_link_fail": 0,  # Нет данных от МФИ-12 левый
            "mfi12r_link_fail": 0,  # Нет данных от МФИ-12 правый
            "prep_done": 0,  # Подготовка завершена
        }

        self.sds2 = {
            "cdmk_valid": 1,  # Исправность ЦДМК
            "cdmk_failure": 0,  # Отказ ЦДМК
            "cdmk_link": 1,  # Наличие связи с ЦДМК по CAN
            "bit4": 0,
            "ufos1_valid": 1,  # Исправность УФОС-01 №1
            "ufos1_failure": 0,  # Отказ УФОС-01 №1
            "fos1_link": 1,  # Наличие связи с УФОС-01 по CAN №1
            "ufos1_work": 1,  # УФОС-01 №1 в режиме "Работа"
            "ufos2_valid": 1,  # Исправность УФОС-01 №2
            "ufos2_failure": 0,  # Отказ УФОС-01 №2
            "ufos2_link": 1,  # Наличие связи с УФОС-01 по CAN №2
            "ufos2_work": 1,  # УФОС-01 №2 в режиме "Работа"
            "bit13": 0,
            "bit14": 0,
            "bit15": 0,
            "bit16": 0,
        }

        self.sds3 = {
            "setup": 0,  # Выставка
            "bit_2": 0,
            "bit_3": 0,
            "adjust": 0,  # Режим Юстировка
            "adjust_auto": 0,  # Ведется автоматическая юстировка
            "adjust_heading": 0,  # Ведется ручная юстировка курса
            "adjust_pitch": 0,  # Ведется ручная юстировка тангажа
            "adjust_roll": 0,  # Ведется ручная юстировка крена
            "adjust_reset": 0,  # Сброс юстировочных значений
            "adjust_reset_heading": 0,  # Сброс юстировочных значений курса
            "adjust_reset_pitch": 0,  # Сброс юстировочных значений тангажа
            "adjust_reset_roll": 0,  # Сброс юстировочных значений крена
            "bit_13": 0,
            "bit_14": 0,
            "bit_15": 0,
            "bit_16": 0,
        }

        self.sds2X = {
            "baro0": 0,  # Текущая коррекция баровысоты[0]
            "baro1": 0,  # Текущая коррекция баровысоты[1]
            "baro_update": 0,  # Признак "Данные коррекции баровысоты обновлены"
            "bit4": 0,
            "ufos1_valid": 0,
            "ufos1_failure": 0,
            "ufos1_link": 0,
            "ufos1_work": 0,
            "ufos2_valid": 0,
            "ufos2_failure": 0,
            "ufos2_link": 0,
            "ufos2_work": 0,
            "bit13": 0,
            "bit14": 0,
            "bit15": 0,
            "bit16": 0,
        }

        self.sds3X = {
            "ailerons_trim_n": 0,  # Нейтральное положение триммера элеронов
            "elevator_trim_n": 0,  # Нейтральное положение триммера РВ
            "rudder_trim_n": 0,  # Нейтральное положение триммера РН
            "engine_start": 0,  # Запуск двигателя
            "manual_mode": 0,  # Ручной режим
            "wow": 0,  # Шасси обжато
            "apu_start": 0,  # ВСУ Запуск
            "apu_work": 0,  # ВСУ Работа
            "engine_fire": 0,  # Пожар двигатель
            "apu_fire": 0,  # ВСУ Пожар
            "engine_failure": 0,  # Отказ двигателя
            "generator_fail": 0,  # Отказ генератора
            "bit13": 0,
            "bit14": 0,
            "bit15": 0,
            "bit16": 0,
        }

        # Упаковка данных в бинарный формат
        self.sds1_data = dict_to_byte(self.sds1)
        self.sds2_data = dict_to_byte(self.sds2)
        self.sds3_data = dict_to_byte(self.sds3)
        self.sds2X_data = dict_to_byte(self.sds2X)
        self.sds3X_data = dict_to_byte(self.sds3X)

        self.sds_01_p1 = {
            "arinc": 0b10001010,  # Восьмеричный код 277
            "id": 0b00,  # Идентификатор
            "vpnp_valid": 0,  # Признак «Исправность ВПНП»
            "vpnp_fail": 0,  # Признак «Отказ ВПНП»
            "data_miss_ch1": 0,  # Признак «Нет данных от ВС» КЛС 1
            "data_fail_ch1": 0,  # Признак «Отказ данных от ВС» КЛС 1
            "data_miss_ch2": 0,  # Признак «Нет данных от ВС» КЛС 2
            "data_fail_ch2": 0,  # Признак «Отказ данных от ВС» КЛС 2
            "_res0": 0,  # Резерв
            "_res1": 0,  # Резерв
            "_res2": 0,  # Резерв
            "_res3": 0,  # Резерв
            "start_test": 0,  # Признак «Тест начального включения»
            "ground": 0,  # Признак «Наземный контроль»
            "setup": 0,  # Признак «Выставка»
            "nav": 0,  # Признак «Навигация»
            "wait": 0,  # Признак «Ожидание»
            "bche_ins": 0,  # Признак «Подогрев БЧЭ ИНС»
            "vpnp_type": 0b00,  # Тип «ВПНП»
            "_res5": 0,  # Резерв
            "matrix": 0b00,  # Матрица состояния СДС (см. табл. 4)
            "parity": 0,  # Дополнение до четности
        }

        self.sds_01_p1_struct = (
                (self.sds_01_p1["arinc"] << 24)
                | (self.sds_01_p1["id"] << 22)
                | (self.sds_01_p1["vpnp_valid"] << 21)
                | (self.sds_01_p1["vpnp_fail"] << 20)
                | (self.sds_01_p1["data_miss_ch1"] << 19)
                | (self.sds_01_p1["data_fail_ch1"] << 18)
                | (self.sds_01_p1["data_miss_ch2"] << 17)
                | (self.sds_01_p1["data_fail_ch2"] << 16)
                | (self.sds_01_p1["_res0"] << 15)
                | (self.sds_01_p1["_res1"] << 14)
                | (self.sds_01_p1["_res2"] << 13)
                | (self.sds_01_p1["_res3"] << 12)
                | (self.sds_01_p1["start_test"] << 11)
                | (self.sds_01_p1["ground"] << 10)
                | (self.sds_01_p1["setup"] << 9)
                | (self.sds_01_p1["nav"] << 8)
                | (self.sds_01_p1["wait"] << 7)
                | (self.sds_01_p1["bche_ins"] << 6)
                | (self.sds_01_p1["vpnp_type"] << 4)
                | (self.sds_01_p1["_res5"] << 3)
                | (self.sds_01_p1["matrix"] << 1)
                | self.sds_01_p1["parity"]
        )

        self.sds_02_p1 = {
            "arinc": 0b10111001,  # Восьмеричный код 277
            "id": 0b00,  # Идентификатор
            "sns": 0,  # Признак «Коррекция по СНС»
            "svs": 0,  # Признак «Коррекция по СВС»
            "dmk": 0,  # Признак «Коррекция по ДМК»
            "low_accuracy": 0,  # Признак «Пониженная точность»
            "_res0": 0,  # Резерв
            "_res1": 0,  # Резерв
            "_res2": 0,  # Резерв
            "_res3": 0,  # Резерв
            "_res4": 0,  # Резерв
            "adjust_mode": 0,  # Признак «Режим юстировка»
            "auto_adjust": 0,  # Признак «Ведется автоматическая юстировка»
            "course_manual": 0,  # Признак «Ведется ручная юстировка курса»
            "pitch_manual": 0,  # Признак «Ведется ручная юстировка тангажа»
            "roll_manual2": 0,  # Признак «Ведется ручная юстировка крена» ?????
            "roll_manual": 0,  # Признак «Ведется ручная юстировка крена» ?????
            "adjust_reset": 0,  # Признак «Сброс юстировочных значений»
            "course_reset": 0,  # Признак «Сброс юстировочных значений курса»
            "pitch_reset": 0,  # Признак «Сброс юстировочных значений тангажа»
            "roll_reset": 0,  # Признак «Сброс юстировочных значений крена»
            "matrix": 0b00,  # Матрица состояния СДС (см. табл. 4)
            "parity": 0,  # Дополнение до четности
        }

        self.sds_02_p1_struct = (
                (self.sds_02_p1["arinc"] << 24)
                | (self.sds_02_p1["id"] << 22)
                | (self.sds_02_p1["sns"] << 21)
                | (self.sds_02_p1["svs"] << 20)
                | (self.sds_02_p1["dmk"] << 19)
                | (self.sds_02_p1["low_accuracy"] << 18)
                | (self.sds_02_p1["_res0"] << 17)
                | (self.sds_02_p1["_res1"] << 16)
                | (self.sds_02_p1["_res2"] << 15)
                | (self.sds_02_p1["_res3"] << 14)
                | (self.sds_02_p1["_res4"] << 13)
                | (self.sds_02_p1["adjust_mode"] << 12)
                | (self.sds_02_p1["auto_adjust"] << 11)
                | (self.sds_02_p1["course_manual"] << 10)
                | (self.sds_02_p1["pitch_manual"] << 9)
                | (self.sds_02_p1["roll_manual2"] << 8)
                | (self.sds_02_p1["roll_manual"] << 7)
                | (self.sds_02_p1["adjust_reset"] << 6)
                | (self.sds_02_p1["course_reset"] << 5)
                | (self.sds_02_p1["pitch_reset"] << 4)
                | (self.sds_02_p1["roll_reset"] << 3)
                | (self.sds_02_p1["matrix"] << 1)
                | self.sds_02_p1["parity"]
        )

        self.sds_03_p1 = {
            "code": 0b10111001,  # Восьмеричный код 271
            "id": 0b00,  # Идентификатор
            "sns_valid": 0,  # Признак «Исправность СНС»
            "sns_fail": 0,  # Признак «Отказ СНС»
            "data_fail": 0,  # Признак «Недостоверность данных СНС»
            "data_update": 0,  # Признак «Признак выдачи обновленных параметров»
            "sns_type": 0b00,  # Тип выбранной СНС
            "elipsoid": 0b00,  # Тип используемого эллипсоида
            "_res0": 0b00000000000,  # Резерв
            "matrix": 0b00,  # Матрица состояния СДС (см. табл. 4)
            "parity": 0,  # Дополнение до четности
        }

        self.sds_03_p1_struct = (
                (self.sds_03_p1["code"] << 24)
                | (self.sds_03_p1["id"] << 22)
                | (self.sds_03_p1["sns_valid"] << 21)
                | (self.sds_03_p1["sns_fail"] << 20)
                | (self.sds_03_p1["data_fail"] << 19)
                | (self.sds_03_p1["data_update"] << 18)
                | (self.sds_03_p1["sns_type"] << 16)
                | (self.sds_03_p1["elipsoid"] << 14)
                | (self.sds_03_p1["_res0"] << 3)
                | (self.sds_03_p1["matrix"] << 1)
                | self.sds_03_p1["parity"]
        )

        self.sds_01_p3 = {
            "parity": 0,
            "matrix": 0b00,
            "reserve": 0b00000000000,
            "elipsoid": 0b00,
            "sns_type": 0b00,
            "data_update": 0,
            "data_fail": 0,
            "sns_fail": 0,
            "sns_valid": 0,
            "id": 0b00,
            "code": 0b00000000,
        }

        self.sds_01_p3_struct = (
                (self.sds_01_p3["parity"] << 31)
                | (self.sds_01_p3["matrix"] << 29)
                | (self.sds_01_p3["reserve"] << 18)
                | (self.sds_01_p3["elipsoid"] << 16)
                | (self.sds_01_p3["sns_type"] << 14)
                | (self.sds_01_p3["data_update"] << 13)
                | (self.sds_01_p3["data_fail"] << 12)
                | (self.sds_01_p3["sns_fail"] << 11)
                | (self.sds_01_p3["sns_valid"] << 10)
                | (self.sds_01_p3["id"] << 8)
                | self.sds_01_p3["code"]
        )

        # Преобразование структуры в 4 байта информации
        self.sds_01_p1_data = struct.pack(">I", self.sds_01_p1_struct)
        self.sds_02_p1_data = struct.pack(">I", self.sds_02_p1_struct)
        self.sds_03_p1_data = struct.pack(">I", self.sds_03_p1_struct)
        self.sds_01_p3_data = struct.pack(">I", self.sds_01_p3_struct)
