envitro
=======

[![Build Status](https://travis-ci.org/MarcMeszaros/envitro.svg?branch=master)](https://travis-ci.org/MarcMeszaros/envitro)

A module for reading values from OS environment variables.

Compared to using os.getenv(), this module provides convenience functions,
for parsing basic datatypes. It also allows specifying optional default values if
the environment variable does not exist. Basic environment variable parsing and
sanitizing is also performed.

Usage
-----

```python
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
bool_default = envitro.bool("BOOL_NOT_FOUND", default=False)
int_default = envitro.int("INTEGER_NOT_FOUND", default=42)
float_default = envitro.float("FLOAT_NOT_FOUND", default=42.44)
str_default = envitro.str("STRING_NOT_FOUND", default="my_default")

# try multiple fallback ENV variables
os.environ["FALLBACK_ENV"] = "fallback_val"
single_fallback = envitro.str("MISSING", fallback="FALLBACK_ENV")
multiple_fallback = envitro.str("MISSING", fallback=["FALL_MISSING_1", "FALL_MISSING_2", "FALLBACK_ENV"])

# get and set raw environment variables
envitro.write("EXISTING_VAR", None) # clear the environment variable
envitro.write("RAW_STRING", " raw_string ")
envitro.read("RAW_STRING") # returns " raw_string "
envitro.read("MISSING_RAW_STRING", default=" defaultval ") # returns " defaultval "

# lists/tuples
os.environ["LIST_ENV"] = "item1,item2,item3"
list_required = envitro.list("LIST_ENV") # returns ["item1", "item2", "item3"]
tuple_required = envitro.tuple("LIST_ENV") # returns ("item1", "item2", "item3")
os.environ["LIST_ENV2"] = "item1;item2;item3"
list_required2 = envitro.list("LIST_ENV2", separator=";") # returns ["item1", "item2", "item3"]
tuple_required2 = envitro.tuple("LIST_ENV2", separator=";") # returns ("item1", "item2", "item3")

# utility functions
envitro.isset("MAYBE_SET_VARIABLE") # return True/False
```

Decorators
----------

There are also decorators available to selectively enable or disable functions based on environment
variables.

```python
import envitro

@envitro.decorators.isset('ALLOW_FOO')
def foo():
    return "Hello World"

envitro.write('ALLOW_FOO', '1')
foo() # allowed

envitro.write('ALLOW_FOO', None)
foo() # return "None" and is not executed

@envitro.decorators.bool('ALLOW_REMOTE')
def get_remote(arg1, arg2):
    return call_remote_service(arg1, arg2)

envitro.write('ALLOW_REMOTE', 'True')
get_remote('hello', 'world') # calls remote service

envitro.write('ALLOW_REMOTE', 'False')
get_remote('hello', 'world') # returns "None" and is not executed
```
