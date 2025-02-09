import os
import sys
import win32gui
import win32process
import psutil
import keyboard
import ast
import customtkinter
from customtkinter import ThemeManager
import os
import PIL
import math
from pycaw.pycaw import AudioUtilities
import comtypes
import pystray
from plyer import notification

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'config.txt')
volumedict = {}
pvolumedict = {}
muteddict = {}
on_first_start = True
tray_icon = None
settings_toggle = True
language = None
theme = None

def get_path(file):
    return os.path.join(script_dir, file)

#Fonts
font_bold_path = get_path('fonts\\Moderustic-Bold.ttf')
font_medium_path = get_path('fonts\\Moderustic-Medium.ttf')

#Icons
icon_path = get_path('images\\icon.ico')

volumedown_icon = PIL.Image.open(get_path('images\\volume-down.png'))
volumedown_dark_icon = PIL.Image.open(get_path('images\\volume-down-dark.png'))

mute_icon = PIL.Image.open(get_path('images\\volume-mute.png'))
mute_dark_icon = PIL.Image.open(get_path('images\\volume-mute-dark.png'))

language_icon = PIL.Image.open(get_path('images\\language.png'))
language_dark_icon = PIL.Image.open(get_path('images\\language_dark.png'))

settings_icon = PIL.Image.open(get_path('images\\settings.png'))
settings_dark_icon = PIL.Image.open(get_path('images\\settings_dark.png'))

theme_icon = PIL.Image.open(get_path('images\\theme.png'))
theme_dark_icon = PIL.Image.open(get_path('images\\theme_dark.png'))

back_icon = PIL.Image.open(get_path('images\\back.png'))
back_dark_icon = PIL.Image.open(get_path('images\\back_dark.png'))


volumedown_image = customtkinter.CTkImage(light_image=volumedown_icon, dark_image=volumedown_dark_icon, size=(50,50))
mute_image = customtkinter.CTkImage(light_image=mute_icon, dark_image=mute_dark_icon, size=(50,50))
language_image = customtkinter.CTkImage(light_image=language_icon, dark_image=language_dark_icon, size=(25,25))
settings_image = customtkinter.CTkImage(light_image=settings_icon, dark_image=settings_dark_icon, size=(25,25))
theme_image = customtkinter.CTkImage(light_image=theme_icon, dark_image=theme_dark_icon, size=(25,25))
back_image = customtkinter.CTkImage(light_image=back_icon, dark_image=back_dark_icon, size=(25,25))

translations = {
    "Русский": {
        "intensity": "Интенсивность приглушения",
        "percentage": "Громкость в процентах",
        "settings": "Настройки",
        "theme": "Тема:",
        "language": "Язык:",
        "notification": "Приложение свернуто в трей и продолжает работать.",
        "expand": "Развернуть",
        "exit": "Выход",
        "restart": "Клавиша\nперезапуска"
    },
    "English": {
        "intensity": "Mute intensity",
        "percentage": "Volume in percents",
        "settings": "Settings",
        "theme": "Theme:",
        "language": "Language:",
        "notification": "The application is minimized to the tray and continues to run.",
        "expand": "Expand",
        "exit": "Exit",
        "restart": "Restart\nhotkey"
    },
    "Українська": {
        "intensity": "Інтенсивність приглушення",
        "percentage": "Гучність у відсотках",
        "settings": "Налаштування",
        "theme": "Тема:",
        "language": "Мова:",
        "notification": "Застосунок згорнуто в трей і продовжує працювати.",
        "expand": "Розгорнути",
        "exit": "Вихід",
        "restart": "Клавiша\nперезапуску"
    },
}
themes = { 
        "Dark Blue": "dark-blue.json",
        "Dark Purple" : "dark-purple.json", 
        "Dark Brown": "dark-brown.json", 
        "Dark Green": "dark-green.json", 
        "Coffee": "brown.json", 
        "White":"white.json",
        "Dark Red": "red.json",
        "White Red": "red.json",
        "Autumn": "autumn.json",
        "Dark Metal": "metal.json",
        "Light Metal": "metal.json",
        "Dark Blue": "midnight.json",
        "Dark Orange": "orange.json",
        "Light Orange": "orange.json",
        "Dark Carrot": "carrot.json",
        "Light Carrot": "carrot.json",
        "Dark Cherry": "cherry.json",
        "Light Cherry": "cherry.json",
        "Dark Pink": "pink.json",
        "Light Pink": "pink.json"
        }

