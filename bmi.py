import customtkinter as ctk
from settings import *
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

class App(ctk.CTk):
    def __init__(self):

        # window setup
        super().__init__(fg_color= GREEN)
        self.title('')
        self.geometry('400x400')
        self.resizable(False, False)
        self.change_title_bar_color()

        # layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0,1,2,3), weight=1, uniform='a')

        # data
        self.metric_bool = ctk.BooleanVar(value=True)
        self.height = ctk.IntVar(value=170)
        self.weight = ctk.DoubleVar(value=65)
        self.bmi = ctk.StringVar()
        self.update_bmi()

        # tracing
        self.height.trace('w', self.update_bmi)
        self.weight.trace('w', self.update_bmi)
        self.metric_bool.trace('w', self.change_units)

        # widgets
        ResulText(self, self.bmi)
        self.weight_input = WeightInput(self, self.weight, self.metric_bool)
        self.height_input = HeightInput(self, self.height, self.metric_bool)
        UnitSwitcher(self, self.metric_bool)

        self.mainloop()

    def change_units(self, *args):
        self.height_input.update_text(self.height.get())
        self.weight_input.update_weight()
    def update_bmi(self, *args):
        height_meter = self.height.get() / 100
        weight = self.weight.get()
        bmi_result = round(weight / height_meter ** 2,2)
        self.bmi.set(bmi_result)

    def change_title_bar_color(self):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = TITLE_HEX_COLOR
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))

        except:
            pass

class ResulText(ctk.CTkLabel):
    def __init__(self, parent, bmi):
        font = ctk.CTkFont(family=FONT, size=MAIN_TEXT_SIZE, weight='bold')
        super().__init__(master=parent, text=22.5, font=font, text_color=WHITE, textvariable=bmi)
        self.grid(column=0, row=0, rowspan=2, sticky='nsew')

class WeightInput(ctk.CTkFrame):
    def __init__(self, parent, weight, metric_bool):
        super().__init__(master=parent,fg_color=WHITE)
        self.grid(column=0, row=2, sticky='nsew', padx=10, pady=10)
        self.weight_class = weight
        self.metric_bool = metric_bool

        # layout
        self.rowconfigure(0, weight=1, uniform='b')
        self.columnconfigure(0, weight=2, uniform='b')
        self.columnconfigure(1, weight=1, uniform='b')
        self.columnconfigure(2, weight=3, uniform='b')
        self.columnconfigure(3, weight=1, uniform='b')
        self.columnconfigure(4, weight=2, uniform='b')

        # output logic
        self.output_string = ctk.StringVar()
        self.update_weight()

        # wdigets
        font = ctk.CTkFont(family=FONT, size=INPUT_FONT_SIZE)
        label = ctk.CTkLabel(self, text='70kg', text_color=BLACK, font=font, textvariable=self.output_string)
        label.grid(row=0, column=2)

        # buttons
        minus_button = ctk.CTkButton(self, text='-', command= lambda: self.update_weight(('minus', 'large')), font=font, text_color=BLACK, fg_color=LIGHT_GRAY, hover_color=GRAY, corner_radius=BUTTON_CORNER_RADIUS)
        minus_button.grid(row=0, column=0, sticky='ns', padx=8, pady=8)

        plus_button = ctk.CTkButton(self, text='+', command= lambda: self.update_weight(('plus', 'large')), font=font, text_color=BLACK, fg_color=LIGHT_GRAY, hover_color=GRAY, corner_radius=BUTTON_CORNER_RADIUS)
        plus_button.grid(row=0, column=4, sticky='ns', padx=8, pady=8)

        small_plus_button = ctk.CTkButton(self, text='+', command= lambda: self.update_weight(('plus', 'small')), font=font, text_color=BLACK, fg_color=LIGHT_GRAY, hover_color=GRAY, corner_radius=BUTTON_CORNER_RADIUS)
        small_plus_button.grid(row=0, column=3, padx=4, pady=4)

        small_minus_button = ctk.CTkButton(self, text='-', command= lambda: self.update_weight(('minus', 'small')), font=font, text_color=BLACK, fg_color=LIGHT_GRAY, hover_color=GRAY, corner_radius=BUTTON_CORNER_RADIUS)
        small_minus_button.grid(row=0, column=1, padx=4, pady=4)

    def update_weight(self, info=None):
        if info:
            if self.metric_bool.get():
                amount = 1 if info[1] == 'large' else 0.1
            else:
                amount = 0.453592 if info[1] == 'large' else 0.453592 / 16

            if info[0] == 'plus':
                self.weight_class.set(self.weight_class.get() + amount)
            else:
                self.weight_class.set(self.weight_class.get() - amount)

        if self.metric_bool.get():
            self.output_string.set(f'{round(self.weight_class.get(), 2)}kg')
        else:
            raw_ounces = self.weight_class.get() * 2.20462 * 16
            pounds, ounces = divmod(raw_ounces, 16)
            self.output_string.set(f'{int(pounds)}lb {int(ounces)}oz')
class HeightInput(ctk.CTkFrame):
    def __init__(self, parent, height, metric_bool):
        super().__init__(master=parent, fg_color=WHITE)
        self.grid(column=0, row=3, sticky='nsew', padx=10, pady=10)
        self.metric_bool = metric_bool

        # widgets
        slider = ctk.CTkSlider(
            self,
            command=self.update_text,
            button_color=GREEN,
            button_hover_color=LIGHT_GRAY,
            progress_color=GREEN,
            fg_color=LIGHT_GRAY,
            variable=height,
            from_=100,
            to=250
        )
        slider.pack(side='left', fill='x', expand=True, padx=10, pady=10)

        self.output_string = ctk.StringVar()
        self.update_text(height.get())

        output_text = ctk.CTkLabel(self, text='1.80m', textvariable=self.output_string, text_color=BLACK, font=ctk.CTkFont(family=FONT, size=INPUT_FONT_SIZE))
        output_text.pack(side='left', fill='x', expand=True, padx=10, pady=10)

    def update_text(self, value):
        if self.metric_bool.get():
            text_string = str(int(value))
            meter = text_string[0]
            cm = text_string[1:]
            self.output_string.set(f'{meter}.{cm}m')
        else:
            feet, inches = divmod(value / 2.54, 12)
            self.output_string.set(f'{int(feet)}\'{int(inches)}\"')

class UnitSwitcher(ctk.CTkLabel):
    def __init__(self, parent, metric_bool):
        font = ctk.CTkFont(family=FONT, size=SWITCH_FONT_SIZE, weight='bold')
        super().__init__(master=parent, text='metric', font=font, text_color=DARK_GREEN)
        self.place(relx=0.98, rely=0.01, anchor='ne')

        self.metric_bool = metric_bool
        self.bind('<Button>', self.change_units)

    def change_units(self, event):
        self.metric_bool.set(not self.metric_bool.get())

        if self.metric_bool.get():
            self.configure(text='metric')
        else:

            self.configure(text='imperial')

if __name__ == '__main__':
    App()