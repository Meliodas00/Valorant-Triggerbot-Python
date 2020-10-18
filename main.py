try:
   import time, sys
   from colorama import Fore, Back, Style, init
   from PIL import ImageGrab
   from win32api import GetSystemMetrics
   import win32.lib.win32con as win32con
   import pyautogui
   import win32gui
   import win32ui
   import winsound
   import keyboard
   import manager
except ModuleNotFoundError as e:
   print('[abort] You seem to be missing some modules.. refer to Readme file\nError: %s' % e); time.sleep(5)
   sys.exit(0)

init(convert = True)
pyautogui.FAILSAFE = False

dc = win32gui.GetDC(0)
dcObj = win32ui.CreateDCFromHandle(dc)
hwnd = win32gui.WindowFromPoint((0,0))
monitor = (0, 0, GetSystemMetrics(0), GetSystemMetrics(1))

class Player:
   def __init__(self, **settings):
      self.show_area = settings['show_area']
      self.scan_size = settings['scan_size']
      self.colour = settings['enemy_colour']
      width, height = pyautogui.size()
      self.pos = [int(width/2-self.scan_size), int(width/2+self.scan_size), int(height/2-self.scan_size), int(height/2+self.scan_size)]
      self.num_of_pixels = 0
      self.bullets_shot = 0
      self.start_time = time.time_ns()
      
   def scan(self):
      self.num_of_pixels = 0
      image = ImageGrab.grab()
      
      try:      
         for j in range(self.pos[0], self.pos[1], 1):
            for k in range(self.pos[2], self.pos[3], 1):
               pix_color = image.getpixel((j,k))
               if pix_color[0] >= self.colour[0][0] and pix_color[0] <= self.colour[1][0]:
                  if pix_color[1] >= self.colour[0][1] and pix_color[1] <= self.colour[1][1]:
                     if pix_color[2] >= self.colour[0][2] and pix_color[2] <= self.colour[1][2]:
                        self.num_of_pixels += 1

      except IndexError:
         sys.exit(win32gui.MessageBox(0, "Area out of bounds", "Terminated" , win32con.MB_OK))

      if self.show_area:
         area = dcObj.Rectangle((self.pos[0], self.pos[2], self.pos[1], self.pos[3]))         
         win32gui.InvalidateRect(hwnd, monitor, True)
         #win32gui.Ellipse(dc, self.pos[0], self.pos[2], self.pos[1], self.pos[3])
         
      return self.num_of_pixels

   def check(self):
      if self.scan() >= 4:
         self.shoot()
      if keyboard.is_pressed('esc'):
         winsound.Beep(200,200)
         msg = ('Script lasted: %s seconds' % (round((time.time_ns()-self.start_time)/10**9, 1)))
         sys.exit(win32gui.MessageBox(0, msg, "Stopped program" , 0x00001000))
      if keyboard.is_pressed('up_arrow'):
         manager.wipe()
         winsound.Beep(200,200)
         sys.exit(win32gui.MessageBox(0, 'Erased settings with exit code 0 ','Stopped program', 0x00001000))

   def shoot(self):
      self.bullets_shot += 1
      pyautogui.click()

manager.intro()

if not manager.check_exist():
   manager.write_settings(input("--Enter scan size in pixels--\n: "), input("\n--Show the area being scanned?--\n: "), input("\n--Enter enemy highlight colour--\n: "))
else:
   print(Fore.CYAN + Style.BRIGHT +"Using current settings:")
   for i in range(3):
      for j in range(2):
         print(manager.read_settings()[i][j])
   print(Style.RESET_ALL)
try:
   player = Player(scan_size = manager.read_raw()[0], show_area = manager.read_raw()[1], enemy_colour = manager.read_raw()[2])
except RuntimeError as e:
   print(Fore.RED + "[alert] Something didnt want to be read...%s" % e)

   
if __name__ == '__main__':
   print("\nProgram running :)")
   while True:
      player.check()
   

