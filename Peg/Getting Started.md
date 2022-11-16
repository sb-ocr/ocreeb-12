![Ocreeb 12 Logo](/Images/Ocreeb-12-1.svg)

This a user guide for Ocreeb 12 with [Peg](https://peg.software/) compatible [firmware](/Peg/Firmware).
Ocreeb is a 12 key Programmable macro keypad with 2 rotary encoders and underglow RGB, running KMK firmware on the Adafruit KB2040. 

Checkout the build :hammer_and_wrench: [video](https://youtu.be/P_oSLBZABGA)

# Quick Start

## Step 1 

Hold down the top right button on Ocreeb and plug it into your computer, you can release it when you see a mass storage device `CIRCUITPY` mounted. This is the first step to customize your device. :warning: If you don't see the device mounted, you won't be able to access the code or change the key mapping using the flashing software.

![Step 1](/Images/Step-01-1.svg)

## Step 2

Download and install the [Peg software](https://peg.software/). A feature-rich flashing solution for configuration through the GUI. Your system may ask you when you first launch to allow access to mass storage devices :warning: This is required for Peg to work.

## Step 3

You should be able to see Ocreeb recognized by Peg in the upper right corner. Out of the box, the macropad is assigned a default keymap.
You can program the keys and encoder from the available keycodes or create your own custom codes | [instructions below ↓](#custom-keycodes)

![Step 3](/Images/Step-03-1.svg)

## Step 4

Once you are happy with the keymap, click on `SAVE MAP` and wait for the `SAFE TO UNPLUG` message.
You can now unplug and replug the device to hide the mass storage drive and use it normally.

To recover access, repeat [Step 1](#step-1) and relaunch Peg if it didn't pickup the device right away.

<br>

# Peg Software[^1]

:warning: [0.9 Beta Warning](https://peg.software/docs/#09-beta-warning)

## Keymap

The Keymap view is your main view. If you want to change what any key does on your keyboard you make that change here.

To map a key you can do it in 1 of 2 ways. You can drag it from below and drop it on the key you want to change, or you can click on the key you want to change and then click on the key you want to change it to below.

## Encoder

The Encoder view is just like the Keymap view just with only your encoder available to map.

:warning: The right side encoder on this version of Ocreeb is reserved to the RGB Hue control, you can only program the encoder's switch in the Keymap view.

## Make Custom

Make Custom is a more advanced section of the Peg client, it allows you to add onto your keycode selection. The peg client supports any keycode you could want to do but the client may not let you make it inside the UI. In the client you can make simple macros, eg: push one key and type out "Hello my name is Cole". To do more advanced keycodes supported by KMK | [instructions below ↓](#custom-keycodes) | or to backup your custom keycodes you can click the `Export` button in the Custom Keycodes tab. This will first let you copy all of your current keycodes for safe keeping and give you a template to edit to make more.
<br>

[^1]: Source: [Peg Client Docs](https://peg.software/docs/Peg_Client/)

# Custom Keycodes

You can make custom keycodes in this JSON format to be able to add them in Peg Flashing Software.

```json
[
  {
    "code":"KC.LT(1, KC.ENT)",
    "display":"L1-ENT",
    "keybinding":"",
    "canHaveSub":false,
    "canHaveSubNumber":false,
    "subNumber":0,
    "Description":"Pushes layer 1 if held and enter if tapped"
  }
]
```
Get started faster by copying the content of this [collection](https://github.com/sb-ocr/ocreeb-12/blob/main/Peg/Firmware/custom-keycodes.json).
Press the `Show import Keycodes` Button and paste in your the json array, click the `Import` button. Now you should be able to see your new keycodes under the `Custom Codes Tab` in your keymap.

Most macros in the example collection are created using one or a combination of these 2 sequences:

1. `send_string()`

It can be used to send any standard English alphabet character, and an assortment of other "standard" keyboard keys (return, space, exclamation points, etc.)

```json
[
  {
    "code": "send_string('git add .')",
    "display": "G AD",
    "keybinding": "",
    "canHaveSub": false,
    "canHaveSubNumber": false,
    "subNumber": 0,
    "Description": "git add . (Send String)"
  }
]
```
2. `simple_key_sequence()`

This is best suited for shortcuts that require multiple modifier keys (⌘, Ctrl, Alt, Shift...)

Nested modifiers are sent to the host in the order in which they are nested. In the example below, this macro will produce the following behavior: `⌘ + control + q` `wait for 400ms then` `Escape`

```json
[
  {
    "code": "simple_key_sequence([KC.LCTRL(KC.LCMD(KC.Q)), KC.MACRO_SLEEP_MS(400), KC.ESCAPE])",
    "display": "LOCK",
    "keybinding": "",
    "canHaveSub": false,
    "canHaveSubNumber": false,
    "subNumber": 0,
    "Description": "Lock Screen (macOS)"
  }
]
```
Here is a full list of possible keys in the [KMK Firmware Docs](https://github.com/KMKfw/kmk_firmware/blob/master/docs/en/keycodes.md) to make you own macros.
<br>

# Layers[^2]

There is a total of 8 possible layout layers in this version of Ocreeb. You can access them from the right side of the window `0 to 7`, in the keymap and encoder views.

When starting out, care should be taken when working with layers, since it's possible to lock yourself to a layer with no way of returning to the base layer short of unplugging your keyboard. This is especially easy to do when using the `KC.TO()` keycode, which deactivates all other layers in the stack.

Some helpful guidelines to keep in mind as you design your layers:

Only reference higher-numbered layers from a given layer
Leave keys as `KC.TRNS` in higher layers when they would overlap with a layer-switch

Further Reading:
- [Layers in KMK](https://github.com/KMKfw/kmk_firmware/blob/master/docs/en/layers.md)
- [Modtap in KMK](https://github.com/KMKfw/kmk_firmware/blob/master/docs/en/modtap.md)


[^2]: Source: [KMK Docs](https://github.com/KMKfw/kmk_firmware/blob/master/docs/en/layers.md)
<br>

# Advanced

If you want to extend the functionality of your macropad beyond what is possible in the Peg software or if you want to manage your keymap directly in the code. You can check this [firmware version](/Firmware) described in the [build video](https://youtu.be/P_oSLBZABGA). This version removes compatibility with Peg and it'is recommended if you want go the code only route.

Build instructions: 
- [Instructables](https://www.instructables.com/DIY-Mechanical-Macro-Keypad-Ocreeb/)
- [Hackster](https://www.hackster.io/ocr_lab/diy-mechanical-macro-keypad-ocreeb-76d00c)

<br>

# Questions

I will do my best to answer any questions regarding the build or configuration of this project.

You can DM with your questions here [LinkTree](https://linktr.ee/salimbenbouz)

Thank you for checking out Ocreeb!
