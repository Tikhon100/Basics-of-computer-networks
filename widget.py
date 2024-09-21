import sys
import serial
import glob
import re
from packet import Packet
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Slot
from ui_form import Ui_Widget
from text_edit_logger import QTextEditLogger
import random
import logging

from typing import List
# this is sparta
class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        self.log_text_edit = QTextEditLogger(self.ui.statusTextEdit)
        self.log_text_edit.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger = logging.getLogger()
        #logger.addHandler(self.log_text_edit)
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
        try:
            selected_port_pair = self.ui.comboBox.currentText()
            com_port1, com_port2 = selected_port_pair.split(" - ")

            port1 = self.com_to_real_port(com_port1)
            port2 = self.com_to_real_port(com_port2)

            speed = self.ui.comboBox_2.currentText()

            ser1 = serial.Serial(port1, baudrate=speed, timeout=1)
            ser2 = serial.Serial(port2, baudrate=speed, timeout=1)

            data_to_send = self.ui.inputTextEdit.toPlainText()
            packets = self.create_packets(data_to_send, "00001110", "0000", com_port1)
            #sent_data_length = len(data_to_send)
            self.ui.inputTextEdit.clear()
            for packet1 in packets:
                packet_data = packet1.data_after_stuffing
                fcs = self.create_fcs(packet_data)
                self.ui.statusTextEdit.clear()
                if self.ui.checkBox.isChecked():
                    packet_data = self.emulate_errors(packet_data)

                """print(f"Оригинальные данные: {packet_data}")
                print(f"Оригинальный FCS: {fcs}")

                print("\nСлучай 1: Без ошибок")
                result = self.check_and_correct_hamming(packet_data, fcs)
                print(f"Результат: {result}")
                print(f"Совпадают с оригиналом: {result == packet_data}")

                print("\nСлучай 2: Одиночная ошибка")
                single_error_data = self.simulate_errors(packet_data, [random.randint(1,len(packet_data))])  # Ошибка в 15-м бите
                print(single_error_data)
                corrected_data = self.check_and_correct_hamming(single_error_data, fcs)
                if corrected_data:
                    print(f"Исправленные данные: {corrected_data}")
                    print(f"Совпадают с оригиналом: {corrected_data == packet_data}")"""


                str3 = ','.join(str(b) for b in packet_data)
                char_list = [chr(int(b)) for b in str3.split(',')]
                result_string = ''.join(char_list)

                print(f"sended {result_string}")
                data_to_send = f"{packet1.flag}{packet1.destination_address}{packet1.source_address}~{result_string}~{fcs}".encode("latin-1")

                for byte in data_to_send:
                    ser1.write(bytes([byte]))

            self.ui.outputTextEdit.clear()

            self.receive_data(ser2)

            ser1.close()
            ser2.close()

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

    def emulate_errors(self, data):
        random_int = random.randint(0, 100)
        print(random_int)

        if random_int <= 60:
            if len(data)>1:
                data = self.simulate_errors(data, [15])
                self.ui.statusTextEdit.append("One bit was changed")
        elif 60 < random_int < 85:
            if len(data)>4:
                data = self.simulate_errors(data, [15,30])
                self.ui.statusTextEdit.append("Two bits were changed")
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



    def receive_data(self, ser2):
            received_packets = []

            while True:
                # Считываем фиксированную часть пакета (флаг и адреса)
                fixed_part = ser2.read(16)
                if len(fixed_part) < 16:
                    break  # Недостаточно данных для полного пакета

                flag = fixed_part[:8]
                dest_addr = fixed_part[8:12]
                src_addr = fixed_part[12:16]

                # Ищем первый разделитель '~'
                while True:
                    byte = ser2.read(1)
                    if not byte:
                        return received_packets  # Неожиданный конец данных
                    if byte == b'~':
                        break

                # Считываем данные до конца пакета (до следующего '~')
                data = bytearray()
                while True:
                    byte = ser2.read(1)
                    if not byte:
                        return received_packets  # Неожиданный конец данных
                    if byte == b'~':
                        break
                    data.append(byte[0])

                fcs = ser2.read(8)
                if not fcs:
                    return received_packets  # Неожиданный конец данных

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
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
