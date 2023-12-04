import time
import smbus
import fcntl

BUS = smbus.SMBus(1)
LCD_ADDR = 0x27
BLEN = 1 #turn on/off background light
 
 
def turn_light(key):
    global BLEN
    BLEN = key
    if key ==1 :
        BUS.write_byte(LCD_ADDR ,0x08)
    else:
        BUS.write_byte(LCD_ADDR ,0x00)
 
def write_word(addr, data):
    global BLEN
    temp = data
    if BLEN == 1:
        temp |= 0x08
    else:
        temp &= 0xF7
    BUS.write_byte(addr ,temp)
 
def send_command(comm):
    # Send bit7-4 firstly
    buf = comm & 0xF0
    buf |= 0x04               # RS = 0, RW = 0, EN = 1
    write_word(LCD_ADDR ,buf)
    time.sleep(0.002)
    buf &= 0xFB               # Make EN = 0
    write_word(LCD_ADDR ,buf)
     
    # Send bit3-0 secondly
    buf = (comm & 0x0F) << 4
    buf |= 0x04               # RS = 0, RW = 0, EN = 1
    write_word(LCD_ADDR ,buf)
    time.sleep(0.002)
    buf &= 0xFB               # Make EN = 0
    write_word(LCD_ADDR ,buf)
 
def send_data(data):
    # Send bit7-4 firstly
    buf = data & 0xF0
    buf |= 0x05               # RS = 1, RW = 0, EN = 1
    write_word(LCD_ADDR ,buf)
    time.sleep(0.002)
    buf &= 0xFB               # Make EN = 0
    write_word(LCD_ADDR ,buf)
     
    # Send bit3-0 secondly
    buf = (data & 0x0F) << 4
    buf |= 0x05               # RS = 1, RW = 0, EN = 1
    write_word(LCD_ADDR ,buf)
    time.sleep(0.002)
    buf &= 0xFB               # Make EN = 0
    write_word(LCD_ADDR ,buf)
 
def init_lcd():
    try:
        send_command(0x33) # Must initialize to 8-line mode at first
        time.sleep(0.005)
        send_command(0x32) # Then initialize to 4-line mode
        time.sleep(0.005)
        send_command(0x28) # 2 Lines & 5*7 dots
        time.sleep(0.005)
        send_command(0x0C) # Enable display without cursor
        time.sleep(0.005)
        send_command(0x01) # Clear Screen
        BUS.write_byte(LCD_ADDR ,0x08)
    except:
        return False
    else:
        return True
 
def clear_lcd():
    send_command(0x01) # Clear Screen
 
def print_lcd(x, y, str):
    if x < 0:
        x = 0
    if x > 15:
        x = 15
    if y <0:
        y = 0
    if y > 1:
        y = 1
 
    # Move cursor
    addr = 0x80 + 0x40 * y + x
    send_command(addr)
     
    for chr in str:
        send_data(ord(chr))

class LCD_SEQUENCE:
    def __init__(self, logPath):
        self.filePath = logPath
        with open(self.filePath, 'w') as file:
            fcntl.flock(file.fileno(), fcntl.LOCK_EX)
            file.write('(0, 0, "LCD INIT")\n')
    
    def add(self, data):
        with open(self.filePath, 'a') as file:
            fcntl.flock(file.fileno(), fcntl.LOCK_EX)
            file.write(f"{str(data)}\n")
        
    def get(self):
        with open(self.filePath, 'r') as file:
            fcntl.flock(file.fileno(), fcntl.LOCK_EX)
            datas = file.read()
        data_list = datas.split('\n')
        # print(data_list)
        if len(data_list) == 1 and data_list[0] == '':
            return False
        with open(self.filePath, 'w') as file:
            fcntl.flock(file.fileno(), fcntl.LOCK_EX)
            for data in data_list[1:]:
                file.write(data)
        return data_list[0]
 
if __name__ == '__main__':
    init_lcd()
    turn_light(1)
    print_lcd(0, 0, 'Hello, world!')
    