import communication
import gestureControl
import LCDcontrol as LCD
import fanControl
import deviceControl
import threading
import time


ARDUINO_PORT = 11
FAN_PORT = 7
LCD_SEQUENCE_1 = LCD.LCD_SEQUENCE('LCD_SEQUENCE_1')


def autoControl():
    temperature, brightness, air_quality, humanity = 0, 0, 0, 0
    while True:
        res = communication.read_data(ARDUINO_PORT)
        if res:
            temperature, brightness, air_quality, humanity = res
        print(f"temperature: {temperature}  brightness:{brightness}  air_quality: {air_quality}  humanity: {humanity}")
        time.sleep(5)


def LCDcontrol(lcd_sequence):
    LCD.init_lcd()
    last_content = None
    while True:
        now = time.strftime('%m/%d %H:%M:%S', time.localtime(time.time()))
        LCD.print_lcd(*(0, 1, now))

        content = lcd_sequence.get()
        if not content:
            LCD.print_lcd(0, 0, "no command      ")
        else:
            # print(f"showing {content}")
            if last_content != content:
                # LCD.clear_lcd()
                try:
                    LCD.print_lcd(*eval(content))
                except:
                    continue
            time.sleep(0.1)
        last_content = content


def main():
    fanControlThread = threading.Thread(target=lambda: fanControl.main(FAN_PORT))
    fanControlThread.setDaemon(True)
    fanControlThread.start()

    LCDcontrolThread = threading.Thread(target=lambda: LCDcontrol(LCD_SEQUENCE_1))
    LCDcontrolThread.setDaemon(True)
    LCDcontrolThread.start()

    # # autoControlThread = threading.Thread(target=autoControl)
    # # autoControlThread.setDaemon(True)
    # # autoControlThread.start()

    gestureControlThread = threading.Thread(target=lambda: gestureControl.main(LCD_SEQUENCE_1))
    gestureControlThread.setDaemon(True)
    gestureControlThread.start()
    pass


if __name__ == "__main__":
    main()
    autoControl()
    # while True:
    #     pass
