import sys
import socket
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QLineEdit, QScrollArea, QPushButton, QGridLayout, QSizePolicy
from PySide2.QtCore import Qt, QTimer

from source.udp import S_UDP_PACK_ODS_DATA


class UDPClient:
    def __init__(self, ip, port):
        self.udp = S_UDP_PACK_ODS_DATA(ip, port)

    def get_package(self):
        return self.udp.get_package()

    def send(self, pack):
        self.udp.send(pack)


class ParameterGUI(QMainWindow):
    def __init__(self, param_dict):
        super().__init__()

        self.param_dict = param_dict
        self.udp_client = None
        self.sending = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.send_udp_data)

        self.initUI()

    def initUI(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout(main_widget)

        ip_port_layout = QHBoxLayout()
        self.ip_entry = QLineEdit()
        self.ip_entry.setPlaceholderText("Enter IP Address")
        self.ip_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        ip_port_layout.addWidget(self.ip_entry)

        self.port_entry = QLineEdit()
        self.port_entry.setPlaceholderText("Enter Port")
        self.port_entry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        ip_port_layout.addWidget(self.port_entry)

        main_layout.addLayout(ip_port_layout)

        self.send_button = QPushButton("Start Sending")
        self.send_button.clicked.connect(self.toggle_sending)
        self.send_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        main_layout.addWidget(self.send_button)

        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        main_layout.addWidget(scroll)

        layout = QVBoxLayout(scroll_widget)

        grid_layout = QGridLayout()
        layout.addLayout(grid_layout)

        self.sliders = {}
        row = 0

        for param, (_, _, _, min_val, max_val) in self.param_dict.items():
            label = QLabel(param)
            label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            grid_layout.addWidget(label, row, 0)

            range_val = max_val - min_val
            if range_val == 0:
                range_val = 1
            scale_factor = 1000 / range_val

            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(int(min_val * scale_factor))
            slider.setMaximum(int(max_val * scale_factor))
            slider.setValue(int((min_val + max_val) / 2 * scale_factor))
            step = (max_val - min_val) / 100
            slider.setSingleStep(int(step * scale_factor))
            slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            slider.valueChanged.connect(lambda value, s=slider, sf=scale_factor, p=param: self.update_entry(p, s, sf))

            grid_layout.addWidget(slider, row, 1)

            entry = QLineEdit()
            entry.setText(str((min_val + max_val) / 2))
            entry.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            entry.returnPressed.connect(lambda e=entry, s=slider, sf=scale_factor, p=param, min_v=min_val, max_v=max_val: self.update_slider(e, s, min_v, max_v, sf))

            grid_layout.addWidget(entry, row, 2)

            self.sliders[param] = (slider, entry, scale_factor)
            row += 1

        # Set stretch factors
        grid_layout.setColumnStretch(0, 1)  # Label column
        grid_layout.setColumnStretch(1, 3)  # Slider column
        grid_layout.setColumnStretch(2, 1)  # Entry column

        self.setWindowTitle('Parameter Adjustment')
        self.show()

    def update_entry(self, param, slider, scale_factor):
        entry = self.sliders[param][1]
        value = slider.value() / scale_factor
        entry.setText(f"{value:.6f}")

    def update_slider(self, entry, slider, min_val, max_val, scale_factor):
        try:
            value = float(entry.text())
            if min_val <= value <= max_val:
                slider.setValue(int(value * scale_factor))
            else:
                entry.setText(f"{slider.value() / scale_factor:.6f}")
        except ValueError:
            entry.setText(f"{slider.value() / scale_factor:.6f}")

    def toggle_sending(self):
        if self.sending:
            self.sending = False
            self.timer.stop()
            self.send_button.setText("Start Sending")
        else:
            ip_address = self.ip_entry.text()
            port = self.port_entry.text()
            if ip_address and port.isdigit():
                self.udp_client = UDPClient(ip_address, int(port))
                self.sending = True
                self.timer.start(10)  # 100 Hz = 10 ms interval
                self.send_button.setText("Stop Sending")

    def send_udp_data(self):
        if self.udp_client:
            for param, (slider, _, scale_factor) in self.sliders.items():
                value = slider.value() / scale_factor
                self.udp_client.udp.udp[param] = self.udp_client.udp.arinc.get_data_arinc(param, value)
            pack = self.udp_client.get_package()
            self.udp_client.send(pack)


if __name__ == '__main__':
    param_dict = {
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

    app = QApplication(sys.argv)

    with open("darkstyle.qss", "r") as file:
        app.setStyleSheet(file.read())

    ex = ParameterGUI(param_dict)
    sys.exit(app.exec_())
