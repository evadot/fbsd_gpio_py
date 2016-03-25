from _fbsd_gpio import ffi, lib as _gpio
from sysctl import filter as sysctl

from .constant import *

GPIOCONTROLLERPOOL= {}

class GpioController(object):
        def __init__(self, unit):
                """GpioController __init__
                :param: unit The GPIO controller unit to operate on
                """
                try:
                        self._desc = sysctl('dev.gpio.{0}.%desc'.format(unit))[0].value
                except IndexError:
                        raise IOError
                self._handle = None
                self._unit = unit

        def __del__(self):
                self.close()

        def __repr__(self):
                return self._desc

        def __getattr__(self, pinname):
                """Magic method to obtain a GpioPin by it's name
                :param pinname: The pin name
                :returns: A GpioPin object
                """
                pin_list = self.pin_list()
                for pin in pin_list:
                        if pin.name == pinname:
                                return pin
                raise AttributeError

        def __iter__(self):
                """Yield every pin available by this controller
                """
                pin_list = self.pin_list()
                for pin in pin_list:
                        yield pin

        def open(self):
                """Obtain an handle for the gpio controller
                """
                try:
                        if GPIOCONTROLLERPOOL[self._unit]['handle'] != -1:
                                GPIOCONTROLLERPOOL[self._unit]['ref'] = GPIOCONTROLLERPOOL[self._unit]['ref'] + 1
                                return
                except KeyError:
                        GPIOCONTROLLERPOOL[self._unit] = {}
                        GPIOCONTROLLERPOOL[self._unit]['handle'] = _gpio.gpio_open(self._unit)
                        if GPIOCONTROLLERPOOL[self._unit]['handle'] == -1:
                                del GPIOCONTROLLERPOOL[self._unit]
                                raise IOError
                        GPIOCONTROLLERPOOL[self._unit]['ref'] = 1

        def close(self):
                """Close the handle for the gpio controller
                """
                try:
                        GPIOCONTROLLERPOOL[self._unit]['ref'] = GPIOCONTROLLERPOOL[self._unit]['ref'] - 1
                        if GPIOCONTROLLERPOOL[self._unit]['ref'] == 0:
                                _gpio.gpio_close(GPIOCONTROLLERPOOL[self._unit]['handle'])
                                del GPIOCONTROLLERPOOL[self._unit]
                except KeyError:
                        pass

        @property
        def handle(self):
                """The handle for the gpio controller
                :returns: The handle
                """
                try:
                        return GPIOCONTROLLERPOOL[self._unit]['handle']
                except KeyError:
                        self.open()
                        return GPIOCONTROLLERPOOL[self._unit]['handle']

        @property
        def description(self):
                """Device description of the gpio controller
                :returns: The description
                """
                return self._desc

        def pin_get_config(self, pin):
                """Get the pin configuration
                :param pin: The pin number
                :returns: The capabilities, flags and name
                """
                pin_cfg = ffi.new('gpio_config_t *')
                pin_cfg.g_pin = pin
                if _gpio.gpio_pin_config(self.handle, pin_cfg) != 0:
                        raise ValueError
                return pin_cfg.g_caps, pin_cfg.g_flags, ffi.string(pin_cfg.g_name)

        def pin_set_name(self, pin, name):
                """Set the name of the pin
                :param name: The name
                """
                if _gpio.gpio_pin_set_name(self.handle, pin, name) != 0:
                        raise IOError

        def pin_low(self, pin):
                """Set the pin value to 0
                :param pin: The pin number
                """
                if _gpio.gpio_pin_low(self.handle, pin) != 0:
                        raise IOError

        def pin_high(self, pin):
                """Set the pin value to 1
                :param pin: The pin number
                """
                if _gpio.gpio_pin_high(self.handle, pin) != 0:
                        raise IOError

        def pin_toggle(self, pin):
                """Toggle the value of the pin
                :param pin: The pin number
                """
                if _gpio.gpio_pin_toggle(self.handle, pin) != 0:
                        raise IOError

        def pin_input(self, pin):
                """Set the pin to input mode
                :param pin: The pin number
                """
                if _gpio.gpio_pin_input(self.handle, pin) != 0:
                        raise IOError

        def pin_output(self, pin):
                """Set the pin to output mode
                :param pin: The pin number
                """
                if _gpio.gpio_pin_output(self.handle, pin) != 0:
                        raise IOError

        def pin_set(self, pin, value):
                """Set the pin value
                :param pin: The pin number
                ;param value: The value to be set (0 or 1)
                """
                if value not in GPIO_VALUES:
                        raise ValueError
                if _gpio.gpio_pin_set(self.handle, pin, value) != 0:
                        raise IOError

        def pin_get(self, pin):
                """Get the value of the pin
                :param pin: The pin number
                :returns: The value
                """
                ret = _gpio.gpio_pin_get(self.handle, pin)
                if ret == -1:
                        raise IOError
                return ret

        def pin_list(self):
                """Get a list of GpioPin object that the controller manages
                :returns: The list of GpioPin
                """
                i = 0
                pin_list = []
                while True:
                        try:
                                pin = GpioPin(i, controller=self)
                        except ValueError:
                                break
                        pin_list.append(pin)
                        i = i + 1

                return pin_list

        def pin(self, num):
                """Return a GpioPin based on the number
                :param num: The pin number
                :returns: A GpioPin object
                """
                return GpioPin(num, controller=self)


class GpioPin(object):
        def __init__(self, num, unit=None, controller=None):
                """GpioPin __init__
                :param num: The pin number
                :param unit: The controller unit number
                :param controller: The GpioController object
                """
                self._num = num
                self._controller = controller
                if unit is not None:
                        self._controller = GpioController(unit)

                if not self._controller:
                        raise ValueError

                self._caps, self._flags, self._name = self._controller.pin_get_config(self._num)

        def __repr__(self):
                """Return the name as the representation
                """
                return self._name

        def __call__(self, value=None):
                """Set or get the value of the pin
                :param value: If set, set the value of the pin
                """
                if value:
                        self._controller.pin_set(self._num, value)
                return self._controller.pin_get(self._num)

        @property
        def name(self):
                """Return the name of the pin
                """
                return self._name

        @name.setter
        def name(self, name):
                """Set the name of the pin
                :param name: The name
                """
                self._controller.pin_set_name(self._num, name)
                self._name = name

        @property
        def input(self):
                """Returns True if the pin is in input mode
                """
                if self._flags & GPIO_PIN_INPUT:
                        return True
                return False

        @input.setter
        def input(self, input):
                """Set the pin mode to input
                :param input: True to set it to input, False to set it to output
                """
                if input == True:
                        self._controller.pin_input(self._num)
                else:
                        self._controller.pin_output(self._num)

        @property
        def output(self):
                """Returns True if the pin is in output mode
                """
                if self._flags & GPIO_PIN_OUTPUT:
                        return True
                return False

        @output.setter
        def output(self, output):
                """Set the pin mode to output
                :param output: True to set it to output, False to set it to input
                """
                if output == True:
                        self._controller.pin_output(self._num)
                else:
                        self._controller.pin_input(self._num)

        def low(self):
                """Set the pin to low
                """
                self._controller.pin_low(self._num)

        def high(self):
                """Set the pin to high
                """
                self._controller.pin_high(self._num)

        def toggle(self):
                """Toggle the pin value
                """
                self._controller.pin_toggle(self._num)

        def set(self, value):
                """Set the pin value
                :param value: The value
                """
                self._controller.pin_set(self._num, value)

        def get(self):
                """Get the pin value
                """
                return self._controller.pin_get(self._num)
