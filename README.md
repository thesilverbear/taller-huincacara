# Sistema de Gestión de Inventario para Lubricentro Huincacara

![Estado](https://img.shields.io/badge/Estado-Entrega_Final-success) ![Deploy](https://img.shields.io/badge/Despliegue-Railway-blue)

**🔗 SITIO EN PRODUCCIÓN:** [https://lubricentro-huincacara2-production.up.railway.app/index](https://lubricentro-huincacara2-production.up.railway.app/index)



## 🆕 Actualización Diciembre 2025 (Entrega Final)
En cumplimiento con los requerimientos de la asignatura **Taller de Diseño de Sistemas**, se han implementado las siguientes mejoras técnicas y de usabilidad:

*   **Validación Estricta de Stock:** Implementación de lógica en el backend (Flask/SQLAlchemy) para impedir asignaciones que generen inventario negativo.
*   **Inclusión y Ergonomía (WCAG):** Ajuste de estilos visuales utilizando **Bootstrap 5** para garantizar alto contraste y áreas táctiles ampliadas (botones y formularios), facilitando el uso por personas con visión reducida o en dispositivos móviles.
*   **Prevención de Errores (UX):** Optimización de los formularios de entrada con selectores dinámicos que muestran el stock en tiempo real.

---

## Descripción del Proyecto

Este proyecto es una aplicación web desarrollada como parte de la actividad de **Aprendizaje + Servicio (A+S)** de la asignatura **Arquitectura de Software** en AIEP. La solución fue creada para el **Lubricentro Huincacara**, una pyme local de la zona Lacustre, con el objetivo de digitalizar y optimizar su gestión manual de inventario.

El sistema reemplaza el tradicional registro en cuaderno por una plataforma web robusta, permitiendo un control preciso, trazable y accesible del stock de aceites, filtros, repuestos e insumos.

## Funcionalidades Principales

La aplicación fue diseñada siguiendo un patrón de arquitectura **Modelo-Vista-Controlador (MVC)**. Sus funcionalidades clave incluyen:

-   **Gestión de Productos:**
    -   Añadir nuevos productos al inventario.
    -   Ver un listado completo de productos con su stock actual.
-   **Gestión de Trabajadores:**
    -   Registrar a los miembros del equipo.
    -   Gestión de estado (activo/inactivo) para mantener integridad histórica.
-   **Control de Movimientos de Inventario:**
    -   **Entradas:** Registro de recepción de productos con validación de tipos de datos.
    -   **Asignaciones:** Asignación de productos a trabajadores con **validación de stock en tiempo real**.
    -   **Mermas:** Registro justificado de pérdidas.
-   **Módulo de Reportes:**
    -   Consultas históricas de movimientos.
    -   Filtros dinámicos por fecha, producto y trabajador.

## Tecnologías Utilizadas

-   **Backend:**
    -   **Lenguaje:** Python 3.10
    -   **Framework:** Flask
    -   **ORM:** SQLAlchemy
-   **Frontend:**
    -   **Framework CSS:** Bootstrap 5 (Responsive & Accesible)
    -   **Motor de Plantillas:** Jinja2
-   **Base de Datos:**
    -   MySQL (Producción en Railway)

## Ejecución en Entorno Local

Para ejecutar este proyecto en un entorno de desarrollo local sigue este paso a paso:

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/thesilverbear/taller-huincacara.git
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
    -   Importante contar con un servidor MySQL en funcionamiento.
    -   Crea un archivo `.env` en la raíz del proyecto y configúralo con tus credenciales:
        ```env
        SECRET_KEY='tu-clave-secreta'
        DATABASE_URL='mysql+mysqlconnector://usuario:password@localhost/lubricentro_db'
        ```

5.  **Iniciar la aplicación:**
    ```bash
    python run.py
    ```
    -   Abre tu navegador y ve a `http://127.0.0.1:5000`.

## Autor

-   **Johann Mora Mira** - *Desarrollo Full Stack e Implementación*
