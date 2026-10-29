from manim import *
import numpy as np

# Vertical Shorts format (9:16)
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.background_color = "#0f0f14"


def circumcenter(A, B, C):
    ax, ay = A[0], A[1]
    bx, by = B[0], B[1]
    cx, cy = C[0], C[1]
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)) / d
    uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx) + (cx**2 + cy**2) * (bx - ax)) / d
    return np.array([ux, uy, 0])


class EulerShort(MovingCameraScene):
    def construct(self):
        # Triangle kept above the bottom 30% of the frame (y > -3.2)
        A = np.array([-3.0, -1.6, 0])
        B = np.array([3.0, -0.8, 0])
        C = np.array([0.8, 3.2, 0])

        O = circumcenter(A, B, C)   # circumcenter
        G = (A + B + C) / 3         # centroid
        H = A + B + C - 2 * O       # orthocenter

        def vertex_label(name, P):
            d = (P - G) / np.linalg.norm(P - G)
            return Text(name, font_size=36, color=WHITE).move_to(P + 0.45 * d)

        def key_label(name, P, color):
            d = (P - G) / np.linalg.norm(P - G)
            return Text(name, font_size=36, color=color).move_to(P + 0.45 * d)

        title = Text("Euler Line", font_size=60, weight=BOLD).to_edge(UP, buff=0.8)
        self.play(Write(title))

        status = Text("Triangle ABC", font_size=40, color=GREY_A).move_to(UP * 5.4)
        self.play(Write(status))

        # 1. Triangle
        tri = Polygon(A, B, C, color=WHITE, stroke_width=4)
        vA, vB, vC = vertex_label("A", A), vertex_label("B", B), vertex_label("C", C)
        self.play(Create(tri), Write(vA), Write(vB), Write(vC), run_time=2)
        self.wait(0.5)

        # 2. Altitudes: lines from each vertex through the orthocenter H
        new_status = Text("Altitudes", font_size=40, color=YELLOW).move_to(UP * 5.4)
        self.play(Transform(status, new_status))
        alts = VGroup(*[DashedLine(P, H, color=YELLOW) for P in (A, B, C)])
        self.play(LaggedStart(*[Create(a) for a in alts], lag_ratio=0.3), run_time=2)
        dotH = Dot(H, color=YELLOW)
        lH = key_label("H", H, YELLOW)
        self.play(FadeIn(dotH), Write(lH))
        self.wait(0.5)

        # 3. Medians: vertex to midpoint of opposite side, meeting at centroid G
        new_status = Text("Medians", font_size=40, color=GREEN).move_to(UP * 5.4)
        self.play(Transform(status, new_status))
        Ma, Mb, Mc = (B + C) / 2, (A + C) / 2, (A + B) / 2
        medians = VGroup(*[Line(P, M, color=GREEN) for P, M in ((A, Ma), (B, Mb), (C, Mc))])
        self.play(Create(medians), run_time=2)
        dotG = Dot(G, color=GREEN)
        lG = key_label("G", G, GREEN)
        self.play(FadeIn(dotG), Write(lG))
        self.wait(0.5)

        # 4. Perpendicular bisectors: midpoint of each side to circumcenter O
        new_status = Text("Perpendicular bisectors", font_size=40, color=BLUE).move_to(UP * 5.4)
        self.play(Transform(status, new_status))
        bisectors = VGroup(*[Line(M, O, color=BLUE) for M in (Ma, Mb, Mc)])
        self.play(Create(bisectors), run_time=2)
        circ = Circle(radius=np.linalg.norm(A - O), color=BLUE).move_to(O)
        dotO = Dot(O, color=BLUE)
        lO = key_label("O", O, BLUE)
        self.play(Create(circ), FadeIn(dotO), Write(lO))
        self.wait(0.5)

        # 5. Clear the clutter, keep the triangle, reveal the Euler line
        self.play(FadeOut(alts), FadeOut(medians), FadeOut(bisectors), FadeOut(circ))
        new_status = Text("H, G, O are collinear", font_size=40, color=YELLOW).move_to(UP * 5.4)
        self.play(Transform(status, new_status))

        u = (H - O) / np.linalg.norm(H - O)
        euler = Line(G - 1.8 * u, G + 1.8 * u, color=YELLOW, stroke_width=6)
        self.play(Create(euler), run_time=2)
        self.wait(1.5)

        # 6. Remove the triangle, zoom onto the Euler line
        self.play(
            FadeOut(tri), FadeOut(vA), FadeOut(vB), FadeOut(vC),
            FadeOut(status), FadeOut(title),
            self.camera.frame.animate.move_to(G).set(width=3.2),
            run_time=2.5,
        )

        # Zoomed labels: name each point and show the 2:1 ratio
        hLabel = Text("H = orthocenter", font_size=26, color=YELLOW).move_to(G + np.array([0, 2.9, 0]))
        gLabel = Text("G = centroid", font_size=26, color=GREEN).move_to(G + np.array([0, 2.5, 0]))
        oLabel = Text("O = circumcenter", font_size=26, color=BLUE).move_to(G + np.array([0, 2.1, 0]))
        self.play(Write(hLabel), Write(gLabel), Write(oLabel))

        # Point labels sit just above the line
        self.play(
            lH.animate.move_to(H + np.array([0, 0.22, 0])).scale(0.5),
            lG.animate.move_to(G + np.array([0, 0.22, 0])).scale(0.5),
            lO.animate.move_to(O + np.array([0, 0.22, 0])).scale(0.5),
        )

        brace_HG = BraceBetweenPoints(H, G, direction=UP * 0.0 + np.array([0, 1, 0]))
        brace_GO = BraceBetweenPoints(G, O, direction=np.array([0, -1, 0]))
        t_HG = Text("2x", font_size=28, color=YELLOW).next_to(brace_HG, UP, buff=0.05)
        t_GO = Text("x", font_size=28, color=GREEN).next_to(brace_GO, DOWN, buff=0.05)
        self.play(Create(brace_HG), Create(brace_GO), Write(t_HG), Write(t_GO))

        ratio = Text("HG : GO = 2 : 1", font_size=30, color=WHITE).move_to(G + np.array([0, 1.4, 0]))
        self.play(Write(ratio))
        self.wait(3)

        # 7. Zoom back out, end card (kept in the centre, clear of the bottom 30%)
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            self.camera.frame.animate.move_to(ORIGIN).set(width=9),
            run_time=1.5,
        )
        end = VGroup(
            Text("Like", font_size=64, color=RED, weight=BOLD),
            Text("Subscribe", font_size=64, color=WHITE, weight=BOLD),
            Text("Share", font_size=64, color=GREEN, weight=BOLD),
        ).arrange(DOWN, buff=0.5).move_to(ORIGIN + UP * 1.5)
        self.play(LaggedStart(*[Write(t) for t in end], lag_ratio=0.4), run_time=2)
        self.wait(2)