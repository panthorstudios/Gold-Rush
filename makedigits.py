#!/usr/bin/env python

from PIL import Image, ImageFont, ImageDraw

font = ImageFont.truetype('assets/fonts/WEST____.TTF', 48) #load the font
tcolor=(255,212,121)
maxw=24

image = Image.new('RGB', (maxw*10,35), "black")
draw = ImageDraw.Draw(image)
for i in range(10):
    digit=str(i)
    size = font.getsize(digit)
    w=size[0]
    pos=(maxw-w)//2
    draw.text((i*maxw+pos,0), str(i), font=font,fill=tcolor) #render the text to the bitmap

image.save('assets/images/digits.png')

