import psutil
from plyer import notification
import PySimpleGUI as sg
import os

def get_battery_det():
    return psutil.sensors_battery()

battery = get_battery_det()

if battery.percent <= 15.5 and not battery.power_plugged:
    location = "/".join(__file__.split('/')[:-1])
    sg.Window(title="Battery Low!", layout=[[sg.Image(filename=os.path.join(location, "critical.png"), key="-IMAGE-"), sg.Text("Battery power {:.2f}%, connect power Immediately".format(battery.percent)), sg.Button("Dismiss")]], margins=(10, 20)).read()
elif battery.percent <= 25.5 and not battery.power_plugged:
    notification.notify(title="Battery Low", message="Only {:.2f}% battery remaining charge fast!".format(battery.percent), timeout=10)