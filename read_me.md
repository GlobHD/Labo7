# Laboratorio VI.1 - Cálculo Numérico con GUI

Este repositorio contiene la resolución del Laboratorio VI.1 de la asignatura Informática II. El proyecto consiste en una aplicación de escritorio desarrollada en Python con una interfaz gráfica (GUI) construida con `tkinter`, diseñada para resolver diversos problemas de cálculo numérico sin depender de librerías externas para los cálculos principales.

## Características principales

La aplicación implementa los siguientes métodos numéricos:

1. **Cálculo de Raíces:**
   * Métodos: Bisección, Newton-Raphson y Secante.
   * Aplica a un polinomio de grado 6 definido por el usuario (por defecto: $f(x) = -25 + 82x - 8x^3 + x^5$).
   * Permite establecer condiciones de parada por error aproximado relativo ($\epsilon_s$) o por cantidad de cifras significativas.

2. **Cálculo de Derivadas:**
   * Método de diferencia finita centrada dividida para calcular la primera derivada en un punto $x$ con un paso $h$.

3. **Sistemas de Ecuaciones Lineales:**
   * Resolución de un sistema matricial de 4x4 mediante Eliminación de Gauss.
   * Soporte para ejecución con y sin pivoteo parcial (incluye detección de pivotes nulos).

4. **Integración Numérica:**
   * Cálculo del área bajo la curva mediante el método de Simpson 1/3 compuesta.

## Requisitos

* Python 3.x
* Módulo `tkinter` (usualmente incluido en la instalación estándar de Python).

## Ejecución

Para iniciar la aplicación, clona este repositorio y ejecuta el script principal desde tu terminal:

```bash
python index.py
```