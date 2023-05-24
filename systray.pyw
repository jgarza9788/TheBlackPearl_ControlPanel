
from infi.systray import SysTrayIcon
import os


def nothing():
    print("this does nothing")

def activateVPN(nothing):
    os.startfile(r"C:\Users\JGarza\GitHub\VPNTools\activate_VPN_close.cmd")

def killVPN(nothing):
    os.startfile(r"C:\Users\JGarza\GitHub\VPNTools\kill_VPN_close.cmd")

menu_options = (
    ("TBP_CP", None, nothing),
    ("----------", None, nothing),
    ("activateVPN", None, activateVPN),
    ("killVPN", None, killVPN),
    ("----------", None, nothing),
    )

systray = SysTrayIcon("icon.ico", "TBP_CP", menu_options)


if __name__ == "__main__":
    systray.start()
    





