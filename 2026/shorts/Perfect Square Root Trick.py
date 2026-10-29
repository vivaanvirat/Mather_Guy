"""
MENTAL MATH SHORT — randomized square roots of perfect squares
Vertical 9:16 "Shorts" video built with Manim Community Edition.

REQUIREMENTS
    pip install manim          (Manim CE) + a LaTeX distribution (MiKTeX/TeX Live)

RENDER
    manim -pqh main.py MentalMathShort

NOTES
    - Each render chooses a random 2-digit root with random.randint.
    - Set SEED to an integer if you want a reproducible render.
    - The video is shortened to roughly 30-45 seconds.
    - Only the relevant tens bracket is shown.
    - If the square ending gives two possible last digits, the scene
      compares against (tens digit followed by 5)^2 to choose the correct one.
"""

from manim import *
import random


# ---------------------------------------------------------------------------
# Shorts (9:16 vertical) render configuration
# ---------------------------------------------------------------------------
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9.0
config.frame_height = 16.0
config.frame_rate = 30
config.background_color = "#0B1220"

ACCENT = "#FFD166"   # yellow
CYAN   = "#4CC9F0"
PINK   = "#EF476F"
GREEN  = "#06D6A0"
REDX   = "#FF5C7A"
CARD   = "#151E31"


# ---------------------------------------------------------------------------
# Random perfect square selection
# ---------------------------------------------------------------------------
# Set SEED = 123, for example, to reproduce the same video.
# Keep SEED = None for a different number on every render.
SEED = None
if SEED is not None:
    random.seed(SEED)


def random_root():
    """
    Pick a random 2-digit root whose square is 4 digits.
    Avoid roots ending in 0 because their square ending is not ambiguous
    and is less interesting for this trick.
    """
    while True:
        r = random.randint(32, 99)
        if r % 10 != 0:
            return r


ROOT = random_root()
N = ROOT * ROOT

TENS = ROOT // 10
ONES = ROOT % 10

LOW = TENS * 10
HIGH = LOW + 10

LOW_SQ = LOW * LOW
HIGH_SQ = HIGH * HIGH

# The midpoint between the two possible roots is always the tens digit + 5.
# Example: if candidates are 43 and 47, the midpoint is 45.
MID_ROOT = LOW + 5
MID_SQ = MID_ROOT * MID_ROOT

LAST = N % 10

# Possible ones digits of a square root, based on the square's last digit.
ONES_MAP = {
    0: [0],
    1: [1, 9],
    4: [2, 8],
    5: [5],
    6: [4, 6],
    9: [3, 7],
}

OPTIONS = sorted(ONES_MAP[LAST])
AMBIGUOUS = len(OPTIONS) == 2

if AMBIGUOUS:
    CHOICE_HIGH = N > MID_SQ
    CHOSEN_ONES = OPTIONS[1] if CHOICE_HIGH else OPTIONS[0]
    CAND_LOW = LOW + OPTIONS[0]
    CAND_HIGH = LOW + OPTIONS[1]
else:
    CHOSEN_ONES = OPTIONS[0]


# ---------------------------------------------------------------------------
# Small builders
# ---------------------------------------------------------------------------
def pill(text, color, fs=32):
    """Solid rounded pill with bold centered text."""
    txt = Text(text, weight=BOLD, font_size=fs, color=WHITE)
    rect = RoundedRectangle(
        corner_radius=0.32,
        width=txt.width + 0.7,
        height=txt.height + 0.5,
        fill_color=color,
        fill_opacity=1,
        stroke_width=0,
    )
    txt.move_to(rect)
    return VGroup(rect, txt)


def step_banner(step, msg, color):
    p = pill(step, color, fs=28)
    t = Text(msg, weight=BOLD, font_size=40, color=WHITE)
    return VGroup(p, t).arrange(RIGHT, buff=0.45)


def build_hud():
    """Bottom answer HUD: sqrt(N) = [tens][ones]"""
    eq = MathTex(rf"\sqrt{{{N}}};=;", font_size=72)

    s1 = RoundedRectangle(
        corner_radius=0.2,
        width=1.25,
        height=1.6,
        stroke_color=ACCENT,
        stroke_width=4,
        fill_color=WHITE,
        fill_opacity=0.08,
    )

    s2 = RoundedRectangle(
        corner_radius=0.2,
        width=1.25,
        height=1.6,
        stroke_color=GREEN,
        stroke_width=4,
        fill_color=WHITE,
        fill_opacity=0.08,
    )

    c1 = Text("TENS", font_size=26, weight=BOLD, color=GREY_B)
    c2 = Text("ONES", font_size=26, weight=BOLD, color=GREY_B)

    s1.next_to(eq, RIGHT, buff=0.4)
    s2.next_to(s1, RIGHT, buff=0.4)

    c1.next_to(s1, DOWN, buff=0.18)
    c2.next_to(s2, DOWN, buff=0.18)

    hud = VGroup(eq, s1, s2, c1, c2).move_to([0, -6.0, 0])
    return hud, s1, s2


