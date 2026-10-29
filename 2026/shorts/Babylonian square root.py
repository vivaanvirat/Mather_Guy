from manim import *

# ==============================================================
#  THE NEWTON–GREGORY METHOD  —  Shorts / Reels edition (9:16)
#  "The fixed-point trick for square roots"
#
#  Render (60 fps, ~60 s):
#      manim -qh newton_gregory_shorts.py NewtonGregoryShort
#
#  Needs:  pip install manim   (Manim Community v0.18+)
#          plus a LaTeX distribution (MathTex requires it)
#
#  Structure:
#    1. Title card
#    2. The setup      (r, g_0, and the averaging formula)
#    3. The key idea   (if g_n = root, then g_{n+1} = g_n — solved live)
#    4. The nudge      (one factor too high, one too low → closer)
#    5. How fast       (1 → ~4 → ~10 → ~23 decimals in 4 steps)
#    6. Like / Subscribe / Share outro
# ==============================================================

# ---- vertical canvas: 1080 x 1920 ----------------------------
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9.0
config.frame_height = 16.0

# ---- palette -------------------------------------------------
ACCENT = "#FFD166"   # warm yellow
FORMULA = "#7EE0E3"  # teal
GOOD = "#06D6A0"     # green
ORANGE = "#FF9F45"   # new-guess orange
HOT = "#FF4E6A"     # red (subscribe)
INK = "#F5F7FA"      # main text
MUTED = "#8FA3BF"    # secondary text
BG = "#0B0F1A"       # background


def fit(m: Mobject, max_width: float = 8.4) -> Mobject:
    """Shrink a mobject if it is wider than the vertical frame."""
    if m.width > max_width:
        m.width = max_width
    return m


