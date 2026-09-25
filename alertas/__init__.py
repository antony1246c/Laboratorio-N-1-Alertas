"""Paquete de alertas sonoras del nodo de telemetria."""

from .reproductor import reproducir_sonido, pausar_sonido, reanudar_sonido

__all__ = ["reproducir_sonido", "pausar_sonido", "reanudar_sonido"]