# ---------------------------------------------------------------------------
# End-card icons
# ---------------------------------------------------------------------------
def thumb_icon(color):
    cuff = RoundedRectangle(
        corner_radius=0.05,
        width=0.34,
        height=0.62,
        fill_color=color,
        fill_opacity=1,
        stroke_width=0,
    ).move_to([-0.36, -0.05, 0])

    hand = Polygon(
        [-0.08, -0.36, 0],
        [0.58, -0.36, 0],
        [0.58, -0.02, 0],
        [0.40, 0.05, 0],
        [0.54, 0.38, 0],
        [0.36, 0.46, 0],
        [0.22, 0.12, 0],
        [-0.08, 0.12, 0],
        fill_color=color,
        fill_opacity=1,
        stroke_width=0,
    )

    return VGroup(cuff, hand)


def bell_icon(color):
    dome = Arc(
        radius=0.24,
        start_angle=0,
        angle=PI,
        arc_center=[0, 0.10, 0],
        color=color,
        stroke_width=7,
    )

    skirt = Polygon(
        [-0.24, 0.10, 0],
        [0.24, 0.10, 0],
        [0.17, -0.18, 0],
        [-0.17, -0.18, 0],
        fill_color=color,
        fill_opacity=1,
        stroke_width=0,
    )

    rim = RoundedRectangle(
        corner_radius=0.04,
        width=0.60,
        height=0.09,
        fill_color=color,
        fill_opacity=1,
        stroke_width=0,
    ).move_to([0, -0.20, 0])

    knob = Circle(
        radius=0.055,
        color=color,
        fill_color=color,
        fill_opacity=1,
    ).move_to([0, 0.37, 0])

    clapper = Circle(
        radius=0.07,
        color=color,
        fill_color=color,
        fill_opacity=1,
    ).move_to([0, -0.34, 0])

    return VGroup(dome, skirt, rim, knob, clapper)


def share_icon(color):
    return Polygon(
        [0.42, 0.06, 0],
        [-0.34, 0.38, 0],
        [-0.08, 0.06, 0],
        [-0.34, -0.26, 0],
        fill_color=color,
        fill_opacity=1,
        stroke_width=0,
    )


def action_button(label, icon, color):
    rect = RoundedRectangle(
        corner_radius=0.5,
        width=4.4,
        height=1.0,
        fill_color=CARD,
        fill_opacity=1,
        stroke_color=color,
        stroke_width=4,
    )
    txt = Text(label, weight=BOLD, font_size=36, color=WHITE)
    inner = VGroup(icon, txt).arrange(RIGHT, buff=0.4)
    inner.move_to(rect)
    return VGroup(rect, inner)


