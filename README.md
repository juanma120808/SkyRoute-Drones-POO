# 🛸 SkyRoute Drones - Sistema Integrado de Telemetría, Logística y Tráfico Aéreo Unmanned (UAS)

**Asignatura:** Algoritmos de Programación Orientada a Objetos  
**Grupo:** 62  
**Docente:** Mario Alejandro Saldarriaga  
**Institución:** Universidad de Medellín (UDEM)  
**Semestre:** 2026-II  

---

## 👥 Integrantes del Equipo
* **Juan Manuel Pava Higuita** - T.I. 1032015000
* **Valery Arboleda Ardila** - T.I. 1020116767
* **Alejandro García Jiménez** - T.I. 1021808372

---

## 📌 Resumen Ejecutivo del Proyecto
**SkyRoute Drones** es un sistema de software desarrollado bajo el paradigma de **Programación Orientada a Objetos (POO)** en Python. El sistema está concebido para gestionar la flota de vehículos aéreos no tripulados (drones) de una empresa de entregas de última milla. 

El sistema incluye:
1. **Módulo de Validaciones de Telemetría y Geofencing**: Filtrado estricto de tramas aeronáuticas, verificación de altitud, batería, estado de motores y coordenadas geográficas.
2. **Módulo de Gestión Logística de Envíos Críticos**: Priorización de entregas médicas/urgentes y estimación de autonomía energética por ruta.
3. **Módulo de Protocolos de Contingencia e Inteligencia de Tráfico Aéreo**: Monitoreo de seguridad en tiempo real, detección de fallas y comando de Retorno Automático a Base (RTH).

---

## 📂 Estructura del Repositorio
```
SkyRoute-Drones-POO/
├── README.md                           # Presentación general e información del proyecto
├── .gitignore                          # Archivos omitidos en el control de versiones
├── docs/                               # Documentación formal del proyecto
│   ├── 01_planteamiento_y_descripcion.md # Marco del problema y contexto operacional
│   ├── 02_requisitos_funcionales.md      # Requisitos innovadores por integrante y prototipos CLI
│   ├── 03_modelo_del_mundo_uml.md        # Notación UML de clases y asignación de responsabilidades
│   └── 04_referencias_y_normativa.md     # Normativa aeronáutica (UAEAC/FAA) y fórmulas matemáticas
└── src/                                # Código fuente modular (Desarrollo POO)
```

---

## 🛠️ Tecnologías y Librerías Previstas
* **Lenguaje Principal:** Python 3.10+
* **Paradigma:** Programación Orientada a Objetos (POO) con encapsulamiento, herencia y polimorfismo.
* **Librerías Externas / Módulos:**
  * `math`: Cálculo de distancias ortodrómicas mediante la fórmula de Haversine.
  * `datetime` / `time`: Registro de marcas temporales (timestamps) de tramas de telemetría.
  * `typing`: Anotaciones estáticas de tipos (`Tuple`, `List`, `Optional`, `Dict`).
  * `tabulate` / `rich` *(Librerías externas)*: Formateo avanzado de salidas y paneles de control en consola.

---

## 📜 Licencia y Uso Académico
Proyecto desarrollado con fines estrictamente académicos para la materia **Algoritmos de Programación Orientada a Objetos** en la Universidad de Medellín.
