from pyb import UART


class LaserLickPort:
    PACKET_START = 0xAA
    DATA_MASK_OPT_RAW = 0x01
    DATA_MASK_CAP_RAW = 0x02

    def __init__(self, port, baudrate=57600):
        assert port.UART is not None, "! LaserLickPort needs a port with UART."
        self.uart = UART(port.UART)
        self.uart.init(baudrate=baudrate, bits=8, parity=None, stop=1, timeout=1, read_buf_len=256)
        self.last_raw_line = None
        self._rx_buffer = b""
        self._max_buffer_len = 512
        self.clear()

    def clear(self):
        if self.uart.any():
            self.uart.read()
        self._rx_buffer = b""

    def set_stream_mask(self, send_opt_raw, send_cap_raw):
        self._write_line("E,{:d},{:d}".format(int(bool(send_opt_raw)), int(bool(send_cap_raw))))

    def read_message(self):
        if self.uart.any():
            chunk = self.uart.read()
            if chunk:
                self._rx_buffer += chunk
                if len(self._rx_buffer) > self._max_buffer_len:
                    if b"\n" in self._rx_buffer:
                        self._rx_buffer = self._rx_buffer.split(b"\n")[-1]
                    else:
                        self._rx_buffer = b""

        while self._rx_buffer:
            start_index = self._rx_buffer.find(bytes([self.PACKET_START]))
            if start_index < 0:
                self._rx_buffer = b""
                return None
            if start_index:
                self._rx_buffer = self._rx_buffer[start_index:]

            if len(self._rx_buffer) < 2:
                return None

            packet_type = self._rx_buffer[1]

            if packet_type == ord("D"):
                if len(self._rx_buffer) < 3:
                    return None
                mask = self._rx_buffer[2]
                payload_length = 0
                if mask & self.DATA_MASK_OPT_RAW:
                    payload_length += 2
                if mask & self.DATA_MASK_CAP_RAW:
                    payload_length += 2
                packet_length = 4 + payload_length
                if len(self._rx_buffer) < packet_length:
                    return None
                packet = self._rx_buffer[:packet_length]
                self._rx_buffer = self._rx_buffer[packet_length:]
                values = self._parse_data_packet(packet)
                if values is not None:
                    return values
                continue

            self._rx_buffer = self._rx_buffer[1:]

        return None

    def _parse_data_packet(self, packet):
        self.last_raw_line = packet
        checksum = 0
        for value in packet[1:-1]:
            checksum ^= value
        if checksum != packet[-1]:
            return None

        mask = packet[2]
        index = 3
        values = {"_type": "D"}

        if mask & self.DATA_MASK_OPT_RAW:
            values["optRaw"] = (packet[index] << 8) | packet[index + 1]
            index += 2
        if mask & self.DATA_MASK_CAP_RAW:
            values["capRaw"] = (packet[index] << 8) | packet[index + 1]
            index += 2
        return values

    def _write_line(self, line):
        self.uart.write(line + "\n")

    def get_last_raw_line(self):
        if self.last_raw_line is None:
            return None
        try:
            return " ".join("{:02X}".format(byte) for byte in self.last_raw_line)
        except Exception:
            return str(self.last_raw_line)
