# SPDX-FileCopyrightText: 2019 Kevin J. Walters for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_midi.channel_pressure`
================================================================================

Channel Pressure MIDI message.


* Author(s): Kevin J. Walters

Implementation Notes
--------------------

"""

from .midi_message import MIDIMessage

__version__ = "1.4.5"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MIDI.git"


class ChannelPressure(MIDIMessage):
    """Channel Pressure MIDI message.

    :param int pressure: The pressure, 0-127.
    """

    _STATUS = 0xD0
    _STATUSMASK = 0xF0
    LENGTH = 2

    def __init__(self, pressure, *, channel=None):
        self.pressure = pressure
        super().__init__(channel=channel)
        if not 0 <= self.pressure <= 127:
            self._raise_valueerror_oor()

    def __bytes__(self):
        return bytes([self._STATUS | (self.channel & self.CHANNELMASK), self.pressure])

    @classmethod
    def from_bytes(cls, msg_bytes):
        return cls(msg_bytes[1], channel=msg_bytes[0] & cls.CHANNELMASK)


ChannelPressure.register_message_type()
