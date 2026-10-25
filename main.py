"""Punto de entrada de la aplicación Yahtzee."""

import tkinter as tk

from backend import JuegoYahtzee
from frontend import InterfazYahtzee


def main() -> None:
    ventana = tk.Tk()
    InterfazYahtzee(ventana, JuegoYahtzee())
    ventana.mainloop()


if __name__ == "__main__":
    main()
