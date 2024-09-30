import os
import win32gui
import win32process
import psutil
import keyboard
import sys
import PIL.Image
from pycaw.pycaw import AudioUtilities
from PySide6.QtWidgets import QApplication, QMainWindow
import PySide6.QtGui
from S0_audio_controls import Ui_mainWindow
from pystray import Icon, Menu, MenuItem
from threading import Thread

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'config.txt')
volumedict = {}
muteddict = {}
image_path = os.path.join(script_dir, 'tray_icon.png')
icon = PIL.Image.open(image_path)



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(PySide6.QtGui.QIcon(image_path))
        self.ui.mute_bind_button.setText(keybind_mute)
        self.ui.decrease_bind_button.setText(keybind_decrease)
        self.ui.percentage_label.setText(f"{decrease_percentage}%")
        self.ui.percentage_slider.setSliderPosition(int(decrease_percentage))
        self.ui.percentage_slider.setValue(int(decrease_percentage))
        self.ui.mute_bind_button.clicked.connect(self.change_mute_binding)
        self.ui.decrease_bind_button.clicked.connect(self.change_decrease_binding)
        self.ui.percentage_slider.valueChanged.connect(self.on_slider_changed)
        keyboard.add_hotkey(keybind_decrease, decrease_volume_by_percentage)
        keyboard.add_hotkey(keybind_mute, mute_app)

    def change_mute_binding(self):
        rewrite_mute()
        self.ui.mute_bind_button.setText(keybind_mute)
        self.ui.decrease_bind_button.setText(keybind_decrease)
        
    def change_decrease_binding(self):
        rewrite_decrease()
        self.ui.decrease_bind_button.setText(keybind_decrease)
        self.ui.mute_bind_button.setText(keybind_mute)
    
    def on_slider_changed(self,value):
        global decrease_percentage
        decrease_percentage = value
        self.ui.percentage_label.setText(f"{decrease_percentage}%")
        save_hotkeys()

    def closeEvent(self, event):
        event.ignore()
        self.hide()


class AudioController():
    def __init__(self, process_name):
        self.process_name = process_name
        self.volume = self.process_volume()

    def process_volume(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                print("Current process volume:", interface.GetMasterVolume())  # debug
                return interface.GetMasterVolume()
            
    def increase_volume(self, decibels):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                self.volume = min(1.0, self.volume + decibels)
                interface.SetMasterVolume(self.volume, None)
                print("Volume raised to", self.volume)  # debug

    def decrease_volume(self, decibels):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                self.volume = max(0.0, self.volume - decibels)
                interface.SetMasterVolume(self.volume, None)
                print("Volume reduced to", self.volume)  # debug

    def mute(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                interface.SetMute(1, None)
                print(self.process_name, "has been muted.")  # debug

    def unmute(self):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                interface.SetMute(0, None)
                print(self.process_name, "has been unmuted.")  # debug

def get_current_process():
    pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
    current_process = psutil.Process(pid[-1]).name()
    print("current process is:",current_process) # debug
    return current_process

def write_hotkey():
    key = keyboard.read_hotkey()
    print(key)
    return key

def save_hotkeys():
    try:
        with open(file_path, "wt") as file:
            file.write(f"{keybind_mute}\n{keybind_decrease}\n{decrease_percentage}")
        file.close()
    except:
        print("Ошибка записи")

def rewrite_mute():
    global keybind_mute
    global keybind_decrease
    keyboard.remove_hotkey(keybind_mute)
    print("Введите клавишу для бинда:") # debug
    keybind_mute = write_hotkey()
    if keybind_mute == keybind_decrease:
        keybind_decrease = "alt+x"
    keyboard.add_hotkey(keybind_mute, mute_app)
    save_hotkeys()

def rewrite_decrease():
    global keybind_decrease
    global keybind_mute
    keyboard.remove_hotkey(keybind_decrease)
    print("Введите клавишу для бинда:") # debug
    keybind_decrease = write_hotkey()
    if keybind_decrease == keybind_mute:
        keybind_mute = "alt+z"
    keyboard.add_hotkey(keybind_decrease, decrease_volume_by_percentage)
    save_hotkeys()

def add_to_dict(my_dict, key, value):
    my_dict[key] = value

def decrease_volume_by_percentage():
    try:
        process_id = get_current_process()
        audio_controller = AudioController(process_id)
        if volumedict.get(str(process_id)) == 0:
            audio_controller.increase_volume(int(decrease_percentage)/100)
            add_to_dict(volumedict, process_id, 1)
        elif volumedict.get(str(process_id)) == 1:
            audio_controller.decrease_volume(int(decrease_percentage)/100)
            add_to_dict(volumedict, process_id, 0)
        else:
            audio_controller.decrease_volume(int(decrease_percentage)/100)
            add_to_dict(volumedict, process_id, 0)
    except:
        print("Ошибка понижения звука") # debug
        
def mute_app():
        try:
            process_id = get_current_process()
            audio_controller = AudioController(process_id)
            if muteddict.get(str(process_id)) == 0:
                audio_controller.mute()
                add_to_dict(muteddict, process_id, 1)
            elif muteddict.get(str(process_id)) == 1:
                audio_controller.unmute()
                add_to_dict(muteddict, process_id, 0)
            else:
                audio_controller.mute()
                add_to_dict(muteddict, process_id, 1)
        except:
            print("Ошибка мута приложения") # debug

def load_settings():
    global keybind_mute, keybind_decrease, decrease_percentage
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        keybind_mute = lines[0].strip()
        keybind_decrease = lines[1].strip()
        decrease_percentage = lines[2].strip()
    except:
        print("Проблемы с открытием файла, устанавливаю дефолтные значения")
        keybind_mute = "alt+z"
        keybind_decrease = "alt+x"
        decrease_percentage = 60
        save_hotkeys()

def create_tray_icon(app_window):
    """Создает иконку в трее."""
    def on_quit(icon, item):
        icon.stop()
        QApplication.quit()
        

    def on_show(icon, item):
        app_window.show()
        tray_icon.hide()

    menu = Menu(
        MenuItem('Показать', on_show),
        MenuItem('Выход', on_quit)
    )
    tray_icon = Icon("VolumeControl", icon, menu=menu)
    return tray_icon


def tray_thread(tray_icon):
    """Запускает иконку в трее в отдельном потоке."""
    tray_icon.run()


def main():
    print("START")
    load_settings()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    tray_icon = create_tray_icon(window)
    thread = Thread(target=tray_thread, args=(tray_icon,), daemon=True)
    thread.start()

    sys.exit(app.exec())
 
if __name__ == "__main__":
    
    main()