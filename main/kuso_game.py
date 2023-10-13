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
        
        # この動作は変わる
        if self.fighter_now >= self.tower_num:
            pyxel.quit()

        # slideが先!!!
        self.update_fighter()
        self.update_slide()



    def draw(self):
        pyxel.cls(1)
        self.draw_tower()
        self.draw_fighter()

        # debug
        pyxel.text(50, 50, f"{pyxel.mouse_x}, {pyxel.mouse_y}", 0)
        floor_idx = (290 - pyxel.mouse_y) // 50
        pyxel.text(0, 0, f"{floor_idx}", 0)
        pyxel.text(10, 10, f"{self.fighter_strength}", 0)
        pyxel.text(10, 20, f"{self.passed}", 0)

    def update_slide(self):
        if self.left_slide != self.fighter_now * 100:
            self.left_slide += 10
        elif self.passed == len(self.tower_info[self.fighter_now]):
            self.passed = 0
            self.fighter_now += 1

    def update_fighter(self):
        if self.is_fighting and self.fighting_time >= 29:
            t, b, m = self.tower_info[self.fighter_now][self.on_fighting]
            
            f = True
            # 敵がいた
            if t == 1 and self.fighter_strength >= m:
                # +
                if b == 1:
                    self.fighter_strength += m

                # *
                elif b == 2 :
                    self.fighter_strength *= m
                
                # bad
                else :
                    f = False

            # 装備or薬
            elif t == 2:
                # +
                if b == 1:
                    self.fighter_strength += m
                
                # -
                elif b == 2 and self.fighter_strength > m:
                    self.fighter_strength -= m
                
                # * 
                elif b == 3:
                    self.fighter_strength *= m
                
                # //
                elif b == 4 and self.fighter_strength >= m:
                    self.fighter_strength //= m
                
                # bad
                else :
                    f = False
            
            else :
                f = False

            # ここでゲームオーバーだと思う
            if f:
                self.tower_info[self.fighter_now][self.on_fighting] = 0, 0, 0
                self.passed += 1

            self.is_fighting = False
            self.fighting_time = 0

        elif self.is_fighting:
            self.fighting_time += 1

        elif (
            pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and
            self.left_slide == self.fighter_now * 100
        ):
            if (
                pyxel.mouse_x >= 140 and
                pyxel.mouse_x <= 200
            ):
                floor_idx = (290 - pyxel.mouse_y) // 50
                if (0 <= floor_idx and floor_idx < len(self.tower_info[self.fighter_now])):
                    self.is_fighting = True
                    self.on_fighting = floor_idx

    # 最後はボスにするかもしれないので確定ではない
    def draw_tower(self):
        slide = self.left_slide

        pyxel.rectb(40 - slide, 240, 60, 50, 0)
        for i in range(self.tower_num):
            T = len(self.tower_info[i])
            for j in range(T):
                pyxel.rectb(40 + 100 * (i + 1) - slide, 240 - 50 * j, 60, 50, 0)
                t, b, m = self.tower_info[i][j]
                if t == 1:
                    pyxel.text(
                        80 + 100 * (i + 1) - slide, 
                        242 - 50 * j, 
                        f"{self.text[b * 2 - 2]}{m}",
                        8
                    )
                elif t == 2:
                    pyxel.text(
                        80 + 100 * (i + 1) - slide, 
                        242 - 50 * j, 
                        f"{self.text[b - 1]}{m}",
                        0
                    )

    def draw_fighter(self):
        pyxel.load("../assets/fighter.pyxres")
        if self.is_fighting:
            i = self.fighting_time // 10 % 3
            u = [
                [0, 32, 16, 32, 40, 5],
                [0, 32, 56, 32, 40, 5],
                [0, 64, 56, 40, 40, 5]
            ]
            pyxel.blt(142, 250 - 50 * self.on_fighting, u[i][0], u[i][1], u[i][2], u[i][3], u[i][4], u[i][5])
        else :
            pyxel.blt(42 + self.fighter_now * 100 - self.left_slide, 250, 0, 0, 16, 32, 40, 5)



    def info(self):
        self.fighter_now = 0 # 現在何棟目か
        self.passed = 0 # 現在棟をいくつ通ったか
        self.left_slide = 0 # いくつスライドさせるかは共通で保持

        # Trueなら下の数字の階で戦っている
        self.is_fighting = False
        self.on_fighting = -1 
        self.fighting_time = 0

        # ファイター何もしていないときのアニメーション
        self.fighter_stop_animation = [
            [0, 0, 16, 32, 40, 5],
            [0, 0, 56, 32, 40, 5]
        ]
        self.fighter_fighting_animation = [
            [0, 32, 16, 32, 40, 5],
            [0, 32, 56, 32, 40, 5],
            [0, 64, 56, 40, 40, 5]
        ]

        # 演算表示
        self.text = ["+", "-", "x", "/"]

        with open('./choimuzu.txt') as f:
            line = f.readline()

            # rstripはいらないかもだけど怖いから入れておきます
            self.fighter_strength, self.tower_num = map(int, line.rstrip("\n").split())
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
