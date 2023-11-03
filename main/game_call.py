import customtkinter as ctk
import subprocess
from PIL import Image


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("system")
        ctk.deactivate_automatic_dpi_awareness()

        self.resizable(width=False, height=False)
        self.difficult_receive = 0
        self.geometry("500x500")
        # self.attributes("-fullscreen", True)  # full screen
        self.title("難易度選択")

        ######

        # label = ctk.CTkLabel(text="難易度選択", fg_color="transparent")

        #######

        self.bg_image = ctk.CTkImage(light_image=Image.open("../assets/back0.png"),
                                     dark_image=Image.open("../assets/back0.png"),
                                     size=(500, 500))
        self.bg = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg.place(x=0, y=0)
        # self.bg.pack(fill="x")

        #####

        self.radio_var = ctk.StringVar()
        self.radio_var.set("selects")

        self.easy_radio_button = ctk.CTkRadioButton(self,
                                                    width=45,
                                                    height=30,
                                                    corner_radius=0,
                                                    border_color="dimgray",
                                                    text_color="black",
                                                    text="かんたん　　",
                                                    bg_color="gray",
                                                    command=self.easy_button_clicked,
                                                    variable=self.radio_var,
                                                    value="easy")
        self.normal_radio_button = ctk.CTkRadioButton(self,
                                                      width=45,
                                                      height=30,
                                                      corner_radius=0,
                                                      border_color="dimgray",
                                                      text_color="black",
                                                      text="ふつう　　　",
                                                      bg_color="gray",
                                                      command=self.normal_button_clicked,
                                                      variable=self.radio_var,
                                                      value="normal")
        self.caratheodory_radio_button = ctk.CTkRadioButton(self,
                                                            width=45,
                                                            height=30,
                                                            corner_radius=0,
                                                            #border_color="dimgray",
                                                            text_color="black",
                                                            text="カラテオドリ",
                                                            bg_color="gray",
                                                            command=self.caratheodory_button_clicked,
                                                            variable=self.radio_var,
                                                            value="caratheodory")

        self.start_button = ctk.CTkButton(self,
                                          width=150,
                                          height=45,
                                          fg_color="gray",
                                          text_color="black",
                                          text="ゲームスタート",
                                          bg_color="gray",
                                          state=ctk.DISABLED,
                                          command=self.start_button_clicked)

        # self.easy_radio_button.pack(padx=20, pady=20, side="left")
        # self.normal_radio_button.pack(padx=20, pady=20, side="left")
        # self.caratheodory_radio_button.pack(padx=20, pady=20, side="left")
        # self.start_button.pack(padx=0, pady=20, side="bottom")
        self.easy_radio_button.grid(row=1, column=0, padx=20, pady=200)
        self.normal_radio_button.grid(row=1, column=1, padx=20, pady=200)
        self.caratheodory_radio_button.grid(row=1, column=2, padx=20, pady=200)
        self.start_button.grid(row=2, column=1, padx=30, pady=0)

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
        self.radio_var.set("selects")
        self.start_button.configure(state=ctk.DISABLED)
        subprocess.run(["python", "kuso_game.py"],
                       input=str(self.difficult_receive), text=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
