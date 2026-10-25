# Yahtzee para dos jugadores

Proyecto académico de Yahtzee en Python con interfaz gráfica y simulación
Monte Carlo de la Ley de los Grandes Números.

## Archivos

- `backend.py`: dados, reglas de puntuación, estado de la partida y simulador.
- `frontend.py`: interfaz gráfica de escritorio con tkinter.
- `main.py`: punto de entrada.
- `Pineda_Jose_Montecarlo.pdf`: documento técnico del proyecto.
- `convergencia_montecarlo.png`: gráfica de convergencia incluida como evidencia.
- `requirements.txt`: dependencias externas.

Aplicación de escritorio en Python con interfaz `tkinter`. Incluye los 13
casilleros estándar, tres lanzamientos por turno, dados conservables, subtotal
superior y bonificación de 35 puntos al alcanzar 63 puntos. El botón **Nueva
partida** limpia la hoja de puntos y reinicia el juego después de confirmarlo.
El Jugador 1 completa sus 13 turnos antes que el Jugador 2. Después de la
tercera tirada, se anota automáticamente la categoría disponible con mayor
puntuación; si se desea terminar el turno antes, se puede usar **Terminar turno
y anotar**. El tablero suma los puntajes automáticamente.

## Ejecución

Se requiere Python 3.10 o posterior. Instala la dependencia de gráficas y
ejecuta la aplicación desde esta carpeta:

```powershell
py -m pip install -r requirements.txt
py main.py
```

El botón **Simulación Monte Carlo** acepta de 100 a 500,000 lanzamientos,
muestra la convergencia de la frecuencia del dado 1 hacia `1/6` y guarda
`convergencia_montecarlo.png` en la carpeta actual.

## Documento técnico

El informe del proyecto, con metodología, arquitectura, resultados de una
simulación reproducible y referencias, está en
`Pineda_Jose_Montecarlo.pdf`.

La metodología USA–MODIFICA–CREA del informe es una interpretación propuesta
porque no se contó con la guía original del curso.
