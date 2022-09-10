# SPDX-FileCopyrightText: 2019 Limor Fried for Adafruit Industries
# SPDX-FileCopyrightText: 2019 Kevin J. Walters for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_midi`
================================================================================

A CircuitPython helper for encoding/decoding MIDI packets over a MIDI or UART connection.


* Author(s): Limor Fried, Kevin J. Walters

Implementation Notes
--------------------

**Hardware:**



**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

from .midi_message import MIDIMessage

__version__ = "1.4.5"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MIDI.git"


class MIDI:
    """MIDI helper class. ``midi_in`` or ``midi_out`` *must* be set or both together.

    :param midi_in: an object which implements ``read(length)``,
        set to ``usb_midi.ports[0]`` for USB MIDI, default None.
    :param midi_out: an object which implements ``write(buffer, length)``,
        set to ``usb_midi.ports[1]`` for USB MIDI, default None.
    :param in_channel: The input channel(s).
        This is used by ``receive`` to filter data.
        This can either be an ``int`` for the wire protocol channel number (0-15)
        a tuple of ``int`` to listen for multiple channels.
        Defaults to all channels.
    :param int out_channel: The wire protocol output channel number (0-15)
        used by ``send`` if no channel is specified,
        defaults to 0 (MIDI Channel 1).
    :param int in_buf_size: Maximum size of input buffer in bytes, default 30.
    :param bool debug: Debug mode, default False.

    """

    def __init__(
        self,
        midi_in=None,
        midi_out=None,
        *,
        in_channel=None,
        out_channel=0,
        in_buf_size=30,
        debug=False
    ):
        if midi_in is None and midi_out is None:
            raise ValueError("No midi_in or midi_out provided")
        self._midi_in = midi_in
        self._midi_out = midi_out
        self._in_channel = in_channel
        self.in_channel = in_channel
        self._out_channel = out_channel
        self.out_channel = out_channel
        self._debug = debug
        # This input buffer holds what has been read from midi_in
        self._in_buf = bytearray(0)
        self._in_buf_size = in_buf_size
        self._outbuf = bytearray(4)
        self._skipped_bytes = 0

    @property
    def in_channel(self):
        """The incoming MIDI channel. Must be 0-15. Correlates to MIDI channels 1-16, e.g.
        ``in_channel = 3`` will listen on MIDI channel 4.
        Can also listen on multiple channels, e.g. ``in_channel  = (0,1,2)``
        will listen on MIDI channels 1-3.
        Default is all channels."""
        return self._in_channel

    @in_channel.setter
    def in_channel(self, channel):
        if channel is None or channel == "ALL":
            self._in_channel = tuple(range(16))
        elif isinstance(channel, int) and 0 <= channel <= 15:
            self._in_channel = channel
        elif isinstance(channel, tuple) and all(0 <= c <= 15 for c in channel):
            self._in_channel = channel
        else:
            raise RuntimeError("Invalid input channel")

    @property
    def out_channel(self):
        """The outgoing MIDI channel. Must be 0-15. Correlates to MIDI channels 1-16, e.g.
        ``out_channel = 3`` will send to MIDI channel 4. Default is 0 (MIDI channel 1)."""
        return self._out_channel

    @out_channel.setter
    def out_channel(self, channel):
        if not 0 <= channel <= 15:
            raise RuntimeError("Invalid output channel")
        self._out_channel = channel

    def receive(self):
        """Read messages from MIDI port, store them in internal read buffer, then parse that data
        and return the first MIDI message (event).
        This maintains the blocking characteristics of the midi_in port.

        :returns MIDIMessage object: Returns object or None for nothing.
        """
        ### could check _midi_in is an object OR correct object OR correct interface here?
        # If the buffer here is not full then read as much as we can fit from
        # the input port
        if len(self._in_buf) < self._in_buf_size:
            bytes_in = self._midi_in.read(self._in_buf_size - len(self._in_buf))
            if bytes_in:
                if self._debug:
                    print("Receiving: ", [hex(i) for i in bytes_in])
                self._in_buf.extend(bytes_in)
                del bytes_in

        (msg, endplusone, skipped) = MIDIMessage.from_message_bytes(
            self._in_buf, self._in_channel
        )
        if endplusone != 0:
            # This is not particularly efficient as it's copying most of bytearray
            # and deleting old one
            self._in_buf = self._in_buf[endplusone:]

        self._skipped_bytes += skipped

        # msg could still be None at this point, e.g. in middle of monster SysEx
        return msg

    def send(self, msg, channel=None):
        """Sends a MIDI message.

        :param msg: Either a MIDIMessage object or a sequence (list) of MIDIMessage objects.
            The channel property will be *updated* as a side-effect of sending message(s).
        :param int channel: Channel number, if not set the ``out_channel`` will be used.

        """
        if channel is None:
            channel = self.out_channel
        if isinstance(msg, MIDIMessage):
            msg.channel = channel
            data = msg.__bytes__()  # bytes(object) does not work in uPy
        else:
            data = bytearray()
            for each_msg in msg:
                each_msg.channel = channel
                data.extend(each_msg.__bytes__())

        self._send(data, len(data))

    def _send(self, packet, num):
        if self._debug:
            print("Sending: ", [hex(i) for i in packet[:num]])
        self._midi_out.write(packet, num)
