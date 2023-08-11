# SPDX-FileCopyrightText: 2019 Kevin J. Walters for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_midi.system_exclusive`
================================================================================

System Exclusive MIDI message.


* Author(s): Kevin J. Walters

Implementation Notes
--------------------

"""

from .midi_message import MIDIMessage

__version__ = "1.4.5"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MIDI.git"


class SystemExclusive(MIDIMessage):
    """System Exclusive MIDI message.

    :param list manufacturer_id: The single byte or three byte
        manufacturer's id as a list or bytearray of numbers between 0-127.
    :param list data: The 7bit data as a list or bytearray of numbers between 0-127.

    This message can only be parsed if it fits within the input buffer in :class:MIDI.
    """

    _STATUS = 0xF0
    _STATUSMASK = 0xFF
    LENGTH = -1
    ENDSTATUS = 0xF7

    def __init__(self, manufacturer_id, data):
        self.manufacturer_id = bytes(manufacturer_id)
        self.data = bytes(data)
        super().__init__()

    def __bytes__(self):
        return (
            bytes([self._STATUS])
            + self.manufacturer_id
            + self.data
            + bytes([self.ENDSTATUS])
        )

    @classmethod
    def from_bytes(cls, msg_bytes):
        # -1 on second arg is to avoid the ENDSTATUS which is passed
        if msg_bytes[1] != 0:  # pylint: disable=no-else-return
            return cls(msg_bytes[1:2], msg_bytes[2:-1])
        else:
            return cls(msg_bytes[1:4], msg_bytes[4:-1])


SystemExclusive.register_message_type()
