import tkinter.font


class ChartifyStyler:
    """Applies Styles to Application."""

    def __init__(self, tk, sheet, figure=None):
        self.root = tk
        self.sheet = sheet
        self.figure = figure

    # ================$ GETTERS $=======================
    def get_sheet_style(self) -> tuple:
        """Returns the current style of sheet."""
        return self.sheet.MT.font()

    def get_sheet_font(self) -> str:
        """Returns the current font of sheet."""
        style = self.get_sheet_style()
        return style[0]

    def get_sheet_font_size(self) -> int:
        """Returns the current font size of sheet."""
        style = self.get_sheet_style()
        return style[1]

    def get_all_fonts(self) -> list:
        """Returns all the fonts on System."""
        return sorted(tkinter.font.families())

    # ================$ SETTERS $======================
    def set_sheet_style(self, font: tuple) -> None:
        """Changes font based on the font param.

        Parameters
        ----------
        font: tuple
            font tuple containing (font_name, font_size, font_style) example: ("Calibri", 13, "bold").
        """
        self.sheet.font(font)

    def set_sheet_font_size(self, size: int) -> None:
        """Increases font size."""
        font: str = self.get_sheet_font()
        style: str = self.get_sheet_style()[2]
        sheet_style = (font, int(size), style)
        self.set_sheet_style(sheet_style)

    def set_sheet_font(self, font: str) -> None:
        """Sets the font for sheet."""
        size: int = self.get_sheet_font_size()
        text_style: str = self.get_sheet_style()[2]
        sheet_style = (font, int(size), text_style)
        self.set_sheet_style(sheet_style)

    def set_fig_bg(self, color: str) -> None:
        """Sets the background of matplotlib figure."""
        if self.figure:
            self.figure.patch.set_facecolor("green")
