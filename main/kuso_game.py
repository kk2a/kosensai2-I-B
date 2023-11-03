import pyxel
import sys

DISPALY_SIZE_W = 400 + 120 * 2
DISPALY_SIZE_H = 364

FLOOR_SIZE_W = 60
FLOOR_SIZE_H = 50
WALL_SIZE_BOTTOM = 8
WALL_SIZE_SIDE = 16
FLOOR_WALL_SIDE = 2 * WALL_SIZE_SIDE + FLOOR_SIZE_W
FLOOR_WALL_BOTTOM = WALL_SIZE_BOTTOM + FLOOR_SIZE_H
CEIL_HEIGHT = 98
BOSS_FLOOR_SIZE_W = 164
BOSS_FLOOR_SIZE_H = 144
BOSS_FLOOR_BOTTOM = 5
BOSS_WALL_SIZE_SIDE = 16

TOWER_SKIP = 40
TOWER_INIT_SKIP_H = 10

ENEMY_NUM = 7
EQUIP_NUM = 5

COL_DEATH = 0
COL_CLEAR = 7

DIFFICULTY_LIST = (
    "easy",
    "normal",
    "Caratheodory"
)

LOAD_PATH = (
    "../assets/fighter.pyxres",
    "../assets/enemy.pyxres",
    "../assets/bgm.json",
    "../assets/gameclear.pyxres",
    "../assets/gameover.pyxres"
)

difficult_receive = int(sys.stdin.read())
print(difficult_receive)
DIFFICULTY = DIFFICULTY_LIST[difficult_receive]
# DIFFICULTY = DIFFICULTY_LIST[2]
PROBLEM_NUMBER = -1

if DIFFICULTY == DIFFICULTY_LIST[2]:
    BOSS_FLOOR_SIZE_W = 204
    BOSS_FLOOR_SIZE_H = 132
    BOSS_FLOOR_BOTTOM = 5
    BOSS_WALL_SIZE_SIDE = 16


def load_bgm(msc, filename, snd1, snd2, snd3):
    import json

    with open(filename, "rt") as file:
        bgm = json.loads(file.read())
        pyxel.sound(snd1).set(*bgm[0])
        pyxel.sound(snd2).set(*bgm[1])
        pyxel.sound(snd3).set(*bgm[2])
        pyxel.music(msc).set([snd1], [snd2], [snd3], [])


