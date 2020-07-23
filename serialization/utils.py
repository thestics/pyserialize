#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# Author: Danil Kovalenko

import re
import typing as tp

from serialization.err import SerializationError


class NamingError(SerializationError):
    pass


class classproperty(property):
    """`property` analogue for class methods"""

    def __get__(self, obj, objtype=None):
        return super(classproperty, self).__get__(objtype)

    def __set__(self, obj, value):
        super(classproperty, self).__set__(type(obj), value)

    def __delete__(self, obj):
        super(classproperty, self).__delete__(type(obj))


def _parse_class_name(cls: tp.Type) -> tp.Tuple[str, str]:
    """
    Parse name of class, handle non compliance with naming conventions
    """
    name_patt = re.compile(r'(?P<encoder_type>\w+)Field(?P<type>Encoder|Decoder)')
    match = name_patt.fullmatch(cls.__name__)

    if match is None:
        raise NamingError('Incorrect encoder/decoder class naming. '
                          'Expected: <Type>Field(Encoder|Decoder)')

    return match.group('encoder_type'), match.group('type')


def get_operated_type_from_class(cls: tp.Type) -> str:
    """
    From provided encoder/decoder class derive
    name of type it operates with
    """
    enc_type, proc_type = _parse_class_name(cls)
    return enc_type


def get_process_type_from_class(cls: tp.Type) -> str:
    """
    From provided encoder/decoder class derive whether it is an encoder
    or a decoder
    """
    enc_type, proc_type = _parse_class_name(cls)
    return proc_type
