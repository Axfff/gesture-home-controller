class LCD_SEQUENCE:
    def __init__(self, logPath):
        self.filePath = logPath
        with open(self.filePath, 'w') as file:
            file.write('(0, 0, "LCD INIT")\n')
    
    def add(self, data):
        with open(self.filePath, 'a') as file:
            file.write(f"{str(data)}\n")
        
    def get(self):
        with open(self.filePath, 'r') as file:
            datas = file.read()
        data_list = datas.split('\n')
        print(data_list)
        if len(data_list) == 1 and data_list[0] == '':
            return False
        with open(self.filePath, 'w') as file:
            for data in data_list[1:]:
                file.write(data)
        return data_list[0]


s = LCD_SEQUENCE('log.txt')
print(s.get())
s.add((1, 1, 1))
s.add((1, 1, 2))
print(s.get())
print(s.get())
print(s.get())


