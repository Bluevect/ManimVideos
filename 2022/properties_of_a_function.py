from manimlib import *
from os import system

to_isolate = ["y", "ax", "b", r"\frac cx"]

t2c_map_tex = {
    "+": WHITE,
    "=": WHITE,
    "y": BLUE_B,
    "ax": YELLOW_B,
    r"\frac cx": TEAL,
    r"\frac 1x": TEAL,
    "b": GREEN_B,
    r"\frac 32": GREEN_B,
}

t2c_map_tex_multi_y = {
    "+": WHITE,
    "=": WHITE,
    "ax": YELLOW_B,
    r"\frac cx": TEAL,
    r"\frac 1x": TEAL,
    "b": GREEN_B,
    r"\frac 32": GREEN_B,
    "y_1": YELLOW_B,
    "y_2": GREEN_B,
    "y_3": TEAL
}

t2c_map = {
    "$a$": YELLOW_B,
    "$b$": GREEN_B,
    "$c$": TEAL,
    "$y_1$": YELLOW_B,
    "$y_3$": TEAL,
    "$x < 0$": RED_B,
    "$x > 0$": RED_B,
    "最大值": RED_B,
    "最小值": RED_B,
    "形状": RED_B,
    "位置": RED_B,
    "正比例函数": RED_B,
    "反比例函数": RED_B,
    "常数函数": RED_B,
    "$b = 0$": GREEN_B,
    "$x_1$": YELLOW_B,
    "$x_2$": YELLOW_B
}

func = Tex(
    r"y = ax + b + \frac cx",
    tex_to_color_map=t2c_map_tex,
    isolate=[*to_isolate]
).to_corner(UL)

# Create a 4x4 (1 unit length) coordinate
axes = Axes(
    x_range=(-4, 4),
    y_range=(-4, 4),
    width=6,
    height=6,

    axis_config={
        "stroke_color": WHITE,
        "stroke_range": 3
    },

    y_axis_config={
        "numbers_to_exclude": [0]
    }
)

axes.add_coordinate_labels(font_size=20)

function_graph = axes.get_graph(
    # y = x - 0.25 + \frac 1x
    lambda x: x - 0.25 + 1 / x,
    color=BLUE_B,
    discontinuities=[0]
)

function_label = axes.get_graph_label(
    function_graph,
    r"y = ax + b + \frac cx"
)

function_label.shift(LEFT * 2.8 + DOWN * 2)


def align_group(text_group):
    for i, item in enumerate(text_group):
        if not i == 0:
            item.next_to(text_group[i - 1], DOWN, aligned_edge=LEFT)


