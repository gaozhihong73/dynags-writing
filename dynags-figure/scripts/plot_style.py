"""DynaGS 论文图件的通用 Matplotlib 样式与导出工具。"""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Sequence

import matplotlib as mpl
import matplotlib.pyplot as plt


COLORBLIND_SAFE = (
    "#0072B2", "#E69F00", "#009E73", "#CC79A7",
    "#56B4E9", "#D55E00", "#F0E442", "#4D4D4D",
)

DEFAULT_WIDTHS = {"column": 3.35, "page": 6.30}
DEFAULT_FONT_FAMILIES = ("Arial", "Times New Roman", "DejaVu Sans")


@contextmanager
def thesis_style(
    *,
    font_families: Sequence[str] = DEFAULT_FONT_FAMILIES,
    base_font_size: float = 8.0,
) -> Iterator[None]:
    """在局部上下文中应用适合论文图件的保守样式。"""
    if base_font_size < 6.5:
        raise ValueError("base_font_size must be at least 6.5 pt")
    rc = {
        "font.family": "sans-serif",
        "font.sans-serif": list(font_families),
        "font.size": base_font_size,
        "axes.labelsize": base_font_size,
        "axes.titlesize": base_font_size,
        "legend.fontsize": max(6.5, base_font_size - 1.0),
        "xtick.labelsize": max(6.5, base_font_size - 1.0),
        "ytick.labelsize": max(6.5, base_font_size - 1.0),
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.axisbelow": True,
        "axes.unicode_minus": False,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "lines.linewidth": 1.4,
        "lines.markersize": 4.0,
        "legend.frameon": False,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
    }
    with mpl.rc_context(rc):
        yield


def figure_size(profile: str = "page", height: float = 3.6) -> tuple[float, float]:
    """返回默认画布尺寸；正式模板给出尺寸时应直接使用模板值。"""
    if profile not in DEFAULT_WIDTHS:
        choices = ", ".join(sorted(DEFAULT_WIDTHS))
        raise ValueError(f"Unknown profile {profile!r}; choose one of: {choices}")
    if height <= 0:
        raise ValueError("height must be positive")
    return DEFAULT_WIDTHS[profile], float(height)


def style_axis(ax: mpl.axes.Axes, grid: str | None = "y") -> None:
    """应用克制的坐标轴和网格样式。"""
    if grid not in {None, "x", "y", "both"}:
        raise ValueError("grid must be None, 'x', 'y', or 'both'")
    ax.tick_params(length=3.0, pad=2.0)
    if grid is not None:
        ax.grid(axis="both" if grid == "both" else grid,
                color="#D9D9D9", linewidth=0.5, alpha=0.65)


def save_figure(
    fig: mpl.figure.Figure,
    output_stem: str | Path,
    *,
    png_dpi: int = 300,
    tiff_dpi: int = 600,
    multiple_formats: bool = False,
    close: bool = True,
) -> dict[str, Path]:
    """默认只导出 PNG；明确启用时导出 PNG、SVG、PDF 和 TIFF。"""
    if png_dpi <= 0 or tiff_dpi <= 0:
        raise ValueError("dpi values must be positive")
    stem = Path(output_stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    paths = {"png": stem.with_suffix(".png")}
    fig.savefig(paths["png"], dpi=png_dpi, bbox_inches="tight")
    if multiple_formats:
        paths["svg"] = stem.with_suffix(".svg")
        paths["pdf"] = stem.with_suffix(".pdf")
        paths["tiff"] = stem.with_suffix(".tiff")
        fig.savefig(paths["svg"], bbox_inches="tight")
        fig.savefig(paths["pdf"], bbox_inches="tight")
        fig.savefig(paths["tiff"], dpi=tiff_dpi, bbox_inches="tight",
                    pil_kwargs={"compression": "tiff_lzw"})
    if close:
        plt.close(fig)
    return paths

