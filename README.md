# Laboratorio N.º 1 — Alertas sonoras para el nodo de telemetría

## Datos del estudiante

**Estudiante:** Solin Rodriguez
**Cédula:** 8-1032-104
**Docente:** Kexy Rodriguez
**Asignatura:** Desarrollo de Software VIII
**Laboratorio:** N.º 1 — Alertas sonoras para el nodo de telemetría

---

## Descripción

Este proyecto corresponde al **Laboratorio N.º 1: Alertas sonoras para el nodo de telemetría**.

El objetivo principal es incorporar un sistema de alertas sonoras al proyecto de monitoreo de telemetría, permitiendo reaccionar ante diferentes eventos detectados en el sistema sin detener la actualización del dashboard ni el proceso de monitoreo.

El sistema permite generar alertas para diferentes situaciones relacionadas con el uso de recursos del equipo y el estado de la conexión de red.

---

## Funcionalidades implementadas

El proyecto incorpora las siguientes funcionalidades:

* 🔊 Alertas sonoras para diferentes eventos.
* 🖥️ Alertas relacionadas con el uso de CPU.
* 💾 Alertas relacionadas con el uso de memoria RAM.
* 🌐 Alertas relacionadas con el tráfico de red.
* 📡 Detección de pérdida de conexión.
* 🔄 Detección de recuperación de conexión.
* ⏱️ Recordatorio cuando la conexión continúa perdida durante el tiempo configurado.
* ⚡ Reproducción de sonidos sin bloquear el funcionamiento del sistema.
* 📋 Gestión de sonidos mediante una cola `deque`.
* 🕒 Uso de marcas de tiempo para controlar las alertas.
* ⚙️ Configuración centralizada de sonidos, tiempos y umbrales.
* 🧪 Pruebas unitarias mediante `unittest`.

---

## Eventos de red

Se implementaron los siguientes eventos:

| Evento                   | Descripción                                                                                    |
| ------------------------ | ---------------------------------------------------------------------------------------------- |
| `red_desconectada`       | Se genera cuando se detecta una pérdida de conexión.                                           |
| `red_conectada`          | Se genera cuando la conexión vuelve a estar disponible.                                        |
| `red_sigue_desconectada` | Se genera como recordatorio cuando la conexión continúa perdida durante el tiempo establecido. |

Los eventos de conexión y desconexión se manejan como eventos de cambio de estado, evitando generar continuamente el mismo evento mientras el estado permanece igual.

---

## Sistema de alertas

Las alertas sonoras se encuentran organizadas dentro del paquete:

```text
alertas/
```

El sistema utiliza una cola de tipo `deque` para administrar las alertas pendientes y marcas de tiempo para controlar su reproducción.

La reproducción se realiza de manera no bloqueante, permitiendo que el sistema continúe:

* Actualizando el dashboard.
* Obteniendo información de los sensores.
* Detectando eventos.
* Procesando nuevas alertas.

Mientras un sonido se encuentra en reproducción.

---

## Estructura del proyecto

Una estructura general del proyecto es:

```text
monitor_iot/
│
├── alertas/
│   ├── __init__.py
│   └── ...
│
├── eventos/
│   ├── __init__.py
│   ├── detectores.py
│   ├── despachador.py
│   └── manejadores.py
│
├── sensores/
│   ├── cpu.py
│   ├── memoria.py
│   ├── red.py
│   └── ...
│
├── tests/
│   ├── __init__.py
│   └── test_alertas.py
│
├── sonidos/
│   └── ...
│
├── config.py
├── main.py
└── README.md
```

La estructura puede variar ligeramente dependiendo de los archivos incluidos en la versión final del proyecto.

---

## Configuración

Los sonidos, tiempos y umbrales utilizados por el sistema se encuentran centralizados en:

```text
config.py
```

Esto permite modificar la configuración sin tener que cambiar directamente la lógica de los sensores o detectores.

---

## Requisitos

Para ejecutar el proyecto se requiere:

* Python 3.x
* `psutil`
* Tkinter
* Sistema operativo compatible con la reproducción de los sonidos utilizados.

Las dependencias adicionales pueden instalarse mediante:

```bash
pip install psutil
```

---

## Ejecución

Desde la carpeta principal del proyecto:

```bash
python main.py
```

Para ejecutar la revisión del proyecto, si está disponible:

```bash
python main.py --revisar
```

---

## Pruebas unitarias

Las pruebas unitarias se encuentran dentro de:

```text
tests/
```

Para ejecutar todas las pruebas:

```bash
python -m unittest discover -v
```

El comando permite verificar el funcionamiento de las funcionalidades implementadas mediante el módulo estándar `unittest` de Python.

Un resultado correcto debe finalizar indicando:

```text
OK
```

---

## Pruebas principales

Las pruebas están orientadas a verificar el comportamiento de las alertas y los eventos implementados, incluyendo:

* Detección de desconexión de red.
* Detección de recuperación de red.
* Generación del evento de conexión perdida prolongada.
* Funcionamiento de la gestión de alertas.

---

## Funcionamiento no bloqueante

Uno de los puntos principales del laboratorio es evitar que la reproducción de sonidos detenga el funcionamiento del sistema.

La reproducción de una alerta se procesa de forma independiente, mientras que el programa principal continúa ejecutando sus tareas de monitoreo.

De esta manera, una alerta sonora no debe impedir que:

```text
Sensores → Detectores → Eventos → Alertas
                 ↓
             Dashboard
```

continúen funcionando.

---

## Identificación de cambios del laboratorio

Las líneas y bloques agregados o modificados específicamente para este laboratorio se encuentran identificados mediante:

```python
# LABORATORIO
```

Esto permite diferenciar las modificaciones realizadas para el Laboratorio N.º 1 respecto al proyecto base.

---

## Tecnologías utilizadas

* **Python**
* **psutil**
* **Tkinter**
* **unittest**
* **collections.deque**
* Reproducción de archivos de sonido
* Arquitectura basada en sensores, detectores y eventos

---

## Autor

**Solin Rodriguez**
**Cédula:** 8-1032-104

**Docente:** Kexy Rodriguez

**Universidad Tecnológica de Panamá**

---

## Nota

Este proyecto fue desarrollado como parte de las actividades académicas de la asignatura **Desarrollo de Software VIII** y corresponde al Laboratorio N.º 1 sobre la implementación de alertas sonoras para un nodo de telemetría.