white_themes = ["Coffee", "White Red", "Autumn", "Light Metal", "Light Orange", "Light Carrot", "Light Cherry", "Light Pink"]

class Gui(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme(get_path(f"themes/{themes[theme]}"))
        customtkinter.FontManager.load_font(font_bold_path)
        customtkinter.FontManager.load_font(font_medium_path)

        self.iconbitmap(icon_path)
        self.title("S0 Audio Controls")
        self.grid_columnconfigure((0,1), weight= 1)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", lambda: on_closing(self))
        self.bind("<Unmap>", lambda event: on_closing(self) if self.state() == "iconic" else None)
        self.settings_window = None

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 300
        window_height = 290
        x = screen_width - window_width
        y = screen_height - window_height/0.78
        self.geometry(f"{window_width}x{window_height}+{x-7}+{y}")

        self.header = customtkinter.CTkLabel(master = self, text = "S0 AudioControls", font = ("Moderustic Bold",17))
        self.header.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "ew", columnspan=2)

        self.label1 = customtkinter.CTkLabel(master = self, text = "Интенсивность заглушения", font = ("Moderustic Medium",16))
        self.label1.grid(row = 1, column = 0, padx = 2, pady = 2, sticky = "ew", columnspan=2)

        slider_variable = customtkinter.IntVar(value = decrease_percentage)
        self.slider = customtkinter.CTkSlider(master = self, width=100, height=20, from_=1, to=100, number_of_steps=100, border_width=6, command=self.slider_event, variable= slider_variable)
        self.slider.grid(row = 2, column = 0, padx = 10, sticky = "ew", columnspan=2)
        self.label2 = customtkinter.CTkLabel(master = self, text = decrease_percentage, font = ("Moderustic Medium",12))
        if checkbox_state:
            self.label2.configure(text = f"{decrease_percentage}%")
        self.label2.grid(row = 3, column = 0, padx = 0, pady = 0, sticky = "ew", columnspan=2)

        initial_switch_value = "1" if checkbox_state else "0"
        self.switch_var = customtkinter.StringVar(value=initial_switch_value)
        self.switch = customtkinter.CTkSwitch(master = self, text='Громкость в процентах', font = ("Moderustic Medium",14), command=self.switch_event, variable=self.switch_var, onvalue="1", offvalue="0")
        self.switch.grid(row=4, column = 0, pady = (0,15), columnspan=2)

        self.label3 = customtkinter.CTkLabel(master = self, text = "", image = volumedown_image)
        self.label3.grid(row = 5, column = 0, padx = (35,0), pady = 5, sticky = "w")

        self.button = customtkinter.CTkButton(master=self, text=keybind_decrease.upper(), width=170, height=50, font = ("Moderustic Bold",17), command=self.button1_event)
        self.button.grid(row = 5, column = 1, pady = 5, padx = (0,10), sticky = "w")

        self.label4 = customtkinter.CTkLabel(master = self, text = "", image = mute_image)
        self.label4.grid(row = 6, column = 0, padx = (35,0), pady = 2, sticky = "w")

        self.button2 = customtkinter.CTkButton(master=self, text=keybind_mute.upper(), width=170, height=50, font = ("Moderustic Bold",17), command=self.button2_event)
        self.button2.grid(row = 6, column = 1, pady = 2, padx = (0,10), sticky = "w")

        self.settings_button = customtkinter.CTkButton(master = self, image= settings_image, command = self.toggle_ui_visibility, text = "", height=25, width=25, fg_color="transparent")
        self.settings_button.grid(row = 0, column = 0 ,pady = 8, padx = 10, sticky = "e",  columnspan=2)

        self.show_ui_button = customtkinter.CTkButton(master = self, image= back_image, command = self.toggle_ui_visibility, text = "", height=25, width=25, fg_color="transparent")
        self.show_ui_button.grid(row = 0, column = 0 ,pady = 8, padx = 10, sticky = "e",  columnspan=2)
        self.show_ui_button.grid_remove()
        
        self.settings_label = customtkinter.CTkLabel(master = self, text = "Настройки", font = ("Moderustic Bold",17))
        self.settings_label.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "ew", columnspan=2)
        self.settings_label.grid_remove()

        self.settings_label1 = customtkinter.CTkLabel(master = self, text = "Тема:", font = ("Moderustic Bold",14))
        self.settings_label1.grid(row = 1, column = 0, pady = 35, sticky = "ew")
        self.settings_label1.grid_remove()

        self.theme_combobox = customtkinter.CTkOptionMenu(master=self, values=["Dark Blue", "Dark Purple", "Dark Brown", 
                                                                            "Dark Green", "Coffee", "Dark Red", "White Red", 
                                                                            "Autumn", "Dark Metal", "Light Metal", "Dark Blue", 
                                                                            "Dark Orange", "Light Orange", "Dark Carrot", "Light Carrot", 
                                                                            "Dark Cherry", "Light Cherry", "Dark Pink", "Light Pink"], 
                                                                            command=self.set_theme, font = ("Moderustic Bold",14),
                                                                            dropdown_font = ("Moderustic Medium",13), anchor = 'center')
        self.theme_combobox.grid(row = 1, column = 1, pady = 35, padx = 10, sticky = "ew")
        self.theme_combobox.grid_remove()

        self.settings_label2 = customtkinter.CTkLabel(master = self, text = "Язык:", font = ("Moderustic Bold",14))
        self.settings_label2.grid(row = 2, column = 0, pady = 2, sticky = "ew")
        self.settings_label2.grid_remove()
        
        self.lang_combobox = customtkinter.CTkOptionMenu(master=self, values=["Русский", "English", "Українська"], command=self.update_language, font = ("Moderustic Bold",14), dropdown_font = ("Moderustic Medium",13), anchor = 'center')
        self.lang_combobox.grid(row = 2, column = 1, pady = 2, padx = 10, sticky = "ew")
        self.lang_combobox.grid_remove()

        self.settings_label3 = customtkinter.CTkLabel(master = self, text = "Клавиша\n перезапуска:", font = ("Moderustic Bold",14))
        self.settings_label3.grid(row = 3, column = 0, pady = 27, sticky = "ew")
        self.settings_label3.grid_remove()

        self.settings_button1 = customtkinter.CTkButton(master=self, text=keybind_restart.upper(), width=178, height=30, font = ("Moderustic Bold",17), command=self.settings_button1_event)
        self.settings_button1.grid(row = 3, column = 1, pady = 27, padx  = (0,10), sticky = "e")
        self.settings_button1.grid_remove()

        self.default_widgets = [self.header, self.label1, self.slider, self.label2, self.switch, self.label3, self.button, self.label4, self.button2, self.settings_button]
        self.settings_widgets = [self.show_ui_button, self.settings_label, self.theme_combobox, self.settings_label1, self.settings_label2, self.lang_combobox, self.settings_label3, self.settings_button1]

    def slider_event(self, value):
        global decrease_percentage
        slider_data = math.ceil(value)
        decrease_percentage = slider_data
        if checkbox_state:
            self.label2.configure(text = f"{slider_data}%")
        else:
            self.label2.configure(text = slider_data)
        save_hotkeys()

    def switch_event(self):
        global checkbox_state
        if self.switch_var.get() == "1":
            checkbox_state = True
            self.label2.configure(text = f"{decrease_percentage}%")
        else:
            checkbox_state = False
            self.label2.configure(text = decrease_percentage)
        save_hotkeys()
    
    def button1_event(self):
        rewrite_decrease(self)
        update_buttons(self)

    def button2_event(self):
        rewrite_mute(self)
        update_buttons(self)

    def settings_button1_event(self):
        rewrite_restart(self)
        update_buttons(self)

    def hide_window(self):
        self.withdraw()
        create_tray_icon()

    def show_window(self):
        self.deiconify()
        if tray_icon:
            tray_icon.stop()

    def toggle_ui_visibility(self):
        if self.settings_button.winfo_viewable():
            for widget in self.default_widgets:
                widget.grid_remove()
            for widget in self.settings_widgets:
                widget.grid()
            self.show_ui_button.lift()
        elif self.show_ui_button.winfo_viewable():
            for widget in self.settings_widgets:
                widget.grid_remove()
            for widget in self.default_widgets:
                widget.grid()
            self.settings_button.lift()

    def update_language(self, choice):
        global language
        language = choice
        self.label1.configure(text=translations[language]["intensity"])
        self.switch.configure(text=translations[language]["percentage"])
        self.settings_label.configure(text=translations[language]["settings"])
        self.settings_label1.configure(text=translations[language]["theme"])
        self.settings_label2.configure(text=translations[language]["language"])
        self.settings_label3.configure(text=translations[language]["restart"])
        save_hotkeys()

    def restart(self):
        self.destroy()
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def set_theme(self, choice, restart = True):
        global theme
        theme = choice
        if theme in white_themes:
            customtkinter.set_appearance_mode("light")
        else:
            customtkinter.set_appearance_mode("dark")
        try:
            new_theme = get_path(f"themes/{themes[theme]}")
            customtkinter.set_default_color_theme(new_theme)
            self.update()
            save_hotkeys()
            if restart == True:
                self.restart()
        except Exception as E:
            print (E)
        
        

