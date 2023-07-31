from manimlib import *


# import numpy as np

class Subtitle(TexText):
    def __init__(self, *tex_strings: str, **kwargs):
        kwargs["font"] = "monospace"
        kwargs["color"] = WHITE

        super().__init__(*tex_strings, **kwargs)
        self.to_edge(DOWN)


# Dot with a mark label (Dot Extended)
class DotX(VGroup):
    def __init__(self,
                 point: np.ndarray = ORIGIN,
                 mark_letter: str = "P",
                 point_config=None,
                 mark_config=None,
                 mark_pos=UL,
                 **kwargs
                 ):
        # Dot
        if point_config:
            self.dot = Dot(point, **point_config)
        else:
            self.dot = Dot(point)

        # Mark letter
        if mark_config:
            self.mark = SingleStringTex(mark_letter, **mark_config)
        else:
            self.mark = SingleStringTex(mark_letter)

        self.mark.next_to(self.dot, mark_pos)

        super().__init__(self.dot, self.mark, **kwargs)

    def get_point(self):
        return self.dot.get_center()


# Triangle with dots and marks (Triangle Extended)
class TriangleX(VGroup):
    def __init__(self, *dotxes: DotX, triangle_config=None, **kwargs):
        # DotXes
        self.dotxes = dotxes

        # Triangle
        points = []
        for dotx in dotxes:
            points.append(dotx.dot.get_center())

        self.triangle_config = triangle_config
        if triangle_config:
            self.tri = Polygon(*points, **triangle_config)
        else:
            self.tri = Polygon(*points)

        super().__init__(*self.dotxes, self.tri, **kwargs)

    def set_color_for_marks(self, color):
        for dotx in self.dotxes:
            dotx.mark.set_color(color)
        return self

    def copy(self):
        copied = super().copy()
        dotxes = []

        for mobject in copied:
            if isinstance(mobject, DotX):
                dotxes.append(mobject)
            elif isinstance(mobject, Polygon):
                copied.tri = mobject

        copied.dotxes = tuple(dotxes)
        return copied


# Line with ticks (Deprecated)
# class TickedLine(VGroup):
#     def __init__(
#             self,
#             start: np.ndarray,
#             end: np.ndarray,
#             line_config=None,
#             tick_width=0.2,
#             tick_color=WHITE,
#             **kwargs
#     ):
#         # Line
#         if line_config:
#             line = Line(start, end, **line_config)
#         else:
#             line = Line(start, end)
#         self.line = line
#
#         # Tick
#         line_angle = line.get_angle()
#         tick_angle = 90 + line_angle
#         mid_point = midpoint(start, end)
#         half_width = tick_width / 2
#
#         tick = Line(half_width * LEFT, half_width * RIGHT, color=tick_color)
#         tick.move_to(mid_point)
#         tick.rotate(tick_angle)
#         self.tick = tick
#
#         super().__init__(line, tick, **kwargs)


# Draw a tick of a line defined by two points
def get_tick(point_a, point_b, width: float = 0.2, color: ManimColor = WHITE):
    vector = point_b - point_a
    line_angle = angle_of_vector(vector)
    tick_angle = PI / 2 + line_angle
    mid_point = midpoint(point_a, point_b)
    half_width = width / 2

    tick = Line(half_width * LEFT, half_width * RIGHT, color=color)
    tick.move_to(mid_point)
    tick.rotate(tick_angle)
    return tick


# Draw double tick of a line defined by two points
def get_double_tick(point_a, point_b, width: float = 0.2, color: ManimColor = WHITE):
    buff = 0.02
    vector_ab = point_b - point_a
    vector_ba = point_a - point_b
    tick1 = get_tick(point_a, point_b, width=width, color=color)
    tick1.shift(vector_ba * buff)
    tick2 = get_tick(point_a, point_b, width=width, color=color)
    tick2.shift(vector_ab * buff)
    return VGroup(tick1, tick2)


