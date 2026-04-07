"""Animation of recursive rectangle filling using Manim Community.

This scene visualizes how a large rectangle is recursively split into
smaller rectangles until each piece is below MAX_BLOCKS.
"""

from __future__ import annotations

from dataclasses import dataclass

from manim import (
    BLUE_E,
    DOWN,
    GREEN_C,
    UP,
    YELLOW,
    Create,
    FadeIn,
    Rectangle,
    Scene,
    Text,
)


@dataclass(frozen=True)
class RectRange:
    """Inclusive rectangle range in grid coordinates."""

    x1: int
    y1: int
    x2: int
    y2: int

    @property
    def width(self) -> int:
        return self.x2 - self.x1 + 1

    @property
    def height(self) -> int:
        return self.y2 - self.y1 + 1

    @property
    def blocks(self) -> int:
        return self.width * self.height


def split_ranges(rect: RectRange, max_blocks: int) -> list[RectRange]:
    """Split an inclusive rectangle recursively, mirroring World._fill_split."""
    if rect.blocks <= max_blocks:
        return [rect]

    if rect.width >= rect.height:
        x_mid = (rect.x1 + rect.x2) // 2
        left = RectRange(rect.x1, rect.y1, x_mid, rect.y2)
        right = RectRange(x_mid + 1, rect.y1, rect.x2, rect.y2)
        return split_ranges(left, max_blocks) + split_ranges(right, max_blocks)

    y_mid = (rect.y1 + rect.y2) // 2
    bottom = RectRange(rect.x1, rect.y1, rect.x2, y_mid)
    top = RectRange(rect.x1, y_mid + 1, rect.x2, rect.y2)
    return split_ranges(bottom, max_blocks) + split_ranges(top, max_blocks)


class FillSplitSimulation(Scene):
    """Animate the fill process for a bounded world using recursive splits."""

    WORLD_W = 50
    WORLD_H = 50
    MAX_BLOCKS = 1000
    TARGET = RectRange(0, 0, 40, 40)

    def _to_scene_rect(self, rect: RectRange, cell_size: float) -> Rectangle:
        """Map grid coordinates to a Manim rectangle centered in the scene."""
        world_w = self.WORLD_W * cell_size
        world_h = self.WORLD_H * cell_size

        x_center = (rect.x1 + rect.x2 + 1) / 2 * cell_size - world_w / 2
        y_center = (rect.y1 + rect.y2 + 1) / 2 * cell_size - world_h / 2

        return Rectangle(
            width=rect.width * cell_size,
            height=rect.height * cell_size,
            stroke_color=YELLOW,
            stroke_width=2,
            fill_color=GREEN_C,
            fill_opacity=0.25,
        ).move_to([x_center, y_center, 0])

    def construct(self) -> None:
        cell_size = 0.12
        world_border = Rectangle(
            width=self.WORLD_W * cell_size,
            height=self.WORLD_H * cell_size,
            stroke_color=BLUE_E,
            stroke_width=2,
            fill_opacity=0,
        )

        title = Text(
            "Simulacion de _fill_split (0-based)",
            font_size=28,
        ).to_edge(UP)

        info = Text(
            f"Target: ({self.TARGET.x1},{self.TARGET.y1}) -> ({self.TARGET.x2},{self.TARGET.y2}) | "
            f"MAX_BLOCKS={self.MAX_BLOCKS}",
            font_size=20,
        ).next_to(title, DOWN, buff=0.2)

        self.play(Create(world_border), FadeIn(title), FadeIn(info), run_time=1.2)

        chunks = split_ranges(self.TARGET, self.MAX_BLOCKS)
        for chunk in chunks:
            rect_vm = self._to_scene_rect(chunk, cell_size)
            self.play(FadeIn(rect_vm), run_time=0.18)

        self.wait(1)