class AudioController():
    '''Методы аудиоконтроллера, ведущие всё взаимодействие со звуком'''
    def __init__(self, process_name):
        self.process_name = process_name
        self.volume = self.process_volume()

    def process_volume(self):
        '''Определение процесса и его громкости'''
        comtypes.CoInitialize()
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                print("Current process volume:", interface.GetMasterVolume())  # debug
                return interface.GetMasterVolume()
            
    def increase_volume(self, decibels):
        '''Метод повышения громкости приложения в фокусе'''
        comtypes.CoInitialize()
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                self.volume = min(1.0, self.volume + decibels)
                interface.SetMasterVolume(self.volume, None)
                print("Volume raised to", self.volume)  # debug

    def decrease_volume(self, decibels):
        '''Метод приглушения приложения в фокусе'''
        comtypes.CoInitialize()
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                self.volume = max(0.0, self.volume - decibels)
                interface.SetMasterVolume(self.volume, None)
                print("Volume reduced to", self.volume)  # debug

    def mute(self):
        '''Метод полного заглушения приложения в фокусе'''
        comtypes.CoInitialize()
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                interface.SetMute(1, None)
                print(self.process_name, "has been muted.")  # debug

    def unmute(self):
        '''Метод снятия заглушения приложения в фокусе'''
        comtypes.CoInitialize()
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                interface.SetMute(0, None)
                print(self.process_name, "has been unmuted.")  # debug

    def set_volume(self, decibels):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            interface = session.SimpleAudioVolume
            if session.Process and session.Process.name() == self.process_name:
                # only set volume in the range 0.0 to 1.0
                self.volume = min(1.0, max(0.0, decibels))
                interface.SetMasterVolume(self.volume, None)
                print("Volume set to", self.volume)  # debug


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
            file.write(f"{keybind_mute}\n{keybind_decrease}\n{decrease_percentage}\n{checkbox_state}\n{language}\n{theme}\n{keybind_restart}")
        file.close()
    except:
        print("Ошибка записи")

