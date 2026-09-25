""" 
config.py 
Parametros de configuracion del nodo de telemetria. 
  
Todo lo que puede cambiar entre una instalacion y otra vive aqui. 
Ningun otro archivo del proyecto debe contener un numero literal. 
  
Unidad 2 - Programacion en Python para sistemas IoT 
Facultad de Ingenieria de Sistemas Computacionales - UTP 
""" 
  
import os 
  
# -------------------------------------------------------------------------- 
# Identificacion del nodo 
# -------------------------------------------------------------------------- 
NODO = "Solin Rodriguez"
UBICACION = "UTP - FISC - Desarrollo de Software VIII"
  
# -------------------------------------------------------------------------- 
# Periodos de muestreo, en segundos. 
# Cada metrica tiene el suyo: leer los procesos es caro, leer la CPU no. 
# -------------------------------------------------------------------------- 
PERIODO_RAPIDO = 1.0      # cpu, memoria, red 
PERIODO_LENTO = 5.0       # disco, procesos, bateria 
PERIODO_REPORTE = 30.0    # resumen periodico hacia la bitacora 
  
REFRESCO_MS = 200         # cada cuanto refresca el dashboard (milisegundos) 
  
# -------------------------------------------------------------------------- 
# Umbrales. Dos valores por metrica: uno para entrar en alarma y otro, 
# mas bajo, para salir de ella. Esa diferencia es la HISTERESIS y evita 
# que una lectura oscilando en el limite genere decenas de eventos falsos. 
# -------------------------------------------------------------------------- 
CPU_ALTO = 80.0  # LABORATORIO: umbral de entrada de CPU
CPU_BAJO = 60.0  # LABORATORIO: umbral de salida de CPU 
CPU_NUCLEO_SATURADO = 90.0    # un nucleo individual por encima de esto 
  
RAM_ALTA = 71.0  # LABORATORIO: umbral de entrada de RAM
RAM_BAJA = 70.0  # LABORATORIO: umbral de salida de RAM 
  
DISCO_LLENO = 10.0            # LABORATORIO: porcentaje de ocupacion
DISCO_ALIVIADO = 85.0 
  
RED_PICO_KBS = 500.0          # kilobytes por segundo 
RED_CALMA_KBS = 200.0 
  
BATERIA_BAJA = 20.0 
BATERIA_RECUPERADA = 30.0 
  
PROCESO_PESADO = 50.0         # % de CPU de un solo proceso 
  
# Variacion brusca entre dos muestras consecutivas: evento de anomalia. 
SALTO_ANOMALO = 40.0 
  
# --------------------------------------------------------------------------
# Alertas sonoras y conexion de red
# --------------------------------------------------------------------------
# LABORATORIO: todos los sonidos, tiempos y parametros de red agregados
# para este laboratorio se centralizan aqui.
SONIDOS_EVENTOS = {
    "cpu_alta": "cpu_alta.wav",
    "ram_alta": "ram_alta.wav",
    "red_pico": "red_pico.wav",
    "red_desconectada": "red_desconectada.wav",
    "red_conectada": "red_conectada.wav",
    "red_sigue_desconectada": "red_sigue_desconectada.wav",
}
RED_RECORDATORIO_SEGUNDOS = 30.0
RED_CONECTIVIDAD_TIMEOUT = 0.2
REPRODUCTOR_SONIDO = "mpv"

# -------------------------------------------------------------------------- 
# Ventana movil y almacenamiento 
# -------------------------------------------------------------------------- 
VENTANA = 10              # muestras que se promedian para evaluar el umbral 
MAX_EVENTOS_LOG = 200     # eventos que se conservan en pantalla 
ARCHIVO_BITACORA = "bitacora.json" 
  
# -------------------------------------------------------------------------- 
# Unidad de disco a vigilar. Se detecta sola segun el sistema operativo. 
# -------------------------------------------------------------------------- 
UNIDAD_DISCO = "C:\\" if os.name == "nt" else "/" 
  
# Cantidad de procesos que se muestran en el ranking. 
TOP_PROCESOS = 8 
  
# Procesos del sistema que no vale la pena reportar: en Linux los 
# 'kworker' y 'kthread' aparecen y desaparecen constantemente y llenarian 
# la bitacora de ruido. 
PROCESOS_IGNORADOS = ("kworker", "kthread", "ksoftirqd", "migration", 
                      "rcu_", "irq/", "svchost") 