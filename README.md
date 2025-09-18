# Sistema de Gestión de Inventario para Lubricentro Huincacara

![Logo Lubricentro](https://imgur.com/a/ekZrcBH) <!-- Opcional: Reemplaza este link por un logo que subas a imgur o similar -->

## Descripción del Proyecto

Este proyecto es una aplicación web desarrollada como parte de la actividad de **Aprendizaje + Servicio (A+S)** de la asignatura **Arquitectura de Software** en AIEP. La solución fue creada para el **Lubricentro Huincacara**, una pyme local de la zona Lacustre, con el objetivo de digitalizar y optimizar su gestión manual de inventario.

El sistema reemplaza el tradicional registro en cuaderno por una página web para la gestión del inventario del Lubricentro, permitiendo un control preciso del stock de aceites, filtros, repuestos e insumos.

## Funcionalidades Principales

La aplicación fue diseñada siguiendo un patrón de arquitectura **Modelo-Vista-Controlador (MVC)**. Sus funcionalidades clave incluyen:

-   **Gestión de Productos:**
    -   Añadir nuevos productos al inventario (aceites, filtros, etc.).
    -   Ver un listado completo de productos con su stock actual.
-   **Gestión de Trabajadores:**
    -   Registrar a los miembros del equipo.
    -   Activar o desactivar trabajadores según su estado contractual.
-   **Control de Movimientos de Inventario:**
    -   **Entradas:** Registrar la recepción de nuevos productos para aumentar el stock.
    -   **Asignaciones:** Asignar productos a un trabajador para un servicio específico, disminuyendo el stock automáticamente.
    -   **Mermas:** Registrar pérdidas de productos por daño o vencimiento.
-   **Módulo de Reportes:**
    -   Consultar el historial de todos los movimientos.
    -   Filtrar los registros por rango de fechas, tipo de producto y/o trabajador para un análisis detallado.

## Tecnologías Utilizadas

-   **Backend:**
    -   **Lenguaje:** Python 3.10
    -   **Framework:** Flask
    -   **ORM:** SQLAlchemy
-   **Frontend:**
    -   **Framework CSS:** Bootstrap 5
    -   **Motor de Plantillas:** Jinja2
-   **Base de Datos:**
    -   MySQL

## Ejecución en Entorno Local

Para ejecutar este proyecto en un entorno de desarrollo local sigue este paso a paso:

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/tu-usuario/taller-huincacara.git
    cd taller-huincacara
    ```

2.  **Crear y activar un entorno virtual:**
    ```bash
    python -m venv venv
    # En Windows (Git Bash)
    source venv/Scripts/activate
    # En macOS/Linux
    source venv/bin/activate
    ```

3.  **Instalar las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar la base de datos:**
    -   Importante contar con un servidor MySQL en funcionamiento + un motor de gestión de base de datos, Ej: MySQL Workbench (gratis).
    -   Crea una base de datos vacía (ej: `lubricentro_db`).
    -   Crea un archivo `.env` en la raíz del proyecto y configúralo con tus credenciales:
        ```env
        SECRET_KEY='tu-clave-secreta-de-ejemplo'
        DATABASE_URL='mysql+mysqlconnector://tu_usuario:tu_contraseña@localhost/lubricentro_db'
        ```

5.  **Iniciar la aplicación:**
    -   La aplicación creará las tablas automáticamente la primera vez que se inicie.
    ```bash
    python run.py
    ```
    -   Abre tu navegador y ve a `http://127.0.0.1:5000`.

## Autor

-   **Johann Mora Mira** - *Desarrollo Completo*
