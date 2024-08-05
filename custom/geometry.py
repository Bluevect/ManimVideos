from manimlib import *


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
