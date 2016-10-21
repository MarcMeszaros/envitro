envitro
=======

A module for reading values from OS environment variables.

Compared to using os.getenv(), this module provides convenience functions,
for parsing basic datatypes. It also allows specifying optional default values if
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
    float_required = envitro.float("FLOAT_ENV")
    str_required = envitro.str("STRING_ENV")

    # basic sanitizing
    os.environ["STR_ENV"] = "  var with spaces  "
    envitro.str("STR_ENV") # returns "var with spaces"

    # falls back to defaults
    bool_default = envitro.bool("BOOL_NOT_FOUND", False)
    int_default = envitro.int("INTEGER_NOT_FOUND", 42)
    float_default = envitro.float("FLOAT_NOT_FOUND", 42.44)
    str_default = envitro.str("STRING_NOT_FOUND", "my_default")

    # get and set raw environment variables
    envitro.set("EXISTING_VAR", None) # clear the environment variable
    envitro.set("RAW_STRING", " raw_string ")
    envitro.get("RAW_STRING") # returns " raw_string "
    envitro.get("MISSING_RAW_STRING", " defaultval ") # returns " defaultval "

    # lists/tuples
    os.environ["LIST_ENV"] = "item1,item2,item3"
    list_required = envitro.list("LIST_ENV") # returns ["item1", "item2", "item3"]
    tuple_required = envitro.tuple("LIST_ENV") # returns ("item1", "item2", "item3")
    os.environ["LIST_ENV2"] = "item1;item2;item3"
    list_required2 = envitro.list("LIST_ENV2", separator=";") # returns ["item1", "item2", "item3"]
    tuple_required2 = envitro.tuple("LIST_ENV2", separator=";") # returns ("item1", "item2", "item3")

    # utility functions
    envitro.isset("MAYBE_SET_VARIABLE") # return True/False


Decorators
----------

There are also decorators available to selectively enable or disable functions based on environment
variables.

.. code-block:: python

    import envitro

    @envitro.decorators.isset('ALLOW_FOO')
    def foo():
        return "Hello World"

    envitro.set('ALLOW_FOO', '1')
    foo() # allowed

    envitro.set('ALLOW_FOO', None)
    foo() # return "None" and is not executed

    @envitro.decorators.bool('ALLOW_REMOTE')
    def get_remote(arg1, arg2):
        return call_remote_service(arg1, arg2)

    envitro.set('ALLOW_REMOTE', 'True')
    get_remote('hello', 'world') # calls remote service

    envitro.set('ALLOW_REMOTE', 'False')
    get_remote('hello', 'world') # returns "None" and is not executed
