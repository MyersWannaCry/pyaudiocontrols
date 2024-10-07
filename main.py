import os
import win32gui
import win32process
import psutil
import keyboard
import sys
import PIL.Image
from pycaw.pycaw import AudioUtilities
from PySide6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu
from PySide6.QtCore import Qt, Slot, QEvent
import PySide6.QtGui
from PySide6.QtGui import QIcon
from S0_audio_controls import Ui_mainWindow
from pystray import Icon, Menu, MenuItem

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'config.txt')
volumedict = {}
muteddict = {}
image_path = os.path.join(script_dir, 'tray_icon.png')
icon = PIL.Image.open(image_path)
on_first_start = True

class MainWindow(QMainWindow):
    '''Инициализация основного окна с отрисовкой интерфейса и обработкой трея с контекстным меню.'''
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

        # Создание иконки в трее
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(image_path))

        # Создание контекстного меню для иконки в трее
        self.tray_menu = QMenu()
        show_action = self.tray_menu.addAction("Показать")
        quit_action = self.tray_menu.addAction("Выход")

        # Подключаем действия к соответствующим функциям
        show_action.triggered.connect(self.show_window)
        quit_action.triggered.connect(self.exit_application)

        # Устанавливаем меню для иконки трея
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

        # Подключение сигнала для двойного клика по иконке
        self.tray_icon.activated.connect(self.tray_icon_activated)

        # Отрисовка окна в правом нижнем углу экрана
        screen_geometry = QApplication.primaryScreen().geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        window_width = self.frameGeometry().width()
        window_height = self.frameGeometry().height()
        x = screen_width - window_width
        y = screen_height - window_height/0.77
        self.move(x, y)


    @Slot()
    def tray_icon_activated(self, reason):
        '''Показывает интерфейс по нажатию на иконку в трее'''
        if reason == QSystemTrayIcon.Trigger:
            self.show_window()

    @Slot()
    def show_window(self):
        '''Показывает интерфейс'''
        self.showNormal()
        self.activateWindow()

    @Slot()
    def exit_application(self):
        '''Закрывает приложение, скрывая иконку в трее'''
        self.tray_icon.hide()
        QApplication.quit()

    def changeEvent(self, event):
        '''При попытке свернуть окно убирает его в трей, показывая уведомление'''
        global on_first_start
        if event.type() == QEvent.WindowStateChange:
            if on_first_start == True:
                if self.windowState() & Qt.WindowMinimized:
                    self.hide()
                    self.tray_icon.showMessage("Приложение свернуто", "Приложение работает в трее.")
                    on_first_start = False
            else:
                if self.windowState() & Qt.WindowMinimized:
                    self.hide()
            super(MainWindow, self).changeEvent(event)


    def change_mute_binding(self):
        '''Обработка нажатия на клавишу бинда мута'''
        rewrite_mute()
        self.ui.mute_bind_button.setText(keybind_mute)
        self.ui.decrease_bind_button.setText(keybind_decrease)
        
    def change_decrease_binding(self):
        '''Обработка нажатия на клавишу бинда приглушения'''
        rewrite_decrease()
        self.ui.decrease_bind_button.setText(keybind_decrease)
        self.ui.mute_bind_button.setText(keybind_mute)
    
    def on_slider_changed(self,value):
        '''Обработка изменения ползунка и текста под ним'''
        global decrease_percentage
        decrease_percentage = value
        self.ui.percentage_label.setText(f"{decrease_percentage}%")
        print(decrease_percentage) # debug
        save_hotkeys()

    def closeEvent(self, event):
        '''Игнорирует попытку закрыть приложение нажатием на крестик'''
        global on_first_start
        if on_first_start == True:
            self.tray_icon.showMessage("Приложение свернуто", "Приложение работает в трее.") 
            on_first_start = False
        else:
            pass
        event.ignore()
        self.hide()


