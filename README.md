# Aplicación Integral de Monitoreo con ESP32, FastAPI, Jinja2, WebSockets y MongoDB


## Descripción

Este proyecto implementa una solución completa de monitoreo y control que utiliza una variedad de tecnologías para recopilar, procesar, visualizar y almacenar datos de sensores en tiempo real. El sistema se basa en un ESP32 para leer los datos de los sensores, FastAPI para la API backend, Jinja2 para la interfaz web, WebSockets para la comunicación en tiempo real y MongoDB para el almacenamiento de datos.

## Características Principales

*   **Recopilación de Datos de Sensores:** El ESP32 recopila datos de diversos sensores (ej. temperatura, humedad, nivel de suelo, distancia, detección de movimiento y humo).
*   **Comunicación Inalámbrica:** El ESP32 se conecta a una red WiFi y envía los datos recopilados a un servidor FastAPI.
*   **API Backend con FastAPI:** FastAPI proporciona una API robusta y eficiente para recibir, procesar y servir los datos de los sensores.
*   **Interfaz Web con Jinja2:** Jinja2 se utiliza para renderizar una interfaz web intuitiva que muestra los datos de los sensores.
*   **Actualizaciones en Tiempo Real con WebSockets:** WebSockets permiten la comunicación bidireccional en tiempo real entre el servidor y el cliente web, lo que permite mostrar los datos de los sensores en tiempo real.
*   **Almacenamiento de Datos con MongoDB:** MongoDB se utiliza para almacenar los datos de los sensores de forma persistente, lo que permite realizar análisis históricos y generar informes.
*   **Alertas:** El sistema genera alertas en tiempo real basadas en los datos de los sensores (ej. detección de movimiento o humo).

## Diagrama de Arquitectura

[Incluye aquí un diagrama de arquitectura que muestre cómo interactúan los diferentes componentes del sistema.  Puedes usar herramientas como draw.io para crear el diagrama y luego exportarlo como una imagen.]

## Tecnologías Utilizadas

*   **Hardware:**
    *   ESP32
    *   [Lista de sensores específicos que utilizas (ej. DHT11, HC-SR04, MQ2, PIR)]
*   **Software/Frameworks:**
    *   Arduino (para la programación del ESP32)
    *   Python
    *   FastAPI
    *   Jinja2
    *   WebSockets
    *   MongoDB
    *   [Otras librerías o dependencias relevantes]

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

*   Arduino IDE con soporte para ESP32
*   Python 3.7+
*   MongoDB
*   pip (el gestor de paquetes de Python)

## Instalación

Sigue estos pasos para instalar y configurar el proyecto:

1.  **Clona el repositorio:**

    ```bash
    git clone [URL del repositorio]
    cd [nombre del directorio del repositorio]
    ```

2.  **Configura el ESP32:**

    *   Abre el archivo `[nombre del archivo .ino]` en el Arduino IDE.
    *   Modifica las credenciales de WiFi (`ssid` y `password`) en el código.
    *   Ajusta la URL del servidor FastAPI (`serverUrl`) si es necesario.
    *   Carga el código en tu ESP32.

3.  **Configura el servidor FastAPI:**

    *   Crea un entorno virtual (opcional pero recomendado):

        ```bash
        python3 -m venv venv
        source venv/bin/activate  # o venv\Scripts\activate en Windows
        ```

    *   Instala las dependencias de Python:

        ```bash
        pip install -r requirements.txt
        ```

    *   Configura la conexión a MongoDB:

        *   Asegúrate de que MongoDB esté instalado y en ejecución.
        *   Modifica la cadena de conexión a MongoDB en el archivo `main.py` (si es necesario).

    *   Ejecuta el servidor FastAPI:

        ```bash
        uvicorn main:app --reload
        ```

4.  **Accede a la interfaz web:**

    *   Abre tu navegador web y navega a la URL del servidor FastAPI (por defecto, `http://localhost:8000`).

## Configuración

*   **Sensores:** Ajusta los pines de los sensores en el código del ESP32 (`[nombre del archivo .ino]`) según tu configuración.
*   **MongoDB:** Modifica la cadena de conexión a MongoDB en el archivo `main.py` para que coincida con tu configuración de MongoDB.
*   **Alertas:** Ajusta los umbrales de las alertas en el archivo `main.py` según tus necesidades.
*   **Interfaz Web:** Personaliza la interfaz web modificando los archivos HTML y CSS en el directorio `templates`.

## Uso

Una vez que hayas instalado y configurado el proyecto, puedes utilizarlo para:

*   **Monitorear los datos de los sensores en tiempo real** a través de la interfaz web.
*   **Recibir alertas** cuando se detecten eventos importantes.
*   **Almacenar los datos de los sensores** para su posterior análisis.

## Próximos Pasos

*   Implementar un sistema de autenticación y autorización para proteger la interfaz web.
*   Agregar soporte para más tipos de sensores.
*   Desarrollar una aplicación móvil para acceder a los datos de los sensores.
*   Implementar un sistema de control para actuar sobre los datos de los sensores (ej. encender o apagar un relé).

## Contribución

¡Las contribuciones son bienvenidas! Si encuentras algún error o tienes alguna sugerencia, no dudes en crear un "issue" o enviar un "pull request".

## Licencia

[Indica la licencia bajo la que se distribuye el proyecto (ej. MIT, Apache 2.0, GPL3)]

## Contacto

[Gabriel Fernando Correa]
[gabrielfcorrea3@gmail.com]