def rewrite_mute(gui):
    '''Перезапись горячей клавиши мута'''
    global keybind_mute
    global keybind_decrease
    global keybind_restart
    if keybind_mute in keyboard._hotkeys:
        keyboard.remove_hotkey(keybind_mute)
    print("Введите клавишу для бинда:") # debug
    keybind_mute = write_hotkey()
    if keybind_mute == keybind_decrease:
        if keybind_decrease in keyboard._hotkeys:
            keyboard.remove_hotkey(keybind_decrease)
            keybind_decrease = "UNMAPPED"
    if keybind_mute == keybind_restart:
        if keybind_restart in keyboard._hotkeys:
            keyboard.remove_hotkey(keybind_restart)
            keybind_restart = "UNMAPPED"
    try:
        keyboard.add_hotkey(keybind_mute, mute_app)
    except Exception as e:
        print(e) #debug TBD: Обработка исключения с неправильно введенной клавишей
    save_hotkeys()
    update_buttons(gui)
    print(f"Keybind_decrease: {keybind_decrease}, Keybind_mute: {keybind_mute}, Keybind_restart: {keybind_restart}") # DEBUG

def rewrite_decrease(gui):
    '''Перезапись горячей клавиши приглушения'''
    global keybind_decrease
    global keybind_mute
    global keybind_restart
    if keybind_decrease in keyboard._hotkeys:
        keyboard.remove_hotkey(keybind_decrease)
    print("Введите клавишу для бинда:") # debug
    keybind_decrease = write_hotkey()
    if keybind_decrease == keybind_mute:
        if keybind_mute in keyboard._hotkeys:
            keyboard.remove_hotkey(keybind_mute)
            keybind_mute = "UNMAPPED"
    if keybind_decrease == keybind_restart:
        if keybind_restart in keyboard._hotkeys:
            keyboard.remove_hotkey(keybind_restart)
            keybind_restart = "UNMAPPED"
    try:
        keyboard.add_hotkey(keybind_decrease, decrease_volume_by_percentage)
    except Exception as e:
        print(e) #debug TBD: Обработку исключения с неправильно введенной клавишей
    save_hotkeys()
    update_buttons(gui)
    print(f"Keybind_decrease: {keybind_decrease}, Keybind_mute: {keybind_mute}, Keybind_restart: {keybind_restart}") # DEBUG

