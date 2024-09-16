import sys
import serial
import glob
import re

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Slot
from ui_form import Ui_Widget
from text_edit_logger import QTextEditLogger

import logging

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        self.log_text_edit = QTextEditLogger(self.ui.statusTextEdit)
        self.log_text_edit.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger = logging.getLogger()
        logger.addHandler(self.log_text_edit)
        logger.setLevel(logging.INFO)

        available_port_pairs = self.get_available_port_pairs()
        self.add_port_pairs_to_combobox(available_port_pairs)
        available_speed = [50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600, 19200, 38400, 57600, 115200]
        self.ui.comboBox_2.addItems(map(str, available_speed))

    def get_available_port_pairs(self):
        virtual_ports = []
        if sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # Поиск виртуальных портов, созданных с помощью socat
            virtual_ports = glob.glob('/tmp/ttyV*')
        result = []
        pattern = r'/tmp/ttyV(\d+)'
        for port in virtual_ports:
            match = re.match(pattern, port)
            if match:
                port_number = int(match.group(1))
                if port_number % 2 == 0:  # Четные номера - первый порт в паре
                    pair = [port, f'/tmp/ttyV{port_number+1}']
                    result.append(pair)
        return result

    def add_port_pairs_to_combobox(self, port_pairs):
            com_port_counter = 0
            for pair in port_pairs:
                com_port_name1 = f"COM{com_port_counter}"
                com_port_name2 = f"COM{com_port_counter + 1}"
                self.ui.comboBox.addItem(f"{com_port_name1} - {com_port_name2}")
                com_port_counter += 2

    def send_data(self):
        try:
            selected_port_pair = self.ui.comboBox.currentText()
            com_port1, com_port2 = selected_port_pair.split(" - ")

            port1 = self.com_to_real_port(com_port1)
            port2 = self.com_to_real_port(com_port2)

            speed = self.ui.comboBox_2.currentText()

            logging.info(f"Initialization ports {com_port1}, {com_port2} with baud {speed}...")
            ser1 = serial.Serial(port1, baudrate=speed, timeout=1)
            ser2 = serial.Serial(port2, baudrate=speed, timeout=1)
            logging.info("Ports initialization was successfull!")

            data_to_send = self.ui.inputTextEdit.toPlainText().encode()
            sent_data_length = len(data_to_send)
            self.ui.inputTextEdit.clear()
            logging.info(f"Sending data through a port {com_port1}, data len is {sent_data_length} bytes...")
            bytes_written = ser1.write(data_to_send)
            logging.info(f"Successfully sended {bytes_written} bytes!")

            logging.info(f"Reading data through a port {com_port2}...");
            data_received = ser2.read(len(data_to_send))
            self.ui.outputTextEdit.setPlainText(data_received.decode())
            received_data_length = len(data_received)
            logging.info(f"Successfully readed {received_data_length} bytes!");

            logging.info(f"Closing ports {com_port1}, {com_port2}...")
            ser1.close()
            ser2.close()
            logging.info("Ports successfully closed!")
        except serial.SerialException as e:
            logging.error(f"Ошибка при работе с последовательным портом: {e}")
        except Exception as e:
            logging.error(f"Неожиданная ошибка: {e}")

    def com_to_real_port(self, com_port):
        com_number = int(com_port[3:])  # COM1 -> 1, COM2 -> 2, и т.д.
            # Преобразуем номер COM-порта в номер ttyV
        ttyv_number = (com_number) # COM1,COM2 -> 2, COM3,COM4 -> 4, и т.д.
            # Формируем реальный путь к порту
        real_port = f"/tmp/ttyV{ttyv_number}"
            # Если это нечетный COM-порт, увеличиваем номер ttyV на 1
        return real_port

    @Slot()
    def send_button_click(self):
        self.send_data()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