class App:
    def __init__(self):
        pyxel.init(DISPALY_SIZE_W, DISPALY_SIZE_H, title="kuso game")
        pyxel.mouse(True)
        self.info()
        load_bgm(0, LOAD_PATH[2], 0, 1, 2)
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.fighter_now < self.tower_num:
            # slideを後にすることで1フレームだけ戻るということがなくなる!!!
            self.update_fighter(TOWER_SKIP + FLOOR_WALL_SIDE)
            self.update_slide(self.fighter_now *
                              (TOWER_SKIP + FLOOR_WALL_SIDE),
                              len(self.tower_info[self.fighter_now]))

    def draw(self):
        # おめでとう的なのをしたい
        if self.fighter_now >= self.tower_num:
            pyxel.cls(COL_CLEAR)
            pyxel.load(LOAD_PATH[3], image=True)
            u = (
                (0, 0, 0, 240, 48, 7),
                (-1, -1)
            )
            tmp = (DISPALY_SIZE_H - 48) / 2  # 48 = \sum_{i} u[i][4]
            for i in range(1):
                pyxel.blt((DISPALY_SIZE_W - u[i][3]) / 2, tmp + 32 * i,
                          u[i][0], u[i][1], u[i][2],
                          u[i][3], u[i][4], u[i][5])
                if pyxel.btnp(pyxel.KEY_Q):
                    pyxel.quit()
                if pyxel.btnp(pyxel.KEY_R):
                    self.info()
            return

        if not self.death:
            self.draw_back()
            self.draw_tower(self.left_slide,
                            TOWER_SKIP + FLOOR_WALL_SIDE,
                            FLOOR_WALL_BOTTOM)
            self.draw_equip(self.left_slide,
                            TOWER_SKIP + FLOOR_WALL_SIDE,
                            FLOOR_WALL_BOTTOM)
            if self.is_fighting:
                if (
                    self.fighter_now == self.tower_num - 1 and
                    not self.can_win_boss
                ):
                    self.draw_fighter(self.left_slide,
                                      TOWER_SKIP + FLOOR_WALL_SIDE,
                                      FLOOR_WALL_BOTTOM)
                    self.draw_enemy(self.left_slide,
                                    TOWER_SKIP + FLOOR_WALL_SIDE,
                                    FLOOR_WALL_BOTTOM)
                else:
                    self.draw_enemy(self.left_slide,
                                    TOWER_SKIP + FLOOR_WALL_SIDE,
                                    FLOOR_WALL_BOTTOM)
                    pyxel.load(LOAD_PATH[0], image=True)
                    self.draw_fighter(self.left_slide,
                                      TOWER_SKIP + FLOOR_WALL_SIDE,
                                      FLOOR_WALL_BOTTOM)
            else:
                self.draw_fighter(self.left_slide,
                                  TOWER_SKIP + FLOOR_WALL_SIDE,
                                  FLOOR_WALL_BOTTOM)
                self.draw_enemy(self.left_slide,
                                TOWER_SKIP + FLOOR_WALL_SIDE,
                                FLOOR_WALL_BOTTOM)
        else:
            pyxel.cls(col=COL_DEATH)
            # display_text.insert(1, f"{self.fighter_strength:04}")
            pyxel.load(LOAD_PATH[4], image=True)
            u = (
                (0, 0, 0, 256, 32, 1),
                (0, 0, 33, 96, 32, 1),
                (0, 0, 64, 96, 32, 1)
            )
            tmp = (DISPALY_SIZE_H - 32 * 3) / 2  # 32 * 3 = \sum_{i}u[i][4]
            for i in range(3):
                pyxel.blt((DISPALY_SIZE_W - u[i][3]) / 2, tmp + 32 * i,
                          u[i][0], u[i][1], u[i][2],
                          u[i][3], u[i][4], u[i][5])
                if pyxel.btnp(pyxel.KEY_Q):
                    pyxel.quit()
                if pyxel.btnp(pyxel.KEY_R):
                    self.info()

        # # debug
        # pyxel.text(50, 10, f"{pyxel.mouse_x}, {pyxel.mouse_y}", 0)
        # floor_idx = (DISPALY_SIZE_H - TOWER_INIT_SKIP_H -
        #              pyxel.mouse_y) // FLOOR_WALL_BOTTOM
        # pyxel.text(0, 0, f"{floor_idx}", 0)
        # pyxel.text(10, 10, f"{self.fighter_strength}", 0)
        # pyxel.text(10, 20, f"{self.passed}", 0)

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
        if self.is_fighting and (pyxel.frame_count - self.fighting_time) >= 30:
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

            # bad
            else:
                f = False

            # 戻る
            self.is_fighting = False
            self.thinking = pyxel.frame_count

            # ここでゲームオーバーだと思う
            if not f:
                self.on_fighting = -1
                self.death = True
                return

            # 成功
            self.tower_info[self.fighter_now][self.on_fighting] = 0, 0, 0, 0
            self.on_fighting = -1
            self.passed += 1

        elif (
            self.is_fighting and
            (pyxel.frame_count - self.fighting_time) == 22
        ):
            t = self.tower_info[self.fighter_now][self.on_fighting][0]
            pyxel.load(LOAD_PATH[0], sound=True)
            pyxel.play(3, t - 1)

        # クリックされたとき
        elif (
            pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and
            self.left_slide == self.fighter_now * S and
            not (self.is_fighting)
        ):
            if self.fighter_now == self.tower_num - 1:
                if (
                    pyxel.mouse_x >= TOWER_SKIP + S + 20 and
                    pyxel.mouse_x <= TOWER_SKIP + S + BOSS_FLOOR_SIZE_W -
                    20 and
                    pyxel.mouse_y <= DISPALY_SIZE_H - TOWER_INIT_SKIP_H and
                    pyxel.mouse_y >= DISPALY_SIZE_H - TOWER_INIT_SKIP_H -
                    BOSS_FLOOR_SIZE_H + 40
                ):
                    if self.tower_info[self.fighter_now][0][0] != 0:
                        self.is_fighting = True
                        self.on_fighting = 0
                        self.fighting_time = pyxel.frame_count
                        _, _, m, _ = self.tower_info[self.fighter_now][0]
                        if m <= self.fighter_strength:
                            self.can_win_boss = True
            elif (
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

    # 背景
    def draw_back(self):
        u = (
            (0, 0, 0, 0, 0, 256, 256),
            (256, 0, 0, 0, 0, 256, 256),
            (512, 0, 0, 0, 0, 128, 256),
            (0, 256, 0, 0, 0, 256, 108),
            (256, 256, 0, 0, 0, 256, 108),
            (512, 256, 0, 0, 0, 128, 108)
        )
        for i in range(6):
            pyxel.image(0).load(0, 0, f"../assets/back{i + 1}.png")
            pyxel.blt(u[i][0], u[i][1], u[i][2], u[i][3],
                      u[i][4], u[i][5], u[i][6])

    # 最後はボスにするかもしれないので確定ではない
    def draw_tower(self, slide, S, Q):
        # タワーの表示
        w = (
            (4, CEIL_HEIGHT, 0, 136, 0, 100, CEIL_HEIGHT, 5),
            (0, Q, 0, 140, 98, 92, 58, 5)
        )

        # タワーは最初
        pyxel.load(LOAD_PATH[0], image=True)
        idx = 0
        # 最初のタワー
        pyxel.blt(
            TOWER_SKIP - slide - w[idx][0], DISPALY_SIZE_H -
            TOWER_INIT_SKIP_H - w[idx][1], w[idx][2], w[idx][3], w[idx][4],
            w[idx][5], w[idx][6], w[idx][7]
        )
        pyxel.line(
            TOWER_SKIP - slide,
            DISPALY_SIZE_H - TOWER_INIT_SKIP_H - 1,
            TOWER_SKIP - slide + FLOOR_WALL_SIDE - 1,
            DISPALY_SIZE_H - TOWER_INIT_SKIP_H - 1,
            0
        )
        for i in range(self.tower_num - 1):
            T = len(self.tower_info[i])
            for j in range(T):
                # 最上階だけ特別
                idx = 1
                if j == T - 1:
                    idx = 0

                pyxel.blt(
                    TOWER_SKIP + S * (i + 1) - slide - w[idx][0],
                    DISPALY_SIZE_H - TOWER_INIT_SKIP_H - Q * j -
                    w[idx][1], w[idx][2], w[idx][3], w[idx][4],
                    w[idx][5], w[idx][6], w[idx][7]
                )

            pyxel.line(
                TOWER_SKIP + S * (i + 1) - slide,
                DISPALY_SIZE_H - TOWER_INIT_SKIP_H - 1,
                TOWER_SKIP + S * (i + 1) - slide + FLOOR_WALL_SIDE - 1,
                DISPALY_SIZE_H - TOWER_INIT_SKIP_H - 1,
                0
            )

        if DIFFICULTY == DIFFICULTY_LIST[2]:
            pyxel.blt(
                TOWER_SKIP + S * self.tower_num - slide,
                DISPALY_SIZE_H - TOWER_INIT_SKIP_H - BOSS_FLOOR_SIZE_H,
                2, 40, 125, BOSS_FLOOR_SIZE_W, BOSS_FLOOR_SIZE_H, 5
            )
        else:
            pyxel.blt(
                TOWER_SKIP + S * self.tower_num - slide,
                DISPALY_SIZE_H - TOWER_INIT_SKIP_H - BOSS_FLOOR_SIZE_H,
                1, 88, 112, BOSS_FLOOR_SIZE_W, BOSS_FLOOR_SIZE_H, 5
            )

    # 武器
    def draw_equip(self, slide, S, Q):
        # 武器の表示
        v = (
            (9, 1, 0, 0, 216, 16, 24, 5),
            (9, 1, 0, 24, 216, 16, 24, 5),
            (9, 1, 0, 48, 216, 16, 24, 5),
            (9, 1, 0, 96, 208, 16, 33, 5),
            (9, 1, 0, 112, 208, 16, 33, 5)
        )

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
    def draw_enemy(self, slide, S, Q):
        # 敵のアニメーション
        u = (
            ((3, 1, 0, 0, 0, 24, 32, 15), (3, 1, 0, 32, 0, 24, 32, 15)),
            ((6, 3, 0, 0, 32, 24, 16, 15), (6, 3, 0, 32, 32, 24, 16, 15)),
            ((11, 4, 0, 0, 59, 12, 10, 15), (11, 4, 0, 16, 59, 12, 10, 15)),
            ((3, 1, 0, 3, 73, 26, 30, 15), (3, 1, 0, 35, 73, 26, 30, 15)),
            ((6, 1, 0, 0, 104, 24, 32, 15), (6, 1, 0, 32, 104, 24, 32, 15)),
            ((3, 1, 0, 0, 143, 26, 33, 15), (3, 1, 0, 32, 143, 26, 33, 15)),
            ((2, 1, 0, 56, 0, 32, 24, 15), (2, 1, 0, 88, 0, 32, 24, 15)),
            ((0, 1, 0, 191, 101, 53, 58, 15),
             (0, 1, 1, 191, 103, 53, 56, 15)),
            ((10, 1, 0, 191, 101, 53, 58, 15),
             (10, 1, 1, 201, 164, 45, 60, 15),
             (10, 1, 0, 191, 168, 57, 53, 15)),
            ((10, 1, 0, 191, 101, 53, 58, 15),
             (10, 1, 1, 201, 164, 45, 60, 15),
             (10, 1, 2, 184, 169, 62, 55, 15)),
            ((20, 15, 0, 160, 3, 88, 93, 15),
             (20, 12, 1, 160, 3, 88, 93, 15)),
            ((-5, 0, 0, 160, 3, 88, 93, 15),
             (-5, 1, 2, 27, 3, 93, 93, 15),
             (-5, 0, 2, 28, 101, 90, 91, 15)),
            ((-10, 0, 0, 160, 3, 88, 93, 15),
             (-10, 1, 2, 27, 3, 93, 93, 15),
             (0, 0, 2, 136, 3, 102, 93, 15))
        )

        pyxel.load(LOAD_PATH[1], image=True)
        for i in range(self.tower_num - 1):
            T = len(self.tower_info[i])
            for j in range(T):
                t, b, m, idx = self.tower_info[i][j]
                if t == 1:
                    k = (pyxel.frame_count) // 25 % 2  # 一般には % len(u[idx])
                    tmp = (FLOOR_WALL_SIDE + u[idx][k][5]) / 2
                    if (self.fighter_now == i and self.on_fighting == j):
                        tmp = u[idx][k][5] + u[idx][k][0] + WALL_SIZE_SIDE

                    self.draw_number(
                        S * (i + 2) - tmp + u[idx][k][5] / 2 - slide,
                        DISPALY_SIZE_H - TOWER_INIT_SKIP_H - Q * (j + 1),
                        t, b, m
                    )

                    pyxel.blt(
                        S * (i + 2) - tmp - slide,
                        DISPALY_SIZE_H - TOWER_INIT_SKIP_H - WALL_SIZE_BOTTOM -
                        Q * j - (u[idx][k][1] + u[idx][k][6]),
                        u[idx][k][2], u[idx][k][3], u[idx][k][4],
                        u[idx][k][5], u[idx][k][6], u[idx][k][7]
                    )

        i = self.tower_num - 1
        j = 0
        t, b, m, idx = self.tower_info[i][j]
        if not (
            self.on_fighting == 0 and
            self.fighter_now == self.tower_num - 1
        ):
            k = (pyxel.frame_count) // 25 % 2  # 一般には % len(u[idx])
            # 変わる
            idx = 10 if DIFFICULTY == DIFFICULTY_LIST[2] else 7
            tmp = (BOSS_FLOOR_SIZE_W + u[idx][k][5]) / 2
            self.draw_number(
                S * (i + 1) + TOWER_SKIP + BOSS_FLOOR_SIZE_W - tmp - slide +
                u[idx][k][5] / 2,
                DISPALY_SIZE_H - TOWER_INIT_SKIP_H - BOSS_FLOOR_BOTTOM -
                (u[idx][k][1] + u[idx][k][6]) - 15,
                t, b, m
            )
            pyxel.blt(
                S * (i + 1) + TOWER_SKIP + BOSS_FLOOR_SIZE_W - tmp - slide +
                u[idx][k][0],
                DISPALY_SIZE_H - TOWER_INIT_SKIP_H - BOSS_FLOOR_BOTTOM + 1 -
                (u[idx][k][1] + u[idx][k][6]),
                u[idx][k][2], u[idx][k][3], u[idx][k][4],
                u[idx][k][5], u[idx][k][6], u[idx][k][7]
            )
        else:
            k = (pyxel.frame_count - self.fighting_time) // 10 % 3
            if DIFFICULTY == DIFFICULTY_LIST[2]:
                # 変わる
                idx = 11 if self.can_win_boss else 12
            else:
                idx = 8 if self.can_win_boss else 9
            tmp = u[idx][k][5] + u[idx][k][0] + BOSS_WALL_SIZE_SIDE + 10
            self.draw_number(
                S * (i + 1) + TOWER_SKIP + BOSS_FLOOR_SIZE_W - tmp - slide +
                u[idx][k][5] / 2,
                DISPALY_SIZE_H - TOWER_INIT_SKIP_H - BOSS_FLOOR_BOTTOM -
                (u[idx][k][1] + u[idx][k][6]) - 15,
                t, b, m
            )
            pyxel.blt(
                S * (i + 1) + TOWER_SKIP + BOSS_FLOOR_SIZE_W - tmp - slide,
                DISPALY_SIZE_H - TOWER_INIT_SKIP_H - BOSS_FLOOR_BOTTOM + 1 -
                (u[idx][k][1] + u[idx][k][6]),
                u[idx][k][2], u[idx][k][3], u[idx][k][4],
                u[idx][k][5], u[idx][k][6], u[idx][k][7]
            )

    # ファイター
    def draw_fighter(self, slide, S, Q):
        # 撃退アニメーション
        u = (
            (
                (-20, 1, 0, 32, 16, 32, 40, 5),
                (-13, 1, 0, 32, 56, 32, 40, 5),
                (10, 1, 0, 64, 56, 40, 40, 5)
            ),
            (
                (2, 1, 0, 32, 16, 32, 40, 5),
                (-4, 1, 0, 28, 96, 35, 40, 5),
                (2, 1, 0, 63, 96, 45, 40, 5)
            ),
            (
                (-15, 1, 0, 32, 16, 32, 40, 5),
                (-19, 1, 0, 28, 96, 35, 40, 5),
                (-18, 1, 0, 35, 152, 31, 32, 5)
            ),
            (
                (-25, 1, 0, 32, 16, 32, 40, 5),
                (-29, 1, 0, 28, 96, 35, 40, 5),
                (-28, 1, 0, 35, 152, 31, 32, 5)
            ),
            (
                (-27, 1, 0, 32, 16, 32, 40, 5),
                (-20, 1, 0, 32, 56, 32, 40, 5),
                (10, 1, 0, 64, 56, 40, 40, 5)
            ),
        )

        # 武器入手アニメーション
        v = (
            (2, 1, 0, 0, 16, 32, 40, 5),
            (2, 1, 0, 32, 16, 32, 40, 5),
            (6, 2, 0, 5, 142, 27, 66, 5)
        )

        # 待機アニメーション
        w = (
            (18, 1, 0, 0, 16, 32, 40, 5),
            (18, 1, 0, 32, 16, 32, 40, 5)
        )

        # 戦っているときのアニメーション
        if self.is_fighting:
            # 倒すときのアニメーション
            if self.fighter_now == self.tower_num - 1:
                i = self.tower_num - 1
                j = 0
                k = (pyxel.frame_count - self.fighting_time) // 10 % 3
                idx = 0 if self.can_win_boss else 2
                if DIFFICULTY == DIFFICULTY_LIST[2]:
                    idx = 4 if self.can_win_boss else 3
                tmp = BOSS_FLOOR_SIZE_W / 2 - u[idx][k][5]
                self.draw_number(
                    S + TOWER_SKIP + BOSS_WALL_SIZE_SIDE + tmp
                    + u[idx][k][5] / 2 + u[idx][k][0],
                    DISPALY_SIZE_H - TOWER_INIT_SKIP_H - BOSS_FLOOR_BOTTOM -
                    u[idx][k][6] - 10,
                    1, -1, self.fighter_strength
                )
                pyxel.blt(
                    S + TOWER_SKIP + BOSS_WALL_SIZE_SIDE + tmp + u[idx][k][0],
                    DISPALY_SIZE_H - TOWER_INIT_SKIP_H - BOSS_FLOOR_BOTTOM +
                    1 - (u[idx][k][1] + u[idx][k][6]),
                    u[idx][k][2], u[idx][k][3], u[idx][k][4],
                    u[idx][k][5], u[idx][k][6], u[idx][k][7]
                )
            elif self.tower_info[self.fighter_now][self.on_fighting][0] == 1:
                j = 1
                i = (pyxel.frame_count - self.fighting_time) // 10 % len(u[j])

                self.draw_number(
                    S + TOWER_SKIP + WALL_SIZE_SIDE + u[j][i][0] +
                    u[j][i][5] / 2, DISPALY_SIZE_H - TOWER_INIT_SKIP_H -
                    Q * (self.on_fighting + 1), 2, -1, self.fighter_strength
                )

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

                self.draw_number(
                    S + TOWER_SKIP + WALL_SIZE_SIDE + v[i][0] +
                    v[i][5] / 2, DISPALY_SIZE_H - TOWER_INIT_SKIP_H -
                    Q * (self.on_fighting + 1), 2, -1, self.fighter_strength
                )

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

            self.draw_number(
                TOWER_SKIP + FLOOR_WALL_SIDE / 2 + self.fighter_now * S -
                slide, DISPALY_SIZE_H - TOWER_INIT_SKIP_H - Q,
                2, -1, self.fighter_strength
            )

            pyxel.blt(
                TOWER_SKIP + FLOOR_WALL_SIDE / 2 +
                self.fighter_now * S - slide - w[i][0],
                DISPALY_SIZE_H - TOWER_INIT_SKIP_H -
                WALL_SIZE_BOTTOM - (w[i][1] + w[i][6]),
                w[i][2], w[i][3], w[i][4],
                w[i][5], w[i][6], w[i][7]
            )

    # 数字を表示
    # センタリングしたいので、xは真ん中を渡す
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

        if b == -1:
            for i in range(pow):
                n = (m // (10 ** (pow - 1 - i)) + 9) % 10
                m %= (10 ** (pow - 1 - i))
                pyxel.blt(
                    x - pow * 4 + 8 * i, y + 1, 0, 8 * n, 0, 8, 8, 5
                )
            return

        if t == 2:
            tmp = 0
            for i in range(pow + 1):
                if i == 0:
                    tmpx = gf[b - 1][3]
                    tmpy = gf[b - 1][4]
                    if b in [2, 4]:
                        tmpx -= 80
                        tmpy += 8
                        tmp = 1
                    pyxel.blt(
                        x - (pow + 1) * 4 + gf[b - 1][0], y + gf[b - 1][1] + 1,
                        tmp, tmpx, tmpy, gf[b - 1][5],
                        gf[b - 1][6], gf[b - 1][7]
                    )
                    continue

                n = (m // (10 ** (pow - i)) + 9) % 10
                m %= (10 ** (pow - i))
                pyxel.blt(
                    x - (pow + 1) * 4 + 8 * i, y + 1, tmp, 8 * n, 0, 8, 8, 5
                )

        # 色違い
        elif t == 1:
            for i in range(pow):
                n = (m // (10 ** (pow - 1 - i)) + 9) % 10
                m %= (10 ** (pow - 1 - i))
                pyxel.blt(
                    x - pow * 4 + 8 * i, y + 1, 1, 8 * n, 0, 8, 8, 5
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
        self.death = False

        #
        self.can_win_boss = False

        # テキストから問題を読み込む
        with open(f"../problem/{DIFFICULTY}/{PROBLEM_NUMBER}.txt") as f:
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
                        b.append(pyxel.rndi(0, ENEMY_NUM - 1))
                    else:
                        b.append(pyxel.rndi(0, EQUIP_NUM - 1))
                    a.append(b)
                self.tower_info.append(a)
            self.max_strength = int(f.readline().rstrip())


App()
