import ctypes


class Arinc:
    def __init__(self):
        self.id_arinc = {
            'pitch': (324, 14, 0.011, -90, 90),
            'roll': (325, 14, 0.011, -180, 180),
            'course_mag': (320, 13, 0.0055, 0, 360),
            'course_track_mag': (317, 13, 0.0055, 0, 360),
            'course_true': (314, 13, 0.0055, 0, 360),
            'course_gyro': (334, 17, 0.09, 0, 360),
            'w_x': (336, 12, 0.015, -512, 512),
            'w_y': (337, 12, 0.015, -512, 512),
            'w_z': (330, 12, 0.015, -512, 512),
            'n_x': (331, 14, 0.001, -8, 8),
            'n_z': (332, 14, 0.001, -8, 8),
            'n_y': (333, 14, 0.001, -8, 8),
            'H_cmplx': (362, 8, 0.1524, -39951, 39951),
            'H_otn': (361, 8, 0.1524, -39951, 39951),
            'B_clx_head': (10, 10, 0.000172, -90, 90),
            'B_clx_tail': (310, 17, 0.0000000838, 0, 0.000172),
            'L_clx_head': (11, 10, 0.000172, -180, 180),
            'L_clx_tail': (311, 17, 0.0000000838, 0, 0.000172),
            'a_vert': (364, 14, 0.001, -8, 8),
            'speed_vert': (365, 13, 0.00508, -168, 168),
            'speed_vert_pot': (360, 13, 0.00508, -168, 168),
            'v_north': (373, 13, 0.2315, -1800, 1800),
            'v_east': (374, 14, 0.2315, -1800, 1800),
            'speed_track': (312, 14, 0.2315, 0, 1800),
            'a_course': (323, 14, 0.001, -8, 8),
            'traj_slope': (322, 14, 0.09, -180, 180),
            'drift_angle': (321, 17, 0.09, -180, 180),
            'wind_speed': (315, 14, 0.2315, -1800, 1800),
            'wind_angle_mag': (372, 9, 1.0, 0, 360),
            'H_abs': (362, 10, 0.1524, -39951, 39951),
            'H_qnh': (362, 10, 0.1524, -39951, 39951),
            'H_qfe': (362, 10, 0.1524, -39951, 39951),
            'airspeed_true': (315, 14, 0.2315, 0, 1800),
            'airspeed_prib': (315, 14, 0.2315, 0, 1800),
            'speed_vert_svs': (360, 13, 0.00508, -168, 168),
            'M': (364, 14, 0.001, -8, 8),
            'temp_h': (360, 13, 0.00508, -168, 168),
            'temp_r': (360, 13, 0.00508, -168, 168),
            'P_f': (360, 13, 0.1524, -39951, 39951),
            'P_h_stat': (362, 10, 0.1524, -39951, 39951),
            'Td1': (0, 10, 0.00508, -168, 168),
            'Td2': (0, 13, 0.00508, -168, 168),
            'altitude_danger': (0, 13, 0.00508, -168, 168),
            'radio_altitude': (0, 9, 0.00508, -168, 168),
            'altitude_trend': (0, 9, 1.0, 0, 0),
            'speed_trend': (0, 9, 1.0, 0, 0),
            'Q': (360, 9, 0.00508, -168, 168),
            'B_clx_head_sns': (10, 9, 0.000172, -90, 90),
            'B_clx_tail_sns': (310, 18, 0.0000000838, 0, 0.000172),
            'L_clx_head_sns': (11, 9, 0.000172, -180, 180),
            'L_clx_tail_sns': (311, 18, 0.0000000838, 0, 0.000172),
            'hdop': (101, 13, 0.03125, 0, 1024),
            'vdop': (101, 13, 0.03125, 0, 1024),
            'pdop': (101, 13, 0.03125, 0, 1024),
            'vertical_speed_sns': (360, 13, 0.00508, -168, 168),
            'speed_track_sns': (101, 13, 0.2315, 0, 1800),
            'v_north_sns': (101, 13, 0.2315, -1800, 1800),
            'v_east_sns': (101, 13, 0.2315, -1800, 1800),
            'track_angle_sns': (101, 13, 0.0055, 0, 360),
            'H_sns': (362, 10, 0.1524, -39951, 39951)
        }

        self.id_non_arinc = {
            'pressure': (0.05, 300.0, 805.0),
            'rudder_trim_pos': (0.1, 0.0, 0.0),
            'ailerons_trim_pos': (0.1, 0.0, 0.0),
            'elevator_trim_pos': (0.1, 0.0, 0.0),
            'battery_current': (0.1, 0.0, 300.0),
            'battery_voltage': (0.1, 0.0, 40.0),
            'generator_current': (0.1, 0.0, 300.0),
            'generator_voltage': (0.1, 0.0, 40.0),
            'oil_pressure': (0.1, 0.0, 10.0),
            'fuel_pressure': (0.1, 0.0, 10.0),
            'fuel_consumption': (0.1, 0.0, 300.0),
            'oil_temperature': (0.1, -60.0, 200.0),
            'fuel_rem_r': (0.1, 0.0, 700.0),
            'fuel_rem_l': (0.1, 0.0, 700.0),
            'engine_torque': (0.1, 0.0, 120.0),
            'engine_rate': (0.1, 0.0, 120.0),
            'engine_exhaust_temperature': (0.1, 0.0, 900.0),
            'flaps_position': (0.1, 0.0, 50.0),
            'alpha': (0.1, -10.0, 50.0),
            'alpha_min': (0.1, -10.0, 50.0),
            'alpha_max': (0.1, -10.0, 50.0),
            'ny_min': (0.1, -10.0, 10.0),
            'ny_max': (0.1, -10.0, 10.0),
            'speed_min': (0.1, 0.0, 400.0),
            'speed_max': (0.1, 0.0, 400.0),
            'fuel_rem': (0.1, 0.0, 1400.0),
            'rudder_position': (0.1, -50.0, 50.0),
            'ailerons_position': (0.1, -50.0, 50.0),
            'elevator_position': (0.1, -50.0, 50.0),
            'slide_position': (0.0001, -0.3, 0.3),
            'adjust_course_value': (0.01, 0.0, 0.0),
            'adjust_pitch_value': (0.01, 0.0, 0.0),
            'adjust_roll_value': (0.01, 0.0, 0.0),
            'Nz_filter': (0.01, 0.0, 0.0),
            'Ny_filter': (0.01, 0.0, 0.0),
            'Vy_filter': (0.01, 0.0, 0.0),
            'Alpha_filter': (0.01, 0.0, 0.0),
            'air_temperature': (0.01, 0.0, 0.0)
        }

        # Загрузка динамической библиотеки
        self.arinc_lib = ctypes.CDLL('source/cpp/libarinc.so')  # Подставьте соответствующее имя вашей библиотеки

        # Определение типов аргументов и возвращаемого значения функции
        self.arinc_lib.encode_arinc.argtypes = [ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float,
                                                ctypes.c_uint16, ctypes.c_uint16]
        self.arinc_lib.encode_arinc.restype = ctypes.c_uint32

    def get_data_arinc(self, name, value):
        label = self.id_arinc[name][0]
        low_bit = self.id_arinc[name][1]
        scale = self.id_arinc[name][2]
        min_v = self.id_arinc[name][3]
        max_v = self.id_arinc[name][4]

        result = self.arinc_lib.encode_arinc(float(value), float(min_v), float(max_v), float(scale), low_bit, label)

        return result

    def get_data_non_arinc(self, name, value):
        scale = self.id_non_arinc[name][0]
        min_v = self.id_non_arinc[name][1]
        max_v = self.id_non_arinc[name][2]

        if value < min_v:
            value = min_v
        elif value > max_v:
            value = max_v

        ipar = int(round(abs(value) / scale))
        if value < 0:
            ipar = -ipar

        return ipar
