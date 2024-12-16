from Connection.Serial_Communication_Wrapper import Wrapper_Serial
from CommonAssit import TimeControl

def main():
    serial_com = Wrapper_Serial(2, stop_bit=1)
    time_start = TimeControl.time()
    serial_com.write("@asdfkajsf\r\n")
    print(f"Write time: {TimeControl.time() - time_start}")

    start_time = TimeControl.time()
    while TimeControl.time() - start_time < 10000:
        if serial_com.isOpen():
            ret = serial_com.read()
            if ret != "":
                print(ret)
    serial_com.close()
    print(serial_com.isOpen())

if __name__ == '__main__':
    main()