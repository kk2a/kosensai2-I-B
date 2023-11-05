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
        self.problem_receive = 0
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
        self.radio_p_var = ctk.StringVar()
        self.radio_p_var.set("selects")

        self.easy_radio_button = ctk.CTkRadioButton(self,
                                                    width=45,
                                                    height=30,
                                                    corner_radius=0,
                                                    border_color="dimgray",
                                                    text_color="black",
                                                    text="かんたん　　",
                                                    bg_color="gray80",
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
                                                      bg_color="gray80",
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
                                                            bg_color="gray80",
                                                            command=self.caratheodory_button_clicked,
                                                            variable=self.radio_var,
                                                            value="caratheodory")

        self.problem_radio_button_1 = ctk.CTkRadioButton(self,
                                                         width=45,
                                                         height=30,
                                                         corner_radius=0,
                                                         #border_color="dimgray",
                                                         text_color="black",
                                                         text="問題１　　　",
                                                         bg_color="gray80",
                                                         command=self.problem_button_cliked_1,
                                                         variable=self.radio_p_var,
                                                         value="0")
        self.problem_radio_button_2 = ctk.CTkRadioButton(self,
                                                         width=45,
                                                         height=30,
                                                         corner_radius=0,
                                                         #border_color="dimgray",
                                                         text_color="black",
                                                         text="問題２　　　",
                                                         bg_color="gray80",
                                                         command=self.problem_button_cliked_2,
                                                         variable=self.radio_p_var,
                                                         value="1")
        self.problem_radio_button_3 = ctk.CTkRadioButton(self,
                                                         width=45,
                                                         height=30,
                                                         corner_radius=0,
                                                         #border_color="dimgray",
                                                         text_color="black",
                                                         text="問題３　　　",
                                                         bg_color="gray80",
                                                         command=self.problem_button_cliked_3,
                                                         variable=self.radio_p_var,
                                                         value="2")

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
        self.easy_radio_button.grid(row=1, column=0, padx=20, pady=100)
        self.normal_radio_button.grid(row=1, column=1, padx=20, pady=100)
        self.caratheodory_radio_button.grid(row=1, column=2, padx=20, pady=100)
        self.problem_radio_button_1.grid(row=2, column=0, padx=20, pady=0)
        self.problem_radio_button_2.grid(row=2, column=1, padx=20, pady=0)
        self.problem_radio_button_3.grid(row=2, column=2, padx=20, pady=0)
        self.start_button.grid(row=3, column=1, padx=30, pady=100)

    def enable_radio_button(self):
        if ((self.radio_var.get() == "easy" or
            self.radio_var.get() == "normal" or
            self.radio_var.get() == "caratheodory") and
            (self.radio_p_var.get() == "0" or
            self.radio_p_var.get() == "1" or
            self.radio_p_var.get() == "2")
            ):
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

    def problem_button_cliked_1(self):
        self.enable_radio_button()
        self.problem_receive = 0
        print("select problem No.1")

    def problem_button_cliked_2(self):
        self.enable_radio_button()
        self.problem_receive = 1
        print("select problem No.2")

    def problem_button_cliked_3(self):
        self.enable_radio_button()
        self.problem_receive = 2
        print("select problem No.3")

    def start_button_clicked(self):
        self.radio_var.set("selects")
        self.radio_p_var.set("selects")
        self.start_button.configure(state=ctk.DISABLED)
        subprocess.run(["pyxel", "run", "kuso_game.py"],
                       input=f"{self.difficult_receive} {self.problem_receive}",
                       text=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
