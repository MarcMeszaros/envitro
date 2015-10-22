envitro
=======

A module for reading configuration values from the OS environment variables.

Compared to using straight os.getenv() this module provides convenience functions,
for parsing basic datatypes. It also allows to specify optional default values if
the environment variable does not exist.

Usage
-----

.. code-block:: python

    import envitro

    # fails when environment variables are missing
    bool_required = envitro.bool("BOOL_ENV")
    int_required = envitro.int("INTEGER_ENV")
    str_required = envitro.str("STRING_ENV")

    # falls back to defaults
    bool_default = envitro.bool("BOOL_NOT_FOUND", False)
    int_default = envitro.int("INTEGER_NOT_FOUND", 42)
    str_default = envitro.str("STRING_NOT_FOUND", "my_default")