def get_unit_vector_on_direction(vector) -> np.ndarray:
    angle = angle_of_vector(vector)
    return np.array([np.cos(angle), np.sin(angle), 0])


#####
# Scenes


t2c_map = {
    "AB": BLUE_B,
    "BC": BLUE_B,
    "BH": BLUE_B,
    "CH": BLUE_B,
    "AH": BLUE_B,
    "AC": BLUE_B,
    r"\angle C": BLUE_B,
    r"\angle BHC": BLUE_B,
    r"\angle BHA": BLUE_B,
    r"\mathrm{Rt}\triangle BHC": BLUE_B,
    r"\mathrm{Rt}\triangle BHA": BLUE_B,
    r"\triangle ABC": BLUE_B,
    "DE": YELLOW_B,
    "EF": YELLOW_B,
    "EI": YELLOW_B,
    "FI": YELLOW_B,
    "DI": YELLOW_B,
    "DF": YELLOW_B,
    r"\angle F": YELLOW_B,
    r"\angle EIF": YELLOW_B,
    r"\angle EID": YELLOW_B,
    r"\mathrm{Rt}\triangle EIF": YELLOW_B,
    r"\mathrm{Rt}\triangle EID": YELLOW_B,
    r"\triangle DEF": YELLOW_B,
    "=": WHITE
}

t2c_map_for_tex_text = {
    "$B$": BLUE_B,
    r"$BH \bot AC$": BLUE_B,
    "$AC$": BLUE_B,
    "$H$": BLUE_B,
    "$E$": YELLOW_B,
    r"$EI \bot DF$": YELLOW_B,
    "$DF$": YELLOW_B,
    "$I$": YELLOW_B
}


