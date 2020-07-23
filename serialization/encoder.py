#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# Author: Danil Kovalenko

from serialization.common import EncoderDecoderBase


class IntFieldEncoder(EncoderDecoderBase, endpoint=True):

    def encode_int(self, value: int) -> dict:
        return {'type': 'int',
                'value': hex(value)[2:]}
