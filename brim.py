from datetime import timedelta, datetime
from time import sleep
from inky import InkyPHAT
inky_display = InkyPHAT("red")
inky_display.set_border(inky_display.WHITE)
from PIL import Image, ImageFont, ImageDraw
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # must use GPIO register as hardware pin numbers error for GPIO setup > 26
GPIO.setup(1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

delta = datetime.now()

Y_OFFSET = -40
FONT_SIZE = 140
broke_file = open("/home/pi/broke", "r") # load the datetime that brim last broke from file 
days_string = broke_file.readline().rstrip()
broke_datetime = datetime.strptime(days_string, "%d/%m/%Y %H:%M:%S")
now_datetime = datetime.now()
current_days = str((now_datetime-broke_datetime).days)

print(broke_datetime)
broke_file.close()

def main():
    # main loop to determine method calls, keep day tracked
    global broke_datetime
    global current_days
    global days_string

    now_datetime = datetime.now()
    if not days_string:
        reset()
        return
    days = str((now_datetime-broke_datetime).days) 
    if days == current_days:  # check the days currently displayed has changed, before refreshing
        sleep(0.2)
        return
    current_days = days
    refresh()

def refresh():
    # refresh the display with current day count
    global current_days
    img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/home/pi/fontfile", FONT_SIZE) # a TTF fontfile must be placed here 
    right = inky_display.WIDTH
    y = (Y_OFFSET) 
    size = draw.textsize(current_days, font, -2)
    x = (right - size[0]) # align to the right by offsetting the size required for the text 
    draw.text((x, y), current_days, inky_display.BLACK, font, -2)
    inky_display.set_image(img)
    inky_display.show()

def reset():
    # brim just broke, save current datetime back to file for persistence 
    global broke_datetime
    broke_file = open("/home/pi/broke", "w+")
    broke_datetime = datetime.now()
    broke_file.write(broke_datetime.strftime("%d/%m/%Y %H:%M:%S"))
    broke_file.close()
    main()

if __name__ == "__main__":
    refresh()
    while True:
        if GPIO.input(1) == GPIO.HIGH:
            reset()
            sleep(2) # register button presses less than 2 seconds only once
        if (datetime.now() - timedelta(minutes=1)) > delta:
            # rate limit main loop by delta 
            delta = datetime.now()
            main()

