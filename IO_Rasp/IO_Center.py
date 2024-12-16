from CommonAssit import TimeControl
# from gpiozero.pins.native import NativeFactory
# from gpiozero import Button as gpButton
# from gpiozero import LED

import threading

import RPi.GPIO as GPIO

# from logilab.common.umessage import message_from_file

# gpio_pin_factory = NativeFactory()
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)


class Input_Port:
    gpio_input = None
    valid_time = 1000
    def __init__(self, gpio_port):
        try:
            self.gpio_input = gpio_port
            GPIO.setup(self.gpio_input, GPIO.IN)
            # self.gpio_input = gpButton(gpio_port, pin_factory=gpio_pin_factory)
        except Exception as error:
            print(f"Cannot create input port. Detail {error}")

    def is_pressed(self):
        return GPIO.input(self.gpio_input) == GPIO.HIGH
        # return self.gpio_input.is_pressed

    def is_released(self):
        return GPIO.input(self.gpio_input) == GPIO.LOW
        # return not self.gpio_input.is_pressed

class Output_Port:
    gpio_output = None

    def __init__(self, gpio_port):
        try:
            self.gpio_output = gpio_port
            GPIO.setup(self.gpio_output, GPIO.OUT)
            # self.gpio_output = LED(gpio_port, pin_factory=gpio_pin_factory)
        except Exception as error:
            print(f"Cannot create output port. Detail {error}")

    def on_with_time_thread(self, time):
        self.on()
        TimeControl.sleep(time)
        self.off()

    def on_with_time(self, time=None):
        if time is None:
            self.on()
        else:
            on_thread = threading.Thread(target=self.on_with_time_thread, args=(time,))
            on_thread.start()

    def off_with_time_thread(self, time):
        self.off()
        TimeControl.sleep(time)
        self.on()

    def off_with_time(self, time=None):
        if time is None:
            self.off()
        else:
            off_thread = threading.Thread(target=self.off_with_time_thread, args=(time,))
            off_thread.start()

    def on(self):
        GPIO.output(self.gpio_output, GPIO.HIGH)
        # self.gpio_output.on()
    def off(self):
        GPIO.output(self.gpio_output, GPIO.LOW)
        # self.gpio_output.off()
