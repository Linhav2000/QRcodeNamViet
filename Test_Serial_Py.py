import serial
from os import linesep
import serial.tools.list_ports
from CommonAssit import TimeControl

port_number = "COM2"
baudrate = 38400
bitsize = serial.EIGHTBITS
parity = serial.PARITY_NONE
stop_bit = serial.STOPBITS_ONE


def get_device_name(serial_number):
    """
    Get full device name/path from serial number
    Parameters
    ----------
    serial_number: string
        The usb-serial's serial number
    Returns
    -------
    string
        Full device name/path, e.g. /dev/ttyUSBx (on *.nix system or COMx on Windows)
    Raises
    ------
    IOError
        When not found device with this serial number
    """
    serial_numbers = []
    activePorts = serial.tools.list_ports.comports()
    for pinfo in activePorts:
        if str(pinfo.name).strip() == str(serial_number).strip():
            return pinfo.device
        # save list of serial numbers for user reference
        serial_numbers.append(pinfo.name.encode('utf-8'))
    raise IOError(
        'Could not find device with provided serial number {}Found devices with following serial numbers: {}{}'.format(
            linesep, linesep, serial_numbers))

def sendAsciiData(serial_port, data):
    if not serial_port.isOpen():
        print("Serial Send Data: The port is not open!")
        return
    dataSend = str(data)
    try:
        if serial_port.isOpen():
            serial_port.write(dataSend.encode("utf-8"))
            print("Serial Data Send: {}".format(data))
        else:
            print("Cannot connect to the serial port")
            return
    except Exception as error:
        print("ERROR Serial Send Data - ERROR; {}".format(error))
        return
def readAsciiData(serial_port):
    output = ""
    if not serial_port.isOpen():
        return output
    try:
        res = serial_port.read_all()
        output += res.decode('utf-8')
    except:
        pass

    return output
if __name__ == '__main__':
    comm = serial.Serial()
    comm.baudrate = baudrate
    comm.stopbits = stop_bit
    comm.parity = parity
    comm.bytesize = bitsize

    try:
        device = get_device_name(port_number)
        comm.port = device
        # Set RTS line to low logic level
        comm.rts = False
        comm.open()
    except Exception as ex:
        print(f"Error open port detail {ex}")

    sendAsciiData(comm, "@ABC\r\n")
    TimeControl.sleep(3)
    time_start = TimeControl.time()

    while TimeControl.time() - time_start < 3000:
        res = readAsciiData(comm)
        if res != "":
            print(res)


    comm.close()

    print("End")