def rewrite_restart(gui):
    global keybind_restart
    global keybind_mute
    global keybind_decrease
    if keybind_restart in keyboard._hotkeys:
        keyboard.remove_hotkey(keybind_restart)
    print("Введите клавишу для бинда:") # debug
    keybind_restart = write_hotkey()
    if keybind_restart == keybind_decrease:
        if keybind_decrease in keyboard._hotkeys:
            keyboard.remove_hotkey(keybind_decrease)
            keybind_decrease = "UNMAPPED"
    if keybind_restart == keybind_mute:
        if keybind_mute in keyboard._hotkeys:
            keyboard.remove_hotkey(keybind_mute)
            keybind_mute = "UNMAPPED"
    try:
        keyboard.add_hotkey(keybind_restart, restart)
    except Exception as e:
        print(e) #debug TBD: Обработка исключения с неправильно введенной клавишей
    save_hotkeys()
    update_buttons(gui)
    print(f"Keybind_decrease: {keybind_decrease}, Keybind_mute: {keybind_mute}, Keybind_restart: {keybind_restart}") # DEBUG

def restart():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def update_buttons(guiname):
    guiname.button.configure(text = str(keybind_decrease.upper()))
    guiname.button2.configure(text = str(keybind_mute.upper()))
    guiname.settings_button1.configure(text = str(keybind_restart.upper()))

def add_to_dict(my_dict, key, value):
    '''Добавление элемента в словарь'''
    my_dict[key] = value

