# SPDX-FileCopyrightText: 2019 Kevin J. Walters for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_midi.stop`
================================================================================

Stop MIDI message.


* Author(s): Kevin J. Walters

Implementation Notes
--------------------

"""

from .midi_message import MIDIMessage

__version__ = "1.4.5"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MIDI.git"


class Stop(MIDIMessage):
    """Stop MIDI message."""

    _STATUS = 0xFC
    _STATUSMASK = 0xFF
    LENGTH = 1


Stop.register_message_type()
