"""Lógica del juego Yahtzee, independiente de la interfaz gráfica."""

from collections import Counter
from pathlib import Path
import random
from typing import ClassVar


class Dado:
    """Dado de seis caras."""

    @staticmethod
    def lanzar() -> int:
        return random.randint(1, 6)


class EvaluadorYahtzee:
    """Calcula los puntos de las 13 categorías estándar de Yahtzee."""

    CATEGORIAS: ClassVar[tuple[str, ...]] = (
        "Unos",
        "Doses",
        "Treses",
        "Cuatros",
        "Cincos",
        "Seises",
        "Trío",
        "Póker",
        "Full House",
        "Escalera menor",
        "Escalera mayor",
        "Yahtzee",
        "Chance",
    )

    @staticmethod
    def puntuar(dados: list[int] | tuple[int, ...], categoria: str) -> int:
        if len(dados) != 5 or any(dado not in range(1, 7) for dado in dados):
            raise ValueError("Se requieren exactamente cinco dados válidos.")
        if categoria not in EvaluadorYahtzee.CATEGORIAS:
            raise ValueError(f"Categoría desconocida: {categoria}")

        conteos = Counter(dados)
        suma = sum(dados)
        if categoria in EvaluadorYahtzee.CATEGORIAS[:6]:
            cara = EvaluadorYahtzee.CATEGORIAS.index(categoria) + 1
            return cara * conteos[cara]
        if categoria == "Trío":
            return suma if max(conteos.values()) >= 3 else 0
        if categoria == "Póker":
            return suma if max(conteos.values()) >= 4 else 0
        if categoria == "Full House":
            return 25 if sorted(conteos.values()) == [2, 3] else 0
        if categoria == "Escalera menor":
            caras = set(dados)
            secuencias = ({1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6})
            return 30 if any(secuencia <= caras for secuencia in secuencias) else 0
        if categoria == "Escalera mayor":
            caras = set(dados)
            return 40 if caras in ({1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}) else 0
        if categoria == "Yahtzee":
            return 50 if max(conteos.values()) == 5 else 0
        return suma

    @staticmethod
    def puntuar_todas(dados: list[int] | tuple[int, ...]) -> dict[str, int]:
        return {
            categoria: EvaluadorYahtzee.puntuar(dados, categoria)
            for categoria in EvaluadorYahtzee.CATEGORIAS
        }


