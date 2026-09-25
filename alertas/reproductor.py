"""
Reproductor de alertas sonoras no bloqueante.

# LABORATORIO
La cola usa deque y cada elemento conserva su marca de tiempo. El hilo
reproductor espera por la condicion y el ciclo principal solamente agrega
la alerta a la cola, por lo que el dashboard no queda bloqueado.
"""

import os
import signal
import subprocess
import threading
import time
from collections import deque

import config

RUTA_SONIDOS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sonidos")

# LABORATORIO: cola solicitada por el enunciado.
cola_sonidos = deque()
_condicion = threading.Condition()
_sonido_pausado = threading.Event()
_sonido_pausado.set()
_proceso_actual = None
_bloqueo_proceso = threading.Lock()
_ultima_reproduccion = 0.0


def _obtener_siguiente():
    with _condicion:
        while not cola_sonidos:
            _condicion.wait()
        return cola_sonidos.popleft()


def trabajador_sonidos():
    global _proceso_actual, _ultima_reproduccion

    while True:
        # LABORATORIO: cada alerta conserva la marca de tiempo de entrada.
        marca, nombre_archivo = _obtener_siguiente()
        _sonido_pausado.wait()

        ruta = os.path.join(RUTA_SONIDOS, nombre_archivo)
        if not os.path.isfile(ruta):
            continue

        try:
            proceso = subprocess.Popen(
                [config.REPRODUCTOR_SONIDO, "--no-video", "--really-quiet", ruta],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            with _bloqueo_proceso:
                _proceso_actual = proceso

            # LABORATORIO: la espera ocurre solamente en este hilo, nunca en
            # nucleo.ciclo() ni en el hilo de Tkinter.
            proceso.wait()
            _ultima_reproduccion = marca
        except Exception as error:
            print(f"Error al reproducir sonido: {error}")
        finally:
            with _bloqueo_proceso:
                _proceso_actual = None


hilo_sonidos = threading.Thread(target=trabajador_sonidos, daemon=True)
hilo_sonidos.start()


def reproducir_sonido(nombre_archivo):
    """Agrega un sonido a la cola y retorna inmediatamente."""
    # LABORATORIO: marca de tiempo + deque, sin esperar a que termine el audio.
    with _condicion:
        cola_sonidos.append((time.monotonic(), nombre_archivo))
        _condicion.notify()


def pausar_sonido():
    _sonido_pausado.clear()
    with _bloqueo_proceso:
        if _proceso_actual is not None:
            try:
                _proceso_actual.send_signal(signal.SIGSTOP)
            except Exception:
                pass


def reanudar_sonido():
    with _bloqueo_proceso:
        if _proceso_actual is not None:
            try:
                _proceso_actual.send_signal(signal.SIGCONT)
            except Exception:
                pass
    _sonido_pausado.set()
