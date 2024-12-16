from ctypes import *

class Wrapper_Serial:
    dll_path = "./comPortdll.dll"
    def __init__(self, port, baudrate=38400, bytesize=8, parity=0, stop_bit=1):
        self.c_lib = self.load_lib()
        self.create_port = self.c_lib.createPort(port, baudrate, bytesize, parity, int(stop_bit * 2))
        self.read_from_port = self.c_lib.ReadFromPort
        self.read_from_port.restype = c_char_p

        self.isOpened = self.c_lib.isOpened
        self.isOpened.restype = c_bool

        # self.write_to_port = self.c_lib.WriteToPortEx
        # self.write_to_port.argtype = (c_wchar_p, c_size_t)

    def load_lib(self):
        try:
            lib = cdll.LoadLibrary(self.dll_path)
            return lib
        except Exception as error:
            print(f"Cannot load the dll. Detail {error}")
            return None

    def write(self, cmd):
        self.c_lib.WriteToPortEx(cmd, len(cmd) * 2)

    def read_all(self):
        return self.read_from_port().decode("utf-8")

    def close(self):
        self.c_lib.closePort()

    def open(self):
        return

    def isOpen(self):
        return self.isOpened()
