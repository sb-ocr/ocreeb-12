# SPDX-FileCopyrightText: 2019 Kevin J. Walters for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_midi.timing_clock`
================================================================================

Timing Clock MIDI message.


* Author(s): Kevin J. Walters

Implementation Notes
--------------------

"""

from .midi_message import MIDIMessage

__version__ = "1.4.5"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MIDI.git"


# Good to have this registered first as it occurs frequently when present
class TimingClock(MIDIMessage):
    """Timing Clock MIDI message.

    This occurs 24 times per quarter note when synchronization is in use.
    If this is not needed it's best to avoid this sending this high frequency
    message to a CircuitPython device to reduce the amount of message processing.
    """

    _STATUS = 0xF8
    _STATUSMASK = 0xFF
    LENGTH = 1


TimingClock.register_message_type()
