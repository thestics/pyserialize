#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# Author: Danil Kovalenko

from serialization.common import EncoderDecoderBase


class IntFieldDecoder(EncoderDecoderBase, endpoint=True):

    def decode_int(self, value: dict) -> int:
        hex_val = value.get('value')
        real_val = int(hex_val, 16)
        return real_val
