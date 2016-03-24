from cffi import FFI
ffi = FFI()

ffi.set_source("_fbsd_gpio",
    """
    #include <libgpio.h>
    #include <sys/gpio.h>
    """,
    libraries=['gpio'])

ffi.cdef("""
/* From sys/gpio.h and libgpio.h */
/* Copyright (c) 2009, Oleksandr Tymoshenko <gonzo@FreeBSD.org> */
/* Copyright (c) 2013-2014 Rui Paulo <rpaulo@FreeBSD.org> */
/* Copyright (c) 2009 Marc Balmer <marc@msys.ch> */
/* Copyright (c) 2004 Alexander Yurchenko <grange@openbsd.org> */

/* GPIO pin states */
#define GPIO_PIN_LOW            0x00    /* low level (logical 0) */
#define GPIO_PIN_HIGH           0x01    /* high level (logical 1) */

/* Max name length of a pin */
#define GPIOMAXNAME             64

#define GPIO_INVALID_HANDLE -1
typedef int gpio_handle_t;
typedef uint32_t gpio_pin_t;

/*
 * Structure describing a GPIO pin configuration.
 */
typedef struct {
        gpio_pin_t      g_pin;
        char            g_name[GPIOMAXNAME];
        uint32_t        g_caps;
        uint32_t        g_flags;
} gpio_config_t;

typedef enum {
        GPIO_VALUE_INVALID      = -1,
        GPIO_VALUE_LOW          = GPIO_PIN_LOW,
        GPIO_VALUE_HIGH         = GPIO_PIN_HIGH
} gpio_value_t;

/*
 * Open /dev/gpiocN or a specific device.
 */
gpio_handle_t   gpio_open(unsigned int);
gpio_handle_t   gpio_open_device(const char *);
void            gpio_close(gpio_handle_t);
/*
 * Get a list of all the GPIO pins.
 */
int             gpio_pin_list(gpio_handle_t, gpio_config_t **);
/*
 * GPIO pin configuration.
 *
 * Retrieve the configuration of a specific GPIO pin.  The pin number is
 * passed through the gpio_config_t structure.
 */
int             gpio_pin_config(gpio_handle_t, gpio_config_t *);
/*
 * Sets the GPIO pin name.  The pin number and pin name to be set are passed
 * as parameters.
 */
int             gpio_pin_set_name(gpio_handle_t, gpio_pin_t, char *);
/*
 * Sets the GPIO flags on a specific GPIO pin.  The pin number and the flags
 * to be set are passed through the gpio_config_t structure.
 */
int             gpio_pin_set_flags(gpio_handle_t, gpio_config_t *);
/*
 * GPIO pin values.
 */
int             gpio_pin_get(gpio_handle_t, gpio_pin_t);
int             gpio_pin_set(gpio_handle_t, gpio_pin_t, int);
int             gpio_pin_toggle(gpio_handle_t, gpio_pin_t);
/*
 * Helper functions to set pin states.
 */
int             gpio_pin_low(gpio_handle_t, gpio_pin_t);
int             gpio_pin_high(gpio_handle_t, gpio_pin_t);
/*
 * Helper functions to configure pins.
 */
int             gpio_pin_input(gpio_handle_t, gpio_pin_t);
int             gpio_pin_output(gpio_handle_t, gpio_pin_t);
int             gpio_pin_opendrain(gpio_handle_t, gpio_pin_t);
int             gpio_pin_pushpull(gpio_handle_t, gpio_pin_t);
int             gpio_pin_tristate(gpio_handle_t, gpio_pin_t);
int             gpio_pin_pullup(gpio_handle_t, gpio_pin_t);
int             gpio_pin_pulldown(gpio_handle_t, gpio_pin_t);
int             gpio_pin_invin(gpio_handle_t, gpio_pin_t);
int             gpio_pin_invout(gpio_handle_t, gpio_pin_t);
int             gpio_pin_pulsate(gpio_handle_t, gpio_pin_t);
""")

if __name__ == "__main__":
    ffi.compile()
