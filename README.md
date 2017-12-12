# ZaPF Jeopardy

Born from the idea to have a Jeopardy at the [ZaPF](https://zapfev.de), this is
the software used the last couple of times.

## Dependencies

To run `jeopardy.py`, you are going to need at least:

* Python 3
* PyQt5
* A way for PyQt5 to play audio and video. On Arch Linux, this can be achieved
	with phonon-qt5-vlc.

## Running ZaPF Jeopardy

To start ZaPF Jeopardy, just run `./jeopardy.py [OPTIONS] GAME_FILE`.

As buzzer keys you can either use the keys 1 to 4 or use a button box, which
talk via a serial device. Currently only
[this button box](https://github.com/scattenlaeufer/arduino_button_box) is
supported.

### Options

There are some options, one can set by adding them to the afore mentioned
command.

| Option | Parameter | Description |
| ------ | --------- | ----------- |
| `--load` |   | Load a saved game. In this case GAME_FILE is the save game. |
| `--save-game` | SAVE_GAME | name of the save game (default: game_backup) |
| `--serial-device` | DEVICE_PATH | path to the serial device used as button box |

This info can also be accessed by running `./jeopardy.py --help`.

