import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

from kmk.extensions import Extension
from kmk.keys import make_argumented_key

def midi_key_validator(note):
    return MidiNoteMeta(note)

class MidiNoteMeta:
    def __init__(self, note):
        self.note = note

class Midi(Extension):

        def __init__(self, port = 1, out_channel = 0):

            #  MIDI setup as MIDI out device
            self.MIDI = adafruit_midi.MIDI(midi_out=usb_midi.ports[port], out_channel=out_channel)

            make_argumented_key(
                validator=midi_key_validator,
                names=('MIDI',),
                on_press=self._on_n,
                on_release=self._off_n,
            )

        def _on_n(self, key, keyboard, *args, **kwargs):
            self.MIDI.send(NoteOn((key.meta.note), 120))

        def _off_n(self, key, keyboard, *args, **kwargs):
            self.MIDI.send(NoteOff((key.meta.note), 120))

        def on_runtime_enable(self, sandbox):
            return

        def on_runtime_disable(self, sandbox):
            return

        def during_bootup(self, sandbox):
            return

        def before_matrix_scan(self, sandbox):
            return

        def after_matrix_scan(self, sandbox):
            return

        def before_hid_send(self, sandbox):
            return

        def after_hid_send(self, sandbox):
            return

        def on_powersave_enable(self, sandbox):
            return

        def on_powersave_disable(self, sandbox):
            return
