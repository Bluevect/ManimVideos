from manimlib import *


class Subtitle(TexText):
    def __init__(self, *tex_strings: str, **kwargs):
        kwargs["font"] = "monospace"
        kwargs["color"] = WHITE

        super().__init__(*tex_strings, **kwargs)
        self.to_edge(DOWN)
