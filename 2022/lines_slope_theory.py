from manimlib import *

# Note:

axis_config = {
    "stroke_color": WHITE,
    "stroke_range": 3
}

# Golden ratio (phi)
phi = (math.sqrt(5) - 1) / 2

# Create a 5x5 (1 unit length) coordinate
axes_large = Axes(
    x_range=(-5, 5),
    y_range=(-5, 5),
    width=8,
    height=8,

    axis_config=axis_config,

    y_axis_config={
        "numbers_to_exclude": [-5, 0]
    }
)

axes_large.add_coordinate_labels(
    font_size=20
)

# Create a 4x4 (1 unit length) coordinate
# This coordinate is for starting() and proving()
axes = Axes(
    x_range=(-4, 4),
    y_range=(-4, 4),
    width=6,
    height=6,

    axis_config=axis_config,

    y_axis_config={
        "numbers_to_exclude": [0]
    }
)

axes.add_coordinate_labels(
    font_size=20
)


# Make all strings in tex_1 aligned left to tex_2
def align_tex_to_left(tex_1, tex_2):
    for i, item in enumerate(tex_1):
        item.align_to(tex_2[i], LEFT)


# Make all mobjects in tex_group aligned left to the previous one
# This would only make the first string aligned (differs from align_tex() )
def align_tex_group_to_left(tex_group):
    for i, item in enumerate(tex_group):
        if not i == 0:
            item.align_to(tex_group[i - 1], LEFT)


