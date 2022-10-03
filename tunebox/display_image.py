import os
import time
from PIL import ImageDraw, ImageFont, Image as PILImage
import inky
from font_roboto import RobotoMedium
import numpy
from tunebox import state_machine


class Image:
    """ image for display """

    FONT = ImageFont.truetype(RobotoMedium, 20)

    def __init__(self):
        self.img = PILImage.new('P', (250, 122), inky.WHITE)

    def draw_date(self):
        datetimestr = time.strftime("%a %b %d")
        draw = ImageDraw.Draw(self.img)
        draw.text((5, 5), datetimestr, inky.BLACK, font=self.FONT)

    def draw_weather_temp(self, forecast):
        draw = ImageDraw.Draw(self.img)
        draw.text((136, 5), "H:", inky.YELLOW, font=self.FONT)
        draw.text(
            (157, 5),
            forecast.temperature["high"],
            inky.BLACK, font=self.FONT
        )
        draw.text(
            (136, 25),
            f'L: {forecast.temperature["low"]}',
            inky.BLACK, font=self.FONT
        )

    def draw_forecast_conditions(self, icon):
        self.img.paste(icon.image, (200, 2), icon.mask)

    def draw_now_playing(self):
        tbstate = state_machine.TuneboxState()
        draw = ImageDraw.Draw(self.img)
        draw.text(
            (25, 66),
            tbstate.now_playing["artist"],
            inky.BLACK, font=self.FONT
        )
        draw.text(
            (25, 46),
            tbstate.now_playing["title"],
            inky.BLACK, font=self.FONT
        )
        icon = Icon(
            os.path.join(
                os.path.dirname(__file__),
                "../tunebox/resources/icon-headphones.png"
            )
        )
        icon.resize(20, 20)
        self.img.paste(icon.image, (4, 47), icon.mask)

    def draw_playing_state(self, playing=False):
        if playing:
            icon_file = "icon-play"
        else:
            icon_file = "icon-pause"
        icon = Icon(
            os.path.join(
                os.path.dirname(__file__),
                "../tunebox/resources/{}.png".format(icon_file)
            )
        )
        icon.resize(22, 22)
        self.img.paste(icon.image, (2, 67), icon.mask)

    def generate(self):
        self.draw_date()
        self.draw_weather_temp(self.forecast)
        # self.draw_forecast_conditions()
        self.draw_now_playing()
        return self.img

    def save(self):
        pxdata = numpy.array(self.img)
        for y in range(self.img.size[0]):
            for x in range(self.img.size[1]):
                if pxdata[x, y] == 0:
                    pxdata[x, y] = 200
                elif pxdata[x, y] == 2:
                    pxdata[x, y] = 150
        bmp = PILImage.fromarray(pxdata)
        bmp.save('out.bmp')


class Icon:
    """ Weather condition icons """
    def __init__(self, path):
        self.image = PILImage.open(path)
        self.create_mask()

    def create_mask(self):
        """Create a transparency mask.
        Takes a source image and converts it into a mask based on alpha value
        """
        mask_image = PILImage.new("1", self.image.size)
        w, h = self.image.size
        for x in range(w):
            for y in range(h):
                p = self.image.getpixel((x, y))
                if p[3] > 0:  # alpha not 0
                    mask_image.putpixel((x, y), 255)

        self.mask = mask_image

    def recolor(self):
        colorimg = PILImage.new("P", self.image.size)
        w, h = self.image.size
        for x in range(w):
            for y in range(h):
                p = self.image.getpixel((x, y))
                if p[3] > 0:  # alpha not 0
                    colorimg.putpixel((x, y), 2)

        self.image = colorimg

    def resize(self, x, y):
        self.image = self.image.resize((x, y))
        self.create_mask()
