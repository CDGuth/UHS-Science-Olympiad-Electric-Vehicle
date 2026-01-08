# [`hubs`](#module-pybricks.hubs "pybricks.hubs") – Programmable Hubs[¶](#hubs-programmable-hubs "Permalink to this headline")

![_images/ev3brick.png](_images/ev3brick.png)

_class_ `EV3Brick`[¶](#pybricks.hubs.EV3Brick "Permalink to this definition")

LEGO® MINDSTORMS® EV3 Brick.

Using the buttons

`buttons.``pressed`()[¶](#pybricks.hubs.EV3Brick.buttons.pressed "Permalink to this definition")

Checks which buttons are currently pressed.

 

Returns:

List of pressed buttons.

Return type:

List of [`Button`](parameters.html#pybricks.parameters.Button "pybricks.parameters.Button")

Using the brick status light

`light.``on`(_color_)[¶](#pybricks.hubs.EV3Brick.light.on "Permalink to this definition")

Turns on the light at the specified color.

 

Parameters:

**color** ([_Color_](parameters.html#pybricks.parameters.Color "pybricks.parameters.Color")) – Color of the light. The light turns off if you choose `None` or a color that is not available.

**Show/hide example**

**Example: Turn the light on and change the color.**

#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.tools import wait
from pybricks.parameters import Color

\# Initialize the EV3
ev3 \= EV3Brick()

\# Turn on a red light
ev3.light.on(Color.RED)

\# Wait
wait(1000)

\# Turn the light off
ev3.light.off()

`light.``off`()[¶](#pybricks.hubs.EV3Brick.light.off "Permalink to this definition")

Turns off the light.

Using the speaker

`speaker.``beep`(_frequency=500_, _duration=100_)[¶](#pybricks.hubs.EV3Brick.speaker.beep "Permalink to this definition")

Play a beep/tone.

 

Parameters:

*   **frequency** ([frequency: Hz](signaltypes.html#frequency)) – Frequency of the beep. Frequencies below 100 are treated as 100.
*   **duration** ([time: ms](signaltypes.html#id1)) – Duration of the beep. If the duration is less than 0, then the method returns immediately and the frequency play continues to play indefinitely.

`speaker.``play_notes`(_notes_, _tempo=120_)[¶](#pybricks.hubs.EV3Brick.speaker.play_notes "Permalink to this definition")

Plays a sequence of musical notes.

For example, you can play: `['C4/4', 'C4/4', 'G4/4', 'G4/4']`.

 

Parameters:

*   **notes** (_iter_) – A sequence of notes to be played (see format below).
*   **tempo** (_int_) – Beats per minute where a quarter note is one beat.

**Show/hide musical note format**

Each note is a string with the following format:

> *   The first character is the name of the note, `A` to `G` or `R` for a rest.
> *   Note names can also include an accidental `#` (sharp) or `b` (flat). `B#`/`Cb` and `E#`/`Fb` are not allowed.
> *   The note name is followed by the octave number `2` to `8`. For example `C4` is middle C. The octave changes to the next number at the note C, for example, `B3` is the note below middle C (`C4`).
> *   The octave is followed by `/` and a number that indicates the size of the note. For example `/4` is a quarter note, `/8` is an eighth note and so on.
> *   This can optionally followed by a `.` to make a dotted note. Dotted notes are 1-1/2 times as long as notes without a dot.
> *   The note can optionally end with a `_` which is a tie or a slur. This causes there to be no pause between this note and the next note.

`speaker.``play_file`(_file\_name_)[¶](#pybricks.hubs.EV3Brick.speaker.play_file "Permalink to this definition")

Plays a sound file.

 

Parameters:

**file\_name** (_str_) – Path to the sound file, including the file extension.

`speaker.``say`(_text_)[¶](#pybricks.hubs.EV3Brick.speaker.say "Permalink to this definition")

Says a given text string.

You can configure the language and voice of the text using [`set_speech_options()`](#pybricks.hubs.EV3Brick.speaker.set_speech_options "pybricks.hubs.EV3Brick.speaker.set_speech_options").

 

Parameters:

**text** (_str_) – What to say.

`speaker.``set_speech_options`(_language=None_, _voice=None_, _speed=None_, _pitch=None_)[¶](#pybricks.hubs.EV3Brick.speaker.set_speech_options "Permalink to this definition")

Configures speech settings used by the [`say()`](#pybricks.hubs.EV3Brick.speaker.say "pybricks.hubs.EV3Brick.speaker.say") method.

Any option that is set to `None` will not be changed. If an option is set to an invalid value [`say()`](#pybricks.hubs.EV3Brick.speaker.say "pybricks.hubs.EV3Brick.speaker.say") will use the default value instead.

 

Parameters:

*   **language** (_str_) – Language of the text. For example, you can choose `'en'` (English) or `'de'` (German). A list of all available languages is given below.
*   **voice** (_str_) – The voice to use. For example, you can choose `'f1'` (female voice variant 1) or `'m3'` (male voice variant 3). A list of all available voices is given below.
*   **speed** (_int_) – Number of words per minute.
*   **pitch** (_int_) – Pitch (0 to 99). Higher numbers make the voice higher pitched and lower numbers make the voice lower pitched.

**Show/hide available languages and voices**

You can choose the following languages:

> *   `'af'`: Afrikaans
> *   `'an'`: Aragonese
> *   `'bg'`: Bulgarian
> *   `'bs'`: Bosnian
> *   `'ca'`: Catalan
> *   `'cs'`: Czech
> *   `'cy'`: Welsh
> *   `'da'`: Danish
> *   `'de'`: German
> *   `'el'`: Greek
> *   `'en'`: English (default)
> *   `'en-gb'`: English (United Kingdom)
> *   `'en-sc'`: English (Scotland)
> *   `'en-uk-north'`: English (United Kingdom, Northern)
> *   `'en-uk-rp'`: English (United Kingdom, Received Pronunciation)
> *   `'en-uk-wmids'`: English (United Kingdom, West Midlands)
> *   `'en-us'`: English (United States)
> *   `'en-wi'`: English (West Indies)
> *   `'eo'`: Esperanto
> *   `'es'`: Spanish
> *   `'es-la'`: Spanish (Latin America)
> *   `'et'`: Estonian
> *   `'fa'`: Persian
> *   `'fa-pin'`: Persian
> *   `'fi'`: Finnish
> *   `'fr-be'`: French (Belgium)
> *   `'fr-fr'`: French (France)
> *   `'ga'`: Irish
> *   `'grc'`: Greek
> *   `'hi'`: Hindi
> *   `'hr'`: Croatian
> *   `'hu'`: Hungarian
> *   `'hy'`: Armenian
> *   `'hy-west'`: Armenian (Western)
> *   `'id'`: Indonesian
> *   `'is'`: Icelandic
> *   `'it'`: Italian
> *   `'jbo'`: Lojban
> *   `'ka'`: Georgian
> *   `'kn'`: Kannada
> *   `'ku'`: Kurdish
> *   `'la'`: Latin
> *   `'lfn'`: Lingua Franca Nova
> *   `'lt'`: Lithuanian
> *   `'lv'`: Latvian
> *   `'mk'`: Macedonian
> *   `'ml'`: Malayalam
> *   `'ms'`: Malay
> *   `'ne'`: Nepali
> *   `'nl'`: Dutch
> *   `'no'`: Norwegian
> *   `'pa'`: Punjabi
> *   `'pl'`: Polish
> *   `'pt-br'`: Portuguese (Brazil)
> *   `'pt-pt'`: Portuguese (Portugal)
> *   `'ro'`: Romanian
> *   `'ru'`: Russian
> *   `'sk'`: Slovak
> *   `'sq'`: Albanian
> *   `'sr'`: Serbian
> *   `'sv'`: Swedish
> *   `'sw'`: Swahili
> *   `'ta'`: Tamil
> *   `'tr'`: Turkish
> *   `'vi'`: Vietnamese
> *   `'vi-hue'`: Vietnamese (Hue)
> *   `'vi-sgn'`: Vietnamese (Saigon)
> *   `'zh'`: Mandarin Chinese
> *   `'zh-yue'`: Cantonese Chinese
> 
> You can choose the following voices:
> 
> *   `'f1'`: female variant 1
> *   `'f2'`: female variant 2
> *   `'f3'`: female variant 3
> *   `'f4'`: female variant 4
> *   `'f5'`: female variant 5
> *   `'m1'`: male variant 1
> *   `'m2'`: male variant 2
> *   `'m3'`: male variant 3
> *   `'m4'`: male variant 4
> *   `'m5'`: male variant 5
> *   `'m6'`: male variant 6
> *   `'m7'`: male variant 7
> *   `'croak'`: croak
> *   `'whisper'`: whisper
> *   `'whisperf'`: female whisper

`speaker.``set_volume`(_volume_, _which='\_all\_'_)[¶](#pybricks.hubs.EV3Brick.speaker.set_volume "Permalink to this definition")

Sets the speaker volume.

 

Parameters:

*   **volume** ([percentage: %](signaltypes.html#percentage)) – Volume of the speaker.
*   **which** (_str_) – Which volume to set. `'Beep'` sets the volume for [`beep()`](#pybricks.hubs.EV3Brick.speaker.beep "pybricks.hubs.EV3Brick.speaker.beep") and [`play_notes()`](#pybricks.hubs.EV3Brick.speaker.play_notes "pybricks.hubs.EV3Brick.speaker.play_notes"). `'PCM'` sets the volume for [`play_file()`](#pybricks.hubs.EV3Brick.speaker.play_file "pybricks.hubs.EV3Brick.speaker.play_file") and [`say()`](#pybricks.hubs.EV3Brick.speaker.say "pybricks.hubs.EV3Brick.speaker.say"). `'_all_'` sets both at the same time.

Using the screen

`screen.``clear`()[¶](#pybricks.hubs.EV3Brick.screen.clear "Permalink to this definition")

Clears the screen. All pixels on the screen will be set to [`Color.WHITE`](parameters.html#pybricks.parameters.Color.WHITE "pybricks.parameters.Color.WHITE").

`screen.``draw_text`(_x_, _y_, _text_, _text\_color=Color.BLACK_, _background\_color=None_)[¶](#pybricks.hubs.EV3Brick.screen.draw_text "Permalink to this definition")

Draws text on the screen.

The most recent font set using [`set_font()`](#pybricks.hubs.EV3Brick.screen.set_font "pybricks.hubs.EV3Brick.screen.set_font") will be used or [`Font.DEFAULT`](media.html#pybricks.media.ev3dev.Font.DEFAULT "pybricks.media.ev3dev.Font.DEFAULT") if no font has been set yet.

 

Parameters:

*   **x** (_int_) – The x-axis value where the left side of the text will start.
*   **y** (_int_) – The y-axis value where the top of the text will start.
*   **text** (_str_) – The text to draw.
*   **text\_color** ([_Color_](parameters.html#pybricks.parameters.Color "pybricks.parameters.Color")) – The color used for drawing the text.
*   **background\_color** ([_Color_](parameters.html#pybricks.parameters.Color "pybricks.parameters.Color")) – The color used to fill the rectangle behind the text or `None` for transparent background.

`screen.``print`(_\*args_, _sep=' '_, _end='\\n'_)[¶](#pybricks.hubs.EV3Brick.screen.print "Permalink to this definition")

Prints a line of text on the screen.

This method works like the builtin `print()` function, but it writes on the screen instead.

You can set the font using [`set_font()`](#pybricks.hubs.EV3Brick.screen.set_font "pybricks.hubs.EV3Brick.screen.set_font"). If no font has been set, [`Font.DEFAULT`](media.html#pybricks.media.ev3dev.Font.DEFAULT "pybricks.media.ev3dev.Font.DEFAULT") will be used. The text is always printed used black text with a white background.

Unlike the builtin `print()`, the text does not wrap if it is too wide to fit on the screen. It just gets cut off. But if the text would go off of the bottom of the screen, the entire image is scrolled up and the text is printed in the new blank area at the bottom of the screen.

 

Parameters:

*   **\*** (_object_) – Zero or more objects to print.
*   **sep** (_str_) – Separator that will be placed between each object that is printed.
*   **end** (_str_) – End of line that will be printed after the last object.

**Show/hide example**

**Example: Say hello… in several ways.**

#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.tools import wait
from pybricks.media.ev3dev import Font

\# It takes some time for fonts to load from file, so it is best to only
\# load them once at the beginning of the program like this:
tiny\_font \= Font(size\=6)
big\_font \= Font(size\=24, bold\=True)
chinese\_font \= Font(size\=24, lang\='zh-cn')

\# Initialize the EV3
ev3 \= EV3Brick()

\# Say hello
ev3.screen.print('Hello!')

\# Say tiny hello
ev3.screen.set\_font(tiny\_font)
ev3.screen.print('hello')

\# Say big hello
ev3.screen.set\_font(big\_font)
ev3.screen.print('HELLO')

\# Say Chinese hello
ev3.screen.set\_font(chinese\_font)
ev3.screen.print('你好')

\# Wait some time to look at the screen
wait(5000)

`screen.``set_font`(_font_)[¶](#pybricks.hubs.EV3Brick.screen.set_font "Permalink to this definition")

Sets the font used for writing on the screen.

The font is used for both [`draw_text()`](#pybricks.hubs.EV3Brick.screen.draw_text "pybricks.hubs.EV3Brick.screen.draw_text") and [`print()`](#pybricks.hubs.EV3Brick.screen.print "pybricks.hubs.EV3Brick.screen.print").

 

Parameters:

**font** ([`Font`](media.html#pybricks.media.ev3dev.Font "pybricks.media.ev3dev.Font")) – The font to use.

**Example:** See example in [`print()`](#pybricks.hubs.EV3Brick.screen.print "pybricks.hubs.EV3Brick.screen.print").

`screen.``load_image`(_source_)[¶](#pybricks.hubs.EV3Brick.screen.load_image "Permalink to this definition")

Clears this image, then draws the `source` image centered in the screen.

 

Parameters:

**source** ([_Image_](media.html#pybricks.media.ev3dev.Image "pybricks.media.ev3dev.Image") _or_ _str_) – The source [`Image`](media.html#pybricks.media.ev3dev.Image "pybricks.media.ev3dev.Image"). If the argument is a string, then the `source` image is loaded from file.

**Show/hide example**

**Example: Show an image on the screen.**

#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.tools import wait
from pybricks.media.ev3dev import Image, ImageFile

\# It takes some time to load images from the SD card, so it is best to load
\# them once at the beginning of a program like this:
ev3\_img \= Image(ImageFile.EV3\_ICON)

\# Initialize the EV3
ev3 \= EV3Brick()

\# Show an image
ev3.screen.load\_image(ev3\_img)

\# Wait some time to look at the image
wait(5000)

`screen.``draw_image`(_x_, _y_, _source_, _transparent=None_)[¶](#pybricks.hubs.EV3Brick.screen.draw_image "Permalink to this definition")

Draws the `source` image on the screen.

 

Parameters:

*   **x** (_int_) – The x-axis value where the left side of the image will start.
*   **y** (_int_) – The y-axis value where the top of the image will start.
*   **source** ([_Image_](media.html#pybricks.media.ev3dev.Image "pybricks.media.ev3dev.Image") _or_ _str_) – The source [`Image`](media.html#pybricks.media.ev3dev.Image "pybricks.media.ev3dev.Image"). If the argument is a string, then the `source` image is loaded from file.
*   **transparent** ([_Color_](parameters.html#pybricks.parameters.Color "pybricks.parameters.Color")) – The color of `image` to treat as transparent or `None` for no transparency.

`screen.``draw_pixel`(_x_, _y_, _color=Color.BLACK_)[¶](#pybricks.hubs.EV3Brick.screen.draw_pixel "Permalink to this definition")

Draws a single pixel on the screen.

 

Parameters:

*   **x** (_int_) – The x coordinate of the pixel.
*   **y** (_int_) – The y coordinate of the pixel.
*   **color** ([_Color_](parameters.html#pybricks.parameters.Color "pybricks.parameters.Color")) – The color of the pixel.

`screen.``draw_line`(_x1_, _y1_, _x2_, _y2_, _width=1_, _color=Color.BLACK_)[¶](#pybricks.hubs.EV3Brick.screen.draw_line "Permalink to this definition")

Draws a line on the screen.

 

Parameters:

*   **x1** (_int_) – The x coordinate of the starting point of the line.
*   **y1** (_int_) – The y coordinate of the starting point of the line.
*   **x2** (_int_) – The x coordinate of the ending point of the line.
*   **y2** (_int_) – The y coordinate of the ending point of the line.
*   **width** (_int_) – The width of the line in pixels.
*   **color** ([_Color_](parameters.html#pybricks.parameters.Color "pybricks.parameters.Color")) – The color of the line.

**Show/hide example**

**Example: Draw some shapes on the screen.**

#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.tools import wait

\# Initialize the EV3
ev3 \= EV3Brick()

\# Draw a rectangle
ev3.screen.draw\_box(10, 10, 40, 40)

\# Draw a solid rectangle
ev3.screen.draw\_box(20, 20, 30, 30, fill\=True)

\# Draw a rectangle with rounded corners
ev3.screen.draw\_box(50, 10, 80, 40, 5)

\# Draw a circle
ev3.screen.draw\_circle(25, 75, 20)

\# Draw a triangle using lines
x1, y1 \= 65, 55
x2, y2 \= 50, 95
x3, y3 \= 80, 95
ev3.screen.draw\_line(x1, y1, x2, y2)
ev3.screen.draw\_line(x2, y2, x3, y3)
ev3.screen.draw\_line(x3, y3, x1, y1)

\# Wait some time to look at the shapes
wait(5000)

`screen.``draw_box`(_x1_, _y1_, _x2_, _y2_, _r=0_, _fill=False_, _color=Color.BLACK_)[¶](#pybricks.hubs.EV3Brick.screen.draw_box "Permalink to this definition")

Draws a box on the screen.

 

Parameters:

*   **x1** (_int_) – The x coordinate of the left side of the box.
*   **y1** (_int_) – The y coordinate of the top of the box.
*   **x2** (_int_) – The x coordinate of the right side of the box.
*   **y2** (_int_) – The y coordinate of the bottom of the box.
*   **r** (_int_) – The radius of the corners of the box.
*   **fill** (_bool_) – If `True`, the box will be filled with `color`, otherwise only the outline of the box will be drawn.
*   **color** ([_Color_](parameters.html#pybricks.parameters.Color "pybricks.parameters.Color")) – The color of the box.

**Example:** See example in [`draw_line()`](#pybricks.hubs.EV3Brick.screen.draw_line "pybricks.hubs.EV3Brick.screen.draw_line").

`screen.``draw_circle`(_x_, _y_, _r_, _fill=False_, _color=Color.BLACK_)[¶](#pybricks.hubs.EV3Brick.screen.draw_circle "Permalink to this definition")

Draws a circle on the screen.

 

Parameters:

*   **x** (_int_) – The x coordinate of the center of the circle.
*   **y** (_int_) – The y coordinate of the center of the circle.
*   **r** (_int_) – The radius of the circle.
*   **fill** (_bool_) – If `True`, the circle will be filled with `color`, otherwise only the circumference will be drawn.
*   **color** ([_Color_](parameters.html#pybricks.parameters.Color "pybricks.parameters.Color")) – The color of the circle.

**Example:** See example in [`draw_line()`](#pybricks.hubs.EV3Brick.screen.draw_line "pybricks.hubs.EV3Brick.screen.draw_line").

`screen.``width`[¶](#pybricks.hubs.EV3Brick.screen.width "Permalink to this definition")

Gets the width of the screen in pixels.

`screen.``height`[¶](#pybricks.hubs.EV3Brick.screen.height "Permalink to this definition")

Gets the height of the screen in pixels.

`screen.``save`(_filename_)[¶](#pybricks.hubs.EV3Brick.screen.save "Permalink to this definition")

Saves the screen as a `.png` file.

 

Parameters:

**filename** (_str_) – The path to the file to be saved.

Raises:

*   `TypeError` – `filename` is not a string.
*   `OSError` – There was a problem saving the file.

Using the battery

`battery.``voltage`()[¶](#pybricks.hubs.EV3Brick.battery.voltage "Permalink to this definition")

Gets the voltage of the battery.

 

Returns:

Battery voltage.

Return type:

[voltage: mV](signaltypes.html#voltage)

`battery.``current`()[¶](#pybricks.hubs.EV3Brick.battery.current "Permalink to this definition")

Gets the current supplied by the battery.

 

Returns:

Battery current.

Return type:

[current: mA](signaltypes.html#current)