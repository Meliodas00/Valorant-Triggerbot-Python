import json
import sys
import time
from colorama import Fore, Back, Style, init

init(convert = True)

def write_settings(scan_size, show_area, col):
    try:
        scan_size = int(scan_size)
    except ValueError:
        scan_size = 10
        print(Fore.RED + Style.DIM + "\n[alert] Not a number, resort to default 10 pixels"); print(Style.RESET_ALL)
    if show_area.casefold().startswith('y'):
        show_area = True
    else:
        show_area = False
    if col.casefold().startswith('red'):
        rgb_col = [[200, 0, 0], [255, 25, 25]]
    elif col.casefold().startswith('purple'):
        rgb_col = [[150, 40, 165],[235, 120, 255]]
    else:
        print(Fore.RED + Style.DIM+ "\n[alert] Not a valid colour, resort to default red"); print(Style.RESET_ALL)
        rgb_col = [[200, 0, 0], [255, 25, 25]]
        col = 'red'
        
    data = {}
    data['settings'] = []
    data['settings'].append({
        'scan_size': scan_size,
        'show_area': show_area,
        'enemy_color': col,
        'enemy_colour': rgb_col
    })

    with open('settings.json', 'w') as outfile:
        json.dump(data, outfile)


def read_settings():
    with open('settings.json') as file:
        data = json.load(file)
        for s in data['settings']:
            return [['-Scansize:', s['scan_size']], ['-Show Area:', s['show_area']], ['-Enemy hightlight colour:', s['enemy_color']]]


def check_exist():
    try:
        with open('settings.json') as file:
            data = json.load(file)
            for s in data['settings']:
                return True
    except:
        return False


def wipe():
    data = {'settings': None}
    with open('settings.json','w') as outfile:
        json.dump(data, outfile)


def read_raw():
    with open('settings.json') as file:
        data = json.load(file)
        for s in data['settings']:
            return [s['scan_size'], s['show_area'], s['enemy_colour']]


def intro():
    with open('README.txt','r') as f:
        if f.mode == 'r':
            lines = f.read().splitlines()
            for i, x in enumerate(lines):
                if i == 9:
                    print(Fore.GREEN + Style.BRIGHT)
                if i > 8:
                    time.sleep(0.06)
                if x.startswith('[alert]'):
                    print(Fore.RED+ Style.DIM)
                if x.startswith('Module'):
                    break
                print(x)
        print(Style.RESET_ALL)
        f.close()
