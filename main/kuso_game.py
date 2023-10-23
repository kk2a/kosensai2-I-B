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

        # おめでとう的なのをしたい
        if self.fighter_now >= self.tower_num:
            pyxel.quit()

        # slideを後にすることで1フレームだけ戻るということがなくなる!!!
        self.update_fighter()
        self.update_slide()

    def draw(self):
        pyxel.cls(11)
        self.draw_tower()
        self.draw_fighter()

        # debug
        pyxel.text(50, 10, f"{pyxel.mouse_x}, {pyxel.mouse_y}", 0)
        floor_idx = (290 - pyxel.mouse_y) // 50
        pyxel.text(0, 0, f"{floor_idx}", 0)
        pyxel.text(10, 10, f"{self.fighter_strength}", 0)
        pyxel.text(10, 20, f"{self.passed}", 0)

    def update_slide(self):
        # スライドしている最中
        if self.left_slide != self.fighter_now * 100:
            self.left_slide += 10
        # すべて倒したら次へ
        elif self.passed == len(self.tower_info[self.fighter_now]):
            self.passed = 0
            self.fighter_now += 1

    def update_fighter(self):
        # 攻撃後に数字は変動
        if self.is_fighting and (pyxel.frame_count - self.fighting_time) >= 29:
            # input.pdfを参考にしてください
            t, b, m, _ = self.tower_info[self.fighter_now][self.on_fighting]
            f = True

            # 敵がいた
            if t == 1 and self.fighter_strength >= m:
                # +
                if b == 1:
                    self.fighter_strength += m

                # *
                elif b == 2:
                    self.fighter_strength *= m

                # bad
                else:
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
                else:
                    f = False

            else:
                f = False

            # ここでゲームオーバーだと思う
            if f:
                self.tower_info[self.fighter_now][self.on_fighting] = 0, 0, 0, 0
                self.passed += 1

            self.is_fighting = False
            self.thinking = pyxel.frame_count

        # クリックされたとき
        elif (
            pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and
            self.left_slide == self.fighter_now * 100 and
            not (self.is_fighting)
        ):
            if (
                pyxel.mouse_x >= 140 and
                pyxel.mouse_x <= 200
            ):
                floor_idx = (290 - pyxel.mouse_y) // 50
                if (0 <= floor_idx and floor_idx < len(self.tower_info[self.fighter_now])):
                    if self.tower_info[self.fighter_now][floor_idx][0] != 0:
                        self.is_fighting = True
                        self.on_fighting = floor_idx
                        self.fighting_time = pyxel.frame_count

    # 最後はボスにするかもしれないので確定ではない
    def draw_tower(self):
        slide = self.left_slide

        u = (
            ((33, 33, 0, 0, 0, 24, 32, 15), (33, 33, 0, 32, 0, 24, 32, 15)),
            ((30, 19, 0, 0, 32, 24, 16, 15), (30, 19, 0, 32, 32, 24, 16, 15)),
            ((35, 14, 0, 0, 59, 12, 10, 15), (35, 14, 0, 16, 59, 12, 10, 15)),
            ((28, 33, 0, 0, 72, 32, 32, 15), (28, 33, 0, 32, 72, 32, 32, 15)),
            ((33, 33, 0, 0, 104, 24, 32, 15), (33, 33, 0, 32, 104, 24, 32, 15)),
            ((28, 33, 0, 0, 144, 32, 32, 15), (28, 33, 0, 32, 144, 32, 32, 15)),
            ((26, 25, 0, 56, 0, 32, 24, 15), (26, 25, 0, 88, 0, 32, 24, 15))
        )

        v = (
            (35, 24, 0, 0, 216, 16, 23, 5),
            (35, 24, 0, 24, 216, 16, 23, 5),
            (35, 24, 0, 48, 216, 16, 23, 5)
        )

        # タワー
        pyxel.rectb(40 - slide, 240, 60, 50, 0)
        for i in range(self.tower_num):
            T = len(self.tower_info[i])
            for j in range(T):
                pyxel.rectb(40 + 100 * (i + 1) - slide,
                            240 - 50 * j, 60, 50, 0)

        # 敵
        pyxel.load(self.load_path[1])
        for i in range(self.tower_num):
            T = len(self.tower_info[i])
            for j in range(T):
                t, b, m, idx = self.tower_info[i][j]
                if t == 1:
                    pyxel.text(
                        75 + 100 * (i + 1) - slide,
                        242 - 50 * j,
                        f"{self.text[b * 2 - 2]}{m}",
                        8
                    )
                    k = (pyxel.frame_count) // 25 % 2  # 一般には % len(u[idx])
                    pyxel.blt(
                        40 + 100 * (i + 1) - slide + u[idx][k][0],
                        290 - 50 * j - u[idx][k][1],
                        u[idx][k][2],
                        u[idx][k][3],
                        u[idx][k][4],
                        u[idx][k][5],
                        u[idx][k][6],
                        u[idx][k][7]
                    )

        # 装備
        pyxel.load(self.load_path[0])
        for i in range(self.tower_num):
            T = len(self.tower_info[i])
            for j in range(T):
                t, b, m, idx = self.tower_info[i][j]
                if t == 2:
                    pyxel.text(
                        75 + 100 * (i + 1) - slide,
                        242 - 50 * j,
                        f"{self.text[b - 1]}{m}",
                        0
                    )
                    pyxel.blt(
                        40 + 100 * (i + 1) - slide + v[idx][0],
                        290 - 50 * j - v[idx][1],
                        v[idx][2],
                        v[idx][3],
                        v[idx][4],
                        v[idx][5],
                        v[idx][6],
                        v[idx][7]
                    )

    # ファイター
    def draw_fighter(self):
        slide = self.left_slide

        u = (
            (0, 32, 16, 32, 40, 5),
            (0, 32, 56, 32, 40, 5),
            (0, 64, 56, 40, 40, 5)
        )

        v = (
            (0, 32, 16, 32, 40, 5),
            (0, 32, 56, 32, 40, 5),
            (0, 64, 56, 40, 40, 5)
        )

        w = (
            (0, 0, 16, 32, 40, 5),
            (0, 32, 16, 32, 40, 5)
        )

        pyxel.load(self.load_path[0])
        # 戦っているときのアニメーション
        if self.is_fighting:
            # 倒すときのアニメーション
            if self.tower_info[self.fighter_now][self.on_fighting][0] == 1:
                i = (pyxel.frame_count - self.fighting_time) // 10 % len(u)
                pyxel.blt(
                    142,
                    250 - 50 * self.on_fighting,
                    u[i][0],
                    u[i][1],
                    u[i][2],
                    u[i][3],
                    u[i][4],
                    u[i][5]
                )

            # 装備などをとるときのアニメーション
            elif self.tower_info[self.fighter_now][self.on_fighting][0] == 2:
                i = (pyxel.frame_count - self.fighting_time) // 10 % len(v)
                pyxel.blt(
                    142,
                    250 - 50 * self.on_fighting,
                    v[i][0],
                    v[i][1],
                    v[i][2],
                    v[i][3],
                    v[i][4],
                    v[i][5]
                )

        # 元の位置にいる
        else:
            # self.thinkingでいい感じ
            i = (pyxel.frame_count - self.thinking) // 20 % len(w)
            pyxel.blt(
                42 + self.fighter_now * 100 - slide,
                250,
                w[i][0],
                w[i][1],
                w[i][2],
                w[i][3],
                w[i][4],
                w[i][5]
            )

    # メンバ変数のまとめ
    def info(self):
        self.fighter_now = 0  # 現在何棟目か
        self.passed = 0  # 現在の棟でいくつ通ったか
        self.left_slide = 0  # いくつスライドさせるかは共通で保持

        # Trueなら下の数字の階で戦っている
        self.is_fighting = False
        self.on_fighting = -1
        self.fighting_time = 0
        self.thinking = 0  # 自己満足です

        #
        self.load_path = (
            "../assets/fighter.pyxres",
            "../assets/enemy_neo.pyxres"
        )

        #
        self.problem_path = (
            "../assets/choimuzu.txt",
            "../assets/test_easy.txt"
        )

        #
        self.enemy_num = 7
        self.equip_num = 3

        # 演算表示
        self.text = ["+", "-", "x", "/"]

        # テキストから問題を読み込む
        with open(self.problem_path[0]) as f:
            line = f.readline()

            # rstripはいらないかもだけど怖いから入れておきます
            self.fighter_strength, self.tower_num = map(
                int, line.rstrip("\n").split())
            self.tower_info = []
            for _ in range(self.tower_num):
                line = f.readline()
                T = int(line.rstrip("\n"))
                a = []
                for __ in range(T):
                    line = f.readline()
                    # ここはrstripいる
                    b = list(map(int, line.rstrip("\n").split()))

                    if b[0] == 1:
                        b.append(pyxel.rndi(0, self.enemy_num - 1))
                    else:
                        b.append(pyxel.rndi(0, self.equip_num - 1))
                    a.append(b)
                self.tower_info.append(a)


App()
