from time import sleep

from fbsd_gpio import (
    GpioPin,
    GPIO_PIN_PULLDOWN,
    GPIO_PIN_PULLUP,
)

SPI_MODE_NONE = 0
SPI_MODE_CPHA = 1
SPI_MODE_CPOL = 2
SPI_MODE_CPOL_CPHA = 3


class GpioSPIBB(object):
    def __init__(self, sclk, mosi, miso, ss, mode=0):
        self._sclk = GpioPin(sclk[1], unit=sclk[0])
        self._mosi = GpioPin(mosi[1], unit=mosi[0])
        self._miso = GpioPin(miso[1], unit=miso[0])
        self._ss = GpioPin(ss[1], unit=ss[0])

        self._sclk.output = True
        self._sclk.flags = GPIO_PIN_PULLDOWN
        self._mosi.output = True
        self._mosi.flags = GPIO_PIN_PULLDOWN
        self._miso.input = True
        self._miso.flags = GPIO_PIN_PULLDOWN
        self._ss.output = True
        self._ss.flags = GPIO_PIN_PULLUP

        self._ss.high()
        self._mode = mode

    def transfer_byte(self, data):
        """Transfer a byte
        :param data: The byte to transfer
        :returns: The byte that was read
        """
        bitmask = 0x80
        ret = 0
        for i in range(0, 8):
            if data & bitmask:
                self._mosi.high()
            else:
                self._mosi.low()

            self._sclk.toggle()
            sleep(0.0001)
            ret = ret << 1
            if self._miso():
                ret = ret | 1
            self._sclk.toggle()
            sleep(0.0001)

            bitmask = bitmask >> 1
        return ret

    def transfer_begin(self):
        """Begin a transfer"""
        self._ss.low()

        if self._mode == SPI_MODE_CPOL or self._mode == SPI_MODE_CPHA:
            self._sclk.high()
        else:
            self._sclk.low()

    def transfer_end(self):
        """End a transfer"""
        if self._mode == SPI_MODE_CPOL or self._mode == SPI_MODE_CPHA:
            self._sclk.high()
        else:
            self._sclk.low()
        self._ss.high()

    def transfer(self, data):
        """Do an SPI transfer
        :param data: A list of byte to transfer
        :returns: The list a read bytes
        """
        self.transfer_begin()

        ret = []
        for b in data:
            ret.append(self.transfer_byte(b))

        self.transfer_end()

        return ret