class Main(Scene):
    # Create a method to move mobjects (graph, label, elbow)
    # This is for proving_by_algebra()
    def move_mobjects(self, graph, exp, color, label, exp_tex, elbow, pos):
        graph_conv = axes_large.get_graph(exp, color=color)
        label_conv = axes_large.get_graph_label(graph_conv, exp_tex)

        elbow_conv = Elbow(width=0.2, angle=PI / 4)
        elbow_conv.move_to(pos)

        if label == exp_tex:
            label_animate = ReplacementTransform(label, label_conv)
        else:
            label_animate = TransformMatchingTex(label, label_conv)

        self.play(
            ReplacementTransform(graph, graph_conv),
            label_animate,
            ReplacementTransform(elbow, elbow_conv),

            run_time=2
        )

        return graph_conv, label_conv, elbow_conv

    # Create a line
    def create_line(self, point_a, point_b, color):
        line = Line(point_a, point_b, color=color, stroke_width=8)
        self.play(ShowCreation(line))
        return line

    # Create a line and return an animation (line -> text)
    # Default color is set to GOLD_A
    def line_to_text(self, point_a, point_b, text):
        line = self.create_line(point_a, point_b, GOLD)
        return ReplacementTransform(line, text)

    # Write all mobjects in a VGroup
    def animate_through(self, group, waiting_time):
        for item in group:
            self.play(
                Write(item),
                run_time=1.5
            )

            self.wait(waiting_time)

    # The entry of animation
    def construct(self):
        self.wait(1)
        self.start()
        self.prove_by_algebra()
        self.prove_by_geometry()
        self.end()

    # Starting
    def start(self):
        # Animate and move coordinate
        self.play(ShowCreation(axes_large))
        self.wait(0.5)

        # Create two line graphs
        line_start_1_graph = axes_large.get_graph(
            lambda x: x + 1,  # y = x + 1
            color=BLUE_B
        )

        line_start_2_graph = axes_large.get_graph(
            lambda x: -x,  # y = -x
            color=YELLOW_B
        )

        line_1_str = "y = mx + a"
        line_2_str = "y = nx + b"

        line_1_tex = Tex(line_1_str, isolate={"y", "x", "m", "a"})
        line_2_tex = Tex(line_2_str, isolate={"y", "x", "n", "b"})

        line_start_1_label = axes_large.get_graph_label(line_start_1_graph, line_1_str)
        line_start_2_label = axes_large.get_graph_label(line_start_2_graph, line_2_str)

        # Animate two line graphs
        self.play(
            ShowCreation(line_start_1_graph),
            ShowCreation(line_start_2_graph),
            FadeIn(line_start_1_label, LEFT),
            FadeIn(line_start_2_label, LEFT),

            run_time=1.5
        )

        # Zoom into elbow
        frame = self.camera.frame

        self.play(
            frame.animate.move_to(axes_large.c2p(-0.5, 0.8)).set_width(10),
            run_time=0.8
        )
        self.wait(0.1)

        # Create an elbow
        elbow = Elbow(width=0.2, angle=PI / 4)
        elbow.move_to(axes_large.c2p(-0.5, 0.8))

        self.play(ShowCreation(elbow))
        self.wait(0.1)

        # Reset to default
        self.play(
            frame.animate.to_default_state(),
            run_time=0.8
        )

        # Move coordinate to the left edge
        group_start = VGroup(
            axes_large,
            elbow,
            line_start_1_graph,
            line_start_2_graph,
            line_start_1_label,
            line_start_2_label
        )
        self.play(group_start.animate.to_edge(LEFT))

        # Show some text
        proof_text = TexText(
            """
                $m \\neq 0$ \n
                $n \\neq 0$ \n
                求证 $mn = -1$
            """,
            tex_to_color_map={
                "$m \\neq 0$": BLUE_B,
                "$n \\neq 0$": YELLOW_B,
                "$mn = -1$": TEAL
            }
        )
        proof_text.to_edge(RIGHT)

        self.play(Write(proof_text))

        # Waiting
        self.wait(3)

        # Fade out
        self.play(FadeOut(proof_text))

        # Show some text
        idea_group = VGroup(
            TexText("""
                改变 $a$ 和 $b$ \n
                两直线仍保持垂直 \n
            """,
                    tex_to_color_map={"$a$": BLUE_B, "$b$": YELLOW_B}  # t2c isn't defined?
                    ),
            TexText("""
                因此使
                $a = 0$, 
                $b = 0$ \n
                简化问题
            """,
                    tex_to_color_map={"$a = 0$": BLUE_B, "$b = 0$": YELLOW_B}
                    )
        )

        idea_group.arrange(DOWN)
        idea_group.to_edge(RIGHT)

        self.play(Write(idea_group[0]), run_time=2)

        # Move lines and elbow
        self.wait()

        # line 1
        tuple_temp = self.move_mobjects(
            line_start_1_graph, lambda x: x + 3, BLUE_B,
            line_start_1_label, line_1_str,
            elbow, axes_large.c2p(-1.5, 1.8)
        )

        # Reset line 1
        line_start_1_graph = tuple_temp[0]
        line_start_1_label = tuple_temp[1]
        elbow = tuple_temp[2]

        # line 2
        tuple_temp = self.move_mobjects(
            line_start_2_graph, lambda x: -x - 3, YELLOW_B,
            line_start_2_label, line_2_str,
            elbow, axes_large.c2p(-3, 0.3)
        )

        # Reset line 2
        line_start_2_graph = tuple_temp[0]
        line_start_2_label = tuple_temp[1]
        elbow = tuple_temp[2]

        # line 1
        tuple_temp = self.move_mobjects(
            line_start_1_graph, lambda x: x - 2, BLUE_B,
            line_start_1_label, line_1_tex,
            elbow, axes_large.c2p(-0.5, -2.2)
        )

        # Reset line 1
        line_start_1_graph = tuple_temp[0]
        line_start_1_label = tuple_temp[1]
        elbow = tuple_temp[2]

        # line 2
        tuple_temp = self.move_mobjects(
            line_start_2_graph, lambda x: -x + 1, YELLOW_B,
            line_start_2_label, line_2_tex,
            elbow, axes_large.c2p(1.5, -0.2)
        )

        # Reset line 2
        line_start_2_graph = tuple_temp[0]
        line_start_2_label = tuple_temp[1]
        elbow = tuple_temp[2]

        # Show some text
        self.play(Write(idea_group[1]), run_time=2)

        # Move lines to origin
        line_1_tex_originated = Tex("y = mx", isolate={"y", "x", "m"})
        line_2_tex_originated = Tex("y = nx", isolate={"y", "x", "n"})

        # line 1
        tuple_temp = self.move_mobjects(
            line_start_1_graph, lambda x: x, BLUE_B,
            line_start_1_label, line_1_tex_originated,
            elbow, axes_large.c2p(0.5, 0.8)
        )

        # Reset line 1
        line_start_1_graph = tuple_temp[0]
        line_start_1_label = tuple_temp[1]
        elbow = tuple_temp[2]

        # line 2
        tuple_temp = self.move_mobjects(
            line_start_2_graph, lambda x: -x, YELLOW_B,
            line_start_2_label, line_2_tex_originated,
            elbow, axes_large.c2p(0, 0.3)
        )

        # Reset line 2
        line_start_2_graph = tuple_temp[0]
        line_start_2_label = tuple_temp[1]
        elbow = tuple_temp[2]

        # Uncreate all
        group_start = VGroup(
            axes_large,
            elbow,
            line_start_1_graph,
            line_start_2_graph,
            line_start_1_label,
            line_start_2_label
        )

        self.play(
            Uncreate(group_start),
            Uncreate(idea_group),

            run_time=2
        )

    # Proving by Algebra (Method 1)
    def prove_by_algebra(self):
        # Animate and move coordinate
        self.play(ShowCreation(axes))
        self.wait(0.5)

        # Create two line graphs
        line_1_graph = axes.get_graph(
            lambda x: 2 * x,  # y = 2x
            color=BLUE_B
        )

        line_2_graph = axes.get_graph(
            lambda x: -0.5 * x,  # y = -\frac 12 x
            color=YELLOW_B
        )

        line_1_str = "y = mx"
        line_2_str = "y = nx"

        line_1_tex = Tex(line_1_str, isolate={"y", "x", "m"})
        line_2_tex = Tex(line_2_str, isolate={"y", "x", "n"})

        line_1_label = axes.get_graph_label(line_1_graph, line_1_tex)
        line_2_label = axes.get_graph_label(line_2_graph, line_2_tex)

        # Animate two line graphs
        self.play(
            ShowCreation(line_1_graph),
            ShowCreation(line_2_graph),
            FadeIn(line_1_label, LEFT),
            FadeIn(line_2_label, LEFT),

            run_time=1.5
        )

        # Create an elbow
        elbow = Elbow(width=0.2, angle=math.atan(2))
        elbow.move_to(axes.c2p(-0.1, 0.3))

        self.play(ShowCreation(elbow))
        self.wait()

        # Move coordinate to the left edge
        group = VGroup(
            axes,
            elbow,
            line_1_graph,
            line_2_graph,
            line_1_label,
            line_2_label
        )

        self.play(group.animate.to_edge(LEFT))

        # Create proof text
        proof_text = VGroup(
            TexText(
                """
                    证法一 $\\ $ 勾股 \n
                    设 $y = mx$ 上有一点 $P(p, mp)$ \n
                    $y = nx$ 上有一点 $Q(q, nq)$
                """,
                tex_to_color_map={
                    "勾股": TEAL,
                    "$y = mx$": BLUE_B,
                    "$P(p, mp)$": BLUE_B,
                    "$y = nx$": YELLOW_B,
                    "$Q(q, nq)$": YELLOW_B
                }
            ),
            TexText(
                """
                    作 $PH$ $\\bot \\ x $ 轴于点 $H$ \n
                    $QI$ $\\bot \\ x $ 轴于点 $I$
                """,
                tex_to_color_map={
                    "$PH$": BLUE_B,
                    "$H$": BLUE_B,
                    "$QI$": YELLOW_B,
                    "$I$": YELLOW_B
                }
            ),
            TexText(
                """
                    连接 $PQ$
                """,
                tex_to_color_map={
                    "$PQ$": TEAL
                }
            ),
            TexText("\n"),
            VGroup(
                Tex(
                    "PQ^2", "=",
                    tex_to_color_map={
                        "PQ^2": TEAL,
                        "OI^2": YELLOW_B,
                        "IQ^2": YELLOW_B,
                        "OH^2": BLUE_B,
                        "PH^2": BLUE_B
                    }
                ),
                Tex(
                    "OI^2", "+", "IQ^2", "+"
                ),
                Tex(
                    "OH^2", "+", "PH^2"
                )
            ),

            TexText(
                """
                    作 $GQ$ $\\bot$ $PH$ 于点 $G$
                """,
                tex_to_color_map={
                    "$GQ$": TEAL,
                    "$PH$": BLUE_B,
                    "$G$": TEAL
                }
            ),

            Tex(
                "PQ^2", "=", "PG^2", "+", "GQ^2",
                tex_to_color_map={
                    "PQ^2": TEAL,
                    "PG^2": BLUE_B,
                    "GQ^2": YELLOW_B
                }
            )

        )
        proof_text.arrange(DOWN)
        proof_text.to_corner(UR)

        # Create points (P, Q)
        p = Dot(color=RED)
        p.move_to(axes.i2gp(1, line_1_graph))
        p_label = Tex("P", t2c={"P": BLUE_B})
        always(p_label.next_to, p)

        q = Dot(color=GREEN)
        q.move_to(axes.i2gp(-1, line_2_graph))
        q_label = Tex("Q", t2c={"Q": YELLOW_B})
        always(q_label.next_to, q, UR)

        # Animate
        self.play(
            Write(proof_text[0]),
            FadeIn(p, scale=0.5),
            FadeIn(q, scale=0.5),
            FadeIn(p_label),
            FadeIn(q_label),

            run_time=1.5
        )

        self.wait(2)

        # Create lines and points (H, I)
        v_line_p = always_redraw(lambda: axes.get_v_line(p.get_bottom()))
        v_line_q = always_redraw(lambda: axes.get_v_line(q.get_bottom()))
        h = Dot(color=RED)
        h.move_to(axes.c2p(1, 0))
        h_label = Tex("H")
        always(h_label.next_to, h)

        i = Dot(color=GREEN)
        i.move_to(axes.c2p(-1, 0))
        i_label = Tex("I")
        always(i_label.next_to, i, UL)

        f_always(h.set_x, p.get_x)
        f_always(i.set_x, q.get_x)

        self.play(
            ShowCreation(v_line_p),
            ShowCreation(v_line_q),
            Write(proof_text[1]),
            FadeIn(h, scale=0.5),
            FadeIn(i, scale=0.5),
            FadeIn(h_label),
            FadeIn(i_label),

            run_time=1.5
        )

        # Move points
        p_tracker = ValueTracker(1)
        f_always(
            p.move_to,
            lambda: axes.i2gp(p_tracker.get_value(), line_1_graph)
        )

        q_tracker = ValueTracker(-1)
        f_always(
            q.move_to,
            lambda: axes.i2gp(q_tracker.get_value(), line_2_graph)
        )

        self.play(
            p_tracker.animate.set_value(2),
            q_tracker.animate.set_value(-3),

            run_time=3
        )

        self.play(
            p_tracker.animate.set_value(-2),
            q_tracker.animate.set_value(3),

            run_time=3
        )

        self.play(
            p_tracker.animate.set_value(1),
            q_tracker.animate.set_value(-3),

            run_time=3
        )

        self.wait()

        # Connect PQ
        pq = DashedLine(q, p)

        self.wait(2)

        self.play(
            ShowCreation(pq),
            Write(proof_text[2]),

            run_time=2
        )

        # Create the origin
        origin = Dot(color=TEAL)
        origin.move_to(axes.c2p(0, 0))
        origin_label = Tex("O")
        origin_label.next_to(origin, DL)

        # Animate the origin
        self.play(
            ShowCreation(origin),
            Write(origin_label)
        )

        # Transform
        exps = VGroup(
            Tex("OP^2", "=", "OH^2", "+", "PH^2",
                tex_to_color_map={
                    "OP^2": BLUE_B
                },
                align=LEFT
                ),

            Tex("OQ^2", "=", "OI^2", "+", "IQ^2",
                tex_to_color_map={
                    "OQ^2": YELLOW_B
                },
                align=LEFT
                ),

            Tex("PQ^2", "=", "OQ^2", "+", "OP^2",
                tex_to_color_map={
                    "OP^2": BLUE_B,
                    "OQ^2": YELLOW_B,
                    "PQ^2": TEAL
                },
                align=LEFT
                )
        )
        exps.arrange(DOWN)

        align_tex_to_left(exps[1], exps[0])
        align_tex_to_left(exps[2], exps[1])

        exps.to_corner(DR)

        # OP^2 = OH^2 + PH^2
        self.play(
            self.line_to_text(origin, p, exps[0][0]),
            Write(exps[0][1]),
            run_time=1.5
        )

        self.play(
            self.line_to_text(origin, h, exps[0][2]),
            Write(exps[0][3]),
            self.line_to_text(p, h, exps[0][4]),
            run_time=1.5
        )

        # OQ^2 = OI^2 + IQ^2
        self.play(
            self.line_to_text(origin, q, exps[1][0]),
            Write(exps[1][1]),
            run_time=1.5
        )

        self.play(
            self.line_to_text(origin, i, exps[1][2]),
            Write(exps[1][3]),
            self.line_to_text(i, q, exps[1][4]),
            run_time=1.5
        )

        # PQ^2 = OQ^2 + OP^2
        self.play(
            self.line_to_text(p, q, exps[2][0]),
            Write(exps[2][1]),
            run_time=1.5
        )

        self.play(
            self.line_to_text(origin, q, exps[2][2]),
            Write(exps[2][3]),
            self.line_to_text(origin, p, exps[2][4]),
            run_time=1.5
        )

        # Transform to simplified tex (PQ^2 = OI^2 + IQ^2 + OH^2 + PH^2)
        proof_text[4].arrange(RIGHT)
        proof_text[4].next_to(proof_text[5], UP)

        self.play(
            exps[2].animate.move_to(proof_text[4])
        )

        self.wait(2)

        self.play(
            ShowCreation(proof_text[3]),
            TransformMatchingTex(exps[0], proof_text[4][2], transform_mismatches=True),
            TransformMatchingTex(exps[1], proof_text[4][1], transform_mismatches=True),
            TransformMatchingTex(exps[2], proof_text[4][0], transform_mismatches=True),
            run_time=2
        )

        # Make a perpendicular line (GQ)
        g = Dot(color=TEAL)
        g.set_x(h.get_x())
        g.set_y(q.get_y())
        g_label = Tex("G")
        g_label.next_to(g, RIGHT)
        gq = DashedLine(q, g)

        self.play(
            ShowCreation(g),
            ShowCreation(g_label),
            ShowCreation(gq),
            Write(proof_text[5]),
            run_time=1.5
        )

        # PQ^2 = PG^2 + GQ^2
        self.play(
            self.line_to_text(p, q, proof_text[6][0]),
            Write(proof_text[6][1]),
            run_time=1.5
        )

        self.play(
            self.line_to_text(p, g, proof_text[6][2]),
            Write(proof_text[6][3]),
            self.line_to_text(g, q, proof_text[6][4]),
            run_time=1.5
        )

        self.wait(3)

        # Transform to letters
        pq_exp_1 = Tex(
            "PQ^2 = q^2 + (nq)^2 + p^2 + (mp)^2",
            isolate={"PQ^2", "(mp)^2", "(nq)^2", "p^2", "q^2"},
            tex_to_color_map={
                "PQ^2": TEAL,
                "q^2": YELLOW_B,
                "(nq)^2": YELLOW_B,
                "p^2": BLUE_B,
                "(mp)^2": BLUE_B
            }
        )

        pq_exp_2 = Tex(
            "PQ^2 = (mp - nq)^2 + (p - q)^2",
            isolate={"PQ^2", "mp", "nq", "(", ")", "p", "q"},
            tex_to_color_map={
                "PQ^2": TEAL,
                "q": YELLOW_B,
                "nq": YELLOW_B,
                "p": BLUE_B,
                "mp": BLUE_B
            }
        )
        pq_exp_1.move_to(proof_text[4])
        pq_exp_2.move_to(proof_text[6])

        self.play(TransformMatchingTex(proof_text[4], pq_exp_1), run_time=3)
        self.wait(2)
        self.play(TransformMatchingTex(proof_text[6], pq_exp_2), run_time=3)

        self.wait(3)

        # Create a screen rectangle covering the screen for texting
        cover = FullScreenRectangle()
        self.play(ShowCreation(cover), run_time=3)

        pq_exps = VGroup(pq_exp_1, pq_exp_2)
        pq_exp_2[0].align_to(pq_exp_1[0], LEFT)
        pq_exp_2[1].align_to(pq_exp_1[1], LEFT)

        pq_exps.to_corner(UL)

        self.play(
            Write(pq_exps),
            run_time=4
        )

        self.wait(2)

        # Transformation
        pq_exps_proof = VGroup(
            Tex(
                "q^2 + (nq)^2 + p^2 + (mp)^2 = (mp)^2 - 2mnpq + (nq)^2 + p^2 - 2pq + q^2",
                isolate={"nq", "mp", "q", "p", "2mnpq", "2pq"},
                tex_to_color_map={
                    "nq": YELLOW_B,
                    "mp": BLUE_B,
                    "q": YELLOW_B,
                    "p": BLUE_B,
                    "2mnpq": TEAL,
                    "2pq": TEAL
                }
            ),
            Tex(
                "0 = - 2mnpq - 2pq",
                isolate={"- 2mnpq", "- 2pq"},
                tex_to_color_map={
                    "- 2mnpq": TEAL,
                    "- 2pq": TEAL
                }
            ),
            Tex(
                "-2mnpq - 2pq = 0",
                isolate={"-2mnpq", "- 2pq"},
                tex_to_color_map={
                    "-2mnpq": TEAL,
                    "- 2pq": TEAL
                }
            ),
            Tex(
                "-2pq(mn + 1) = 0",
                isolate={"mn", "-2pq", "1"},
                tex_to_color_map={
                    "-2pq": TEAL,
                    "mn": BLUE_B
                }
            ),
            Tex(
                "\\because p \\neq 0, \\ q \\neq 0",
                tex_to_color_map={
                    "p": BLUE_B,
                    "\\ q": YELLOW_B
                    # "q": YELLOW_B change the color of "\\neq" INSTEAD OF "q"
                }
            ),
            Tex(
                "\\therefore mn + 1 = 0",
                isolate={"mn"},
                tex_to_color_map={
                    "mn": BLUE_B
                }
            ),
            Tex(
                "\\therefore mn = -1 \\quad \\blacksquare",
                isolate={"mn"},
                tex_to_color_map={
                    "mn": BLUE_B
                }
            ),
        )

        # PQ^2 expressions transform
        pq_exps = VGroup(
            Tex(
                "q^2 + (nq)^2 + p^2 + (mp)^2",
                isolate={"mp", "nq", "p", "q"},
                tex_to_color_map={
                    "q": YELLOW_B,
                    "nq": YELLOW_B,
                    "p": BLUE_B,
                    "mp": BLUE_B
                }
            ),
            Tex("="),
            Tex(
                "(mp - nq)^2 + (p - q)^2",
                isolate={"mp", "nq", "p", "q"},
                tex_to_color_map={
                    "q": YELLOW_B,
                    "nq": YELLOW_B,
                    "p": BLUE_B,
                    "mp": BLUE_B
                }
            )
        )
        pq_exps.arrange(RIGHT)
        pq_exps.to_corner(UL)

        self.play(
            ReplacementTransform(pq_exp_1, pq_exps[0]),
            run_time=1.5
        )
        self.play(
            Write(pq_exps[1]),
            run_time=1.5
        )
        self.play(
            ReplacementTransform(pq_exp_2, pq_exps[2]),
            run_time=1.5
        )

        self.wait(2)

        # A group of animation (details in animate_through() !)
        pq_exps_proof[0].scale(0.9)
        pq_exps_proof.next_to(pq_exps, DOWN)
        pq_exps_proof.to_edge(LEFT)
        pq_exps_proof.arrange(DOWN)
        align_tex_group_to_left(pq_exps_proof)

        self.animate_through(pq_exps_proof, 2.5)

        self.wait(5.5)

        # Fade out all
        self.play(
            FadeOut(pq_exps_proof),
            FadeOut(pq_exps)
        )

    # Proving by Geometry (Method 2)
    def prove_by_geometry(self):
        # Animate and move coordinate
        self.play(ShowCreation(axes))
        self.wait(0.5)

        # Create two line graphs
        line_1_graph = axes.get_graph(
            lambda x: 2 * x,  # y = 2x
            color=BLUE_B
        )

        line_2_graph = axes.get_graph(
            lambda x: -0.5 * x,  # y = -\frac 12 x
            color=YELLOW_B
        )

        line_1_str = "y = mx"
        line_2_str = "y = nx"

        line_1_tex = Tex(line_1_str, isolate={"y", "x", "m"})
        line_2_tex = Tex(line_2_str, isolate={"y", "x", "n"})

        line_1_label = axes.get_graph_label(line_1_graph, line_1_tex)
        line_2_label = axes.get_graph_label(line_2_graph, line_2_tex)

        # Animate two line graphs
        self.play(
            ShowCreation(line_1_graph),
            ShowCreation(line_2_graph),
            FadeIn(line_1_label, LEFT),
            FadeIn(line_2_label, LEFT),

            run_time=1.5
        )

        # Create an elbow
        elbow = Elbow(width=0.2, angle=math.atan(2))
        elbow.move_to(axes.c2p(-0.1, 0.3))

        self.play(ShowCreation(elbow))
        self.wait()

        # Move coordinate to the left edge
        group = VGroup(
            axes,
            elbow,
            line_1_graph,
            line_2_graph,
            line_1_label,
            line_2_label
        )

        self.play(group.animate.to_edge(LEFT))

        # Show the proof text
        proof_text = VGroup(
            TexText(
                """
                    证法二 $\\ $ 三角形全等 \n
                    设 $y = mx$ 上有一点 $P(p, mp)$ \n
                    $y = nx$ 上有一点 $Q(q, nq)$ \n
                    且 $OP = OQ$
                """,
                tex_to_color_map={
                    "三角形全等": TEAL,
                    "$y = mx$": BLUE_B,
                    "$P(p, mp)$": BLUE_B,
                    "$y = nx$": YELLOW_B,
                    "$Q(q, nq)$": YELLOW_B,
                    "$OP = OQ$": TEAL
                }
            ),
            TexText(
                """
                    作 $PH$ $\\bot \\ x $ 轴于点 $H$ \n
                    $QI$ $\\bot \\ x $ 轴于点 $I$
                """,
                tex_to_color_map={
                    "$PH$": BLUE_B,
                    "$H$": BLUE_B,
                    "$QI$": YELLOW_B,
                    "$I$": YELLOW_B
                }
            ),
            Tex(
                "\\angle PHO = \\angle QIO = 90^\\circ"
            ),

            VGroup(
                Tex("\\angle 1 + \\angle 2 = 90^\\circ"),
                Tex("\\angle 1 + \\angle 3 = 90^\\circ"),
                Tex("\\angle 2 = \\angle 3")
            ),

            Tex("OP = OQ"),

            Tex("""
                \\begin{cases}
                    \\angle PHO = \\angle QIO = 90^\\circ \\\\
                    \\angle 2 = \\angle 3 \\\\
                    OP = OQ
                \\end{cases}
            """),

            Tex(
                "\\triangle QIO \\cong \\triangle OHP \\ (AAS)",
                tex_to_color_map={
                    "\\triangle QIO": GREEN,
                    "\\triangle OHP": RED,
                    "AAS": TEAL
                }
            )
        )

        proof_text.arrange(DOWN)
        proof_text.to_corner(UR)

        # Create points (P, Q)
        p = Dot(color=RED)
        p.move_to(axes.i2gp(1, line_1_graph))
        p_label = Tex("P", t2c={"P": BLUE_B})
        always(p_label.next_to, p)

        q = Dot(color=GREEN)
        q.move_to(axes.i2gp(-2, line_2_graph))
        q_label = Tex("Q", t2c={"Q": YELLOW_B})
        always(q_label.next_to, q, UR)

        # Create the origin
        origin = Dot(color=TEAL)
        origin.move_to(axes.c2p(0, 0))
        origin_label = Tex("O")
        origin_label.next_to(origin, DL)

        # Animate the origin
        self.play(
            ShowCreation(origin),
            Write(origin_label)
        )

        # Animate
        self.play(
            Write(proof_text[0]),
            FadeIn(p, scale=0.5),
            FadeIn(q, scale=0.5),
            FadeIn(p_label),
            FadeIn(q_label),

            run_time=1.5
        )

        self.wait(2)

        # Create lines and points (H, I)
        v_line_p = always_redraw(lambda: axes.get_v_line(p.get_bottom()))
        v_line_q = always_redraw(lambda: axes.get_v_line(q.get_bottom()))
        h = Dot(color=RED)
        h.move_to(axes.c2p(1, 0))
        h_label = Tex("H")
        always(h_label.next_to, h)

        i = Dot(color=GREEN)
        i.move_to(axes.c2p(-1, 0))
        i_label = Tex("I")
        always(i_label.next_to, i, UL)

        f_always(h.set_x, p.get_x)
        f_always(i.set_x, q.get_x)

        self.play(
            ShowCreation(v_line_p),
            ShowCreation(v_line_q),
            Write(proof_text[1]),
            FadeIn(h, scale=0.5),
            FadeIn(i, scale=0.5),
            FadeIn(h_label),
            FadeIn(i_label),

            run_time=1.5
        )

        # Highlight OP and OQ
        op_red = self.create_line(origin, p, RED)
        oq = self.create_line(origin, q, GREEN)

        # Move points
        p_tracker = ValueTracker(1)
        f_always(
            op_red.put_start_and_end_on,
            origin.get_center, p.get_center
        )
        f_always(
            p.move_to,
            lambda: axes.i2gp(p_tracker.get_value(), line_1_graph)
        )

        q_tracker = ValueTracker(-2)
        f_always(
            oq.put_start_and_end_on,
            origin.get_center, q.get_center
        )
        f_always(
            q.move_to,
            lambda: axes.i2gp(q_tracker.get_value(), line_2_graph)
        )

        self.play(
            p_tracker.animate.set_value(2),
            q_tracker.animate.set_value(-4),

            run_time=3
        )

        self.play(
            p_tracker.animate.set_value(-1),
            q_tracker.animate.set_value(2),

            run_time=3
        )

        self.play(
            p_tracker.animate.set_value(1),
            q_tracker.animate.set_value(-2),

            run_time=3
        )

        self.wait(2)

        # Create elbows and angles
        # Angle PHO
        angle_pho = Elbow(width=0.2, angle=PI / 2)
        angle_pho.move_to(axes.c2p(0.8, 0.2))

        # Angle QIO
        angle_qio = Elbow(width=0.2)
        angle_qio.move_to(axes.c2p(-1.8, 0.2))

        # Animate elbows (1)
        self.play(
            ShowCreation(angle_qio),
            ShowCreation(angle_pho),
            Write(proof_text[2]),
            run_time=1.5
        )
        self.wait()

        # Angle 1 (2)
        angle_1 = Arc(
            arc_center=axes.c2p(0, 0),
            radius=0.3,
            start_angle=PI / 2 + math.atan(2),
            angle=math.atan(0.5)
        )
        angle_1_label = Tex("1")
        angle_1_label.next_to(angle_1, UL * 0.5)
        angle_1_label.scale(0.8)

        self.play(
            ShowCreation(angle_1),
            ShowCreation(angle_1_label),
            run_time=1.5
        )

        # Angle 2 (3)
        angle_2 = Arc(
            arc_center=axes.c2p(0, 0),
            radius=0.3,
            start_angle=0,
            angle=math.atan(2)
        )
        angle_2_label = Tex("2")
        angle_2_label.next_to(angle_2, UR * 0.5)
        angle_2_label.scale(0.8)
        proof_text[3].arrange(DOWN)
        proof_text[3].next_to(proof_text[2], DOWN)

        # Angle 1 + Angle 2 = 90 Degrees
        self.play(
            ShowCreation(angle_2),
            ShowCreation(angle_2_label),
            Write(proof_text[3][0]),
            run_time=1.5
        )

        # Angle 3 (4)
        angle_3 = Arc(
            arc_center=axes.c2p(-2, 1),
            radius=0.3,
            start_angle=PI * 3 / 2,
            angle=math.atan(2)
        )
        angle_3_label = Tex("3")
        angle_3_label.next_to(angle_3, RIGHT * 0.5)
        angle_3_label.scale(0.8)

        # Angle 1 + Angle 3 = 90 Degrees
        self.play(
            ShowCreation(angle_3),
            ShowCreation(angle_3_label),
            Write(proof_text[3][1]),
            run_time=1.5
        )

        self.wait()

        # Angle 2 = Angle 3
        self.play(
            Write(proof_text[3][2]),
            run_time=1.5
        )

        self.wait()

        # Uncreate the others and put "Angle 2 = Angle 3" above
        self.play(
            Uncreate(proof_text[3][0]),
            Uncreate(proof_text[3][1]),
            run_time=1.5
        )

        self.wait(0.5)

        self.play(
            proof_text[3][2].animate.shift(UP * 1.4),
            run_time=1.5
        )

        self.wait()

        # OP = OQ
        self.play(Write(proof_text[4]), run_time=1.5)

        self.wait()

        # Text transform
        # Create a VGroup for adding bracket to the conditions
        cond_group = VGroup(
            proof_text[2],
            proof_text[3],
            proof_text[4]
        )
        proof_text[5].move_to(cond_group)

        self.play(
            TransformMatchingParts(cond_group, proof_text[5]),
            run_time=1.5
        )
        self.wait()

        proof_text[6].next_to(proof_text[5], DOWN)
        self.play(Write(proof_text[6]), run_time=1.5)

        self.wait(2)

        # Uncreate all except "\\triangle QIO \\cong \\triangle OHP \\ (AAS)"
        for i, item in enumerate(proof_text):
            if not i == 6 and not 2 <= i <= 4:
                self.play(Uncreate(proof_text[i]), run_time=0.2)

        self.play(proof_text[6].animate.move_to(proof_text[0]))

        cond_1 = Tex("QI = OH", tex_to_color_map={"QI": GREEN, "OH": RED})
        cond_2 = Tex("OI = PH", tex_to_color_map={"OI": GREEN, "PH": RED})

        cond_1.next_to(proof_text[6], DOWN)
        cond_2.next_to(cond_1, DOWN)

        self.wait(2)

        self.play(
            Write(cond_1),
            Write(cond_2)
        )

        exps = Tex(
            """
                \\begin{cases}
                    nq = p \\\\
                    -q = mp
                \\end{cases}
            """,
            color=TEAL
        )
        exp_1 = Tex("nq = p", tex_to_color_map={"nq": YELLOW_B, "p": BLUE_B})
        exp_2 = Tex("-q = mp", tex_to_color_map={"q": YELLOW_B, "mp": BLUE_B})

        exps.next_to(cond_2, DOWN * 2)

        self.wait(2)

        self.play(Write(exps))

        self.wait(3)

        # Create a screen rectangle covering the screen for texting
        cover = FullScreenRectangle()
        self.play(ShowCreation(cover), run_time=3)

        # Text Transform
        exps = exps.copy()
        exps.to_corner(UL)
        exps.shift(FRAME_WIDTH * (1 - phi) * RIGHT)
        self.play(Write(exps))

        exp_2.next_to(exps, DOWN)
        self.play(Write(exp_2))

        self.wait()

        exp_2_transformed = Tex("q = -mp", tex_to_color_map={"q": YELLOW_B, "mp": BLUE_B})
        exp_2_transformed.next_to(exp_2, DOWN)
        self.play(Write(exp_2_transformed))

        exp_group = VGroup(
            exp_1,
            Tex("n(-mp) = p", tex_to_color_map={"n": TEAL, "m": TEAL, "p": BLUE_B}),
            Tex("-mnp = p", tex_to_color_map={"n": TEAL, "m": TEAL, "p": BLUE_B}),
            Tex("-mn = 1", tex_to_color_map={"mn": BLUE_B}),
            Tex("\\therefore mn = -1 \\quad \\blacksquare", tex_to_color_map={"mn": BLUE_B})
        )

        exp_group.arrange(DOWN)
        exp_group.next_to(exp_2_transformed, DOWN * 2)
        align_tex_group_to_left(exp_group)
        exp_group.shift(0.5 * LEFT)

        self.animate_through(exp_group, 2.5)

        # Fade out all
        self.wait(3)
        self.play(
            FadeOut(exps),
            FadeOut(exp_2),
            FadeOut(exp_2_transformed),
            FadeOut(exp_group),
            run_time=1.5
        )

    # Ending
    def end(self):
        central_text = VGroup(
            TexText("Thanks for watching!", font_size=95, color=YELLOW_B),
            TexText("Presented by 歌迷就好"),
            TexText(
                "Powered by ManimGL v1.3.0",
                tex_to_color_map={"ManimGL": BLUE_B, "v1.3.0": YELLOW_B}
            )
        )
        central_text.arrange(DOWN)
        central_text.to_edge(TOP)
        central_text.shift(DOWN)

        self.animate_through(central_text, 0.3)

        self.wait(2)