class ShowQuestionScene(Scene):
    current_subtitle = None

    def change_subtitle(self, new_subtitle, run_time=0.5, waiting_time=1.0):
        if not self.current_subtitle:
            print("Warning: Subtitle does not exist!")
            return None

        self.play(
            ReplacementTransform(self.current_subtitle, new_subtitle),
            run_time=run_time
        )
        self.current_subtitle = new_subtitle

        if waiting_time > 0:
            self.wait(waiting_time)
        elif waiting_time != 0:
            print(f"Warning: Illegal waiting time: {waiting_time}!")

    def line_to_text(self, dot_a, dot_b, text, lining_time=0.5, run_time=0.5):
        point_a = dot_a.get_center()
        point_b = dot_b.get_center()
        vector_ab = point_b - point_a
        vector_ba = point_a - point_b
        line = Line(dot_a.get_edge_center(vector_ab), dot_b.get_edge_center(vector_ba), color=GOLD, stroke_width=8)
        self.play(
            ShowCreation(line),
            run_time=lining_time
        )

        self.play(
            ReplacementTransform(line, text),
            run_time=run_time
        )

    def construct(self):
        self.wait()

        # ==== Debug ====
        # Create axes
        axes = Axes(
            x_range=(-7, 7),
            y_range=(-4, 4),
            width=14,
            height=8,

            axis_config={
                "stroke_color": WHITE,
                "stroke_range": 3
            }
        )

        axes.add_coordinate_labels(
            font_size=25,
            text_config={"font": "monospace"}
        )

        # self.play(ShowCreation(axes))
        # self.wait()

        # ==== Debug ends ====

        # ==== Show question ====
        dotx_a = DotX(np.array([-3, 3, 0]), "A", mark_pos=UP)
        dotx_b = DotX(np.array([-4.2, 1, 0]), "B", mark_pos=LEFT)
        dotx_c = DotX(np.array([-2.2, 1, 0]), "C", mark_pos=RIGHT)

        orig_triangle1 = TriangleX(dotx_a, dotx_b, dotx_c).set_color(BLUE_B) \
            .set_color_for_marks(WHITE)
        self.play(ShowCreation(orig_triangle1))
        self.wait()

        dotx_d = DotX(np.array([3, 3, 0]), "D", mark_pos=UP)
        dotx_e = DotX(np.array([1.8, 1, 0]), "E", mark_pos=LEFT)
        dotx_f = DotX(np.array([3.8, 1, 0]), "F", mark_pos=RIGHT)

        orig_triangle2 = TriangleX(dotx_d, dotx_e, dotx_f).set_color(YELLOW_B) \
            .set_color_for_marks(WHITE)
        self.play(ReplacementTransform(orig_triangle1.copy(), orig_triangle2))

        self.current_subtitle = Subtitle("这是两个三角形")
        self.play(Write(self.current_subtitle))
        self.wait()

        self.change_subtitle(Subtitle("其中，"))

        conditions = Tex(
            "AB", "=", "DE", r",\quad ", "BC", "=", "EF",
            r",\quad ", r"\angle C", "=", r"\angle F",
            color=WHITE, tex_to_color_map=t2c_map
        )
        conditions.move_to(ORIGIN + DOWN)

        # AB
        self.line_to_text(dotx_a.dot, dotx_b.dot, conditions[0])
        self.play(Write(conditions[1]), run_time=0.5)
        # DE
        self.line_to_text(dotx_d.dot, dotx_e.dot, conditions[2])
        self.play(Write(conditions[3]), run_time=0.5)
        # BC
        self.line_to_text(dotx_b.dot, dotx_c.dot, conditions[4])
        self.play(Write(conditions[5]), run_time=0.5)
        # EF
        self.line_to_text(dotx_e.dot, dotx_f.dot, conditions[6])
        self.play(Write(conditions[7]), run_time=0.5)
        # \angle C
        angle_c = Arc(
            start_angle=np.pi - np.arctan(2.5),
            angle=np.arctan(2.5),
            arc_center=dotx_c.dot.get_center(),
            radius=0.3,
            color=BLUE_B
        )
        self.play(ShowCreation(angle_c), run_time=0.5)
        self.wait(0.5)
        self.play(ReplacementTransform(angle_c.copy(), conditions[8]), run_time=0.5)
        self.play(Write(conditions[9]), run_time=0.5)
        # \angle F
        angle_f = Arc(
            start_angle=np.pi - np.arctan(2.5),
            angle=np.arctan(2.5),
            arc_center=dotx_f.dot.get_center(),
            radius=0.3,
            color=YELLOW_B
        )
        self.play(ShowCreation(angle_f), run_time=0.5)
        self.wait(0.5)
        self.play(ReplacementTransform(angle_f.copy(), conditions[10]), run_time=0.5)
        self.wait()

        self.change_subtitle(Subtitle("众所周知，"), waiting_time=0.5)
        self.change_subtitle(
            Subtitle("三角形两边及一个邻角分别相等不能判定两个三角形全等"),
            run_time=0.3,
            waiting_time=2
        )
        self.change_subtitle(Subtitle("即 SSA 不能判定两个三角形全等"), run_time=0.3)
        self.change_subtitle(Subtitle("下面给出一个 SSA 的伪证"), waiting_time=4)

        self.play(self.current_subtitle.animate.shift(0.5 * UP), run_time=0.5, rate_func=smooth)
        self.play(self.current_subtitle.animate.shift(3 * DOWN), run_time=0.5, rate_func=rush_into)
        self.remove(self.current_subtitle)
        self.play(conditions.animate.shift(5 * DOWN), run_time=0.5, rate_func=rush_into)
        self.remove(conditions)

        dotx_a = DotX(np.array([2.5, 3, 0]), "A", mark_pos=UP)
        dotx_b = DotX(np.array([0.8, 1, 0]), "B", mark_pos=DOWN)
        dotx_c = DotX(np.array([3.2, 1, 0]), "C", mark_pos=DOWN)
        triangle1 = TriangleX(dotx_a, dotx_b, dotx_c).set_color(color=BLUE_B).set_color_for_marks(WHITE)
        dotx_d = DotX(np.array([5.8, 3, 0]), "D", mark_pos=UP)
        dotx_e = DotX(np.array([4.1, 1, 0]), "E", mark_pos=DOWN)
        dotx_f = DotX(np.array([6.5, 1, 0]), "F", mark_pos=DOWN)
        triangle2 = TriangleX(dotx_d, dotx_e, dotx_f).set_color(color=YELLOW_B).set_color_for_marks(WHITE)

        self.play(
            FadeOut(angle_c),
            FadeOut(angle_f)
        )

        self.play(
            ReplacementTransform(orig_triangle1, triangle1),
            ReplacementTransform(orig_triangle2, triangle2)
        )

        y_axis = Line(4 * DOWN, 4 * UP, color=WHITE, stroke_width=3)
        self.play(ShowCreation(y_axis))

        # Add ticks
        self.current_subtitle = Subtitle("为方便, 标记相等的线段和角度")
        self.play(Write(self.current_subtitle))

        tick_ab = get_tick(dotx_a.get_point(), dotx_b.get_point())
        tick_de = get_tick(dotx_d.get_point(), dotx_e.get_point())
        tick_bc = get_double_tick(dotx_b.get_point(), dotx_c.get_point())
        tick_ef = get_double_tick(dotx_e.get_point(), dotx_f.get_point())

        angle_c = Arc(
            start_angle=np.pi - np.arctan(2.8571),  # (y_A - y_C) / (x_C - x_A)
            angle=np.arctan(2.8571),
            arc_center=dotx_c.get_point(),
            radius=0.3,
            color=WHITE
        )
        angle_f = Arc(
            start_angle=np.pi - np.arctan(2.8571),
            angle=np.arctan(2.8571),
            arc_center=dotx_f.get_point(),
            radius=0.3,
            color=WHITE
        )

        self.play(
            ShowCreation(tick_ab),
            ShowCreation(tick_de)
        )
        self.play(
            ShowCreation(tick_bc),
            ShowCreation(tick_ef)
        )
        self.play(
            ShowCreation(angle_c),
            ShowCreation(angle_f)
        )

        self.play(FadeOut(self.current_subtitle))
        self.current_subtitle = None

        proof = VGroup(
            TexText(r"证明：过点 $B$ 作 $BH \bot AC$ 交 $AC$ 于", tex_to_color_map=t2c_map_for_tex_text, color=WHITE),
            TexText(r"点 $H$，过点 $E$ 作 $EI \bot DF$ 交 $DF$ 于", tex_to_color_map=t2c_map_for_tex_text, color=WHITE),
            TexText(r"点 $I$ .", tex_to_color_map=t2c_map_for_tex_text, color=WHITE),
            Tex(r"\because BC = EF, \ \angle C = \angle F,",
                tex_to_color_map=t2c_map, color=WHITE),
            Tex(r"\angle BHC", "=", r"\angle EIF", r"= 90^\circ", tex_to_color_map=t2c_map, color=WHITE),
            Tex(r"\therefore ", r"\mathrm{Rt}\triangle BHC", r"\cong", r"\mathrm{Rt}\triangle EIF", r"\ \mathrm{(HL)}",
                tex_to_color_map=t2c_map, color=WHITE),
            Tex(r"\therefore BH = EI, \ CH = FI", tex_to_color_map=t2c_map, color=WHITE),
            Tex(
                r"\because AB = DE, \ ", r"\angle BHA", "=", r"\angle EID", r"= 90^\circ",
                tex_to_color_map=t2c_map,
                color=WHITE
            ).set_color_by_tex_to_color_map(t2c_map),
            Tex(r"\therefore ", r"\mathrm{Rt}\triangle BHA", r"\cong", r"\mathrm{Rt}\triangle EID", r"\ \mathrm{(HL)}",
                tex_to_color_map=t2c_map, color=WHITE),
            Tex(r"\therefore AH = DI", tex_to_color_map=t2c_map, color=WHITE),
            # Tex(r"\because AC = AH + CH, \ DF = DI + FI", tex_to_color_map=t2c_map, color=WHITE),
            Tex(r"\therefore AC = DF", tex_to_color_map=t2c_map, color=WHITE),
            Tex(r"\therefore ", r"\triangle ABC", r"\cong", r"\triangle DEF", r"\ \mathrm{(SSS)} \quad \blacksquare",
                tex_to_color_map=t2c_map, color=WHITE)
        ).arrange(DOWN).scale(0.8)

        for i, tex_text in enumerate(proof):
            if not i == 0:
                tex_text.align_to(proof[i - 1], LEFT)

        proof.to_corner(UL).shift(0.2 * UL)

        dotx_h = DotX(np.array([2.9381, 1.7483, 0]), "H", mark_pos=UR, point_config={"color": BLUE_B})
        dotx_i = DotX(np.array([6.2381, 1.7483, 0]), "I", mark_pos=UR, point_config={"color": YELLOW_B})

        for i, tex_text in enumerate(proof):
            self.play(Write(tex_text))
            if i > 2:
                self.wait(2)
            if i == 2:
                # Calculate the function analysis of AC and BH,
                # Set y_AC = y_BH to solve the position of H
                bh = DashedLine(dotx_b.dot.get_center(), dotx_h.dot.get_center(), color=BLUE_B)
                self.play(ShowCreation(bh), ShowCreation(dotx_h))
                # angle: (y_H - y_B) / (x_H - x_B) + PI / 2
                elbow1 = Elbow(angle=0.3499 + PI / 2).move_to(dotx_h.dot)
                elbow1.shift(0.1 * UP + 0.22 * LEFT)
                self.play(ShowCreation(elbow1))

                ei = DashedLine(dotx_e.dot.get_center(), dotx_i.dot.get_center(), color=YELLOW_B)
                self.play(ShowCreation(ei), ShowCreation(dotx_i))
                elbow2 = Elbow(angle=0.3499 + PI / 2).move_to(dotx_i.dot)
                elbow2.shift(0.1 * UP + 0.22 * LEFT)
                self.play(ShowCreation(elbow2))

            if i == 5:
                triangle_bhc = Polygon(
                    dotx_b.get_point(),
                    dotx_c.get_point(),
                    dotx_h.get_point(),
                    color=GOLD
                ).set_fill(GOLD, opacity=0.5)
                triangle_eif = Polygon(
                    dotx_e.get_point(),
                    dotx_i.get_point(),
                    dotx_f.get_point(),
                    color=GOLD
                ).set_fill(GOLD, opacity=0.5)

                self.play(
                    ShowCreationThenDestruction(triangle_bhc),
                    ShowCreationThenDestruction(triangle_eif),
                    ShowCreationThenDestructionAround(tex_text),
                    run_time=4
                )

            if i == 8:
                triangle_bha = Polygon(
                    dotx_b.get_point(),
                    dotx_h.get_point(),
                    dotx_a.get_point(),
                    color=GOLD
                ).set_fill(GOLD, opacity=0.5)
                triangle_eid = Polygon(
                    dotx_e.get_point(),
                    dotx_i.get_point(),
                    dotx_d.get_point(),
                    color=GOLD
                ).set_fill(GOLD, opacity=0.5)

                self.wait()
                self.play(
                    ShowCreationThenDestruction(triangle_bha),
                    ShowCreationThenDestruction(triangle_eid),
                    ShowCreationThenDestructionAround(tex_text),
                    run_time=4
                )

            # if i == 12:
            if i == 11:
                triangle_abc = Polygon(
                    dotx_a.get_point(),
                    dotx_b.get_point(),
                    dotx_c.get_point(),
                    color=GOLD
                ).set_fill(GOLD, opacity=0.5)
                triangle_def = Polygon(
                    dotx_d.get_point(),
                    dotx_e.get_point(),
                    dotx_f.get_point(),
                    color=GOLD
                ).set_fill(GOLD, opacity=0.5)

                self.wait()
                self.play(
                    ShowCreationThenDestruction(triangle_abc),
                    ShowCreationThenDestruction(triangle_def),
                    ShowCreationThenDestructionAround(tex_text),
                    run_time=4
                )

        self.current_subtitle = Subtitle("通过证明两个小三角形全等，我们似乎证明了 SSA")
        self.play(Write(self.current_subtitle))
        self.wait()
        self.change_subtitle(Subtitle("这样的结论明显是错的"))
        self.change_subtitle(Subtitle("那么错在哪呢？"))
        self.wait()

        count = 5
        count_tex = SingleStringTex(str(count), color=WHITE).to_corner(DR)
        self.play(Write(count_tex))
        for i in range(count - 1, 0, -1):
            new_count_tex = SingleStringTex(str(i), color=WHITE).to_corner(DR)
            # A number countdown takes 2s!
            self.wait()
            self.play(ReplacementTransform(count_tex, new_count_tex))
            count_tex = new_count_tex

        self.wait()
        self.play(Uncreate(count_tex))
        self.wait()
        self.play(self.current_subtitle.animate.shift(0.5 * UP), run_time=0.5, rate_func=smooth)
        self.play(self.current_subtitle.animate.shift(3 * DOWN), run_time=0.5, rate_func=rush_into)
        self.remove(self.current_subtitle)

        # Create a screen rectangle covering the screen for texting
        cover = FullScreenRectangle(color="#333333")
        self.play(ShowCreation(cover), run_time=3)
        self.wait()

        # ==== Show question part ends ====

        # ==== Prove cosine law ====
        self.current_subtitle = Subtitle(
            "为了继续探究 SSA, 我们需要先证明余弦定理",
            tex_to_color_map={
                "余弦定理": BLUE_B
            }
        )
        self.play(Write(self.current_subtitle))
        self.wait()
        self.change_subtitle(Subtitle("如果已经知道了就长按快进吧"))
        self.wait()
        self.play(FadeOut(self.current_subtitle))

        cosine_law_intro = VGroup(
            TexText(
                "余弦定理：三角形中任意一边的平方等于其他两边的平方的和",
                color=WHITE,
                tex_to_color_map={
                    "余弦定理": BLUE_B
                }
            ),
            TexText(
                "减去这两边与它们的夹角的余弦的积的两倍",
                color=WHITE
            ),
            TexText(
                r"分别记两边为 $a$, $b$, 第三边为 $c$, 两边夹角为 $\theta$,",
                color=WHITE,
                tex_to_color_map={
                    "$a$": BLUE_B,
                    "$b$": BLUE_B,
                    "$c$": YELLOW_B,
                    r"$\theta$": BLUE_B
                }
            ),
            Tex(
                "c^2", "=", "a^2", "+", "b^2", "-", r"2ab\cos \theta",
                tex_to_color_map={
                    "c^2": YELLOW_B,
                    "a^2": BLUE_B,
                    "b^2": BLUE_B,
                    r"2ab\cos \theta": BLUE_B,
                    "=": WHITE,
                    "+": WHITE,
                    "-": WHITE
                }
            )
        ).arrange(DOWN)

        for i, tex_text in enumerate(cosine_law_intro):
            if i > 0:
                tex_text.align_to(cosine_law_intro[i - 1], LEFT)

        cosine_law_intro.to_edge(UL).shift(0.1 * UL)

        dotx_a_temp = DotX(np.array([5.8, 1, 0]), "A", mark_pos=UP)
        dotx_b_temp = DotX(np.array([4.1, -1, 0]), "B", mark_pos=DOWN)
        dotx_c_temp = DotX(np.array([6.5, -1, 0]), "C", mark_pos=DOWN)
        triangle_temp = TriangleX(dotx_a_temp, dotx_b_temp, dotx_c_temp) \
            .set_color(color=BLUE_B).set_color_for_marks(WHITE)
        angle_theta = Arc(
            start_angle=np.pi - np.arctan(2.8571),
            angle=np.arctan(2.8571),
            arc_center=dotx_c_temp.get_point(),
            radius=0.3,
            color=WHITE
        )
        midpoint_bc = midpoint(dotx_b_temp.get_point(), dotx_c_temp.get_point())
        midpoint_ac = midpoint(dotx_a_temp.get_point(), dotx_c_temp.get_point())
        midpoint_ab = midpoint(dotx_a_temp.get_point(), dotx_b_temp.get_point())

        a_tex = Tex("a", color=WHITE).next_to(midpoint_bc, DOWN)
        b_tex = Tex("b", color=WHITE).next_to(
            midpoint_ac, get_unit_vector_on_direction(midpoint_ac - dotx_b_temp.get_point()))
        c_tex = Tex("c", color=WHITE).next_to(
            midpoint_ab, get_unit_vector_on_direction(midpoint_ab - dotx_c_temp.get_point()))
        theta_tex = Tex(r"\theta", color=WHITE).next_to(angle_theta, 0.2 * UP + 0.5 * LEFT)

        for i, tex_text in enumerate(cosine_law_intro):
            if i != 3:
                self.play(Write(tex_text))
                if i != 0:
                    self.wait(2)

            if i == 2:
                self.play(ShowCreation(triangle_temp))
                self.play(ShowCreation(angle_theta))
                self.play(Write(theta_tex))
                self.play(
                    Write(a_tex),
                    Write(b_tex),
                    Write(c_tex)
                )

            elif i == 3:
                self.line_to_text(dotx_a_temp.dot, dotx_b_temp.dot, tex_text[0])
                self.play(Write(tex_text[1]))
                self.line_to_text(dotx_b_temp.dot, dotx_c_temp.dot, tex_text[2])
                self.play(Write(tex_text[3]))
                self.line_to_text(dotx_a_temp.dot, dotx_c_temp.dot, tex_text[4])
                self.play(Write(tex_text[5]))
                self.play(ReplacementTransform(angle_theta.copy(), tex_text[6]))

        self.current_subtitle = Subtitle("(其余两个角也有对应关系)")
        self.play(Write(self.current_subtitle))
        self.wait(4)
        self.play(Uncreate(self.current_subtitle))
        self.current_subtitle = None

        # cosine_law = None

        for i, tex_text in enumerate(cosine_law_intro):
            if i < 3:
                self.play(FadeOut(tex_text, RIGHT), run_time=0.4 - 0.1 * i)
            else:
                cosine_law = tex_text.copy().to_corner(UR)
                self.play(ReplacementTransform(tex_text, cosine_law), run_time=2)

        self.current_subtitle = Subtitle("先讨论锐角三角形的情况")
        self.play(Write(self.current_subtitle))
        self.wait(2)
        self.play(FadeOut(self.current_subtitle))

        t2c_map_for_tex_text_2 = {
            "$A$": BLUE_B,
            r"$AH \bot BC$": BLUE_B,
            "$BC$": BLUE_B,
            "$H$": BLUE_B,
            "勾股定理": BLUE_B
        }

        proof_for_acute_triangles = VGroup(
            TexText(r"过点 $A$ 作 $AH \bot BC$ 交 $BC$ 于点 $H$", color=WHITE, tex_to_color_map=t2c_map_for_tex_text_2),
            TexText(r"设 $HC = x$, 则 $BH = a - x$", color=WHITE, tex_to_color_map=t2c_map_for_tex_text_2),
            TexText("根据勾股定理得", color=WHITE, tex_to_color_map=t2c_map_for_tex_text_2),
            Tex("c^2", "-", "(a - x)^2", "=", "b^2", "-", "x^2", color=WHITE),
            Tex("c^2", "-", "a^2", "+", "2ax", "-", "x^2", "=", "b^2", "-", "x^2", color=WHITE),
            Tex("c^2", "-", "a^2", "-", "b^2", "+", "2ax", "=", "0", color=WHITE),
            Tex("2ax", "=", "a^2", "+", "b^2", "-", "c^2", color=WHITE),
            Tex("x", "=", r"\frac {a^2 + b^2 - c^2}{2a}", color=WHITE),
            Tex(r"\cos \theta", "=", r"\frac xb", "=", r"\frac {a^2 + b^2 - c^2}{2ab}", color=WHITE),
            Tex("2ab", r"\cos \theta", "=", "a^2", "+", "b^2", "-", "c^2", color=WHITE),
            Tex("c^2", "=", "a^2", "+", "b^2", "-2ab", r"\cos \theta", r"\quad", r"\blacksquare", color=WHITE)
        ).arrange(DOWN * 1.5).scale(0.8)

        for i, tex_text in enumerate(proof_for_acute_triangles):
            if 0 < i <= 3:
                tex_text.align_to(proof_for_acute_triangles[i - 1], LEFT)
            else:
                tex_text.align_to(proof_for_acute_triangles[2], LEFT)

        proof_for_acute_triangles.to_edge(UL).shift(0.1 * UL)

        y_axis = Line(4 * DOWN, 4 * UP, color=WHITE, stroke_width=3)
        self.play(ShowCreation(y_axis))

        # Assign mobjects
        dotx_h_temp = DotX(np.array([5.8, -1, 0]), "H", mark_pos=DOWN, point_config={"color": BLUE_B})
        ah = DashedLine(dotx_a_temp.dot.get_center(), dotx_h_temp.dot.get_center(), color=BLUE_B)

        hc = Line(dotx_h_temp.get_point(), dotx_c_temp.get_point())
        brace_hc = Brace(hc, DOWN).shift(0.7 * DOWN)
        brace_tex_hc = Tex("x").next_to(brace_hc, DOWN)

        bh = Line(dotx_b_temp.get_point(), dotx_h_temp.get_point())
        brace_bh = Brace(bh, DOWN).shift(0.7 * DOWN)
        brace_tex_bh = Tex("a - x").next_to(brace_bh, DOWN)

        # Animate tex texts
        for i, tex_text in enumerate(proof_for_acute_triangles):
            if i <= 3:
                self.play(Write(tex_text))
                self.wait(2)
            elif i <= 7:
                self.play(TransformMatchingTex(proof_for_acute_triangles[i - 1].copy(), tex_text))
                self.wait(2)
            elif i > 7:
                tex_text.next_to(proof_for_acute_triangles[i - 1], 1.5 * DOWN)
                tex_text.align_to(proof_for_acute_triangles[i - 1], LEFT)
                self.play(TransformMatchingTex(proof_for_acute_triangles[i - 1].copy(), tex_text))
                self.wait(2)

            if i == 0:
                self.play(
                    ShowCreation(dotx_h_temp),
                    ShowCreation(ah)
                )
            elif i == 1:

                self.play(
                    ShowCreation(brace_hc),
                    ShowCreation(brace_tex_hc)
                )

                self.play(
                    ShowCreation(brace_bh),
                    ShowCreation(brace_tex_bh)
                )
            elif i == 7:
                for j in range(3, 7):
                    self.play(FadeOut(proof_for_acute_triangles[j], LEFT), run_time=0.4 - 0.1 * (j - 3))

                self.play(tex_text.animate.shift(2.75 * UP))

        # Fade Out and Uncreate
        self.wait(4)

        for i in range(0, 11):
            if 0 <= i <= 2 or 7 <= i <= 11:
                self.play(FadeOut(proof_for_acute_triangles[i], LEFT), run_time=0.2)

        self.play(
            Uncreate(brace_bh),
            Uncreate(brace_hc),
            Uncreate(brace_tex_bh),
            Uncreate(brace_tex_hc),
            run_time=0.5
        )
        self.play(
            Uncreate(a_tex),
            Uncreate(b_tex),
            Uncreate(c_tex),
            Uncreate(angle_theta),
            Uncreate(theta_tex),
            run_time=0.5
        )
        # self.play(
        #     Uncreate(triangle_temp),
        #     Uncreate(ah),
        #     Uncreate(dotx_h_temp),
        #     run_time=0.5
        # )

        self.current_subtitle = Subtitle("讨论钝角三角形的情况")
        self.play(Write(self.current_subtitle))

        # Abandoned temporarily...
