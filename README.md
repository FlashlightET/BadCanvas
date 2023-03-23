# BadCanvas
Bad Apple on the SC-88pro. Also runs on the SC-55, SC-88, SC-8850, and SD-90, etc.

Code sucks. Includes arbitrary numbers used to get the timing correct.

The bad apple with amen break midi is to put the video over and test sync. I do not remember where i got the original midi from.

# To convert video to the format
Requires ffmpeg and imagemagick.

I used the original upload of bad apple (sm8628149) as the base, and it starts on exactly the 4th beat of a 138bpm midi.

Convert video to png files:
```batch
ffmpeg -i  "H:\butthead\[Touhou] Bad Apple!! PV [Shadow]  [sm8628149].mp4" -vf scale=32x16 "i:\\apple\\in\\%04d.png"
```
Note: this converts video to 32x16 instead of 16x16 which is the actual size of the screen. The spaghetti code takes care of that already.

Turn png files black and white:
```batch
magick mogrify -monochrome *.png
```
in the directory of the folder (in this case, `i:\\apple\\in\\`). **please don't** run this in your downloads folder or any other important folder as it will turn EVERY PNG FILE IN THE FOLDER into a dithered 1-bit black and white image. you have been warned.

# regarding midi devices in the realtime script
when the script is run, the midi outputs will be listed. find your midi device and set outport to open that instead of "USB MIDI Interface 2".
