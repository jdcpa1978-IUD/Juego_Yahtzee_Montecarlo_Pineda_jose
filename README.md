# Juego Yahtzee Monte Carlo Pineda José

Este repositorio contiene la implementación del juego clásico de Yahtzee para
dos jugadores con una interfaz gráfica en tkinter (Python), así como un módulo
de simulación estadística basado en el método de Monte Carlo para mostrar
numéricamente la Ley de los Grandes Números.

## Archivos

- `backend.py`: dados, reglas de puntuación, estado de la partida y simulador.
- `frontend.py`: interfaz gráfica de escritorio con tkinter.
- `main.py`: punto de entrada de la aplicación.
- `Pineda_Jose_Montecarlo.pdf`: documento técnico del proyecto.
- `convergencia_montecarlo.png`: gráfica de convergencia incluida como evidencia.
- `requirements.txt`: dependencias externas.

## Juego

La aplicación implementa las 13 categorías estándar, tres lanzamientos por
turno, dados conservables, subtotal superior y bonificación de 35 puntos al
alcanzar 63 puntos. **Nueva partida** limpia la hoja de puntos después de
solicitar confirmación.

El Jugador 1 completa sus 13 turnos antes que el Jugador 2. Después de la
tercera tirada, se anota automáticamente la categoría disponible con mayor
puntuación inmediata. Para terminar antes, se puede usar **Terminar turno y
anotar**. El tablero actualiza los puntajes automáticamente.

## Ejecución

Se requiere Python 3.10 o posterior. Desde PowerShell, dentro de la carpeta del
proyecto, instala las dependencias y ejecuta la aplicación:

```powershell
py -m pip install -r requirements.txt
py main.py
```

El botón **Simulación Monte Carlo** acepta de 100 a 500,000 lanzamientos,
muestra la convergencia de la frecuencia del dado 1 hacia `1/6` y guarda la
gráfica como `convergencia_montecarlo.png` en la carpeta actual.

## Documento técnico

El informe técnico contiene introducción, metodología, arquitectura, resultados
de una simulación reproducible, conclusiones y referencias. La interpretación
USA–MODIFICA–CREA se presenta como propuesta, ya que no se contó con la guía
original del curso.
