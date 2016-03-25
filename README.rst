fbsd_gpio: cffi-based Python bindings for FreeBSD libgpio
=========================================================

Requirements:

- Python 2.7 or 3.4
- cffi
- sysctl

How to install
--------------

Python package on FreeBSD 11 have problem when using python source that needed to compile thing, so the easiest way is to use the binary packages uploaded to pypi:

.. code-block:: shell

    pip install --only-binary freebsd-11 fbsd_gpio

How to use
----------

The fbsd_gpio module expose two classes, GpioController and GpioPin

Use gpio controller unit 0 (/dev/gpioc0) and list all the pins name:

.. code-block:: python

   from fbsd_gpio import GpioController

   gpioc = GpioController(0)
   for pin in gpioc:
       print(pin)

Set pin 127 to output and logical value 1

.. code-block:: python

   from fbsd_gpio import GpioController, GPIO_VALUE_HIGH

   gpioc = GpioController(0)
   gpioc.pin_output(127)
   # The two following lines are equivalent
   gpioc.pin_set(127, GPIO_VALUE_HIGH)
   gpioc.pin_high(127)

Alternativelly you can use the GpioPin class:

.. code-block:: python

   from fbsd_gpio import GpioPin, GPIO_VALUE_HIGH

   pin = GpioPin(127, unit=0)
   pin.ouput = True
   # The following lines are equivalent
   pin.set(GPIO_VALUE_HIGH)
   pin.high()
   pin(GPIO_VALUE_HIGH)

Or use the name of the pin directly:

.. code-block:: python

   from fbsd_gpio import GpioController, GPIO_VALUE_HIGH

   gpioc = GpioController(0)
   gpioc.gpioled0.output = True
   # The three following lines are equivalent
   gpioc.gpioled.set(GPIO_VALUE_HIGH)
   gpioc.gpioled0.high()
   gpioc.gpioled0(GPIO_VALUE_HIGH)

Get the value of a pin:

.. code-block:: python

   from fbsd_gpio import GpioPin

   pin = GpioPin(128, unit=0)
   if pin.input:
       print('Pin is input mode')
   else
       print('Pin is output mode')
   # The two following lines are equivalent
       value = pin.get()
       value = pin()

Toggle the value of a pin:

.. code-block:: python

   from fbsd_gpio import GpioPin

   pin = GpioPin(128, unit=0)
   pin.toggle()

Change the name of a pin:

.. code-block:: python

   from fbsd_gpio import GpioPin

   pin = GpioPin(128, unit=0)
   pin.name = 'green_led'
