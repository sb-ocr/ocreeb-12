# SPDX-FileCopyrightText: 2021 Raphaël Doursenaud
#
# SPDX-License-Identifier: MIT

"""
`adafruit_midi.mtc_quarter_frame`
================================================================================

MIDI Time Code (MTC) Quarter Frame message.


* Author(s): Raphaël Doursenaud

Implementation Notes
--------------------

Based upon the official MMA0001 / RP004 / RP008 v4.2.1 MIDI Time Code Specification

"""

from adafruit_midi.midi_message import MIDIMessage

__version__ = "1.4.5"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MIDI.git"


class MtcQuarterFrame(MIDIMessage):
    """MIDI Time Code (MTC) Quarter Frame message.

    :param msgtype: The quarter frame message type:

        0. Frame count LS nibble
        1. Frame count MS nibble
        2. Seconds count LS nibble
        3. Seconds count MS nibble
        4. Minutes count LS nibble
        5. Minutes count MS nibble
        6. Hours count LS nibble
        7. Hours count MS nibble and SMPTE Type

    :param value: The quarter frame value for the specified type.
    """

    _STATUS = 0xF1
    _STATUSMASK = 0xFF
    LENGTH = 2

    def __init__(self, msgtype, value):
        self.type = msgtype
        self.value = value
        super().__init__()
        if not 0 <= self.type <= 7 or not 0 <= self.value <= 0x0F:
            self._raise_valueerror_oor()

    def __bytes__(self):
        return bytes(
            [
                self._STATUS,
                (self.type << 4) + self.value,  # Assemble low and high nibbles
            ]
        )

    @classmethod
    def from_bytes(cls, msg_bytes):
        return cls(msg_bytes[1] >> 4, msg_bytes[1] & 15)  # High nibble  # Low nibble


MtcQuarterFrame.register_message_type()
