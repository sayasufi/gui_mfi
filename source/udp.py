import socket
import struct

from source.convert_data import Arinc
from source.unions import Unions


# Определение структуры
class S_UDP_PACK_ODS_DATA:
    def __init__(self, ip: str = "192.168.7.255", port: int = 17300):
        self.unions = Unions()
        self.arinc = Arinc()
        self.number_package = 0
        self.UDP_IP = ip  # IP адрес получателя
        self.UDP_PORT = port  # Порт получателя

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.udp = {
            "preface_1": 0xCD,  # Преамбула	0xCDEFFA01
            "preface_2": 0xEF,  # Преамбула
            "preface_3": 0xFA,  # Преамбула
            "preface_4": 0x01,  # Преамбула
            "reciever_addr": 0x0001,  # Адресат пакета 0x0001
            "sender_addr": 0x0002,  # Источник пакета 0x0002
            "id": 0x0001,  # № пакета 0x0003
            "reserv_1": 0x0000,
            "reserv_2": 0x0000,
            "reserv_3": 0x0000,
            "size": 0x0008,  # Длина всего пакета 0x03A2
            "sds1": struct.unpack("H", self.unions.sds1_data)[0],
            "_reserve0": 0x0000,
            "sds2": struct.unpack("H", self.unions.sds2_data)[0],
            "sds3": struct.unpack("H", self.unions.sds3_data)[0],
            "sds4": 0x0000,
            "r1": 0x0000,
            "r2": 0x0000,
            "r3": 0x0000,
            "r4": 0x0000,
            "r5": 0x0000,
            "r6": 0x0000,
            "r7": 0x0000,
            "r8": 0x0000,
            "r9": 0x0000,
            "r10": 0x0000,
            "r11": 0x0000,
            # # /******/
            # # /* P1 */
            # # /******/
            "preface_ar_1": 0x00000000,  # 0xA1FA,  # Преамбула канала ARINC-429 №1(Данные ИНС) ВПНП-1М */
            "cnt_p1": 0,  # Счетчик посылок
            "sds_01_p1": 0x00000000,  # struct.unpack("I", self.unions.sds_01_p1_data)[0],
            "sds_02_p1": 0x00000000,  # struct.unpack("I", self.unions.sds_02_p1_data)[0],
            "sds_03_p1": 0x00000000,  # struct.unpack("I", self.unions.sds_03_p1_data)[0],
            "sds_04_p1": 0x00000000,  # СДС 4
            "sds_05_p1": 0x00000000,  # СДС 5
            "pitch": self.arinc.get_data_arinc("pitch", 0),  # Угол тангажа
            "roll": self.arinc.get_data_arinc("roll", 0),  # Угол крена
            "course_mag": self.arinc.get_data_arinc("course_mag", 0),  # Курс магнитный
            "course_track_mag": self.arinc.get_data_arinc("course_track_mag", 0),  # Магнитный путевой угол
            "course_true": self.arinc.get_data_arinc("course_true", 0),  # Истинный курс
            "course_gyro": self.arinc.get_data_arinc("course_gyro", 0),  # Гироскопический курс
            "w_x": self.arinc.get_data_arinc("w_x", 0),  # Угловая скорость тангажа
            "w_y": self.arinc.get_data_arinc("w_y", 0),  # Угловая скорость крена
            "w_z": self.arinc.get_data_arinc("w_z", 0),  # Угловая скорость рысканья
            "n_x": self.arinc.get_data_arinc("n_x", 0),  # Продольное ускорение
            "n_y": self.arinc.get_data_arinc("n_y", 0),  # Боковое ускорение
            "n_z": self.arinc.get_data_arinc("n_z", 0),  # Нормальное ускорение
            "L_clx_head": self.arinc.get_data_arinc("L_clx_head", 0),  # Географические координаты долгота старшая часть
            "L_clx_tail": self.arinc.get_data_arinc("L_clx_tail", 0),  # Географические координаты долгота младшая часть
            "B_clx_head": self.arinc.get_data_arinc("B_clx_head", 0),  # Географические координаты широта старшая часть
            "B_clx_tail": self.arinc.get_data_arinc("B_clx_tail", 0),  # Географические координаты широта младшая часть
            "H_cmplx": self.arinc.get_data_arinc("H_cmplx", 0),  # Комплексная высота полета
            "H_otn": self.arinc.get_data_arinc("H_otn", 0),  # Относительная барометрическая высота
            "a_vert": self.arinc.get_data_arinc("a_vert", 0),  # Вертикальное ускорение
            "speed_vert": self.arinc.get_data_arinc("speed_vert", 0),  # Вертикальная скорость
            "speed_vert_pot": self.arinc.get_data_arinc("speed_vert_pot", 0),  # Потенциальная вертикальная скорость
            "v_north": self.arinc.get_data_arinc("v_north", 0),  # Путевая скорость N/S
            "v_east": self.arinc.get_data_arinc("v_east", 0),  # Путевая скорость E/W
            "speed_track": self.arinc.get_data_arinc("speed_track", 0),  # Путевая скорость
            "a_course": self.arinc.get_data_arinc("a_course", 0),  # Ускорение вдоль траектории полета
            "traj_slope": self.arinc.get_data_arinc("traj_slope", 0),  # Угол наклона траектории
            "drift_angle": self.arinc.get_data_arinc("drift_angle", 0),  # Угол сноса
            "wind_speed": self.arinc.get_data_arinc("wind_speed", 0),  # Скорость ветра
            "wind_angle_mag": self.arinc.get_data_arinc("wind_angle_mag", 0),  # Магнитное направление ветра
            "mult_txt": 0x00000000,  # Мультиплексор ТЕХН
            "time_on": 0x00000000,  # Время от включения 005
            "time_nav": 0x00000000,  # Время от начала навигации 006
            "reserv_4": 0x00000000,
            "reserv_5": 0x00000000,
            "reserv_6": 0x00000000,
            "reserv_7": 0x00000000,
            "reserv_8": 0x00000000,
            "reserv_9": 0x00000000,
            "reserv_10": 0x00000000,
            "reserv_11": 0x00000000,
            "p1_end_sig": 0x00000000,  # 0xAF1A,  # Индентификатор окончания пакета №1
            "reserv_12": 0x00000000,  # !!!
            # # /******/
            # # /* P2 */
            # # /******/
            "preface_ar_2": 0x00000000,  # 0xA2FA,  # Преамбула канала ARINC-429 №2(Данные СВС) ВПНП-1М
            "cnt_p2": 0,  # Счетчик посылок
            "sds_01_p2": 0x00000000,  # СДС 1
            "sds_02_p2": 0x00000000,  # СДС 2
            "H_abs": self.arinc.get_data_arinc("H_abs", 0),  # абсолютная барометрическая высота [м]
            "H_qnh": self.arinc.get_data_arinc("H_qnh", 0),  # относительная баровысота (коррекция по QNH) [м]
            "H_qfe": self.arinc.get_data_arinc("H_qfe", 0),  # относительная баровысота (коррекция по QFE) [м]
            "airspeed_true": self.arinc.get_data_arinc("airspeed_true", 0),  # истинная (воздушная) скорость [км/ч]
            "airspeed_prib": self.arinc.get_data_arinc("airspeed_prib", 0),  # приборная скорость [км/ч]
            "speed_vert_svs": self.arinc.get_data_arinc("speed_vert_svs", 0),  # вертикальная скорость [м/с]
            "M": self.arinc.get_data_arinc("M", 0),  # число Маха полета [ед.М]
            "temp_h": self.arinc.get_data_arinc("temp_h", 0),  # температура наружного воздуха [°С]
            "temp_r": self.arinc.get_data_arinc("temp_r", 0),  # температура торможения [°С]
            "Q": self.arinc.get_data_arinc("Q", 0),  # скоростной напор [Па]
            "P_f": self.arinc.get_data_arinc("P_f", 0),  # Полное давление [мм.рт.ст]
            "P_h_stat": self.arinc.get_data_arinc("P_h_stat", 0),  # статическое давление воздуха [мм.рт.ст]
            "Td1": self.arinc.get_data_arinc("Td1", 0),  # температура датчика давления воздуха Д1 [°С]
            "Td2": self.arinc.get_data_arinc("Td2", 0),  # температура датчика давления воздуха Д2 [°С]
            "reserv_13": 0x00000000,
            "reserv_14": 0x00000000,
            "reserv_15": 0x00000000,
            "reserv_16": 0x00000000,
            "altitude_danger": self.arinc.get_data_arinc("altitude_danger", 0),  # опасная высота
            "radio_altitude": self.arinc.get_data_arinc("radio_altitude", 0),  # Высота от Радиовысотомера
            "altitude_trend": self.arinc.get_data_arinc("altitude_trend", 0),  # Тренд высоты Habs
            "speed_trend": self.arinc.get_data_arinc("speed_trend", 0),  # Тренд скорости приборной
            "p2_end_sig": 0x00000000,  # 0xAF2A,
            # # /******/
            # # /* P3 */
            # # /******/
            "preface_ar_3": 0x00000000,  # 0xA3FA,  # Преамбула канала ARINC-429 №3(Данные СНС) ВПНП-1М
            "cnt_p3": 0,  # Счетчик посылок
            "sds_01_p3": struct.unpack("I", self.unions.sds_01_p3_data)[0],
            "sds_02_p3": 0x00000000,  # СДС 2
            "sds_03_p3": 0x00000000,  # СДС 3
            "hdop": self.arinc.get_data_arinc("hdop", 0),  # Геометрический фактор HDOP умноженный на 10
            "vdop": self.arinc.get_data_arinc("vdop", 0),  # Геометрический фактор VDOP умноженный на 10
            "pdop": self.arinc.get_data_arinc("pdop", 0),  # Геометрический фактор PDOP умноженный на 10
            "vertical_speed_sns": self.arinc.get_data_arinc("vertical_speed_sns", 0),  # вертикальная скорость
            "speed_track_sns": self.arinc.get_data_arinc("speed_track_sns", 0),  # Путевая скорость
            "v_north_sns": self.arinc.get_data_arinc("v_north_sns", 0),  # Путевая скорость N/S
            "v_east_sns": self.arinc.get_data_arinc("v_east_sns", 0),  # Путевая скорость E/W
            "track_angle_sns": self.arinc.get_data_arinc("track_angle_sns", 0),  # путевой угол
            "H_sns": self.arinc.get_data_arinc("H_sns", 300),  # высота СНС [м]
            "L_clx_head_sns": self.arinc.get_data_arinc("L_clx_head_sns", 0),
            # Географические координаты долгота старшая часть
            "L_clx_tail_sns": self.arinc.get_data_arinc("L_clx_tail_sns", 0),
            # Географические координаты долгота младшая часть
            "B_clx_head_sns": self.arinc.get_data_arinc("B_clx_head_sns", 0),
            # Географические координаты широта старшая часть
            "B_clx_tail_sns": self.arinc.get_data_arinc("B_clx_tail_sns", 0),
            # Географические координаты широта младшая часть
            "time_cur": 0x00000000,  # Текущее время
            "date_cur": 0x00000000,  # Текущая дата
            "reserv_21": 0x00000000,
            "reserv_22": 0x00000000,
            "reserv_23": 0x00000000,
            "reserv_24": 0x00000000,
            "reserv_25": 0x00000000,
            "reserv_26": 0x00000000,
            "reserv_27": 0x00000000,
            "reserv_28": 0x00000000,
            "p3_end_sig": 0x00000000,  # 0xAF3A,  # Идентификатор окончания пакета №3
            "sds1X": 0x0000,
            "sds2X": struct.unpack("H", self.unions.sds2X_data)[0],
            "sds3X": struct.unpack("H", self.unions.sds3X_data)[0],
            "sds4X": 0x0000,
            "pressure": self.arinc.get_data_non_arinc("pressure", 0),  # Давление(коррекция)
            "flash_page": 0x0000,  # Номер используемой страницы FLASH
            "flash_block": 0x0000,  # Номер используемогог блока FLASH
            "_reserve1": 0x0000,
            "rudder_trim_pos": self.arinc.get_data_non_arinc("rudder_trim_pos", 0),
            "ailerons_trim_pos": self.arinc.get_data_non_arinc("ailerons_trim_pos", 0),
            "elevator_trim_pos": self.arinc.get_data_non_arinc("elevator_trim_pos", 0),
            "battery_current": self.arinc.get_data_non_arinc("battery_current", 0),  # Ток аккумулятора
            "battery_voltage": self.arinc.get_data_non_arinc("battery_voltage", 0),  # Напряжение аккумулятора
            "generator_current": self.arinc.get_data_non_arinc("generator_current", 0),  # Ток генератора
            "generator_voltage": self.arinc.get_data_non_arinc("generator_voltage", 0),  # Напряжение генератора
            "oil_pressure": self.arinc.get_data_non_arinc("oil_pressure", 0),  # Давление масла
            "fuel_pressure": self.arinc.get_data_non_arinc("fuel_pressure", 0),  # Давление топлива
            "fuel_consumption": self.arinc.get_data_non_arinc("fuel_consumption", 0),  # Расход топлива
            "oil_temperature": self.arinc.get_data_non_arinc("oil_temperature", 0),  # Температура масла
            "fuel_rem_l": self.arinc.get_data_non_arinc("fuel_rem_l", 0),  # Остаток топлива в левом баке
            "fuel_rem_r": self.arinc.get_data_non_arinc("fuel_rem_r", 0),  # Остаток топлива в правом баке
            "engine_torque": self.arinc.get_data_non_arinc("engine_torque", 0),  # Значение крутящего момента/шага винта
            "engine_rate": self.arinc.get_data_non_arinc("engine_rate", 0),  # Значение оборотов двигателя
            "engine_exhaust_temperature": self.arinc.get_data_non_arinc("engine_exhaust_temperature", 0),
            # Температура выходящих газов двигателя
            "flaps_position": self.arinc.get_data_non_arinc("flaps_position", 0),  # Положение закрылков
            "oil_radiator_position": 0x0000,  # Положение створки маслорадиатора
            "alpha": self.arinc.get_data_non_arinc("alpha", 0),  # Расчетный угол атаки
            "alpha_min": self.arinc.get_data_non_arinc("alpha_min", 0),  # Угол атаки минимально допустимый
            "alpha_max": self.arinc.get_data_non_arinc("alpha_max", 0),  # Угол атаки максимально допустимый
            "ny_min": self.arinc.get_data_non_arinc("ny_min", 0),  # Перегрузка минимально допустимая
            "ny_max": self.arinc.get_data_non_arinc("ny_max", 0),  # Перегрузка максимально допустимая
            "speed_min": self.arinc.get_data_non_arinc("speed_min", 0),  # Скорость минимально допустимая
            "speed_max": self.arinc.get_data_non_arinc("speed_max", 0),  # Скорость максимально допустимая
            "fuel_rem": self.arinc.get_data_non_arinc("fuel_rem", 0),  # Общий остаток топлива
            "rudder_position": self.arinc.get_data_non_arinc("rudder_position", 0),  # Положение руля направления
            "ailerons_position": self.arinc.get_data_non_arinc("ailerons_position", 0),  # Положение элеронов
            "elevator_position": self.arinc.get_data_non_arinc("elevator_position", 0),  # Положение руля высоты
            "slide_position": self.arinc.get_data_non_arinc("slide_position", 0),
            # Положение шарика скольжения(боковая перегрузка)
            "adjust_course_value": self.arinc.get_data_non_arinc("adjust_course_value", 0),
            "adjust_pitch_value": self.arinc.get_data_non_arinc("adjust_pitch_value", 0),
            "adjust_roll_value": self.arinc.get_data_non_arinc("adjust_roll_value", 0),
            "Nz_filter": self.arinc.get_data_non_arinc("Nz_filter", 0),
            "Ny_filter": self.arinc.get_data_non_arinc("Ny_filter", 0),
            "Vy_filter": self.arinc.get_data_non_arinc("Vy_filter", 0),
            "Alpha_filter": self.arinc.get_data_non_arinc("Alpha_filter", 0),
            "air_temperature": self.arinc.get_data_non_arinc("air_temperature", 0),
            "_reserve3": 0x00000000,
            "cnt_ispr": 0,  # Счетчик исправности
            "crc_pack": 0x00000000,  # Контрольная сумма пакета
        }

    def get_package(self):
        self.udp["cnt_p1"] = self.number_package
        self.udp["cnt_p2"] = self.number_package
        self.udp["cnt_p3"] = self.number_package
        self.udp["cnt_ispr"] = self.number_package

        list_udp = list(self.udp.values())
        for i in range(len(list_udp)):
            if isinstance(list_udp[i], tuple):
                print(list_udp[i])
                list_udp[i] = list_udp[i][0]

        packed_data1 = struct.pack("H" * 27, *list_udp[:27])
        packed_data2 = struct.pack("I" * 105, *list_udp[27:132])
        packed_data3 = struct.pack("H" * 46, *list_udp[132:178])
        packed_data4 = struct.pack("I" * 3, *list_udp[178:])

        self.number_package += 1
        return packed_data1 + packed_data2 + packed_data3 + packed_data4

    def send(self, package):
        self.sock.sendto(package, (self.UDP_IP, self.UDP_PORT))

    def close(self):
        self.sock.close()
