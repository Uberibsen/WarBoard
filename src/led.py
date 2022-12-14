import neopixel
import board
import constants.constants as constant

class WS2812:
    """LED settings and color definitions"""
    def towns_settings():
        """WS2812 settings for town LEDs"""
        pixels_towns = neopixel.NeoPixel(board.D18, 12, bpp = 3, brightness = 0.2, auto_write = True, pixel_order = neopixel.RGB)
        return pixels_towns

    def casualty_rate_settings():
        """WS2812 settings for casualites LEDs"""
        pixels_casualites = neopixel.NeoPixel(board.D21, 2, bpp = 3, brightness = 0.2, auto_write = True, pixel_order = neopixel.RGB)
        return pixels_casualites

    def define_town_led_colors(json_response):
        """Define each LED color from JSON response"""
        led_colors = []
        for town in json_response['towns'].values():
            if town == "WARDENS":
                led_colors.append(constant.WARDEN_TEAM_COLOR)
            if town == "COLONIALS":
                led_colors.append(constant.COLONIAL_TEAM_COLOR)    
            if town == "NONE":
                led_colors.append(constant.NEUTRAL_TEAM_COLOR) 
            if town == "NUKED":
                led_colors.append(constant.NUKED_COLOR)
        return led_colors

    def define_casualty_rate_led_colors(json_response):
        """Write LED color cooresponding to casualty rate"""
        led_colors = []
        for casualty_rate in json_response["casualty_rate"].values():
            if int(casualty_rate) < 100:
                led_colors.append(constant.CASUALTY_RATE_0)
            if int(casualty_rate) in range(100, 199):
                led_colors.append(constant.CASUALTY_RATE_100)
            if int(casualty_rate) in range(200, 299):
                led_colors.append(constant.CASUALTY_RATE_200)
            if int(casualty_rate) in range(300, 399):
                led_colors.append(constant.CASUALTY_RATE_300)
            if int(casualty_rate) in range(400, 499):
                led_colors.append(constant.CASUALTY_RATE_400)
            if int(casualty_rate) in range(500, 599):
                led_colors.append(constant.CASUALTY_RATE_500)
            if int(casualty_rate) in range(600, 699):
                led_colors.append(constant.CASUALTY_RATE_600)
            if int(casualty_rate) in range(700, 799):
                led_colors.append(constant.CASUALTY_RATE_700)
            if int(casualty_rate) >= 800:
                led_colors.append(constant.CASUALTY_RATE_800)               
        return led_colors

    def write_led_colors(data):
        """Write the colors in order to the LEDs"""
        pixels_towns = WS2812.towns_settings()
        pixels_casualites = WS2812.casualty_rate_settings()
        town_led_colors = WS2812.define_town_led_colors(data)
        casualty_rate_led = WS2812.define_casualty_rate_led_colors(data)
        
        for town_led in enumerate(town_led_colors):
            pixels_towns[town_led[0]] = town_led[1]
        for casualty_led in enumerate(casualty_rate_led):
            pixels_casualites[casualty_led[0]] = casualty_led[1]