def decrease_volume_by_percentage():
    '''Понижение звука на определенный процент и запоминание, приглушено ли приложение'''
    try:
        process_id = get_current_process()
        audio_controller = AudioController(process_id)
        temp_percentage = round(float(decrease_percentage)*round(audio_controller.process_volume(),1)/100,1)
        if volumedict.get(str(process_id)) == 0:
            if checkbox_state == True:
                audio_controller.increase_volume(pvolumedict.get(str(process_id)))
            else:
                audio_controller.increase_volume(int(decrease_percentage)/100)
            add_to_dict(volumedict, process_id, 1)
            add_to_dict(pvolumedict,process_id, temp_percentage)
        elif volumedict.get(str(process_id)) == 1:
            if checkbox_state == True:
                audio_controller.decrease_volume(temp_percentage)
            else:
                audio_controller.decrease_volume(int(decrease_percentage)/100)
            add_to_dict(volumedict, process_id, 0)
            add_to_dict(pvolumedict,process_id, temp_percentage)
        else:
            if checkbox_state == True:
                audio_controller.decrease_volume(temp_percentage)
            else:
                audio_controller.decrease_volume(int(decrease_percentage)/100)
            add_to_dict(volumedict, process_id, 0)
            add_to_dict(pvolumedict,process_id, temp_percentage)
    except Exception as e:
        print(f"Ошибка понижения звука: {e}") # debug
        
def mute_app():
        '''Заглушение звука и запоминание, в муте ли приложение'''
        try:
            process_id = get_current_process()
            audio_controller = AudioController(process_id)
            if muteddict.get(process_id) == 0:
                audio_controller.mute()
                add_to_dict(muteddict, process_id, 1)
            elif muteddict.get(process_id) == 1:
                audio_controller.unmute()
                add_to_dict(muteddict, process_id, 0)
            else:
                audio_controller.mute()
                add_to_dict(muteddict, process_id, 1)
        except:
            print("Ошибка мута приложения") # debug

def on_closing(gui):
    global on_first_start
    '''Функция сворачивания окна в трей при закрытии'''
    gui.withdraw()
    if on_first_start == True:
            show_notification()
            on_first_start = False
    create_tray_icon(gui)

def create_tray_icon(gui):
    '''Создание трей-меню с функциями развернуть и выйти'''
    def show_app(icon, item):
        gui.deiconify()
        gui.attributes('-topmost', True)
        gui.attributes('-topmost', False)
        gui.focus_force()
        icon.stop()

    def quit_app(icon, item):
        icon.stop()
        gui.quit()

    tray_icon_image = PIL.Image.open(icon_path)
    icon = pystray.Icon("audio_control", tray_icon_image, menu=pystray.Menu(
        pystray.MenuItem(translations[language]["expand"], show_app),
        pystray.MenuItem(translations[language]["exit"], quit_app)))
    icon.run()

def show_notification():
    notification.notify(
        title="S0 AudioControls",
        message=translations[language]["notification"],
        app_icon=icon_path,
        timeout = 1
    )


def load_settings():
    '''Загрузка настроек из файла'''
    global keybind_mute, keybind_decrease, decrease_percentage, checkbox_state, language, theme, keybind_restart
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        keybind_mute = lines[0].strip()
        keybind_decrease = lines[1].strip()
        decrease_percentage = lines[2].strip()
        checkbox_state = ast.literal_eval(lines[3].strip())
        language = lines[4].strip()
        theme = lines[5].strip()
        keybind_restart  = lines[6].strip()
        keyboard.add_hotkey(keybind_decrease, decrease_volume_by_percentage)
        keyboard.add_hotkey(keybind_mute, mute_app)
        keyboard.add_hotkey(keybind_restart, restart)
    except Exception as E:
        print(f"Проблемы с открытием файла, устанавливаю дефолтные значения. Ошибка:\n{E}") # debug
        keybind_mute = "f11"
        keybind_decrease = "f10"
        decrease_percentage = 20
        checkbox_state = False
        language = "English"
        theme = "Dark Metal"
        keybind_restart = "f12"
        save_hotkeys()


def main():
    print("START") # debug
    load_settings()
    gui = Gui()
    gui.focus_force()
    gui.update_language(choice=language)
    gui.lang_combobox.set(language)
    gui.set_theme(choice = theme, restart = False)
    gui.theme_combobox.set(theme)
    on_closing(gui)
    gui.mainloop()

if __name__ == "__main__":
    
    main()