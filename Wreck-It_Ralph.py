import os
import ctypes

def day0():
  text = "Ralph aqui! A escola não é tão ruim, mas prefiro um fliperama cheio de desafios!"
  title = "DE.Wreck-it-Ralph"
  ctypes.windll.user32.MessageBoxW(0, text, title, 0x40)  
  os.system('shutdown /t 5')

day0()
