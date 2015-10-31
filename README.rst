envitro
=======

A module for reading configuration values from the OS environment variables.

Compared to using straight os.getenv() this module provides convenience functions,
for parsing basic datatypes. It also allows to specify optional default values if
the environment variable does not exist. Basic environment variable parsing and
sanitizing is also performed.

Usage
-----

.. code-block:: python

    import os
    import envitro

    # fails when environment variables are missing
    bool_required = envitro.bool("BOOL_ENV")
    int_required = envitro.int("INTEGER_ENV")
    str_required = envitro.str("STRING_ENV")

    # basic sanitizing
    os.environ["STR_ENV"] = "  var with spaces  "
    envitro.str("STR_ENV") # returns "var with spaces"

    # falls back to defaults
    bool_default = envitro.bool("BOOL_NOT_FOUND", False)
    int_default = envitro.int("INTEGER_NOT_FOUND", 42)
    str_default = envitro.str("STRING_NOT_FOUND", "my_default")

    # get and set raw environment variables
    envitro.set("EXISTING_VAR", None) # clear the environment variable
    envitro.set("RAW_STRING", " raw_string ")
    envitro.get("RAW_STRING") # returns " raw_string "
    envitro.get("MISSING_RAW_STRING", " defaultval ") # returns " defaultval "

    # utility functions
    envitro.isset("MAYBE_SET_VARIABLE") # return True/False
