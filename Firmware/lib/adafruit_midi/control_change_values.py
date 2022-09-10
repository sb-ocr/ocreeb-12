# SPDX-FileCopyrightText: 2021 Mark Komus for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_midi.control_change_values`
================================================================================

Definition for standard MIDI control change values.


* Author(s): Mark Komus

Implementation Notes
--------------------

"""

__version__ = "1.4.5"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MIDI.git"

MOD_WHEEL = 1
BREATH_CONTROL = 2
FOOT_CONTROLLER = 4
VOLUME = 7
PAN = 10
EXPRESSION = 11
SUSTAIN_PEDAL = 64
PORTAMENTO = 65
FILTER_RESONANCE = 71
RELEASE_TIME = 72
ATTACK_TIME = 74
CUTOFF_FREQUENCY = 74
DECAY_TIME = 75
VIBRATO_RATE = 76
VIBRATO_DEPTH = 77
VIBRATO_DELAY = 78
ALL_CONTROLLERS_OFF = 121
ALL_NOTES_OFF = 123
