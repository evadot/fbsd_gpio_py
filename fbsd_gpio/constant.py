#
# Pin caps/flags
#
GPIO_PIN_INPUT = 0x1
GPIO_PIN_OUTPUT = 0x2
GPIO_PIN_OPENDRAIN = 0x4
GPIO_PIN_PUSHPULL = 0x8
GPIO_PIN_TRISTATE = 0x10
GPIO_PIN_PULLUP = 0x20
GPIO_PIN_PULLDOWN = 0x40
GPIO_PIN_INVIN = 0x80
GPIO_PIN_INVOUT = 0x100
GPIO_PIN_PULSTATE = 0x200

GPIO_CAPS = [GPIO_PIN_INPUT,
             GPIO_PIN_OUTPUT,
             GPIO_PIN_OPENDRAIN,
             GPIO_PIN_PUSHPULL,
             GPIO_PIN_TRISTATE,
             GPIO_PIN_PULLUP,
             GPIO_PIN_PULLDOWN,
             GPIO_PIN_INVIN,
             GPIO_PIN_INVOUT,
             GPIO_PIN_PULSTATE]

#
# Pin Values
#
GPIO_VALUE_LOW = 0
GPIO_VALUE_HIGH = 1

GPIO_VALUES = [GPIO_VALUE_LOW, GPIO_VALUE_HIGH]

#
# Event related value
#
GPIO_EVENT_FALLING = 0x1
GPIO_EVENT_RISING = 0x2

GPIO_EVENTS = [GPIO_EVENT_RISING, GPIO_EVENT_FALLING]