class AudioController():
    '''Методы аудиоконтроллера, ведущие всё взаимодействие со звуком'''
    def __init__(self, process_name):
        self.process_name = process_name
        self.volume = self.process_volume()

    def process_volume(self):
        '''Определение процесса и его громкости'''
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                print("Current process volume:", interface.GetMasterVolume())  # debug
                return interface.GetMasterVolume()
            
    def increase_volume(self, decibels):
        '''Метод повышения громкости приложения в фокусе'''
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                self.volume = min(1.0, self.volume + decibels)
                interface.SetMasterVolume(self.volume, None)
                print("Volume raised to", self.volume)  # debug

    def decrease_volume(self, decibels):
        '''Метод приглушения приложения в фокусе'''
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                self.volume = max(0.0, self.volume - decibels)
                interface.SetMasterVolume(self.volume, None)
                print("Volume reduced to", self.volume)  # debug

    def mute(self):
        '''Метод полного заглушения приложения в фокусе'''
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                interface.SetMute(1, None)
                print(self.process_name, "has been muted.")  # debug

    def unmute(self):
        '''Метод снятия заглушения приложения в фокусе'''
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                interface.SetMute(0, None)
                print(self.process_name, "has been unmuted.")  # debug

def get_current_process():
    '''Функция получения процесса на переднем плане'''
    pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
    current_process = psutil.Process(pid[-1]).name()
    print("current process is:",current_process) # debug
    return current_process

def write_hotkey():
    '''Обработка считывания горячей клавиши'''
    key = keyboard.read_hotkey()
    print(key) #debug
    return key 

def save_hotkeys():
    '''Обработка сохранения данных мута, приглушения и процентажа приглушения в файл'''
    try:
        with open(file_path, "wt") as file:
            file.write(f"{keybind_mute}\n{keybind_decrease}\n{decrease_percentage}")
        file.close()
    except:
        print("Ошибка записи")

def rewrite_mute():
    '''Перезапись горячей клавиши мута'''
    global keybind_mute
    global keybind_decrease
    keyboard.remove_hotkey(keybind_mute)
    print("Введите клавишу для бинда:") # debug
    keybind_mute = write_hotkey()
    if keybind_mute == keybind_decrease:
        keybind_decrease = "f10"
    try:
        keyboard.add_hotkey(keybind_mute, mute_app)
    except Exception as e:
        print(e) #debug TBD: Обработку исключения с неправильно введенной клавишей
    save_hotkeys()

def rewrite_decrease():
    '''Перезапись горячей клавиши приглушения'''
    global keybind_decrease
    global keybind_mute
    keyboard.remove_hotkey(keybind_decrease)
    print("Введите клавишу для бинда:") # debug
    keybind_decrease = write_hotkey()
    if keybind_decrease == keybind_mute:
        keybind_mute = "f11"
    try:
        keyboard.add_hotkey(keybind_decrease, decrease_volume_by_percentage)
    except Exception as e:
        print(e) #debug TBD: Обработку исключения с неправильно введенной клавишей
    save_hotkeys()

def add_to_dict(my_dict, key, value):
    '''Добавление элемента в словарь'''
    my_dict[key] = value

def decrease_volume_by_percentage():
    '''Понижение звука на определенный процент и запоминание, приглушено ли приложение'''
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
        '''Заглушение звука и запоминание, в муте ли приложение'''
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
    '''Загрузка настроек из файла'''
    global keybind_mute, keybind_decrease, decrease_percentage
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        keybind_mute = lines[0].strip()
        keybind_decrease = lines[1].strip()
        decrease_percentage = lines[2].strip()
    except:
        print("Проблемы с открытием файла, устанавливаю дефолтные значения") # debug
        keybind_mute = "f11"
        keybind_decrease = "f10"
        decrease_percentage = 20
        save_hotkeys()


def main():
    print("START") # debug
    load_settings()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()


    sys.exit(app.exec())
 
if __name__ == "__main__":
    
    main()