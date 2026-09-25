"""Sensor de trafico y estado de conexion de red."""

import socket
import time

import psutil
import config

ETIQUETA = "Red"
UNIDAD = "KB/s"

KB = 1024.0
MB = 1024.0 ** 2
_anterior = {"enviados": 0, "recibidos": 0, "marca": 0.0}
_iniciado = False
_conexion_anterior = None


def disponible():
    try:
        return psutil.net_io_counters() is not None
    except Exception:
        return False


def conectada():
    """Comprueba la conectividad sin permanecer esperando demasiado."""
    try:
        interfaces = psutil.net_if_stats()
        if not any(datos.isup for nombre, datos in interfaces.items() if nombre != "lo"):
            return False
        # LABORATORIO: timeout centralizado en config.py para limitar la espera.
        with socket.create_connection(("8.8.8.8", 53), timeout=config.RED_CONECTIVIDAD_TIMEOUT):
            return True
    except (OSError, socket.timeout):
        return False


def estado_conexion():
    """Devuelve solamente los flancos de conexion/desconexion."""
    global _conexion_anterior
    estado_actual = conectada()
    if _conexion_anterior is None:
        _conexion_anterior = estado_actual
        return None

    evento = None
    # LABORATORIO: flanco de perdida de conexion.
    if _conexion_anterior and not estado_actual:
        evento = "red_desconectada"
    # LABORATORIO: flanco de recuperacion de conexion.
    elif not _conexion_anterior and estado_actual:
        evento = "red_conectada"

    _conexion_anterior = estado_actual
    return evento


def _iniciar():
    global _iniciado
    c = psutil.net_io_counters()
    _anterior.update({"enviados": c.bytes_sent, "recibidos": c.bytes_recv, "marca": time.monotonic()})
    _iniciado = True


def leer():
    global _iniciado
    evento_conexion = estado_conexion()
    conectividad_actual = _conexion_anterior

    if not _iniciado:
        _iniciar()
        return None

    try:
        c = psutil.net_io_counters()
    except Exception:
        return None

    ahora = time.monotonic()
    transcurrido = ahora - _anterior["marca"]
    if transcurrido <= 0:
        return None

    subida = (c.bytes_sent - _anterior["enviados"]) / KB / transcurrido
    bajada = (c.bytes_recv - _anterior["recibidos"]) / KB / transcurrido
    _anterior.update({"enviados": c.bytes_sent, "recibidos": c.bytes_recv, "marca": ahora})
    total = subida + bajada
    tope = max(config.RED_PICO_KBS * 2, 1.0)

    return {
        "valor": round(total, 1),
        "unidad": UNIDAD,
        "porcentaje": min(100.0, total / tope * 100.0),
        "detalle": f"sube {subida:.1f} | baja {bajada:.1f} KB/s | total {(c.bytes_sent + c.bytes_recv) / MB:.0f} MB",
        "extra": {
            "subida_kbs": round(subida, 1),
            "bajada_kbs": round(bajada, 1),
            "conectada": conectividad_actual,
            "evento_conexion": evento_conexion,
        },
    }
