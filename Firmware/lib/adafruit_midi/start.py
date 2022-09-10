# SPDX-FileCopyrightText: 2019 Kevin J. Walters for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_midi.start`
================================================================================

Start MIDI message.


* Author(s): Kevin J. Walters

Implementation Notes
--------------------

"""

from .midi_message import MIDIMessage

__version__ = "1.4.5"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MIDI.git"


class Start(MIDIMessage):
    """Start MIDI message."""

    _STATUS = 0xFA
    _STATUSMASK = 0xFF
    LENGTH = 1


Start.register_message_type()
