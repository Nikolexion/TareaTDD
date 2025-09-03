[![Python Tests](https://github.com/Nikolexion/TareaTDD/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/Nikolexion/TareaTDD/actions/workflows/main.yml)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![License](https://img.shields.io/badge/license-MIT-informational)

# 🎲 Juego de Dudo - TareaTDD

Proyecto desarrollado siguiendo la metodología **Test-Driven Development (TDD)** que implementa el clásico juego de dados "Dudo" o "Cacho".

## 📋 Descripción

El juego de Dudo es un juego de dados de tradicional chileno donde los jugadores deben hacer apuestas sobre la cantidad de dados con una pinta específica que hay en la mesa, considerando todos los dados de todos los jugadores.

### 🎯 Características principales:
- Soporte para múltiples jugadores (bots y humanos)
- Modo "obligado" para mayor estrategia
- Sistema de apuestas, dudas y calzadas
- Interfaz por consola interactiva

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.11 o superior
- pip (gestor de paquetes de Python)

### Dependencias
Instalar las dependencias necesarias:

```bash
pip install pytest pytest-mock pytest-cov
```

### Estructura del Proyecto
```
TareaTDD/
├── src/
│   ├── juego/
│   │   ├── arbitro_ronda.py      # Lógica de arbitraje de rondas
│   │   ├── cacho.py              # Manejo del conjunto de dados
│   │   ├── contador_pintas.py    # Contador de pintas en dados
│   │   ├── dado.py               # Clase individual del dado
│   │   ├── gestor_partida.py     # Gestor principal del juego
│   │   ├── jugador.py            # Clases de jugadores (humano/bot)
│   │   └── validador_apuesta.py  # Validación de apuestas
│   └── servicios/
│       └── generador_aleatorio.py # Generador de números aleatorios
├── testing/
│   └── test_*.py                 # Pruebas unitarias
├── dudo.py                       # Archivo principal del juego
├── pyproject.toml               # Configuración del proyecto
└── README.md                    # Este archivo
```

## 🎮 Cómo Jugar

### Ejecutar el Juego
Para iniciar una partida, ejecuta:

```bash
python dudo.py
```
El juego preguntará:
```
¿Quieres jugar tú mismo (1) o ver una partida automática de bots (2)? Ingresa 1 o 2:
```
Donde al entregar "1" como input permitirá al usuario jugar una partida de Dudo contra 3 Bots, mientras que al dar como input "2" o cualquier otro input ejecutará una partida automática de 4 Bots.

### Reglas Básicas
1. **Elección del orden de turnos**: Todos los jugadores tiran dados para elegir el primer jugador, el cual elegirá si se juega en sentido horario o antihorario
2. **Inicio**: Cada jugador lanza sus 5 dados
3. **Apuesta**: Los jugadores hacen apuestas sobre cuántos dados de una pinta específica hay en total
4. **Acciones disponibles**:
   - **Apostar**: Hacer una apuesta mayor a la anterior
   - **Dudar**: Cuestionar la apuesta actual
   - **Calzar**: Apostar que la cantidad es exacta
5. **Eliminación**: Los jugadores que pierden van perdiendo dados
6. **Victoria**: El último jugador con dados gana

### Reglas Especiales
- **As (1)**: Funciona como comodín, puede representar cualquier pinta
- **Modo Obligado**: Reglas especiales que se activan en ciertas condiciones
- **Calzada**: Si aciertas exactamente, recuperas un dado

## 🧪 Pruebas

Para poder ejecutar las pruebas creadas se puede de la siguiente forma:
```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar con reporte de cobertura
pytest --cov=src --cov-report=term-missing

# Ejecutar pruebas específicas
pytest testing/test_dado.py

# Ejecutar con modo verbose
pytest -v
```