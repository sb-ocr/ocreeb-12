# QMK VIA Macropad Information

I've encountered several issues when using KMK with my macropad over time, as it would often stop working, requiring me to disconnect and reconnect the cable. I attempted to update Circuitpython and the KMK firmware, but didn't succeed. As an alternative, I thought about installing QMK along with VIA since I have a Keychron V4 with that firmware, and the ability to visually change my macropad configuration seems more appealing.

First, I recommend watching this [video](https://www.youtube.com/watch?v=hjml-K-pV4E) to learn how to set up QMK, in addition to following the official documentation to create a QMK environment. Once you have a QMK environment, you can place the files from this repository in the "Firmware/QMK_VIA/danibcorr" folder. If you prefer not to set up a QMK environment, there's a file with a ".uf2" extension in the same folder that can be flashed directly onto the KB 2040 microcontroller, and its configuration can be modified later in VIA. Due to the fact that I configured QMK along with VIA locally, VIA won't automatically recognize the macropad, so you'll need to follow the instructions in this [video](https://www.youtube.com/watch?v=7d5yzBOup9U).

Although the video shows the pins to which each element on the PCB is connected, I'm grouping them below:

- Column 1 → Pin D3 → GP3.
- Column 2 → Pin D4 → GP4.
- Column 3 → Pin D5 → GP5.
- Column 4 → Pin D6 → GP6.
- Row 1 → Pin D7 → GP7.
- Row 2 → Pin D8 → GP8.
- Row 3 → Pin D9 → GP9.
- ROT1_A → Pin A2 → GP28.
- ROT1_B → Pin A1 → GP27.
- ROT1_SWITCH → Pin A0 → GP26.
- ROT2_A → Pin SCK → GP18.
- ROT2_B → Pin MISO → GP20.
- ROT2_SWITCH → Pin MOSI → GP19.