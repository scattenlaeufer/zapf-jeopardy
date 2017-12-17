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

## Games

A game consist of a JSON file, that contains all the information needed and the
media files used as possible answers.

### JSON file

The game file itself is a text file, that is processable by a JSON parser and
contains a list of five dictionaries, which each are interpreted as the
categories of the game. The entries of those dictionaries are structured as
follows:

| Key      | Type       | Content                                   |
| -------- | ---------- | ----------------------------------------- |
| category | string     | Name of the category                      |
| level    | dictionary | Dictionary containing the separat answers |

The level-dictionaries are thusly structured:

| Key             | Type    | Content                                                             |
| --------------- | ------- | ------------------------------------------------------------------- |
| answer          | string  | The answer to be shown                                              |
| question        | string  | A possible question to the answer                                   |
| type            | string  | The type of the answer (either `text`, `image`, `audio` or `video`) |
| double_jeopardy | boolean | Whether this answer is a Double Jeopardy or not                     |

### Answer Types

Answers can be either a text, an image, an audio file or a video. If it's
anything but a text, the entry in the game file must be a relative path from
the location of the game file to the media file. At some point there might be
support for absolute paths, but currently that's not the case. Which type of
answer is being used needs to be declared in `type` for the program to use the
correct method of displaying the answer.
