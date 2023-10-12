import pyxel

class App:
    def __init__(self):
        pyxel.init(400, 300, title="kuso game")
        pyxel.mouse(True)
        self.info()

        pyxel.run(self.update, self.draw)

                
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()


    def draw(self):
        pyxel.cls(1)
        self.update_slide()
        # self.draw_tower()
        pyxel.text(50, 50, f"{pyxel.mouse_x}, {pyxel.mouse_y}", 0)
        floor_idx = (290 - pyxel.mouse_y) // 50
        pyxel.text(0, 0, f"{floor_idx}", 0)

    def update_slide(self):
        if self.left_slide != self.fighter_now * 110:
            self.left_slide += 22

    def update_fighter(self):
        if (
            pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and
            self.left_slide != self.fighter_now * 110 and 
            not(self.is_fighting)
        ):
            if (
                pyxel.mouse_x >= 150 and
                pyxel.mouse_x <= 210
            ):
                floor_idx = (290 - pyxel.mouse_y) // 50
                if (0 <= floor_idx and floor_idx < len(self.tower_info[self.fighter_now])):
                    self.is_fighting = True
                    self.on_fighting = floor_idx


    # def draw_tower(self, x):
    #     pyxel.rectb(40, 240, 60, 50, 0)
    #     for i in range(5):
    #         pyxel.rectb(150, 240 - 50 * i, 60, 50, 0)
    #     # pyxel.rectb(150, 190, 60, 50, 0)
    #     pyxel.rectb(260, 240, 60, 50, 0)

    def info(self):
        self.fighter_now = 0 # 現在何棟目か
        self.left_slide = 0

        # Trueなら下の数字の階で戦っている
        self.is_fighting = False
        self.on_fighting = -1 

        with open('./choimuzu.txt') as f:
            line = f.readline()

            # rstripはいらないかもだけど怖いから入れておきます
            self.yuusha_strength, self.tower_num = map(int, line.rstrip("\n").split())
            self.tower_info = []
            for _ in range(self.tower_num):
                line = f.readline()
                T = int(line.rstrip("\n"))
                a = []
                for __ in range(T):
                    line = f.readline()

                    # ここはrstripいる
                    a.append(list(map(int, line.rstrip("\n").split())))
                self.tower_info.append(a)

App()