# ---------------------------------------------------------------------------
# The scene
# ---------------------------------------------------------------------------
class MentalMathShort(Scene):
    def _play(self, *args, rt=1.0, **kwargs):
        self.play(*args, run_time=rt, **kwargs)
        self.t += rt

    def _sync(self, target):
        """Hold until the scene clock reaches a voiceover/timeline timestamp."""
        if target > self.t + 1e-9:
            self.wait(target - self.t)
            self.t = float(target)

    def construct(self):
        self.t = 0.0

        # ====================================================================
        # Hook
        # ====================================================================
        header = pill("MENTAL MATH TRICK", CYAN, fs=26).move_to([0, 7.0, 0])

        t1 = Text("Square root of a BIG number…", font_size=36)
        t2a = Text("…in your ", font_size=64, weight=BOLD)
        t2b = Text("HEAD?", font_size=64, weight=BOLD, color=ACCENT)
        t2 = VGroup(t2a, t2b).arrange(RIGHT, buff=0.15)

        title = VGroup(t1, t2).arrange(DOWN, buff=0.45).move_to([0, 2.8, 0])

        sub = pill("works for PERFECT SQUARES", GREEN, fs=28)
        sub.next_to(title, DOWN, buff=0.7)

        self._play(FadeIn(header, shift=DOWN * 0.4), rt=0.5)
        self._play(Write(title), rt=1.4)
        self._play(Circumscribe(t2[1], color=ACCENT, buff=0.1), rt=0.8)
        self._play(FadeIn(sub, shift=UP * 0.25), rt=0.5)
        self._sync(3.5)

        # ====================================================================
        # Show the random number
        # ====================================================================
        self._play(FadeOut(title, sub, shift=UP * 0.8), rt=0.5)

        big = Text(str(N), weight=BOLD, font_size=130).move_to([0, 2.0, 0])
        self._play(Write(big), rt=0.8)
        self._play(Indicate(big, color=ACCENT, scale_factor=1.05), rt=0.7)

        hud, s1, s2 = build_hud()

        self._play(
            AnimationGroup(
                FadeOut(big, shift=DOWN * 1.5),
                FadeIn(hud, shift=UP * 1.8),
                lag_ratio=0.35,
            ),
            rt=0.9,
        )
        self._play(Indicate(hud, color=ACCENT, scale_factor=1.02), rt=0.6)
        self._sync(7.0)

        # ====================================================================
        # STEP 1: tens digit — show only the relevant bracket
        # ====================================================================
        banner = step_banner("STEP 1", "Find the TENS digit", PINK)
        banner.move_to([0, 3.6, 0])
        self._play(GrowFromCenter(banner), rt=0.7)
        self._sync(8.0)

        caption = Text(
            f"Which bracket is {N} in?",
            font_size=36,
            color=GREY_B,
        ).move_to([0, 2.3, 0])

        bracket_fs = 50 if HIGH == 100 else 58
        ineq_fs = 46 if HIGH == 100 else 56

        low_lab = MathTex(
            rf"{LOW}^2 = {LOW_SQ}",
            font_size=bracket_fs,
            color=CYAN,
        )

        ineq = MathTex(
            rf"{LOW_SQ} \;<\; {N} \;<\; {HIGH_SQ}",
            font_size=ineq_fs,
            color=GREEN,
        )

        high_lab = MathTex(
            rf"{HIGH}^2 = {HIGH_SQ}",
            font_size=bracket_fs,
            color=CYAN,
        )

        bracket = VGroup(low_lab, ineq, high_lab).arrange(DOWN, buff=0.55)
        bracket.move_to([0, -0.2, 0])

        self._play(FadeIn(caption, shift=UP * 0.25), rt=0.6)
        self._play(FadeIn(low_lab, shift=LEFT * 0.7), rt=0.7)
        self._play(Write(ineq), rt=1.0)
        self._play(FadeIn(high_lab, shift=RIGHT * 0.7), rt=0.7)
        self._play(Indicate(ineq, color=GREEN, scale_factor=1.04), rt=0.8)

        chip = pill(f"TENS = {TENS}", ACCENT, fs=40).move_to([0, -3.2, 0])
        self._play(GrowFromCenter(chip), rt=0.6)

        d_tens = MathTex(str(TENS), font_size=96, color=ACCENT)
        d_tens.move_to(s1.get_center())

        self._play(
            GrowFromCenter(d_tens),
            Flash(
                s1.get_center(),
                color=ACCENT,
                line_length=0.5,
                num_lines=14,
                flash_radius=1.8,
            ),
            rt=0.9,
        )
        self._sync(13.5)

        # ====================================================================
        # STEP 2: last digit
        # ====================================================================
        self._play(FadeOut(caption, bracket, chip, shift=DOWN * 0.5), rt=0.6)

        banner2 = step_banner("STEP 2", "Find the LAST digit", PINK)
        banner2.move_to([0, 3.6, 0])

        self._play(ReplacementTransform(banner, banner2), rt=0.7)

        big = Text(str(N), weight=BOLD, font_size=120).move_to([0, 1.7, 0])
        self._play(Write(big), rt=0.7)
        self._play(big[-1].animate.set_color(PINK), rt=0.5)

        last_box = SurroundingRectangle(
            big[-1],
            color=PINK,
            buff=0.12,
            corner_radius=0.1,
        )
        self._play(Create(last_box), rt=0.5)
        self._sync(16.5)

        # --------------------------------------------------------------------
        # If the ending is unique, fill the ones digit immediately.
        # If ambiguous, show both candidates and compare with MID_ROOT^2.
        # --------------------------------------------------------------------
        if not AMBIGUOUS:
            rule_text = f"ends in {LAST}  ->  root ends in {CHOSEN_ONES}"
            rule = pill(
                rule_text,
                PINK,
                fs=30 if len(rule_text) < 36 else 26,
            ).move_to([0, -0.7, 0])

            self._play(GrowFromCenter(rule), rt=0.8)

            d_ones = MathTex(str(CHOSEN_ONES), font_size=96, color=GREEN)
            d_ones.move_to(s2.get_center())

            self._play(
                GrowFromCenter(d_ones),
                Flash(
                    s2.get_center(),
                    color=GREEN,
                    line_length=0.5,
                    num_lines=14,
                    flash_radius=1.8,
                ),
                rt=0.9,
            )

            self._play(Indicate(hud, color=GREEN, scale_factor=1.04), rt=0.8)

            self._play(
                FadeOut(big, last_box, rule, banner2, shift=UP * 0.6),
                rt=0.7,
            )

            self._sync(24.0)

        else:
            rule_text = (
                f"ends in {LAST}  ->  root ends in "
                f"{OPTIONS[0]} or {OPTIONS[1]}"
            )
            rule = pill(
                rule_text,
                PINK,
                fs=30 if len(rule_text) <= 38 else 26,
            ).move_to([0, -0.7, 0])

            self._play(GrowFromCenter(rule), rt=0.8)

            c1 = pill(str(CAND_LOW), CYAN, fs=44)
            c2 = pill(str(CAND_HIGH), PINK, fs=44)
            cands = VGroup(c1, c2).arrange(RIGHT, buff=0.9)
            cands.move_to([0, -2.1, 0])

            self._play(
                LaggedStart(
                    GrowFromCenter(c1),
                    GrowFromCenter(c2),
                    lag_ratio=0.35,
                ),
                rt=1.0,
            )

            mid_lab = MathTex(
                rf"{MID_ROOT}^2 = {MID_SQ}",
                font_size=54,
                color=ACCENT,
            ).move_to([0, -3.4, 0])

            self._play(FadeIn(mid_lab, shift=UP * 0.2), rt=0.7)

            rel = "<" if N < MID_SQ else ">"

            decide = MathTex(
                rf"{N} \;{rel}\; {MID_SQ} \;\Rightarrow\; {ROOT}",
                font_size=54,
                color=GREEN,
            ).move_to([0, -4.45, 0])

            self._play(Write(decide), rt=1.0)
            self._play(Indicate(decide, color=GREEN, scale_factor=1.05), rt=0.8)

            d_ones = MathTex(str(CHOSEN_ONES), font_size=96, color=GREEN)
            d_ones.move_to(s2.get_center())

            self._play(
                GrowFromCenter(d_ones),
                Flash(
                    s2.get_center(),
                    color=GREEN,
                    line_length=0.5,
                    num_lines=14,
                    flash_radius=1.8,
                ),
                rt=0.9,
            )

            self._play(Indicate(hud, color=GREEN, scale_factor=1.04), rt=0.8)

            self._play(
                FadeOut(
                    big,
                    last_box,
                    rule,
                    cands,
                    mid_lab,
                    decide,
                    banner2,
                    shift=UP * 0.6,
                ),
                rt=0.7,
            )

            self._sync(27.5)

        # ====================================================================
        # Payoff: reveal the answer
        # ====================================================================
        pay = MathTex(
            rf"\sqrt{{{N}}} = {ROOT}",
            font_size=84,
        ).move_to([0, 1.8, 0])

        paybox = SurroundingRectangle(
            pay,
            color=GREEN,
            buff=0.35,
            corner_radius=0.18,
        )

        self._play(GrowFromCenter(pay), rt=0.8)

        self._play(
            Create(paybox),
            Flash(
                pay.get_center(),
                color=GREEN,
                line_length=0.6,
                num_lines=18,
                flash_radius=2.4,
            ),
            rt=0.9,
        )

        chk = MathTex(
            rf"{ROOT}^2 = {N}",
            font_size=48,
            color=GREY_A,
        ).next_to(paybox, DOWN, buff=0.5)

        self._play(FadeIn(chk, shift=UP * 0.2), rt=0.7)

        # ====================================================================
        # End card: LIKE / SUBSCRIBE / SHARE
        # ====================================================================
        self._play(FadeOut(pay, paybox, chk), rt=0.6)

        head = Text(
            "If this helped…",
            font_size=36,
            weight=BOLD,
            color=GREY_B,
        ).move_to([0, 3.2, 0])

        btns = VGroup(
            action_button("LIKE", thumb_icon(CYAN), CYAN),
            action_button("SUBSCRIBE", bell_icon(PINK), PINK),
            action_button("SHARE", share_icon(GREEN), GREEN),
        )

        btns.arrange(DOWN, buff=0.55).move_to([0, -0.2, 0])

        self._play(FadeIn(head, shift=DOWN * 0.2), rt=0.5)

        self._play(
            LaggedStart(
                *[GrowFromCenter(b) for b in btns],
                lag_ratio=0.25,
            ),
            rt=1.5,
        )

        follow = Text(
            "More mental-math tricks — follow!",
            font_size=34,
            weight=BOLD,
            color=ACCENT,
        ).move_to([0, -4.25, 0])

        self._play(FadeIn(follow, shift=UP * 0.2), rt=0.6)

        for b in btns:
            self._play(
                b.animate.scale(1.08),
                rate_func=there_and_back,
                rt=0.35,
            )

        self._sync(31.5 if not AMBIGUOUS else 34.5)

        self._play(FadeOut(*self.mobjects), rt=1.0)