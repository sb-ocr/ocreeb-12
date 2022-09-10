# SPDX-FileCopyrightText: 2019 Kevin J. Walters for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_midi.midi_message`
================================================================================

An abstract class for objects which represent MIDI messages (events).
When individual messages are imported they register themselves with
:func:register_message_type which makes them recognised
by the parser, :func:from_message_bytes.

Large messages like :class:SystemExclusive can only be parsed if they fit
within the input buffer in :class:MIDI.


* Author(s): Kevin J. Walters

Implementation Notes
--------------------

"""

__version__ = "1.4.5"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MIDI.git"

# From C3 - A and B are above G
# Semitones     A   B   C   D   E   F   G
NOTE_OFFSET = [21, 23, 12, 14, 16, 17, 19]


def channel_filter(channel, channel_spec):
    """
    Utility function to return True iff the given channel matches channel_spec.
    """
    if isinstance(channel_spec, int):
        return channel == channel_spec
    if isinstance(channel_spec, tuple):
        return channel in channel_spec
    raise ValueError("Incorrect type for channel_spec" + str(type(channel_spec)))


def note_parser(note):
    """If note is a string then it will be parsed and converted to a MIDI note (key) number, e.g.
    "C4" will return 60, "C#4" will return 61. If note is not a string it will simply be returned.

    :param note: Either 0-127 int or a str representing the note, e.g. "C#4"
    """
    midi_note = note
    if isinstance(note, str):
        if len(note) < 2:
            raise ValueError("Bad note format")
        noteidx = ord(note[0].upper()) - 65  # 65 os ord('A')
        if not 0 <= noteidx <= 6:
            raise ValueError("Bad note")
        sharpen = 0
        if note[1] == "#":
            sharpen = 1
        elif note[1] == "b":
            sharpen = -1
        # int may throw exception here
        midi_note = int(note[1 + abs(sharpen) :]) * 12 + NOTE_OFFSET[noteidx] + sharpen

    return midi_note


class MIDIMessage:
    """
    The parent class for MIDI messages.

    Class variables:

      * ``_STATUS`` - extracted from status byte with channel replaced by 0s
        (high bit is always set by convention).
      * ``_STATUSMASK`` - mask used to compared a status byte with ``_STATUS`` value.
      * ``LENGTH`` - length for a fixed size message *including* status
        or -1 for variable length.
      * ``CHANNELMASK`` - mask used to apply a (wire protocol) channel number.
      * ``ENDSTATUS`` - the end of message status byte, only set for variable length.

    This is an *abstract* class.
    """

    _STATUS = None
    _STATUSMASK = None
    LENGTH = None
    CHANNELMASK = 0x0F
    ENDSTATUS = None

    # Commonly used exceptions to save memory
    @staticmethod
    def _raise_valueerror_oor():
        raise ValueError("Out of range")

    # Each element is ((status, mask), class)
    # order is more specific masks first
    _statusandmask_to_class = []

    def __init__(self, *, channel=None):
        self._channel = channel  # dealing with pylint inadequacy
        self.channel = channel

    @property
    def channel(self):
        """The channel number of the MIDI message where appropriate.
        This is *updated* by MIDI.send() method.
        """
        return self._channel

    @channel.setter
    def channel(self, channel):
        if channel is not None and not 0 <= channel <= 15:
            raise ValueError("Channel must be 0-15 or None")
        self._channel = channel

    @classmethod
    def register_message_type(cls):
        """Register a new message by its status value and mask.
        This is called automagically at ``import`` time for each message.
        """
        ### These must be inserted with more specific masks first
        insert_idx = len(MIDIMessage._statusandmask_to_class)
        for idx, m_type in enumerate(MIDIMessage._statusandmask_to_class):
            if cls._STATUSMASK > m_type[0][1]:
                insert_idx = idx
                break

        MIDIMessage._statusandmask_to_class.insert(
            insert_idx, ((cls._STATUS, cls._STATUSMASK), cls)
        )

    # pylint: disable=too-many-arguments
    @classmethod
    def _search_eom_status(cls, buf, eom_status, msgstartidx, msgendidxplusone, endidx):
        good_termination = False
        bad_termination = False

        msgendidxplusone = msgstartidx + 1
        while msgendidxplusone <= endidx:
            # Look for a status byte
            # Second rule of the MIDI club is status bytes have MSB set
            if buf[msgendidxplusone] & 0x80:
                # pylint: disable=simplifiable-if-statement
                if buf[msgendidxplusone] == eom_status:
                    good_termination = True
                else:
                    bad_termination = True
                break
            msgendidxplusone += 1

        if good_termination or bad_termination:
            msgendidxplusone += 1

        return (msgendidxplusone, good_termination, bad_termination)

    @classmethod
    def _match_message_status(cls, buf, msgstartidx, msgendidxplusone, endidx):
        msgclass = None
        status = buf[msgstartidx]
        known_msg = False
        complete_msg = False
        bad_termination = False

        # Rummage through our list looking for a status match
        for status_mask, msgclass in MIDIMessage._statusandmask_to_class:
            masked_status = status & status_mask[1]
            if status_mask[0] == masked_status:
                known_msg = True
                # Check there's enough left to parse a complete message
                # this value can be changed later for a var. length msgs
                complete_msg = len(buf) - msgstartidx >= msgclass.LENGTH
                if not complete_msg:
                    break

                if msgclass.LENGTH < 0:  # indicator of variable length message
                    (
                        msgendidxplusone,
                        terminated_msg,
                        bad_termination,
                    ) = cls._search_eom_status(
                        buf, msgclass.ENDSTATUS, msgstartidx, msgendidxplusone, endidx
                    )
                    if not terminated_msg:
                        complete_msg = False
                else:  # fixed length message
                    msgendidxplusone = msgstartidx + msgclass.LENGTH
                break

        return (
            msgclass,
            status,
            known_msg,
            complete_msg,
            bad_termination,
            msgendidxplusone,
        )

    # pylint: disable=too-many-locals,too-many-branches
    @classmethod
    def from_message_bytes(cls, midibytes, channel_in):
        """Create an appropriate object of the correct class for the
        first message found in some MIDI bytes filtered by channel_in.

        Returns (messageobject, endplusone, skipped)
        or for no messages, partial messages or messages for other channels
        (None, endplusone, skipped).
        """
        endidx = len(midibytes) - 1
        skipped = 0
        preamble = True

        msgstartidx = 0
        msgendidxplusone = 0
        while True:
            msg = None
            # Look for a status byte
            # Second rule of the MIDI club is status bytes have MSB set
            while msgstartidx <= endidx and not midibytes[msgstartidx] & 0x80:
                msgstartidx += 1
                if preamble:
                    skipped += 1
            preamble = False

            # Either no message or a partial one
            if msgstartidx > endidx:
                return (None, endidx + 1, skipped)

            # Try and match the status byte found in midibytes
            (
                msgclass,
                status,
                known_message,
                complete_message,
                bad_termination,
                msgendidxplusone,
            ) = cls._match_message_status(
                midibytes, msgstartidx, msgendidxplusone, endidx
            )
            channel_match_orna = True
            if complete_message and not bad_termination:
                try:
                    msg = msgclass.from_bytes(midibytes[msgstartidx:msgendidxplusone])
                    if msg.channel is not None:
                        channel_match_orna = channel_filter(msg.channel, channel_in)

                except (ValueError, TypeError) as ex:
                    msg = MIDIBadEvent(midibytes[msgstartidx:msgendidxplusone], ex)

            # break out of while loop for a complete message on good channel
            # or we have one we do not know about
            if known_message:
                if complete_message:
                    if channel_match_orna:
                        break
                    # advance to next message
                    msgstartidx = msgendidxplusone
                else:
                    # Important case of a known message but one that is not
                    # yet complete - leave bytes in buffer and wait for more
                    break
            else:
                msg = MIDIUnknownEvent(status)
                # length cannot be known
                # next read will skip past leftover data bytes
                msgendidxplusone = msgstartidx + 1
                break

        return (msg, msgendidxplusone, skipped)

    # A default method for constructing wire messages with no data.
    # Returns an (immutable) bytes with just the status code in.
    def __bytes__(self):
        """Return the ``bytes`` wire protocol representation of the object
        with channel number applied where appropriate."""
        return bytes([self._STATUS])

    # databytes value present to keep interface uniform but unused
    # A default method for constructing message objects with no data.
    # Returns the new object.
    # pylint: disable=unused-argument
    @classmethod
    def from_bytes(cls, msg_bytes):
        """Creates an object from the byte stream of the wire protocol
        representation of the MIDI message."""
        return cls()


# DO NOT try to register these messages
class MIDIUnknownEvent(MIDIMessage):
    """An unknown MIDI message.

    :param int status: The MIDI status number.

    This can either occur because there is no class representing the message
    or because it is not imported.
    """

    LENGTH = -1

    def __init__(self, status):
        self.status = status
        super().__init__()


class MIDIBadEvent(MIDIMessage):
    """A bad MIDI message, one that could not be parsed/constructed.

    :param list msg_bytes: The MIDI status including any embedded channel number
        and associated subsequent data bytes.
    :param Exception exception: The exception used to store the repr() text representation.

    This could be due to status bytes appearing where data bytes are expected.
    The channel property will not be set.
    """

    LENGTH = -1

    def __init__(self, msg_bytes, exception):
        self.data = bytes(msg_bytes)
        self.exception_text = repr(exception)
        super().__init__()