class NewtonGregoryShort(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.title_card()
        self.wipe()
        self.setup_lines()
        self.wipe()
        self.proof()
        self.wipe()
        self.nudge()
        self.wipe()
        self.speed()
        self.wipe()
        self.outro()

    def wipe(self):
        """Fade out everything on stage between sections."""
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # ==========================================================
    # 1. TITLE  (0:00 - 0:06)
    # ==========================================================
    def title_card(self):
        kicker = Text("MATH SHORTS", font_size=28, weight=BOLD, color=ACCENT)
        title = VGroup(
            Text("The Newton–Raphson", font_size=46, weight=BOLD, color=INK),
            Text("Method", font_size=46, weight=BOLD, color=INK),
        ).arrange(DOWN, buff=0.15)
        aka = Text("a.k.a. Newton–Raphson", font_size=24, color=MUTED, slant=ITALIC)
        hero = MathTex(r"\sqrt{x}", font_size=110, color=ACCENT)
        sub = Text("…with no calculator", font_size=30, color=MUTED)

        VGroup(kicker, title, aka, hero, sub).arrange(DOWN, buff=0.5)

        self.play(FadeIn(kicker, shift=0.3 * UP))
        self.play(Write(title), run_time=1)
        #self.play(FadeIn(aka, shift=0.2 * UP))
        self.play(FadeIn(hero, scale=0.5), run_time=0.8)
        self.play(FadeIn(sub))
        self.wait(0.5)

    # ==========================================================
    # 2. THE SETUP  (0:06 - 0:16)
    # ==========================================================
    def setup_lines(self):
        head = Text("THE SETUP", font_size=36, weight=BOLD, color=ACCENT)
        head.to_edge(UP, buff=0.7)

        r_line = VGroup(
            MathTex(r"r", font_size=48, color=ACCENT),
            Text("= the number you're rooting", font_size=30, color=MUTED),
        ).arrange(RIGHT, buff=0.3)
        g_line = VGroup(
            MathTex(r"g_0", font_size=48, color=ACCENT),
            Text("= closest guess you can make", font_size=30, color=MUTED),
        ).arrange(RIGHT, buff=0.3)
        defs = VGroup(r_line, g_line).arrange(DOWN, buff=0.5)
        defs.next_to(head, DOWN, buff=0.8)

        formula = MathTex(r"g_{n+1} = \frac{1}{2}\left(g_n + \frac{r}{g_n}\right)",
                          font_size=54, color=INK)
        formula.move_to(DOWN * 1.2)
        box = SurroundingRectangle(formula, color=ACCENT, buff=0.3)
        cap = Text("average your guess  with  r ÷ guess",
                   font_size=28, color=INK)
        cap.next_to(formula, DOWN, buff=1.0)

        self.play(FadeIn(head, shift=0.3 * UP))
        self.play(FadeIn(r_line, shift=0.2 * UP))
        self.play(FadeIn(g_line, shift=0.2 * UP))
        self.wait(0.5)
        self.play(Write(formula), run_time=1.0)
        self.play(Create(box))
        self.play(FadeIn(cap))
        self.wait(1.2)

    # ==========================================================
    # 3. THE KEY IDEA  (0:16 - 0:32)
    #    Assume g_n is the root — watch the formula agree.
    # ==========================================================
    def proof(self):
        head = Text("THE KEY IDEA", font_size=36, weight=BOLD, color=ACCENT)
        head.to_edge(UP, buff=0.7)
        sup = Text("pretend your guess is already perfect:  g = √r",
                   font_size=28, color=MUTED)
        sup.next_to(head, DOWN, buff=0.5)

        l1 = MathTex(r"g_{n+1} = \frac{1}{2}\left(g_n + \frac{r}{g_n}\right)",
                     font_size=44, color=INK)
        l1.move_to(UP * 0.8)
        c1 = Text("now swap in  g_n = √r", font_size=28, color=MUTED)
        c1.next_to(l1, DOWN, buff=0.5)

        l2 = MathTex(r"g_{n+1} = \frac{1}{2}\left(\sqrt{r} + \frac{r}{\sqrt{r}}\right)",
                     font_size=44, color=INK)
        l2.move_to(l1)
        c2 = Text("and  r ÷ √r  =  √r", font_size=28, color=MUTED)
        c2.next_to(l2, DOWN, buff=0.5)

        l3 = MathTex(r"g_{n+1} = \frac{1}{2}\left(\sqrt{r} + \sqrt{r}\right)",
                     font_size=44, color=INK)
        l3.move_to(l2)

        l4 = MathTex(r"g_{n+1} = \frac{1}{2} \cdot 2\sqrt{r} = \sqrt{r}",
                     font_size=44, color=GOOD)
        l4.move_to(l3)

        final = MathTex(r"g_{n+1} = g_n", font_size=64, color=GOOD)
        final.move_to(DOWN * 2.4)
        fbox = SurroundingRectangle(final, color=GOOD, buff=0.3)
        fcap = Text("the perfect root is a fixed point ✓",
                    font_size=28, color=MUTED)
        fcap.next_to(fbox, DOWN, buff=0.5)

        self.play(FadeIn(head, shift=0.3 * UP), FadeIn(sup, shift=0.2 * UP))
        self.play(Write(l1), run_time=0.8)
        self.play(FadeIn(c1))
        self.wait(0.5)
        self.play(FadeTransform(l1, l2), FadeTransform(c1, c2))
        self.wait(0.7)
        self.play(FadeTransform(l2, l3), run_time=0.7)
        self.wait(0.5)
        self.play(FadeTransform(l3, l4), run_time=0.7)
        self.wait(0.6)
        self.play(FadeOut(c2))
        self.play(Write(final), run_time=0.8)
        self.play(Create(fbox))
        self.play(FadeIn(fcap))
        self.wait(1.4)

    # ==========================================================
    # 4. THE NUDGE  (0:32 - 0:45)
    # ==========================================================
    def nudge(self):
        head = Text("SO IT NUDGES YOU CLOSER", font_size=36, weight=BOLD,
                    color=ACCENT)
        head.to_edge(UP, buff=0.7)

        big = MathTex(r"g_n > \sqrt{r} \;\Longrightarrow\; \frac{r}{g_n} < \sqrt{r}",
                      font_size=38, color=INK)
        small = MathTex(r"g_n < \sqrt{r} \;\Longrightarrow\; \frac{r}{g_n} > \sqrt{r}",
                        font_size=38, color=INK)
        lines = VGroup(big, small).arrange(DOWN, buff=0.4)
        lines.next_to(head, DOWN, buff=0.7)

        hint = Text("one factor too big, one too small…",
                    font_size=26, color=MUTED)
        hint.next_to(lines, DOWN, buff=0.5)

        # live example:  r = 2, guess g = 2
        # (hand-built number line — no NumberLine API, works on every version)
        ex = Text("example:  r = 2,  g = 2", font_size=28,
                  weight=BOLD, color=ACCENT)
        ex.next_to(hint, DOWN, buff=0.6)
        nl = Line(LEFT * 4.0, RIGHT * 4.0,
                  stroke_color="#445677", stroke_width=3)
        nl.move_to(DOWN * 2.2)

        def n2p(x):
            """map data x in [0, 3] to a point on the line"""
            return nl.get_start() + (x / 3.0) * (nl.get_end() - nl.get_start())

        g_dot = Dot(n2p(2), radius=0.13, color=ACCENT)
        g_lab = MathTex(r"g = 2", font_size=32, color=ACCENT)
        g_lab.next_to(g_dot, UP, buff=0.4)

        rg_dot = Dot(n2p(1), radius=0.13, color=FORMULA)
        rg_lab = MathTex(r"\frac{r}{g} = 1", font_size=32, color=FORMULA)
        rg_lab.next_to(rg_dot, UP, buff=0.4)

        avg_dot = Dot(n2p(1.5), radius=0.13, color=ORANGE)
        avg_lab = MathTex(r"\frac{g + r/g}{2} = 1.5", font_size=32, color=ORANGE)
        avg_lab.next_to(avg_dot, UP, buff=1.15)

        root_dot = Dot(n2p(1.4142), radius=0.13, color=GOOD)
        root_lab = MathTex(r"\sqrt{2} \approx 1.414", font_size=32, color=GOOD)
        root_lab.next_to(root_dot, DOWN, buff=0.5)

        cap = Text("the average lands between them — closer to √r",
                   font_size=26, color=INK)
        cap.next_to(nl, DOWN, buff=1.8)

        self.play(FadeIn(head, shift=0.3 * UP))
        self.play(Write(big), run_time=0.8)
        self.play(Write(small), run_time=0.8)
        self.play(FadeIn(hint))
        self.wait(0.4)

        self.play(Create(nl), FadeIn(ex), run_time=0.8)
        self.play(FadeIn(g_dot, scale=0.4), FadeIn(g_lab))
        self.play(FadeIn(rg_dot, scale=0.4), FadeIn(rg_lab))
        self.play(FadeIn(avg_dot, scale=0.4), FadeIn(avg_lab))
        self.play(Flash(n2p(1.5), color=ORANGE, flash_radius=0.4))
        self.play(FadeIn(root_dot, scale=0.4), FadeIn(root_lab))
        self.play(Indicate(root_dot, scale_factor=2.2), FadeIn(cap))
        self.wait(1.2)

    # ==========================================================
    # 5. HOW FAST?  (0:45 - 0:57)
    # ==========================================================
    def speed(self):
        head = Text("HOW FAST?", font_size=38, weight=BOLD, color=ACCENT)
        head.to_edge(UP, buff=0.7)
        intro = Text("each step roughly squares your error —", font_size=30,
                     color=MUTED)
        intro.next_to(head, DOWN, buff=0.6)

        rows = [
            Text("1st iteration  →  1 decimal", font_size=32,
                 color=INK, t2c={"1 decimal": GOOD}),
            Text("2nd iteration  →  ~4 decimals", font_size=32,
                 color=INK, t2c={"~4 decimals": GOOD}),
            Text("3rd iteration  →  ~10 decimals", font_size=32,
                 color=INK, t2c={"~10 decimals": GOOD}),
            Text("4th iteration  →  ~23 decimals", font_size=32,
                 color=INK, t2c={"~23 decimals": GOOD}),
        ]
        for r in rows:
            fit(r, 8.2)
        rows_g = VGroup(*rows).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        rows_g.next_to(intro, DOWN, buff=0.8)

        punch = Text("…calculator-beating precision, from ONE guess!",
                     font_size=30, weight=BOLD, color=ACCENT)
        fit(punch, 8.2)
        punch.next_to(rows_g, DOWN, buff=0.9)

        self.play(FadeIn(head, shift=0.3 * UP))
        self.play(FadeIn(intro))
        for r in rows:
            self.play(FadeIn(r, shift=0.25 * UP), run_time=0.45)
            self.wait(0.35)
        self.play(Circumscribe(rows[3], color=GOOD), run_time=0.9)
        self.play(FadeIn(punch, shift=0.2 * UP))
        self.wait(1.5)

    # ==========================================================
    # 6. OUTRO: like, subscribe, share  (0:57 - 1:04)
    # ==========================================================
    def outro(self):
        thanks = Text("Thanks for watching!", font_size=42,
                       weight=BOLD, color=INK)
        sub = Text("More 60-second math, every week",
                   font_size=26, color=MUTED)

        like = self.button("LIKE", GOOD)
        subs = self.button("SUBSCRIBE", HOT)
        share = self.button("SHARE", ACCENT)
        row = VGroup(like, subs, share).arrange(RIGHT, buff=0.35)

        VGroup(thanks, sub, row).arrange(DOWN, buff=0.8)

        self.play(FadeIn(thanks, shift=0.3 * UP))
        self.play(FadeIn(sub))
        for b in (like, subs, share):
            self.play(FadeIn(b, scale=0.6), run_time=0.35)
        self.play(row.animate(rate_func=there_and_back).scale(1.12),
                  run_time=0.9)
        self.play(row.animate(rate_func=there_and_back).scale(1.12),
                  run_time=0.9)
        self.wait(1.5)

    def button(self, label, color):
        box = RoundedRectangle(corner_radius=0.32, width=2.45, height=0.8,
                               fill_color=color, fill_opacity=1.0,
                               stroke_width=0)
        txt = Text(label, font_size=24, weight=BOLD, color=BG)
        return VGroup(box, txt)