import pyxel

class App:
    def __init__(self):
        pyxel.init(300, 250, title="kuso game")
        pyxel.mouse(True)
        self.info()

        pyxel.run(self.update, self.draw)

    def info(self):
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
                    a.append(list(map(int, line.rstrip("\n").split())))
                self.tower_info.append(a)


    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        

    def draw(self):
        pyxel.cls(1)

        self.draw_tower()
    
    def draw_tower(self):
        pyxel.rectb(150, 190, 60, 50, 0)


App()
