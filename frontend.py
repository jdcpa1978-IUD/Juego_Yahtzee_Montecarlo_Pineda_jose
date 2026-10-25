"""Interfaz gráfica de Yahtzee construida con tkinter."""

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from pathlib import Path

from backend import EvaluadorYahtzee, JuegoYahtzee, SimuladorMontecarlo


class InterfazYahtzee:
    def __init__(self, ventana: tk.Tk, juego: JuegoYahtzee):
        self.ventana = ventana
        self.juego = juego
        self.ventana.title("Yahtzee para dos jugadores")
        self.ventana.minsize(760, 650)
        self.seleccionados = [tk.BooleanVar(value=False) for _ in range(5)]
        self.botones_dados: list[ttk.Button] = []
        self.mensaje_turno = ""

        self._crear_interfaz()
        self._actualizar()

    def _crear_interfaz(self) -> None:
        contenedor = ttk.Frame(self.ventana, padding=16)
        contenedor.pack(fill="both", expand=True)

        ttk.Label(
            contenedor, text="YAHTZEE", font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")
        self.estado = ttk.Label(contenedor, font=("Segoe UI", 11))
        self.estado.pack(anchor="w", pady=(4, 12))

        dados_frame = ttk.LabelFrame(contenedor, text="Dados (selecciona para conservar)", padding=10)
        dados_frame.pack(fill="x", pady=5)
        for indice in range(5):
            boton = ttk.Button(
                dados_frame,
                text="—",
                command=lambda i=indice: self._alternar_dado(i),
                width=12,
            )
            boton.grid(row=0, column=indice, padx=5, pady=5, sticky="ew")
            self.botones_dados.append(boton)
            dados_frame.columnconfigure(indice, weight=1)

        controles = ttk.Frame(contenedor)
        controles.pack(fill="x", pady=6)
        self.boton_lanzar = ttk.Button(
            controles, text="Lanzar dados", command=self._lanzar
        )
        self.boton_lanzar.pack(side="left")
        self.boton_puntuar = ttk.Button(
            controles,
            text="Terminar turno y anotar",
            command=self._puntuar_automaticamente,
        )
        self.boton_puntuar.pack(side="left", padx=8)
        self.boton_reiniciar = ttk.Button(
            controles, text="Nueva partida", command=self._reiniciar
        )
        self.boton_reiniciar.pack(side="left", padx=8)
        self.boton_montecarlo = ttk.Button(
            controles, text="Simulación Monte Carlo", command=self._montecarlo
        )
        self.boton_montecarlo.pack(side="right")
        self.sugerencia = ttk.Label(contenedor, justify="left")
        self.sugerencia.pack(anchor="w", pady=(2, 6))

        tabla = ttk.LabelFrame(contenedor, text="Hoja de puntos", padding=8)
        tabla.pack(fill="both", expand=True, pady=8)
        ttk.Label(tabla, text="Categoría", font=("", 10, "bold")).grid(
            row=0, column=0, sticky="w", padx=4
        )
        for columna, jugador in enumerate(self.juego.jugadores, start=1):
            ttk.Label(tabla, text=jugador, font=("", 10, "bold")).grid(
                row=0, column=columna, padx=4
            )

        self.celdas_puntaje: dict[tuple[str, str], ttk.Label] = {}
        for fila, categoria in enumerate(EvaluadorYahtzee.CATEGORIAS, start=1):
            ttk.Label(tabla, text=categoria).grid(
                row=fila, column=0, sticky="w", padx=4, pady=1
            )
            for columna, jugador in enumerate(self.juego.jugadores, start=1):
                celda = ttk.Label(tabla, text="—", width=10, anchor="center")
                celda.grid(row=fila, column=columna, padx=4, pady=1)
                self.celdas_puntaje[jugador, categoria] = celda

        self.resumen = ttk.Label(contenedor, justify="left")
        self.resumen.pack(anchor="w", pady=(6, 0))

    def _alternar_dado(self, indice: int) -> None:
        if not self.juego.ha_lanzado or self.juego.lanzamientos_restantes == 0:
            return
        fijado = not self.seleccionados[indice].get()
        self.seleccionados[indice].set(fijado)
        self.juego.fijar_dado(indice, fijado)
        self._actualizar()

    def _lanzar(self) -> None:
        try:
            self.juego.lanzar_dados()
        except (RuntimeError, ValueError) as error:
            messagebox.showerror("No se pudo lanzar", str(error), parent=self.ventana)
            return
        if self.juego.lanzamientos_restantes == 0:
            try:
                self._anotar_mejor_categoria()
            except (RuntimeError, ValueError) as error:
                messagebox.showerror(
                    "No se pudo puntuar", str(error), parent=self.ventana
                )
        self._actualizar()

    def _puntuar_automaticamente(self) -> None:
        try:
            self._anotar_mejor_categoria()
        except (RuntimeError, ValueError) as error:
            messagebox.showerror("No se pudo puntuar", str(error), parent=self.ventana)
            return
        self._actualizar()

    def _anotar_mejor_categoria(self) -> None:
        categoria, puntos = self.juego.puntuar_automaticamente()
        self.mensaje_turno = f"Se anotó automáticamente: {categoria} ({puntos} puntos)."
        for seleccionado in self.seleccionados:
            seleccionado.set(False)

    def _reiniciar(self) -> None:
        confirmar = messagebox.askyesno(
            "Nueva partida",
            "¿Quieres borrar los puntajes y comenzar una partida nueva?",
            parent=self.ventana,
        )
        if not confirmar:
            return
        self.juego = JuegoYahtzee(self.juego.jugadores)
        self.mensaje_turno = ""
        for seleccionado in self.seleccionados:
            seleccionado.set(False)
        self._actualizar()

    def _actualizar(self) -> None:
        activo = self.juego.nombre_jugador_activo
        self.estado.configure(
            text=(
                f"Turno: {activo}    |    Ronda: {min(self.juego.ronda, 13)} de 13"
                f"    |    Lanzamientos restantes: {self.juego.lanzamientos_restantes}"
            )
        )
        puede_fijar = self.juego.ha_lanzado and self.juego.lanzamientos_restantes > 0
        for indice, boton in enumerate(self.botones_dados):
            valor = self.juego.dados[indice] or "—"
            marca = "  ✓ Conservado" if self.seleccionados[indice].get() else ""
            boton.configure(
                text=f"Dado {indice + 1}: {valor}{marca}",
                state="normal" if puede_fijar else "disabled",
            )
        self.boton_lanzar.configure(
            state="normal"
            if not self.juego.terminado and self.juego.lanzamientos_restantes > 0
            else "disabled"
        )
        self.boton_puntuar.configure(
            state="normal"
            if self.juego.ha_lanzado
            and not self.juego.terminado
            and self.juego.lanzamientos_restantes > 0
            else "disabled"
        )
        self.boton_montecarlo.configure(
            state="disabled" if self.juego.terminado else "normal"
        )
        if self.mensaje_turno:
            texto_sugerencia = self.mensaje_turno
        elif self.juego.ha_lanzado:
            categoria, puntos = self.juego.mejor_categoria_disponible()
            texto_sugerencia = (
                f"Si terminas ahora, se anotará {categoria} ({puntos} puntos)."
                " En la tercera tirada se anotará automáticamente."
            )
        else:
            texto_sugerencia = (
                "Lanza hasta tres veces. Tras la tercera tirada se anotará"
                " automáticamente la categoría disponible con más puntos."
            )
        self.sugerencia.configure(text=texto_sugerencia)

        for jugador in self.juego.jugadores:
            for categoria in EvaluadorYahtzee.CATEGORIAS:
                puntos = self.juego.puntajes[jugador][categoria]
                self.celdas_puntaje[jugador, categoria].configure(
                    text="—" if puntos is None else str(puntos)
                )

        lineas = []
        for jugador in self.juego.jugadores:
            subtotal = self.juego.subtotal_superior(jugador)
            bonificacion = self.juego.bonificacion_superior(jugador)
            total = self.juego.puntaje_total(jugador)
            lineas.append(
                f"{jugador}: subtotal superior {subtotal}/63"
                f" | bonificación {bonificacion} | total {total}"
            )
        self.resumen.configure(text="\n".join(lineas))

        if self.juego.terminado:
            ganador = max(self.juego.jugadores, key=self.juego.puntaje_total)
            puntajes = [self.juego.puntaje_total(j) for j in self.juego.jugadores]
            if puntajes[0] == puntajes[1]:
                resultado = "La partida terminó en empate."
            else:
                resultado = f"¡{ganador} gana la partida!"
            self.estado.configure(text=f"Partida finalizada. {resultado}")

    def _montecarlo(self) -> None:
        n = simpledialog.askinteger(
            "Simulación Monte Carlo",
            "Número de lanzamientos (100 a 500,000):",
            initialvalue=100_000,
            minvalue=100,
            maxvalue=500_000,
            parent=self.ventana,
        )
        if n is None:
            return
        try:
            frecuencias, ruta = SimuladorMontecarlo.simular(n)
        except (RuntimeError, OSError, ValueError) as error:
            messagebox.showerror("Error de simulación", str(error), parent=self.ventana)
            return

        ventana_grafica = tk.Toplevel(self.ventana)
        ventana_grafica.title("Convergencia de Monte Carlo")
        imagen = tk.PhotoImage(file=str(Path(ruta).resolve()))
        etiqueta_grafica = ttk.Label(ventana_grafica, image=imagen)
        etiqueta_grafica.image = imagen
        etiqueta_grafica.pack(fill="both", expand=True)
        messagebox.showinfo(
            "Simulación completada",
            f"Frecuencia final del 1: {frecuencias[-1]:.5f}\n"
            f"Gráfica guardada en: {Path(ruta).resolve()}",
            parent=ventana_grafica,
        )
