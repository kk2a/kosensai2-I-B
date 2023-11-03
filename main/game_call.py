import customtkinter as ctk
import subprocess


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.difficult_receive = 0
        self.geometry("1000x500")
        # self.attributes("-fullscreen", True)  # full screen
        self.title("難易度選択")

        self.radio_var = ctk.StringVar()
        self.radio_var.set("selects")

        self.easy_radio_button = ctk.CTkRadioButton(self, text="かんたん",
                                                    variable=self.radio_var,
                                                    value="easy",
                                                    command=self.easy_button_clicked)
        self.normal_radio_button = ctk.CTkRadioButton(self, text="ふつう",
                                                      variable=self.radio_var,
                                                      value="normal",
                                                      command=self.normal_button_clicked)
        self.caratheodory_radio_button = ctk.CTkRadioButton(self, text="カラテオドリ",
                                                            variable=self.radio_var,
                                                            value="caratheodory",
                                                            command=self.caratheodory_button_clicked)

        self.start_button = ctk.CTkButton(self, text="start",
                                          command=self.start_button_clicked, state=ctk.DISABLED)
        self.exit_button = ctk.CTkButton(self, text="ゲーム終了",
                                         command=self.exit_button_clicked)

        self.easy_radio_button.pack(padx=20, pady=20, side="left")
        self.normal_radio_button.pack(padx=20, pady=20, side="left")
        self.caratheodory_radio_button.pack(padx=20, pady=20, side="left")

        self.start_button.pack(padx=20, pady=20, side="left")

        self.exit_button.pack(padx=20, pady=20, side="right")

    def enable_radio_button(self):
        if self.radio_var.get() == "easy" or self.radio_var.get() == "normal" or self.radio_var.get() == "caratheodory":
            self.start_button.configure(state=ctk.NORMAL)
        else:
            self.start_button.configure(state=ctk.DISABLED)

    def easy_button_clicked(self):
        self.enable_radio_button()
        self.difficult_receive = 0
        print("easy game selected")

    def normal_button_clicked(self):
        self.enable_radio_button()
        self.difficult_receive = 1
        print("normal game start")

    def caratheodory_button_clicked(self):
        self.enable_radio_button()
        self.difficult_receive = 2
        print("caratheodory game start")

    def start_button_clicked(self):
        subprocess.run(["python", "kuso_game.py"],
                       input=str(self.difficult_receive), text=True)

    def exit_button_clicked(self):
        print("exit")
        self.destroy()


app = App()
app.mainloop()

