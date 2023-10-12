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


    def draw(self):
        pyxel.cls(1)
        self.update_slide()
        self.draw_tower()

        # debug
        pyxel.text(50, 50, f"{pyxel.mouse_x}, {pyxel.mouse_y}", 0)
        floor_idx = (290 - pyxel.mouse_y) // 50
        pyxel.text(0, 0, f"{floor_idx}", 0)

    def update_slide(self):
        if self.left_slide != self.fighter_now * 110:
            self.left_slide += 22
        elif self.passed == len(self.tower_info[self.fighter_now]):
            self.passed = 0
            self.fighter_now += 1

    def update_fighter(self):
        if self.is_fighting:
            t, b, m = self.tower_info[self.fighter_now][self.on_fighting]
            
            # 敵がいた
            if t == 1 and self.fighter_strength >= m:
                # +
                if b == 1:
                    self.fighter_strength += m

                # *
                else :
                    self.fighter_strength *= m

            # 装備or薬
            elif t == 2:
                # +
                if b == 1:
                    self.fighter_strength += m
                
                # -
                if b == 2 and self.fighter_strength > m:
                    self.fighter_strength -= m
                
                # * 
                if b == 3:
                    self.fighter_strength *= m
                
                # //
                if b == 4 and self.fighter_strength >= m:
                    self.fighter_strength //= m

            self.tower_info[self.fighter_now][self.on_fighting] = 0, 0, 0

            self.is_fighting = False
            self.on_fighting = -1
            self.passed += 1

        elif (
            pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and
            self.left_slide != self.fighter_now * 110
        ):
            if (
                pyxel.mouse_x >= 150 and
                pyxel.mouse_x <= 210
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

    def info(self):
        self.fighter_now = 0 # 現在何棟目か
        self.passed = 0 # 現在の棟でいくつ通ったか
        self.left_slide = 0 # いくつスライドさせるかは共通で保持

        # Trueなら下の数字の階で戦っている
        self.is_fighting = False
        self.on_fighting = -1 

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
