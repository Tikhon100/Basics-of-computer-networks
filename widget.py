import sys
import serial
import time

from packet import Packet
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Slot
from ui_form import Ui_Widget
from text_edit_logger import QTextEditLogger
from PyQt5.QtCore import QThread

import logging
import threading
import random
from typing import List
from PyQt5.QtCore import pyqtSignal


class AtomicVariable:
    def __init__(self, initial_value):
        self._value = initial_value
        self._lock = threading.Lock()

    def get(self):
        with self._lock:
            return self._value

    def set(self, new_value):
        with self._lock:
            self._value = new_value

    def increment(self):
        with self._lock:
            self._value += 1

# this is sparta
class Widget(QWidget):

    def __init__(self, station_id, parent=None):
        super().__init__(parent)

        self.send_data_flag = AtomicVariable(0)
        self.pull_data_to_token = AtomicVariable(0)
        self.packets_to_send = []

        self.port1 = ""
        self.port2 = ""
        self.station_id = station_id

        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.log_text_edit = QTextEditLogger(self.ui.statusTextEdit)
        self.log_text_edit.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger = logging.getLogger()

        logging.basicConfig(filename='output.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        logger.setLevel(logging.INFO)

        self.connect_to_com_ports(station_id)
        self.ui.label_7.setText(self.ui.label_7.text() + " Write:" + self.port1 + "    Read:" + self.port2)

        self.thread = QThread()
        self.thread.run = self.com_ports_ring
        self.thread.start()


        if self.station_id == 1:
            self.send_data_flag.set(1)

    def com_ports_ring(self):
        self.input_ser = serial.Serial(self.port2, 9600, timeout=1)

        self.output_ser = serial.Serial(self.port1, 9600)

        while True:
            data = bytearray(self.input_ser.read(4))
            #print(f"point 0 {data} {threading.current_thread().ident}")
            if data:
                #print(f"point 1 {threading.current_thread().ident}")
                if (data[-1]==48): # можно отправлять (пришел пустой токен)
                   # print(f"point 2 {threading.current_thread().ident}")
                    if self.ui.checkBox_3.isChecked():
                        print(f"{threading.current_thread().ident} Empty token readed and re-adress to next station")
                    if self.pull_data_to_token.get() == 1: # если   есть что отправить
                        #print(f"point 3 {threading.current_thread().ident}")
                        try:
                            packet_data = self.packets_to_send[0].data_after_stuffing
                            fcs = self.create_fcs(packet_data)
                            if self.ui.checkBox.isChecked():
                                packet_data = self.emulate_errors(packet_data)
                            str3 = ','.join(str(b) for b in packet_data)
                            char_list = [chr(int(b)) for b in str3.split(',')]
                            result_string = ''.join(char_list)
                            selected_text = self.ui.comboBox.currentText()
                            currentToken = "000" + selected_text
                            data_to_send = f"{currentToken}{self.packets_to_send[0].flag}{self.packets_to_send[0].destination_address}6666~{result_string}~{fcs}".encode("latin-1")

                            #print(data_to_send)
                            #print("lol_send")

                            (self.output_ser.write(data_to_send))

                            self.packets_to_send.pop(0)

                            if not self.packets_to_send:
                                self.pull_data_to_token.set(0)
                        except serial.SerialException as e:
                            logging.error(f"Ошибка при работе с последовательным портом: {e}")
                        except Exception as e:
                            logging.error(f"Неожиданная ошибка: {e}")
                    else: # если нечего отправлять
                        #print(f"point 4 {threading.current_thread().ident}")
                        time.sleep(0.5)
                        self.output_ser.write(data)
                else:   # пришел не пустой токен
                    #print(f"point 5 {threading.current_thread().ident}")
                    if data[-1] == self.station_id + 48 : # данные для текущей станции

                        self.receive_data(self.input_ser)# приняли данные
                        packet = "0000"
                        data_to_send = f"{packet}".encode("latin-1")
                        self.output_ser.write(data_to_send) # запустили пустой токен дальше
                        #print(f"point 6 {threading.current_thread().ident}")
                    else: # данные для кого то другого

                        #print(f"point 7 {threading.current_thread().ident}")
                        data_to_resend = self.read_data_to_resend(self.input_ser)
                        data.extend(data_to_resend)
                        #print (data_to_resend)
                        if self.ui.checkBox_3.isChecked():
                            print(f"Token get and re-adress to next station, data is {data_to_resend}")
                        self.output_ser.write(data)
            else:
                #print(f"point 8 {threading.current_thread().ident}")
                if self.send_data_flag.get() !=0:
                    #print(f"point 9 {threading.current_thread().ident}")
                    self.input_ser.timeout = 1
                    data = self.input_ser.read(4)
                    self.input_ser.timeout = 1                                       ##########################################
                    self.send_data_flag.set(0)
                    packet = "0000"
                    if self.ui.checkBox_2.isChecked():
                        currentToken[self.station_id-1] = "1"
                    data_to_send = f"{packet}".encode("latin-1")
                    self.output_ser.write(data_to_send)

        self.input_ser.close()
        self.output_ser.close()

    def connect_to_com_ports(self, number):
        if number == 1:
            self.port1 = '/tmp/ttyV0'
            self.port2 = '/tmp/ttyV5'
            self.ui.comboBox.addItem("2")
            self.ui.comboBox.addItem("3")
        elif number == 2:
            self.port2 = '/tmp/ttyV1'
            self.port1 = '/tmp/ttyV2'
            self.ui.comboBox.addItem("1")
            self.ui.comboBox.addItem("3")
        elif number == 3:
            self.port2 = '/tmp/ttyV3'
            self.port1 = '/tmp/ttyV4'
            self.ui.comboBox.addItem("1")
            self.ui.comboBox.addItem("2")

    def handle_empty_token(self):
        self.ui.statusTextEdit.append(f"{threading.current_thread().ident} Empty token readed and re-adress to next station")

    def create_packets(self, input_string: str, flag: bytes, destination_address: bytes, source_address: bytes) -> List[Packet]:
        print(f"input string: {input_string}")
        packets = []
        input_bytes = input_string.encode("latin-1")

        for i in range(0, len(input_bytes), 14):
            chunk = input_bytes[i:i + 14]
            if len(chunk) <= 14:
                packet1 = Packet(flag, destination_address, source_address, chunk, "0")
                packets.append(packet1)
            else:
                            # Разбиваем длинный кусок на несколько пакетов длиной 14 байт
                for j in range(0, len(chunk), 14):
                    sub_chunk = chunk[j:j + 14]
                    packet1 = Packet(flag, destination_address, source_address, sub_chunk, "0")
                    packets.append(packet1)
        return packets


    def send_data(self):
        data_to_send = self.ui.inputTextEdit.toPlainText()
        self.packets_to_send = self.create_packets(data_to_send, "00001110", "0000", self.port1)
        self.pull_data_to_token.set(1);

    def emulate_errors(self, data):
        random_int = random.randint(0, 100)
        #print(random_int)

        if random_int <= 60:
            if len(data)>1:
                data = self.simulate_errors(data, [15])
                self.ui.statusTextEdit.append(">>>>>>>>>>One bit was changed<<<<<<<<<<")
        elif 60 < random_int < 85:
            if len(data)>4:
                data = self.simulate_errors(data, [15,30])
                self.ui.statusTextEdit.append(">>>>>>>>>>Two bits were changed<<<<<<<<<<")
        return data

    def simulate_errors(self, data, error_positions):
        data_bits = list(''.join(format(byte, '08b') for byte in data))
        for pos in error_positions:
            if pos <= len(data_bits):
                data_bits[pos-1] = '1' if data_bits[pos-1] == '0' else '0'
        return bytes(int(''.join(data_bits[i:i+8]), 2) for i in range(0, len(data_bits), 8))

    def perform_unstuffing(self, data):
                # Преобразуем байты в строку битов
        bit_string = ''.join(format(byte, '08b') for byte in data)

        unstuffed_bits = ''
        count_ones = 0

        i = 0
        while i < len(bit_string):
            bit = bit_string[i]
            unstuffed_bits += bit
            if bit == '1':
                count_ones += 1
                if count_ones == 5 and i + 1 < len(bit_string) and bit_string[i+1] == '0':
                    i += 1  # Пропускаем следующий бит (удаляем вставленный ноль)
                    count_ones = 0
            else:
                count_ones = 0
            i += 1

                # Удаляем добавленные нули справа
        unstuffed_bits = unstuffed_bits.rstrip('0')

                # Дополняем строку нулями справа до кратности 8, если необходимо
        while len(unstuffed_bits) % 8 != 0:
            unstuffed_bits += '0'

                # Преобразуем обратно в байты
        unstuffed_bytes = bytes(int(unstuffed_bits[i:i+8], 2) for i in range(0, len(unstuffed_bits), 8))

        return unstuffed_bytes

    @Slot()
    def send_button_click(self):
        self.send_data()
    @Slot()
    def clearInput(self):
        self.ui.inputTextEdit.clear()
    @Slot()
    def clearOutput(self):
        self.ui.outputTextEdit.clear()
    @Slot()
    def clearStatus(self):
        self.ui.statusTextEdit.clear()
    @Slot()
    def newToken(self):
        if self.ui.checkBox_3.isChecked():
            self.ui.statusTextEdit.append("New token generated")
    def highPriority(self):
        if self.ui.checkBox_2.isChecked():
            self.ui.statusTextEdit.append("Station priority changed to 1")
        else:
            self.ui.statusTextEdit.append("Station priority changed to 0")
    def read_from_port(self, ser):
        received_data = b''
        while True:
                # Читаем данные из порта
            chunk = ser.read(100)  # Читаем до 100 байт за раз
            if chunk:
                received_data += chunk
                    # Проверяем, есть ли в полученных данных завершающий символ
                if b'~' in received_data:
                    break
            else:
                    # Если данных больше нет, прерываем цикл
                break
        return received_data

    def insert_brackets(self,binary_string):
        result = ""
        count_ones = 0

        for i in range(len(binary_string)):
            if binary_string[i] == '1':
                count_ones += 1
                result += '1'
            elif binary_string[i] == '0':
                if count_ones >= 5:
                    result += '[0]'
                else:
                    result += '0'
                count_ones = 0  # Сбрасываем счетчик единиц после нуля
            elif binary_string[i] == ' ':
                result+=' '
        return result

    def read_data_to_resend(self, ser2):
        data = bytearray()
        # Считываем фиксированную часть пакета (флаг и адреса)
        fixed_part = ser2.read(16)
        if len(fixed_part) < 16:
            return data
        data.extend(fixed_part)

        # Ищем первый разделитель '~'
        while True:
            byte = ser2.read(1)
            if not byte:
                return data  # Неожиданный конец данных
            if byte == b'~':
                data.append(byte[0])
                break

        # Считываем данные до конца пакета (до следующего '~')

        while True:
            byte = ser2.read(1)
            if not byte:
                return data  # Неожиданный конец данных
            if byte == b'~':
                data.append(byte[0])
                break
            data.append(byte[0])

        fcs = ser2.read(8)
        data.extend(fcs)
        if not fcs:
            return data  # Неожиданный конец данных
        print(data)
        return data

    def receive_data(self, ser2):

        # Считываем фиксированную часть пакета (флаг и адреса)
        fixed_part = ser2.read(16)
        if len(fixed_part) < 16:
            return

        flag = fixed_part[:8]
        dest_addr = fixed_part[8:12]
        src_addr = fixed_part[12:16]

        # Ищем первый разделитель '~'
        while True:
            byte = ser2.read(1)
            if not byte:
                return   # Неожиданный конец данных
            if byte == b'~':
                break

        # Считываем данные до конца пакета (до следующего '~')
        data = bytearray()
        while True:
            byte = ser2.read(1)
            if not byte:
                return   # Неожиданный конец данных
            if byte == b'~':
                break
            data.append(byte[0])

        fcs = ser2.read(8)
        if not fcs:
            return   # Неожиданный конец данных

        try:


            self.ui.statusTextEdit.append("Received packet:")
            self.ui.statusTextEdit.append(f"Flag: {flag.decode()}")
            self.ui.statusTextEdit.append(f"Destination: {dest_addr.decode()}")
            self.ui.statusTextEdit.append(f"Source: {src_addr.decode()}")
            self.ui.statusTextEdit.append(f"FCS(rec): {fcs.decode()} FCS:(calc): {self.create_fcs(data)}")

            if fcs.decode() != self.create_fcs(data):
                self.ui.statusTextEdit.append(f"Data with error: {self.perform_unstuffing(data)}")
                data = self.check_and_correct_hamming(data, fcs.decode())

            # Выполняем дестаффинг данных
            unstuffed_data = self.perform_unstuffing(data)
            self.ui.statusTextEdit.append(f"Data (unstuffed): {' '.join(format(b, '08b') for b in unstuffed_data)}")
            self.ui.statusTextEdit.append(f"Data size (unstuffed): {len(unstuffed_data)} bytes")
            str = ' '.join(format(b, '08b') for b in data)
            formatted_string = self.insert_brackets(str)
            self.ui.statusTextEdit.append(f"Data (stuffed)  : {formatted_string}")

            packet1 = Packet(flag.decode("latin-1"), dest_addr.decode("latin-1"), src_addr.decode("latin-1"), bytes(unstuffed_data), "0")
            packet1.fcs = fcs.hex()

            # Преобразуем байты обратно в текст
            try:
                original_text = unstuffed_data.decode('latin-1')
                self.ui.outputTextEdit.insertPlainText(original_text)
            except UnicodeDecodeError:
                self.ui.statusTextEdit.append("Error: Unable to decode unstuffed data")

        except Exception as e:
            self.ui.statusTextEdit.append(f"Error processing packet: {str(e)}")
        return

    def calculate_fcs_size(self, data_size):
                r = 0
                while 2**r < data_size + r + 1:
                    r += 1
                return max(r + 1, 8)  # Минимальный размер FCS теперь 8

    def create_fcs(self, data):
                self.data_size = len(data) * 8
                self.fcs_size = self.calculate_fcs_size(self.data_size)
                self.actual_fcs_size = min(self.fcs_size, 8)

                data_bits = ''.join(format(byte, '08b') for byte in data)
                fcs = ['0'] * 8

                overall_parity = 0
                for i in range(self.actual_fcs_size - 1):
                    parity = 0
                    for j in range(self.data_size):
                        if (j + 1) & (1 << i):
                            parity ^= int(data_bits[j])
                    fcs[i] = str(parity)
                    overall_parity ^= parity

                for bit in data_bits:
                    overall_parity ^= int(bit)

                fcs[self.actual_fcs_size - 1] = str(overall_parity)

                # Заполняем оставшиеся биты нулями, если actual_fcs_size < 8
                for i in range(self.actual_fcs_size, 8):
                    fcs[i] = '0'

                return ''.join(fcs)

    def check_and_correct_hamming(self, data, fcs):
                data_bits = ''.join(format(byte, '08b') for byte in data)
                syndrome = 0

                overall_parity = int(fcs[self.actual_fcs_size - 1])
                calculated_overall_parity = 0

                for i in range(self.actual_fcs_size - 1):
                    parity = 0
                    for j in range(self.data_size):
                        if (j + 1) & (1 << i):
                            parity ^= int(data_bits[j])
                    if parity != int(fcs[i]):
                        syndrome |= (1 << i)
                    calculated_overall_parity ^= parity

                for bit in data_bits:
                    calculated_overall_parity ^= int(bit)

                if syndrome == 0 and calculated_overall_parity == overall_parity:
                    self.ui.statusTextEdit.append("No errors found.")
                    return data
                elif syndrome != 0 and calculated_overall_parity != overall_parity:
                    self.ui.statusTextEdit.append("Single error detected and fixed")
                    error_pos = syndrome - 1
                    corrected_bits = list(data_bits)
                    corrected_bits[error_pos] = '1' if corrected_bits[error_pos] == '0' else '0'
                    corrected_bits = ''.join(corrected_bits)
                    corrected_data = bytes(int(corrected_bits[i:i+8], 2) for i in range(0, len(corrected_bits), 8))
                    return corrected_data
                else:
                    self.ui.statusTextEdit.append("A double error was detected. Correction is not possible.")
                    return data

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget(1)
    widget.setWindowTitle("Station 1")
    widget.show()

    widget2 = Widget(2)
    widget2.setWindowTitle("Station 2")
    widget2.show()

    widget3 = Widget(3)
    widget3.setWindowTitle("Station 3")
    widget3.show()

    sys.exit(app.exec())
