import pyxel

DISPALY_SIZE_W = 400 + 120 * 2
DISPALY_SIZE_H = 364

FLOOR_SIZE_W = 60
FLOOR_SIZE_H = 50
WALL_SIZE_BOTTOM = 8
WALL_SIZE_SIDE = 16
FLOOR_WALL_SIDE = 2 * WALL_SIZE_SIDE + FLOOR_SIZE_W
FLOOR_WALL_BOTTOM = WALL_SIZE_BOTTOM + FLOOR_SIZE_H
CEIL_HEIGHT = 90

TOWER_SKIP = 40
TOWER_INIT_SKIP_H = 10


class App:
    def __init__(self):
        pyxel.init(DISPALY_SIZE_W, DISPALY_SIZE_H, title="kuso game")
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
        self.update_fighter(TOWER_SKIP + FLOOR_WALL_SIDE)
        self.update_slide(self.fighter_now * (TOWER_SKIP + FLOOR_WALL_SIDE),
                          len(self.tower_info[self.fighter_now]))

    def draw(self):
        pyxel.cls(11)
        self.draw_tower(self.left_slide,
                        TOWER_SKIP + FLOOR_WALL_SIDE,
                        FLOOR_WALL_BOTTOM)
        self.draw_fighter(self.left_slide,
                          TOWER_SKIP + FLOOR_WALL_SIDE,
                          FLOOR_WALL_BOTTOM)

        # debug
        pyxel.text(50, 10, f"{pyxel.mouse_x}, {pyxel.mouse_y}", 0)
        floor_idx = (DISPALY_SIZE_H - TOWER_INIT_SKIP_H -
                     pyxel.mouse_y) // FLOOR_WALL_BOTTOM
        pyxel.text(0, 0, f"{floor_idx}", 0)
        pyxel.text(10, 10, f"{self.fighter_strength}", 0)
        pyxel.text(10, 20, f"{self.passed}", 0)

    def update_slide(self, p, le):
        # スライドしている最中
        if self.left_slide != p:
            self.left_slide += min(p - self.left_slide,
                                   (p - self.left_slide + 14) // 15 + 3)
        # すべて倒したら次へ
        elif self.passed == le:
            self.passed = 0
            self.fighter_now += 1

    def update_fighter(self, S):
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

            # 武器or薬
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

            self.is_fighting = False
            self.thinking = pyxel.frame_count

            # ここでゲームオーバーだと思う
            if not(f):
                self.on_fighting = -1
                return

            self.tower_info[self.fighter_now][self.on_fighting] = 0, 0, 0, 0
            self.on_fighting = -1
            self.passed += 1

        # クリックされたとき
        elif (
            pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and
            self.left_slide == self.fighter_now * S and
            not (self.is_fighting)
        ):
            if (
                pyxel.mouse_x >= TOWER_SKIP + S and
                pyxel.mouse_x <= 2 * S
            ):
                idx = (DISPALY_SIZE_H - TOWER_INIT_SKIP_H -
                       pyxel.mouse_y) // FLOOR_WALL_BOTTOM
                res = (DISPALY_SIZE_H - TOWER_INIT_SKIP_H -
                       pyxel.mouse_y) % FLOOR_WALL_BOTTOM
                if (
                    0 <= idx and
                    idx < len(self.tower_info[self.fighter_now]) and
                    WALL_SIZE_BOTTOM <= res
                ):
                    if self.tower_info[self.fighter_now][idx][0] != 0:
                        self.is_fighting = True
                        self.on_fighting = idx
                        self.fighting_time = pyxel.frame_count

    # 最後はボスにするかもしれないので確定ではない
    def draw_tower(self, slide, S, Q):
        # 敵のアニメーション
        u = (
            ((3, 1, 0, 0, 0, 24, 32, 15), (3, 1, 0, 32, 0, 24, 32, 15)),
            ((6, 3, 0, 0, 32, 24, 16, 15), (6, 3, 0, 32, 32, 24, 16, 15)),
            ((11, 4, 0, 0, 59, 12, 10, 15), (11, 4, 0, 16, 59, 12, 10, 15)),
            ((3, 1, 0, 3, 73, 26, 30, 15), (3, 1, 0, 35, 73, 26, 30, 15)),
            ((6, 1, 0, 0, 104, 24, 32, 15), (6, 1, 0, 32, 104, 24, 32, 15)),
            ((3, 1, 0, 0, 143, 26, 33, 15), (3, 1, 0, 32, 143, 26, 33, 15)),
            ((2, 1, 0, 56, 0, 32, 24, 15), (2, 1, 0, 88, 0, 32, 24, 15))
        )

        # 武器の表示
        v = (
            (9, 1, 0, 0, 216, 16, 24, 5),
            (9, 1, 0, 24, 216, 16, 24, 5),
            (9, 1, 0, 48, 216, 16, 24, 5),
            (9, 1, 0, 96, 208, 16, 33, 5),
            (9, 1, 0, 112, 208, 16, 33, 5)
        )

        # タワーの表示
        w = (
            (0, CEIL_HEIGHT, 0, 140, 8, 92, 90, 5),
            (0, Q, 0, 140, 98, 92, 58, 5)
        )

        # タワー
        pyxel.load(self.load_path[0])
        pyxel.blt(
            TOWER_SKIP - slide, DISPALY_SIZE_H - TOWER_INIT_SKIP_H -
            CEIL_HEIGHT, 0, 140, 8, 92, 90, 5
        )
        # pyxel.blt(
        #     TOWER_SKIP - slide, 
        #     DISPALY_SIZE_H - TOWER_INIT_SKIP_H - TOWER_INIT_SKIP_H
        #     + w[idx][1], w[idx][2], w[idx][3], w[idx][4], 
        #     w[idx][5], w[idx][6], w[idx][7]
        # )
        for i in range(self.tower_num):
            T = len(self.tower_info[i])
            for j in range(T):
                idx = 1
                if j == T - 1:
                    idx = 0
                pyxel.blt(
                    TOWER_SKIP + S * (i + 1) - slide, 
                    DISPALY_SIZE_H - TOWER_INIT_SKIP_H - Q * j -
                    + w[idx][1], w[idx][2], w[idx][3], w[idx][4], 
                    w[idx][5], w[idx][6], w[idx][7]
                )

        # 武器
        for i in range(self.tower_num):
            T = len(self.tower_info[i])
            for j in range(T):
                t, b, m, idx = self.tower_info[i][j]
                if t == 2:
                    tmp = (FLOOR_WALL_SIDE + v[idx][5]) / 2
                    if (self.fighter_now == i and self.on_fighting == j):
                        tmp = v[idx][0] + v[idx][5] + WALL_SIZE_SIDE

                    self.draw_number(
                        S * (i + 2) - tmp + v[idx][5] / 2 - slide,
                        DISPALY_SIZE_H - TOWER_INIT_SKIP_H - Q * (j + 1),
                        t, b, m
                    )

                    pyxel.blt(
                        S * (i + 2) - tmp - slide,
                        DISPALY_SIZE_H - TOWER_INIT_SKIP_H - WALL_SIZE_BOTTOM -
                        Q * j - (v[idx][1] + v[idx][6]),
                        v[idx][2], v[idx][3], v[idx][4],
                        v[idx][5], v[idx][6], v[idx][7]
                    )

        # 敵
        pyxel.load(self.load_path[1])
        for i in range(self.tower_num):
            T = len(self.tower_info[i])
            for j in range(T):
                t, b, m, idx = self.tower_info[i][j]
                if t == 1:
                    k = (pyxel.frame_count) // 25 % 2  # 一般には % len(u[idx])
                    tmp = (FLOOR_WALL_SIDE + u[idx][k][5]) / 2
                    if (self.fighter_now == i and self.on_fighting == j):
                        tmp = u[idx][k][5] + u[idx][k][0] + WALL_SIZE_SIDE

                    pyxel.text(
                        S * (i + 2) - tmp - slide,
                        DISPALY_SIZE_H - TOWER_INIT_SKIP_H - Q * (j + 1) + 2,
                        f"{self.text[b * 2 - 2]}{m}", 8
                    )
                    pyxel.blt(
                        S * (i + 2) - tmp - slide,
                        DISPALY_SIZE_H - TOWER_INIT_SKIP_H - WALL_SIZE_BOTTOM -
                        Q * j - (u[idx][k][1] + u[idx][k][6]),
                        u[idx][k][2], u[idx][k][3], u[idx][k][4],
                        u[idx][k][5], u[idx][k][6], u[idx][k][7]
                    )

    # ファイター
    def draw_fighter(self, slide, S, Q):
        # 撃退アニメーション
        u = (
            (
                (0, 1, 0, 32, 16, 32, 40, 5),
                (6, 1, 0, 32, 56, 32, 40, 5),
                (3, 1, 0, 64, 56, 40, 40, 5)
            ),
            (
                (2, 1, 0, 32, 16, 32, 40, 5),
                (-4, 1, 0, 28, 96, 35, 40, 5),
                (2, 1, 0, 63, 96, 45, 40, 5)
            )
        )

        # 武器入手アニメーション
        v = (
            (2, 1, 0, 32, 16, 32, 40, 5),
            (2, 1, 0, 32, 56, 32, 40, 5),
            (2, 1, 0, 64, 56, 40, 40, 5)
        )

        # 待機アニメーション
        w = (
            (18, 1, 0, 0, 16, 32, 40, 5),
            (18, 1, 0, 32, 16, 32, 40, 5)
        )

        pyxel.load(self.load_path[0])
        # 戦っているときのアニメーション
        if self.is_fighting:
            # 倒すときのアニメーション
            if self.tower_info[self.fighter_now][self.on_fighting][0] == 1:
                j = 1
                i = (pyxel.frame_count - self.fighting_time) // 10 % len(u[j])
                pyxel.blt(
                    S + TOWER_SKIP + WALL_SIZE_SIDE + u[j][i][0],
                    DISPALY_SIZE_H - TOWER_INIT_SKIP_H - WALL_SIZE_BOTTOM -
                    Q * self.on_fighting - (u[j][i][1] + u[j][i][6]),
                    u[j][i][2], u[j][i][3], u[j][i][4],
                    u[j][i][5], u[j][i][6], u[j][i][7]
                )

            # 武器などをとるときのアニメーション
            elif self.tower_info[self.fighter_now][self.on_fighting][0] == 2:
                i = (pyxel.frame_count - self.fighting_time) // 10 % len(v)
                pyxel.blt(
                    S + TOWER_SKIP + WALL_SIZE_SIDE + v[i][0],
                    DISPALY_SIZE_H - TOWER_INIT_SKIP_H - WALL_SIZE_BOTTOM -
                    Q * self.on_fighting - (v[i][1] + v[i][6]),
                    v[i][2], v[i][3], v[i][4],
                    v[i][5], v[i][6], v[i][7]
                )

        # 元の位置にいる
        else:
            # self.thinkingでいい感じ
            i = (pyxel.frame_count - self.thinking) // 20 % len(w)
            pyxel.blt(
                TOWER_SKIP + FLOOR_WALL_SIDE / 2 +
                self.fighter_now * S - slide - w[i][0],
                DISPALY_SIZE_H - TOWER_INIT_SKIP_H -
                WALL_SIZE_BOTTOM - (w[i][1] + w[i][6]),
                w[i][2], w[i][3], w[i][4],
                w[i][5], w[i][6], w[i][7]
            )

    def draw_number(self, x, y, t, b, m):
        gf = (
            (0.5, 0.5, 0, 80, 0, 7, 7, 5),
            (0.5, 0.5, 0, 80, 8, 7, 7, 5),
            (0.5, 0.5, 0, 88, 0, 7, 7, 5),
            (0.5, 0.5, 0, 88, 8, 7, 7, 5)
        )

        pow = 0
        while 10 ** pow <= m:
            pow += 1

        if t == 2:
            for i in range(pow + 1):
                if i == 0:
                    pyxel.blt(
                        x - (pow + 1) * 4 + gf[b - 1][0], y + gf[b - 1][1] + 1,
                        gf[b - 1][2], gf[b - 1][3], gf[b - 1][4],
                        gf[b - 1][5], gf[b - 1][6], gf[b - 1][7]
                    )
                    continue

                n = (m // (10 ** (pow - i)) + 9) % 10
                m %= (10 ** (pow - i))
                pyxel.blt(
                    x - (pow + 1) * 4 + 8 * i, y + 1, 0, 8 * n, 0, 8, 8, 5
                )

        # 色違い
        elif t == 1:
            for i in range(pow + 1):
                if i == 0:
                    pyxel.blt(
                        x - (pow + 1) * 4 + gf[b - 1][0], y + gf[b - 1][1] + 1,
                        gf[b - 1][2], gf[b - 1][3], gf[b - 1][4],
                        gf[b - 1][5], gf[b - 1][6], gf[b - 1][7]
                    )
                    continue

                n = (m // (10 ** (pow - i)) + 9) % 10
                m %= (10 ** (pow - i))
                pyxel.blt(
                    x - (pow + 1) * 4 + 8 * i, y + 1, 0, 8 * n, 0, 8, 8, 5
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
            "../assets/enemy.pyxres"
        )

        #
        self.problem_path = (
            "../assets/choimuzu.txt",
            "../assets/test_easy.txt"
        )

        #
        self.enemy_num = 7
        self.equip_num = 5

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
