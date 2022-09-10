# SPDX-FileCopyrightText: 2019 Kevin J. Walters for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_midi.pitch_bend`
================================================================================

Pitch Bend Change MIDI message.


* Author(s): Kevin J. Walters

Implementation Notes
--------------------

"""

from .midi_message import MIDIMessage

__version__ = "1.4.5"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MIDI.git"


class PitchBend(MIDIMessage):
    """Pitch Bend Change MIDI message.

    :param int pitch_bend: A 14bit unsigned int representing the degree of
        bend from 0 through 8192 (midpoint, no bend) to 16383.
    """

    _STATUS = 0xE0
    _STATUSMASK = 0xF0
    LENGTH = 3

    def __init__(self, pitch_bend, *, channel=None):
        self.pitch_bend = pitch_bend
        super().__init__(channel=channel)
        if not 0 <= self.pitch_bend <= 16383:
            self._raise_valueerror_oor()

    def __bytes__(self):
        return bytes(
            [
                self._STATUS | (self.channel & self.CHANNELMASK),
                self.pitch_bend & 0x7F,
                (self.pitch_bend >> 7) & 0x7F,
            ]
        )

    @classmethod
    def from_bytes(cls, msg_bytes):
        return cls(
            msg_bytes[2] << 7 | msg_bytes[1], channel=msg_bytes[0] & cls.CHANNELMASK
        )


PitchBend.register_message_type()
