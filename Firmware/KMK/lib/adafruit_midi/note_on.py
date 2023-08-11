# SPDX-FileCopyrightText: 2019 Kevin J. Walters for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_midi.note_on`
================================================================================

Note On Change MIDI message.


* Author(s): Kevin J. Walters

Implementation Notes
--------------------

"""

from .midi_message import MIDIMessage, note_parser

__version__ = "1.4.5"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MIDI.git"


class NoteOn(MIDIMessage):
    """Note On Change MIDI message.

    :param note: The note (key) number either as an ``int`` (0-127) or a
        ``str`` which is parsed, e.g. "C4" (middle C) is 60, "A4" is 69.
    :param int velocity: The strike velocity, 0-127, 0 is equivalent
        to a Note Off, defaults to 127.
    """

    _STATUS = 0x90
    _STATUSMASK = 0xF0
    LENGTH = 3

    def __init__(self, note, velocity=127, *, channel=None):
        self.note = note_parser(note)
        self.velocity = velocity
        super().__init__(channel=channel)
        if not 0 <= self.note <= 127 or not 0 <= self.velocity <= 127:
            self._raise_valueerror_oor()

    def __bytes__(self):
        return bytes(
            [self._STATUS | (self.channel & self.CHANNELMASK), self.note, self.velocity]
        )

    @classmethod
    def from_bytes(cls, msg_bytes):
        return cls(msg_bytes[1], msg_bytes[2], channel=msg_bytes[0] & cls.CHANNELMASK)


NoteOn.register_message_type()
