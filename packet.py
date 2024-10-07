
class Packet:
    def __init__(self, flag, destination_address, source_address, data_before_stuffing, fcs):
        self.flag = flag
        self.destination_address = destination_address
        self.source_address = source_address
        self.data_before_stuffing = data_before_stuffing
        self.fcs = fcs

    @property
    def flag(self):
        return self._flag

    @flag.setter
    def flag(self, value):
        if isinstance(value, bytes) and len(value) != 8:
            raise ValueError("Поле flag должно состоять из 8 байт")
        self._flag = value

    @property
    def destination_address(self):
        return self._destination_address

    @destination_address.setter
    def destination_address(self, value):
        if isinstance(value, bytes) and len(value) != 10:
            raise ValueError("Поле destination_address должно состоять из 10 байт")
        self._destination_address = value

    @property
    def source_address(self):
        return self._source_address

    @source_address.setter
    def source_address(self, value):
        if isinstance(value, bytes) and len(value) != 4:
            raise ValueError("Поле source_address должно состоять из 4 байт")
        self._source_address = value

    @property
    def data_before_stuffing(self):
        return self._data_before_stuffing

    @data_before_stuffing.setter
    def data_before_stuffing(self, value):
        if isinstance(value, bytes) and len(value) > 15:
            raise ValueError("Поле data_before_stuffing не должно превышать 15 символов")
        self._data_before_stuffing = value
        self._data_after_stuffing = self._perform_stuffing(value)

    def _perform_stuffing(self, data):
            # Преобразуем байты в строку битов
        bit_string = ''.join(format(byte, '08b') for byte in data)

        stuffed_bits = ''
        count_ones = 0

        for bit in bit_string:
            stuffed_bits += bit
            if bit == '1':
                count_ones += 1
                if count_ones == 5:
                    stuffed_bits += '0'  # Вставляем 0 после пяти единиц
                    count_ones = 0
            else:
                count_ones = 0

            # Дополняем строку нулями справа до кратности 8
        while len(stuffed_bits) % 8 != 0:
            stuffed_bits += '0'
            # Преобразуем обратно в байты
        stuffed_bytes = bytes(int(stuffed_bits[i:i+8], 2) for i in range(0, len(stuffed_bits), 8))

        return stuffed_bytes



    @property
    def data_after_stuffing(self):
        return self._data_after_stuffing


class token:
    def __init__(self, priority1, priority2, priority3, full_flag):
        self._priority1 = priority1
        self._priority2 = priority2
        self._priority3 = priority3
        self.full_flag = full_flag

    @property
    def priority1(self):
        return self._priority1

    @priority1.setter
    def priority1(self, value):
        if isinstance(value, bytes) and len(value) != 1:
            raise ValueError("Поле priority1 должно состоять из 1 байта")
        self._priority1 = value

    @property
    def priority2(self):
        return self._priority2

    @priority2.setter
    def priority2(self, value):
        if isinstance(value, bytes) and len(value) != 1:
            raise ValueError("Поле priority2 должно состоять из 1 байта")
        self._priority2 = value

    @property
    def priority3(self):
        return self._priority3

    @priority3.setter
    def priority3(self, value):
        if isinstance(value, bytes) and len(value) != 1:
            raise ValueError("Поле priority3 должно состоять из 1 байта")
        self._priority3 = value

    @property
    def full_flag(self):
        return self.full_flag

    @full_flag.setter
    def full_flag(self, value):
        if isinstance(value, bytes) and len(value) != 1:
            raise ValueError("Поле full_flag должно состоять из 1 байта")
        self._full_flag = value

