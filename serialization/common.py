#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# Author: Danil Kovalenko
from __future__ import annotations
import typing as tp

from serialization.err import SerializationError
from serialization.utils import get_operated_type_from_class, get_process_type_from_class, classproperty


class ConsistencyError(SerializationError):
    pass


class EncoderDecoderBase:
    """
    Base class for fields encoders/decoders

    Defines set of supported types. For each supported type one must
    implement encoder and decoder classes. Latter has to implement
    `encode_<TYPENAME>` and `decode_<TYPENAME>` respectively.
    Collects all subclasses, which specify `endpoint=True` in inheritance.
    For each type defined in `supported_types` tests that one have implemented
    class <TYPENAME>Field<Encoder|Decoder>, which in turn implements
    methods `encode_<TYPENAME>` and `decode_<TYPENAME>`
    """

    _encoders = {}
    _decoders = {}

    def __init_subclass__(cls, **kwargs):
        if kwargs.get('endpoint', False) is True:
            field_type = get_operated_type_from_class(cls)
            proc_type = get_process_type_from_class(cls)

            if proc_type == 'Encoder':
                EncoderDecoderBase._encoders[field_type] = cls
            else:
                EncoderDecoderBase._decoders[field_type] = cls

    @classmethod
    def assert_type_consistency(cls):
        for k, v in cls._encoders.items():
            if k not in cls._decoders:
                raise ConsistencyError(f'For type `{k}` encoder defined, '
                                       f'but decoder is not.')

        for k, v in cls._decoders.items():
            if k not in cls._encoders:
                raise ConsistencyError(f'For type `{k} decoder defined,`'
                                       f'but encoder is not.')

    @classproperty
    def encoders(cls) -> tp.Tuple[tp.Type[EncoderDecoderBase], ...]:
        cls.assert_type_consistency()
        return tuple(cls._encoders.values())

    @classproperty
    def decoders(cls) -> tp.Tuple[tp.Type[EncoderDecoderBase], ...]:
        cls.assert_type_consistency()
        return tuple(cls._decoders.values())


def get_encoder():
    """
    Get field encoder.

    """
    bases = EncoderDecoderBase.encoders

    class Encoder(*bases):
        """
        Class for all field encoder

        Inherits on-the-fly from all currently known field encoders
        Implements main method `encode` which encodes python object to json value
        """

        def encode(self, value: object) -> dict:
            err_msg = f'Unsupported value type: {type(value).__name__}'

            encoder_name = f'encode_{type(value).__name__}'
            encoder = getattr(self, encoder_name, NotImplemented)

            if encoder is NotImplemented:
                raise NotImplementedError(err_msg)

            return encoder(value)

    return Encoder()


def get_decoder():
    """
    Get field decoder.

    """
    bases = EncoderDecoderBase.decoders

    class Decoder(*bases):
        """
        Class for all field decoder

        Inherits on-the-fly from all currently known field decoders
        Implements main method `decoder` which decodes json value to python object
        """

        def decode(self, value: dict) -> object:
            val_type = value.get('type')
            err_msg = f'Unsupported value type: {val_type}'
            decoder_name = f'decode_{val_type}'
            decoder = getattr(self, decoder_name, NotImplementedError)

            if decoder is NotImplemented:
                raise NotImplementedError(err_msg)

            return decoder(value)

    return Decoder()