class Main(Scene):
    # For change_tex()
    current_tex = None

    # Change TexText by ReplacementTransform in DL
    def change_tex(self, tex_str, run_time, waiting_time):
        updated_tex = TexText(tex_str, tex_to_color_map=t2c_map)
        updated_tex.to_corner(DL)
        self.play(
            ReplacementTransform(self.current_tex, updated_tex),
            run_time=run_time
        )
        self.wait(waiting_time)
        self.current_tex = updated_tex

    # Write all mobjects in a VGroup
    def animate_through(self, group, waiting_time):
        for i in group:
            self.play(
                Write(i),
                run_time=1.5
            )

            self.wait(waiting_time)

    # The entry of animation
    def construct(self):
        self.wait()
        self.start()
        self.observe()
        self.solve_for_min_or_max_value()
        self.show_formula()
        self.end()

    def start(self):
        explore = TexText("探究一类函数的性质", color=BLUE_B, font_size=65)
        func_large = Tex(
            r"y = ax + b + \frac cx",
            font_size=75,
            tex_to_color_map={
                "y": BLUE_B,
                "ax": YELLOW_B,
                r"\frac cx": TEAL,
                "b": GREEN_B
            }
        )
        explore.shift(UP)
        func_large.next_to(explore, DOWN * 3)

        self.play(Write(explore))
        self.wait(0.5)
        self.play(Write(func_large))
        self.wait(2)

        self.play(
            Uncreate(explore),
            Uncreate(func_large)
        )

    def observe(self):
        # Base
        self.wait()
        self.play(ShowCreation(axes))

        self.play(
            ShowCreation(function_graph),
            ShowCreation(function_label)
        )

        self.wait()

        # Move label to corner, coordinate to right edge
        function_label_isolated = Tex(
            r"y = ax + b + \frac cx", color=BLUE_B, isolate=[*to_isolate]
        )
        function_label_isolated.replace(function_label)
        function_label_isolated.match_style(function_label)
        self.remove(function_label)

        self.play(
            TransformMatchingTex(function_label_isolated, func)
        )
        self.play(
            VGroup(axes, function_graph).animate.to_edge(RIGHT)
        )

        # Show some text
        change_value = TexText(
            r"改变 $a$, $b$, $c$ 的值, \\ 观察函数图像",
            tex_to_color_map={
                "$a$": YELLOW_B,
                "$b$": GREEN_B,
                "$c$": TEAL
            }
        )
        change_value.to_corner(DL)
        self.play(Write(change_value))

        # Create a box group with values
        values_group = VGroup(
            VGroup(
                Tex("a = ", color=YELLOW_B),
                DecimalNumber(
                    1, num_decimal_places=2, color=YELLOW_B,
                    font_size=40, include_sign=True
                )
            ),
            VGroup(
                Tex("b = ", color=GREEN_B),
                DecimalNumber(
                    -0.25, num_decimal_places=2, color=GREEN_B,
                    font_size=40, include_sign=True
                )
            ),
            VGroup(
                Tex("c = ", color=TEAL),
                DecimalNumber(
                    1, num_decimal_places=2, color=TEAL,
                    font_size=40, include_sign=True
                )
            )
        )
        num_a = values_group[0][1]
        num_b = values_group[1][1]
        num_c = values_group[2][1]

        for item in values_group:
            item.arrange(RIGHT)

        values_group.arrange(DOWN)
        values_group.next_to(func, DOWN * 2)

        # Create a border for values_group using Rectangle()
        border = Rectangle()
        border.set_stroke(color=GOLD)
        border.set_width(values_group.get_width())
        border.set_height(values_group.get_height() + 0.25)
        border.move_to(values_group)

        # Show the value box and the border
        self.play(
            ShowCreation(values_group),
            DrawBorderThenFill(border)
        )

        self.wait(2)

        # Change values
        self.current_tex = change_value
        self.change_tex(r"改变 $a$", 1, 2)

        # Change "a" from 1 to 2
        function_graph_previous = function_graph

        # Replace previous graph with updated graph every loop
        for i in range(1, 101):
            a = 1 + i / 100

            # Update the DecimalNumber
            num_a.set_value(a)

            # Create updated graph
            function_graph_temp = axes.get_graph(
                lambda x: a * x - 0.25 + 1 / x, color=BLUE_B, discontinuities=[0]
            )

            # Animate
            self.play(
                ReplacementTransform(function_graph_previous, function_graph_temp),
                run_time=0.001
            )
            function_graph_previous = function_graph_temp

        self.wait(3)

        # Show some text
        self.change_tex(
            r"当 $a$, $c$ $ > 0$ 时, \\ $y$ 轴左边发生最大值 \\ $y$ 轴右边发生最小值",
            1, 2
        )
        self.play(Indicate(num_a), Indicate(num_c))
        self.wait(6)
        self.change_tex(r"改变 $a$", 1, 2)

        # Change "a" from 2 to -1
        # Duplicated code, it's inefficient and complicated to package into a function :(
        for i in range(1, 301):
            a = 2 - i / 100
            num_a.set_value(a)

            function_graph_temp = axes.get_graph(
                lambda x: a * x - 0.25 + 1 / x, color=BLUE_B, discontinuities=[0]
            )

            self.play(
                ReplacementTransform(function_graph_previous, function_graph_temp),
                run_time=0.001
            )
            function_graph_previous = function_graph_temp

        self.wait(3)

        # Show some text
        self.change_tex(
            r"当 $a$, $c$ 异号时, \\ 不发生极值",
            1, 2
        )
        self.play(Indicate(num_a), Indicate(num_c))
        self.wait(6)
        self.change_tex(r"改变 $c$", 1, 2)

        # Change "c" from 1 to 2
        for i in range(1, 101):
            c = 1 + i / 100
            num_c.set_value(c)

            function_graph_temp = axes.get_graph(
                lambda x: -x - 0.25 + c / x, color=BLUE_B, discontinuities=[0]
            )

            self.play(
                ReplacementTransform(function_graph_previous, function_graph_temp),
                run_time=0.001
            )
            function_graph_previous = function_graph_temp

        self.wait(2)

        # Change "c" from 2 to -1
        for i in range(1, 301):
            c = 2 - i / 100
            num_c.set_value(c)

            function_graph_temp = axes.get_graph(
                lambda x: -x - 0.25 + c / x, color=BLUE_B, discontinuities=[0]
            )

            self.play(
                ReplacementTransform(function_graph_previous, function_graph_temp),
                run_time=0.001
            )
            function_graph_previous = function_graph_temp

        self.wait(3)

        # Show some text
        self.change_tex(
            r"当 $a$, $c$ $ < 0$ 时, \\ $y$ 轴左边发生最小值 \\ $y$ 轴右边发生最大值",
            1, 2
        )
        self.play(Indicate(num_a), Indicate(num_c))
        self.wait(6)
        self.change_tex(r"改变 $b$", 1, 2)

        # Change "b" from -0.25 to -1.25
        for i in range(1, 101):
            b = -0.25 - i / 100
            num_b.set_value(b)

            function_graph_temp = axes.get_graph(
                lambda x: -x + b - 1 / x, color=BLUE_B, discontinuities=[0]
            )

            self.play(
                ReplacementTransform(function_graph_previous, function_graph_temp),
                run_time=0.001
            )
            function_graph_previous = function_graph_temp

        self.wait()

        # Change "b" from -1.25 to 0.75
        for i in range(1, 201):
            b = -1.25 + i / 100
            num_b.set_value(b)

            function_graph_temp = axes.get_graph(
                lambda x: -x + b - 1 / x, color=BLUE_B, discontinuities=[0]
            )

            self.play(
                ReplacementTransform(function_graph_previous, function_graph_temp),
                run_time=0.001
            )
            function_graph_previous = function_graph_temp

        self.wait()

        # Change "b" from 0.75 to -0.25
        for i in range(1, 101):
            b = 0.75 - i / 100
            num_b.set_value(b)

            function_graph_temp = axes.get_graph(
                lambda x: -x + b - 1 / x, color=BLUE_B, discontinuities=[0]
            )

            self.play(
                ReplacementTransform(function_graph_previous, function_graph_temp),
                run_time=0.001
            )
            function_graph_previous = function_graph_temp

        # Show some text
        self.change_tex(
            r"$a$, $c$ 决定函数的形状及位置 \\ $b$ 决定函数的位置",
            1, 2
        )
        self.play(Indicate(num_a), Indicate(num_b), Indicate(num_c))
        self.wait(6)

        # Create a screen rectangle covering the screen for texting
        cover = FullScreenRectangle()
        self.play(ShowCreation(cover), run_time=3)

        # Show some text
        min_and_max = VGroup(
            TexText(
                r"当 $a$, $c$ 同号时, 函数发生极值",
                tex_to_color_map=t2c_map
            ),
            TexText(
                r"当 $a$, $c$ $ < 0$ 时",
                tex_to_color_map=t2c_map
            ),
            TexText(
                r"$x < 0$ 时发生极小值",
                tex_to_color_map=t2c_map
            ),
            TexText(
                r"$x > 0$ 时发生极大值",
                tex_to_color_map=t2c_map
            ),
            TexText(
                r"当 $a$, $c$ $ > 0$ 时",
                tex_to_color_map=t2c_map
            ),
            TexText(
                r"$x < 0$ 时发生极大值",
                tex_to_color_map=t2c_map
            ),
            TexText(
                r"$x > 0$ 时发生极小值",
                tex_to_color_map=t2c_map
            ),
            TexText(
                r"当 $a$, $c$ 异号时, 函数不发生极值",
                tex_to_color_map=t2c_map
            )
        )

        min_and_max.arrange(DOWN)
        min_and_max.to_corner(UL)

        # Set indent and position
        for i, tex_text in enumerate(min_and_max):
            tex_text.to_edge(LEFT)
            if i > 0 and not i == 7:
                tex_text.shift(RIGHT)
                if 2 <= i <= 3 or 5 <= i <= 6:
                    tex_text.shift(RIGHT)

        self.animate_through(min_and_max, 1)
        self.wait(7)
        self.play(FadeOut(min_and_max))

    def solve_for_min_or_max_value(self):
        # Show some text
        question = TexText("那么如何求出极值呢？").to_corner(DL)
        self.play(Write(question))
        self.wait(2)

        # Show some text
        self.current_tex = question

        func_specific = Tex(
            r"y = x + \frac 32 + \frac 1x",
            tex_to_color_map=t2c_map_tex,
            color=YELLOW_B,
            isolate=[*to_isolate]
        ).to_corner(UL)

        self.change_tex(r"讨论一个具体的函数", 1, 0)
        self.play(Write(func_specific))

        # Base
        axes_base = Axes(
            x_range=(-4, 4),
            y_range=(-4, 4),
            width=6,
            height=6,

            axis_config={
                "stroke_color": WHITE,
                "stroke_range": 3
            },

            y_axis_config={
                "numbers_to_exclude": [0]
            }
        )

        axes_base.add_coordinate_labels(font_size=20)

        func_graph_specific = axes_base.get_graph(
            lambda x: x + 1.5 + 1 / x,
            color=BLUE_B,
            discontinuities=[0]
        )

        self.play(
            ShowCreation(axes_base),
            ShowCreation(func_graph_specific)
        )
        self.wait(0.5)
        self.play(
            VGroup(axes_base, func_graph_specific).animate.to_edge(RIGHT)
        )
        self.wait()

        self.change_tex(r"由于函数由 \\ 正比例函数、反比例函数 \\ 和常数函数相加得到", 1, 2)

        # Proportional function
        prop_func = Tex("y_1", "= x", tex_to_color_map=t2c_map_tex_multi_y, color=YELLOW_B)
        # Constant function
        const_func = Tex("y_2", r"= \frac 32", tex_to_color_map=t2c_map_tex_multi_y)
        # Inverse proportional function
        inv_prop_func = Tex("y_3", r"= \frac 1x", tex_to_color_map=t2c_map_tex_multi_y)

        prop_func.next_to(func, DOWN, aligned_edge=LEFT)
        const_func.next_to(prop_func, DOWN, aligned_edge=LEFT)
        inv_prop_func.next_to(const_func, DOWN, aligned_edge=LEFT)

        self.play(
            Write(prop_func),
            Write(const_func),
            Write(inv_prop_func)
        )
        self.wait(3)

        # Show expression
        exp = Tex(
            "y", "=", "y_1", "+", "y_2", "+", "y_3",
            color=BLUE_B,
            tex_to_color_map=t2c_map_tex_multi_y
        ).to_corner(DL)

        self.play(ReplacementTransform(self.current_tex, exp[0]))
        self.play(Write(exp[1]))
        self.play(ReplacementTransform(prop_func[0].copy(), exp[2]))
        self.play(Write(exp[3]))
        self.play(ReplacementTransform(const_func[0].copy(), exp[4]))
        self.play(Write(exp[5]))
        self.play(ReplacementTransform(inv_prop_func[0].copy(), exp[6]))

        self.wait()
        self.play(ShowCreationThenDestructionAround(exp))
        self.wait(2)
        self.play(FadeOut(exp))

        # Show some text
        self.current_tex = TexText(r"画出函数图像").to_corner(DL)
        self.play(Write(self.current_tex))
        self.wait()

        # Draw graphs
        prop_func_graph = axes_base.get_graph(lambda x: x, color=YELLOW_B)
        const_func_graph = axes_base.get_graph(lambda x: 1.5, color=GREEN_B)
        inv_prop_func_graph = axes_base.get_graph(
            lambda x: 1 / x if not x == 0 else 10, color=TEAL, discontinuities=[0])
        # Prevent runtime error (Divide by 0)

        self.play(ShowCreationThenDestructionAround(prop_func))
        self.play(ShowCreation(prop_func_graph))
        self.wait()
        self.play(ShowCreationThenDestructionAround(const_func))
        self.play(ShowCreation(const_func_graph))
        self.wait()
        self.play(ShowCreationThenDestructionAround(inv_prop_func))
        self.play(ShowCreation(inv_prop_func_graph))
        self.wait()

        # Show some text
        self.change_tex(r"简化 \\ 使 $b = 0$", 1, 1)

        # Set b = 0
        zero_func = Tex(
            "y_2", " = 0",
            tex_to_color_map={
                "0": GREEN_B,
                **t2c_map_tex_multi_y
            }
        ).next_to(prop_func, DOWN, aligned_edge=LEFT)
        func_specific_zeroed = Tex(
            r"y = x + \frac 1x",
            tex_to_color_map=t2c_map_tex,
            color=YELLOW_B,
            isolate=[*to_isolate]
        ).to_corner(UL)
        func_graph_specific_zeroed = axes_base.get_graph(
            lambda x: x + 1 / x if not x == 0 else 10,  # Prevent runtime error (Divide by 0)
            color=BLUE_B,
            discontinuities=[0]
        )

        self.play(
            ReplacementTransform(const_func, zero_func),
            ReplacementTransform(func_specific, func_specific_zeroed),
            ReplacementTransform(func_graph_specific, func_graph_specific_zeroed),
            inv_prop_func.animate.next_to(zero_func, DOWN, aligned_edge=LEFT),
            FadeOut(const_func_graph, DOWN)
        )

        # Show some text
        self.change_tex("观察函数图像", 1, 2)

        # Show dots
        dot_from_prop_func = Dot(color=RED).move_to(axes_base.i2gp(-3, prop_func_graph))
        dot_from_inv_prop_func = Dot(color=RED).move_to((axes_base.i2gp(-3, inv_prop_func_graph)))
        dot_from_func = Dot(color=RED).move_to(axes_base.i2gp(-3, func_graph_specific_zeroed))
        self.play(
            ShowCreation(dot_from_prop_func),
            ShowCreation(dot_from_inv_prop_func),
            ShowCreation(dot_from_func)
        )

        # Move dots
        x_tracker = ValueTracker(-3)
        f_always(
            dot_from_prop_func.move_to,
            lambda: axes_base.i2gp(x_tracker.get_value(), prop_func_graph)
        )
        f_always(
            dot_from_inv_prop_func.move_to,
            lambda: axes_base.i2gp(x_tracker.get_value(), inv_prop_func_graph)
        )
        f_always(
            dot_from_func.move_to,
            lambda: axes_base.i2gp(x_tracker.get_value(), func_graph_specific_zeroed)
        )

        self.play(x_tracker.animate.set_value(2), run_time=3)
        self.play(x_tracker.animate.set_value(0.5), run_time=3)
        self.play(x_tracker.animate.set_value(-2.5), run_time=3)

        # Show some text
        self.change_tex("$y_1$ 与 $y_3$ 的交点处发生极值", 1, 1)

        # Move dots
        self.play(x_tracker.animate.set_value(-1), run_time=2)
        self.play(
            Flash(dot_from_func, color=YELLOW_B),
            Flash(dot_from_prop_func, color=YELLOW_B),
            # Flash(dot_from_inv_prop_func, color=YELLOW_B)
        )
        self.wait()
        self.play(x_tracker.animate.set_value(1), run_time=2)
        self.play(
            Flash(dot_from_func, color=YELLOW_B),
            Flash(dot_from_prop_func, color=YELLOW_B),
            # Flash(dot_from_inv_prop_func, color=YELLOW_B)
        )
        self.wait()

        # Show some text
        equation = Tex(r"x = \frac 1x", color=YELLOW_B, tex_to_color_map=t2c_map_tex).to_corner(DL)
        self.play(ReplacementTransform(self.current_tex, equation))
        self.wait(3)

        solution = Tex(
            r"x_1 = 1,\ x_2 = -1",
            color=YELLOW_B,
            tex_to_color_map={
                "x_1": BLUE_B,
                "x_2": BLUE_B,
                "=": WHITE
            }
        ).to_corner(DL)
        self.play(ReplacementTransform(equation, solution))
        self.wait(2)

        # Show the result
        self.play(FadeOut(solution))

        map_temp = {
            "y_{min}": BLUE_B,
            "y_{max}": BLUE_B,
            "(x > 0)": RED,
            "(x < 0)": RED,
            r"-\frac 12": YELLOW_B,
            r"\frac 72": YELLOW_B
        }

        results = VGroup(
            Tex(r"(x < 0)\ y_{max}", "=", "-1",
                r"\times", "2", "=", "-2", tex_to_color_map=map_temp),

            Tex(r"(x > 0)\ y_{min}", "=", "1",
                r"\times", "2", "=", "2", tex_to_color_map=map_temp)
        )
        results.arrange(DOWN)
        results.to_corner(DL)
        results[1].next_to(results[0], DOWN, aligned_edge=LEFT)

        self.play(Write(results[1]))

        h_line_from_prop_func = always_redraw(
            lambda: axes_base.get_h_line(dot_from_prop_func.get_center(), color=RED))
        h_line_from_func = always_redraw(
            lambda: axes_base.get_h_line(dot_from_func.get_center(), color=RED))
        self.play(
            ShowCreation(h_line_from_prop_func),
            ShowCreation(h_line_from_func),
            run_time=2
        )

        self.wait(2)
        self.play(
            ShowCreationThenDestructionAround(results[1][3]),
            Flash(dot_from_prop_func),
            run_time=1.5
        )
        self.play(
            ShowCreationThenDestructionAround(results[1][len(results[1]) - 1]),
            Flash(dot_from_func),
            run_time=1.5
        )

        self.wait(2)
        self.play(Write(results[0]))
        self.play(x_tracker.animate.set_value(-1), run_time=3)
        self.play(
            ShowCreationThenDestructionAround(results[0][3]),
            Flash(dot_from_prop_func),
            run_time=1.5
        )
        self.play(
            ShowCreationThenDestructionAround(results[0][len(results[0]) - 1]),
            Flash(dot_from_func),
            run_time=1.5
        )

        # Fade out dots and lines
        self.play(
            FadeOut(dot_from_func),
            FadeOut(dot_from_prop_func),
            FadeOut(dot_from_inv_prop_func),
            FadeOut(h_line_from_prop_func),
            FadeOut(h_line_from_func)
        )

        # Add the constant back
        results_with_constant = VGroup(
            Tex(r"(x < 0)\ y_{max}", "=", "-1",
                r"\times", "2", "+", r"\frac 32", "=", r"-\frac 12", tex_to_color_map=map_temp),

            Tex(r"(x > 0)\ y_{min}", "=", "1",
                r"\times", "2", "+", r"\frac 32", "=", r"\frac 72", tex_to_color_map=map_temp)
        )
        results_with_constant.arrange(DOWN)
        results_with_constant.to_corner(DL)
        results_with_constant[1].next_to(results_with_constant[0], DOWN, aligned_edge=LEFT)

        add_the_constant_back = TexText("加回常数项").to_edge(UP)
        self.play(Write(add_the_constant_back))
        self.wait()

        # Redefine variables for back transformation
        func_specific = Tex(
            r"y = x + \frac 32 + \frac 1x",
            tex_to_color_map=t2c_map_tex,
            color=YELLOW_B,
            isolate=[*to_isolate]
        ).to_corner(UL)

        const_func = Tex("y_2", r"= \frac 32", tex_to_color_map=t2c_map_tex_multi_y) \
            .next_to(prop_func, DOWN, aligned_edge=LEFT)

        func_graph_specific = axes_base.get_graph(
            # Prevent runtime error (Divide by 0)
            lambda x: x + 1.5 + 1 / x if not x == 0 else 10,
            color=BLUE_B,
            discontinuities=[0]
        )

        # Transform back
        self.play(
            ReplacementTransform(func_specific_zeroed, func_specific),
            ReplacementTransform(zero_func, const_func),
            ReplacementTransform(func_graph_specific_zeroed, func_graph_specific),
            prop_func.animate.next_to(func_specific, DOWN, aligned_edge=LEFT),
            # const_func.animate.next_to(prop_func, DOWN, aligned_edge=LEFT),
            inv_prop_func.animate.next_to(const_func, DOWN, aligned_edge=LEFT),
            ShowCreation(const_func_graph)
        )

        # Transform results
        self.play(
            TransformMatchingTex(results[0], results_with_constant[0]),
            TransformMatchingTex(results[1], results_with_constant[1]),
            run_time=2
        )

        # Indicate dots and text
        dot_from_func = Dot(color=RED).move_to(axes_base.i2gp(-1, func_graph_specific))
        x_tracker = ValueTracker(-1)
        f_always(
            dot_from_func.move_to,
            lambda: axes_base.i2gp(x_tracker.get_value(), func_graph_specific)
        )

        self.play(
            ShowCreation(dot_from_func)
        )

        self.play(
            ShowCreationThenDestructionAround(
                results_with_constant[0][len(results_with_constant[0]) - 1]),
            Flash(dot_from_func),
            run_time=1.5
        )
        self.wait(2)
        self.play(x_tracker.animate.set_value(1), run_time=3)
        self.play(
            ShowCreationThenDestructionAround(
                results_with_constant[1][len(results_with_constant[1]) - 1]),
            Flash(dot_from_func),
            run_time=1.5
        )
        self.wait(4)

        # Fade out everything
        self.play(FadeOut(add_the_constant_back, UP))
        self.play(
            FadeOut(
                VGroup(
                    axes_base, func_graph_specific,
                    prop_func_graph, const_func_graph, inv_prop_func_graph, dot_from_func
                ), RIGHT),
            run_time=1.5
        )
        left_group = VGroup(
            func_specific, prop_func, const_func, inv_prop_func, results_with_constant)
        for i, item in enumerate(left_group):
            self.play(FadeOut(item, LEFT), run_time=0.2 + i / 20)

    def show_formula(self):
        # Show some text
        text_group_left = VGroup(
            TexText("对于发生极值的此类函数", tex_to_color_map=t2c_map),
            Tex(
                r"y = ax + b + \frac cx",
                tex_to_color_map=t2c_map_tex,
                isolate=[*to_isolate]
            ),
            TexText("联立"),
            Tex("a", "x", "=", r"\frac cx", color=YELLOW_B,
                tex_to_color_map={r"\frac cx": TEAL, "=": WHITE})
        )
        text_group_left[0].to_corner(UL)
        align_group(text_group_left)

        self.animate_through(text_group_left, 1)
        self.wait()

        # Solve animation
        exp_to_solve = text_group_left[3].copy()
        self.play(exp_to_solve.animate.shift(5 * RIGHT))

        squared = Tex("a", "x^2", "=", "c", tex_to_color_map={
            "a": YELLOW_B,
            "x^2": YELLOW_B,
            "c": TEAL
        }).move_to(exp_to_solve)
        self.play(
            TransformMatchingTex(
                exp_to_solve, squared,
                key_map={"x": "x^2", r"\frac cx": "c"}
            )
        )
        self.wait()

        moved = Tex("x", "^2", "=", r"\frac ca", tex_to_color_map={
            "x": YELLOW_B,
            "^2": YELLOW_B,
            r"\frac ca": TEAL
        }).move_to(squared)
        self.play(
            TransformMatchingTex(
                squared, moved,
                key_map={"a": r"\frac ca"},
                path_arc=90 * DEGREES
            )
        )

        final = Tex("x", "=", r"\pm", r"\sqrt", r"{\frac ca}", color=GREEN_B, tex_to_color_map={
            "x": YELLOW_B,
            r"{\frac ca}": TEAL,
            "=": WHITE
        }).move_to(moved)
        self.play(
            TransformMatchingTex(
                moved, final,
                key_map={"^2": r"\sqrt"}
            )
        )

        text_group_left_extra = VGroup(
            TexText("得"),
            final.copy()
        )
        text_group_left_extra[0].next_to(text_group_left[3], DOWN, aligned_edge=LEFT)
        align_group(text_group_left_extra)

        self.play(Write(text_group_left_extra[0]))
        self.play(ReplacementTransform(final, text_group_left_extra[1]))

        x_solution = Tex(
            "x_1", "=", r"\sqrt", r"{\frac ca}", r"\quad ", "x_2", "=", "-", r"\sqrt", r"{\frac ca}",
            color=GREEN_B, tex_to_color_map={
                "x_1": YELLOW_B,
                "x_2": YELLOW_B,
                r"{\frac ca}": TEAL,
                "=": WHITE
            }).next_to(text_group_left_extra[0], DOWN, aligned_edge=LEFT)
        self.play(TransformMatchingTex(text_group_left_extra[1], x_solution))
        self.wait()

        result_text = TexText("则 $x_1$, $x_2$ 处发生极值", tex_to_color_map=t2c_map) \
            .next_to(x_solution, DOWN, aligned_edge=LEFT)
        self.play(Write(result_text))
        self.wait()

        # Show the line
        top = text_group_left[0].get_right() + RIGHT + 0.5 * UP
        line = Line(top, top + 7.5 * DOWN)
        self.play(ShowCreation(line))

        # Show some text
        text_group_right = VGroup(
            TexText("极值"),
            Tex(
                "y", "=", "2", "a", "x", "+", "b", color=GREEN_B,
                tex_to_color_map=t2c_map_tex
            ),
            Tex(
                "y", "=", r"\pm", "2", "a", r"\sqrt", r"{\frac ca}", "+", "b", color=GREEN_B,
                tex_to_color_map={**t2c_map_tex, "2": GREEN_B, r"{\frac ca}": TEAL}
            ),
            Tex(
                "y", "=", r"\pm", "2", "a", r"\frac {\sqrt {ac}}{a}", "+", "b", color=GREEN_B,
                tex_to_color_map={**t2c_map_tex, r"\frac {\sqrt {ac}}{a}": TEAL}
            ),
            Tex(
                "y", "=", r"\pm", "2", r"\sqrt {ac}", "+", "b", color=GREEN_B,
                tex_to_color_map={**t2c_map_tex, r"\sqrt {ac}": TEAL}
            ),
            Tex(
                "y_1", "=", "2", r"\sqrt {ac}", "+", "b", color=GREEN_B,
                tex_to_color_map={**t2c_map_tex_multi_y, r"\sqrt {ac}": TEAL}
            ),
            Tex(
                "y_2", "=", "-2", r"\sqrt {ac}", "+", "b", color=GREEN_B,
                tex_to_color_map={"y_2": YELLOW_B, r"\sqrt {ac}": TEAL, "=": WHITE, "+": WHITE}
            )
        )
        text_group_right[0].next_to(text_group_left, RIGHT * 6, aligned_edge=UP)
        align_group(text_group_right)
        self.play(Write(text_group_right[0]))
        self.play(Write(text_group_right[1][0]))
        self.play(Write(text_group_right[1][1]))

        # Show the coordinate temporarily
        axes_temp = Axes(
            x_range=(-4, 4),
            y_range=(-4, 4),
            width=6,
            height=6,

            axis_config={
                "stroke_color": WHITE,
                "stroke_range": 3
            },

            y_axis_config={
                "numbers_to_exclude": [0]
            }
        )
        axes_temp.add_coordinate_labels(font_size=20)

        self.play(ShowCreation(axes_temp.to_corner(DR).scale(0.9)))
        func_graph = axes_temp.get_graph(
            # Prevent runtime error (Divide by 0)
            lambda x: x + 1.5 + 1 / x if not x == 0 else 10,
            color=BLUE_B,
            discontinuities=[0]
        )
        func_graph_zeroed = axes_temp.get_graph(
            # Prevent runtime error (Divide by 0)
            lambda x: x + 1 / x if not x == 0 else 10,
            color=BLUE_B,
            discontinuities=[0]
        )
        prop_func_graph = axes_temp.get_graph(lambda x: x, color=YELLOW_B)
        inv_prop_func_graph = axes_temp.get_graph(
            lambda x: 1 / x if not x == 0 else 10, color=TEAL, discontinuities=[0])
        self.play(
            ShowCreation(func_graph),
            ShowCreation(prop_func_graph),
            ShowCreation(inv_prop_func_graph)
        )
        self.wait()
        self.play(ReplacementTransform(func_graph, func_graph_zeroed))

        dot_from_prop_func = Dot(color=RED).move_to(axes_temp.i2gp(1, prop_func_graph))
        dot_from_func_zeroed = Dot(color=RED).move_to(axes_temp.i2gp(1, func_graph_zeroed))
        dot_from_func = Dot(color=RED).move_to(axes_temp.i2gp(1, func_graph))

        self.play(ShowCreation(dot_from_prop_func))
        self.play(
            ReplacementTransform(dot_from_prop_func.copy(), text_group_right[1][3]),
            ReplacementTransform(dot_from_prop_func.copy(), text_group_right[1][4])
        )
        self.play(
            ReplacementTransform(dot_from_prop_func, dot_from_func_zeroed),
            Write(text_group_right[1][2])
        )
        self.wait()

        self.play(Write(text_group_right[1][5]))
        func_graph = axes_temp.get_graph(
            # Prevent runtime error (Divide by 0)
            lambda x: x + 1.5 + 1 / x if not x == 0 else 10,
            color=BLUE_B,
            discontinuities=[0]
        )
        self.play(
            ReplacementTransform(func_graph_zeroed, func_graph),
            ReplacementTransform(dot_from_func_zeroed, dot_from_func),
            Write(text_group_right[1][6])
        )
        self.wait()
        self.play(
            ShowCreationThenDestructionAround(text_group_right[1]),
            Flash(dot_from_func)
        )

        self.play(
            Uncreate(axes_temp),
            Uncreate(func_graph),
            Uncreate(prop_func_graph),
            Uncreate(inv_prop_func_graph),
            Uncreate(dot_from_func),
            run_time=2
        )
        self.wait()

        self.play(ShowCreationThenDestructionAround(x_solution), run_time=2)
        self.wait()
        self.play(
            TransformMatchingTex(
                text_group_right[1].copy(), text_group_right[2],
                key_map={"x": r"{\frac ca}"}
            ),
            run_time=2
        )
        self.wait()

        self.play(
            TransformMatchingTex(
                text_group_right[2].copy(), text_group_right[3],
                key_map={r"{\frac ca}": r"\frac {\sqrt {ac}}{a}"}
            ),
            run_time=2
        )
        self.wait()

        self.play(
            TransformMatchingTex(
                text_group_right[3].copy(), text_group_right[4],
                key_map={r"\frac {\sqrt {ac}}{a}": r"\sqrt {ac}"}
            ),
            run_time=2
        )
        self.play(ShowCreationThenDestructionAround(text_group_right[4]))
        self.wait()

        self.play(
            TransformMatchingTex(text_group_right[4].copy(), text_group_right[5])
        )
        self.play(
            TransformMatchingTex(text_group_right[4].copy(), text_group_right[6])
        )
        self.play(
            ShowCreationThenDestructionAround(text_group_right[5]),
            ShowCreationThenDestructionAround(text_group_right[6])
        )
        self.wait(4)

        # Fade out everything
        self.play(FadeOut(text_group_left, LEFT), run_time=0.2)
        self.play(FadeOut(text_group_left_extra[0], LEFT), run_time=0.2)
        self.play(FadeOut(x_solution, LEFT), run_time=0.2)
        self.play(FadeOut(result_text, LEFT), run_time=0.2)
        self.play(Uncreate(line), run_time=0.2)
        for item in text_group_right:
            self.play(FadeOut(item, RIGHT), run_time=0.2)

    def end(self):
        welcome = TexText("欢迎在评论区讨论其他做法！", font_size=65, color=BLUE_B)
        self.play(FadeIn(welcome, DOWN))
        self.play(WiggleOutThenIn(welcome))
        self.play(FadeOut(welcome, DOWN))
        self.wait()

        central_text = VGroup(
            TexText("Thanks for watching!", font_size=95, color=YELLOW_B),
            TexText("Presented by 歌迷就好"),
            TexText(
                "Powered by ManimGL v1.4.1",
                tex_to_color_map={"ManimGL": BLUE_B, "v1.4.1": GREEN_B}
            )
        )
        central_text.arrange(DOWN)
        central_text.to_edge(TOP)
        central_text.shift(DOWN)

        self.animate_through(central_text, 0.3)

        self.wait(2)


class Cover(Scene):
    def construct(self):
        self.play(Write(
            Tex(
                r"y = ax + b + \frac cx",
                font_size=105,
                tex_to_color_map={
                    "y": BLUE_B,
                    "ax": YELLOW_B,
                    r"\frac cx": TEAL,
                    "b": GREEN_B
                }
            )
        ))


if __name__ == "__main__":
    system(f"manimgl {__file__} Main")