class JuegoYahtzee:
    """Estado de una partida para dos jugadores."""

    MAX_LANZAMIENTOS: ClassVar[int] = 3

    def __init__(self, jugadores: tuple[str, str] = ("Jugador 1", "Jugador 2")):
        if len(jugadores) != 2:
            raise ValueError("Yahtzee requiere exactamente dos jugadores.")
        self.jugadores = jugadores
        self.puntajes: dict[str, dict[str, int | None]] = {
            jugador: {categoria: None for categoria in EvaluadorYahtzee.CATEGORIAS}
            for jugador in jugadores
        }
        self.jugador_activo = 0
        self.ronda = 1
        self.lanzamientos_restantes = self.MAX_LANZAMIENTOS
        self.dados = [0] * 5
        self.dados_fijados = [False] * 5
        self.ha_lanzado = False
        self.terminado = False

    @property
    def nombre_jugador_activo(self) -> str:
        return self.jugadores[self.jugador_activo]

    def fijar_dado(self, indice: int, fijado: bool) -> None:
        if not 0 <= indice < len(self.dados):
            raise IndexError("Índice de dado fuera de rango.")
        if not self.ha_lanzado or self.lanzamientos_restantes == 0:
            raise RuntimeError("No se pueden cambiar los dados fijados ahora.")
        self.dados_fijados[indice] = bool(fijado)

    def lanzar_dados(self) -> list[int]:
        if self.terminado:
            raise RuntimeError("La partida ya terminó.")
        if self.lanzamientos_restantes == 0:
            raise RuntimeError("No quedan lanzamientos en este turno.")

        for indice, fijado in enumerate(self.dados_fijados):
            if not fijado:
                self.dados[indice] = Dado.lanzar()
        self.lanzamientos_restantes -= 1
        self.ha_lanzado = True
        return self.dados.copy()

    def puntuar(self, categoria: str) -> int:
        if self.terminado:
            raise RuntimeError("La partida ya terminó.")
        if not self.ha_lanzado:
            raise RuntimeError("Debes lanzar los dados antes de puntuar.")
        if categoria not in EvaluadorYahtzee.CATEGORIAS:
            raise ValueError(f"Categoría desconocida: {categoria}")

        jugador = self.nombre_jugador_activo
        if self.puntajes[jugador][categoria] is not None:
            raise ValueError("Esa categoría ya fue utilizada por este jugador.")
        puntos = EvaluadorYahtzee.puntuar(self.dados, categoria)
        self.puntajes[jugador][categoria] = puntos
        self._siguiente_turno()
        return puntos

    def mejor_categoria_disponible(self) -> tuple[str, int]:
        if self.terminado:
            raise RuntimeError("La partida ya terminó.")
        if not self.ha_lanzado:
            raise RuntimeError("Debes lanzar los dados antes de puntuar.")

        puntajes_disponibles = {
            categoria: EvaluadorYahtzee.puntuar(self.dados, categoria)
            for categoria in EvaluadorYahtzee.CATEGORIAS
            if self.puntajes[self.nombre_jugador_activo][categoria] is None
        }
        if not puntajes_disponibles:
            raise RuntimeError("No quedan categorías disponibles para este jugador.")
        return max(puntajes_disponibles.items(), key=lambda item: item[1])

    def puntuar_automaticamente(self) -> tuple[str, int]:
        categoria, puntos = self.mejor_categoria_disponible()
        self.puntuar(categoria)
        return categoria, puntos

    def subtotal_superior(self, jugador: str) -> int:
        if jugador not in self.puntajes:
            raise ValueError(f"Jugador desconocido: {jugador}")
        return sum(
            self.puntajes[jugador][categoria] or 0
            for categoria in EvaluadorYahtzee.CATEGORIAS[:6]
        )

    def bonificacion_superior(self, jugador: str) -> int:
        return 35 if self.subtotal_superior(jugador) >= 63 else 0

    def puntaje_total(self, jugador: str) -> int:
        if jugador not in self.puntajes:
            raise ValueError(f"Jugador desconocido: {jugador}")
        total = sum(puntos or 0 for puntos in self.puntajes[jugador].values())
        return total + self.bonificacion_superior(jugador)

    def _siguiente_turno(self) -> None:
        if self.ronda < 13:
            self.ronda += 1
        elif self.jugador_activo == 0:
            self.jugador_activo = 1
            self.ronda = 1
        else:
            self.terminado = True
        self.lanzamientos_restantes = self.MAX_LANZAMIENTOS
        self.dados = [0] * 5
        self.dados_fijados = [False] * 5
        self.ha_lanzado = False


class SimuladorMontecarlo:
    """Simula lanzamientos y guarda una gráfica de convergencia."""

    @staticmethod
    def simular(
        n: int, ruta_grafica: str | Path = "convergencia_montecarlo.png"
    ) -> tuple[list[float], Path]:
        if isinstance(n, bool) or not isinstance(n, int) or not 100 <= n <= 500_000:
            raise ValueError("N debe ser un entero entre 100 y 500,000.")

        acumulados = []
        cantidad_unos = 0
        for lanzamiento in range(1, n + 1):
            cantidad_unos += Dado.lanzar() == 1
            acumulados.append(cantidad_unos / lanzamiento)

        try:
            import matplotlib

            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except ImportError as error:
            raise RuntimeError(
                "La gráfica requiere matplotlib. Instálalo con: pip install -r requirements.txt"
            ) from error

        destino = Path(ruta_grafica)
        figura, eje = plt.subplots(figsize=(10, 5))
        eje.plot(range(1, n + 1), acumulados, linewidth=0.8, label="Frecuencia observada")
        eje.axhline(1 / 6, color="red", linestyle="--", label="Probabilidad teórica (1/6)")
        eje.set(
            title=f"Convergencia de la frecuencia del 1 ({n:,} lanzamientos)",
            xlabel="Número de lanzamientos",
            ylabel="Frecuencia acumulada del 1",
        )
        eje.grid(True, alpha=0.3)
        eje.legend()
        figura.tight_layout()
        figura.savefig(destino, dpi=150)
        plt.close(figura)
        return acumulados, destino
