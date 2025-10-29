
# Sistema Experto para Recomendación de Técnicas de Aprendizaje Profundo

## Descripción
Este proyecto es un sistema experto diseñado para [describir brevemente el propósito del sistema, por ejemplo: "diagnosticar problemas técnicos en equipos" o "recomendar tratamientos médicos basados en síntomas"]. Utiliza una base de conocimiento en formato JSON y una interfaz gráfica desarrollada con PyQt5 para facilitar la interacción con el usuario.

## Características
- **Interfaz gráfica intuitiva** desarrollada con PyQt5.
- **Base de conocimiento** en formato JSON para facilitar la actualización y mantenimiento.
- **Pruebas automatizadas** para validar la lógica del sistema experto.
- **Módulos independientes** para facilitar la escalabilidad y el mantenimiento.

## Requisitos
- Python 3.11
- Bibliotecas externas: Ver `requisitos.txt`.

## Instalación

### 1. Clonar el Repositorio
Clona el repositorio del proyecto desde GitHub (o descarga el código fuente):
```bash
git clone https://github.com/RenatoLXIX/tarea3ia.git
```

### 2. Crear un Entorno Virtual
Abre una terminal en la carpeta del proyecto y ejecuta:
```bash
python -m venv mi_entorno
```

### 3. Activar el Entorno Virtual
- **Windows:**
  ```bash
  mi_entorno\Scripts\Activate
  ```
- **Linux/Mac:**
  ```bash
  source mi_entorno/bin/activate
  ```

### 4. Instalar Dependencias
Instala las bibliotecas necesarias:
```bash
pip install -r requisitoss.txt
```

## Ejecución
Ejecuta el siguiente comando para iniciar el sistema experto:
```bash
python main.py
```

## Estructura del Proyecto
```
.
├── base_conocimiento.json  # Base de conocimiento del sistema experto
├── interfaz_grafica.py     # Interfaz gráfica del sistema
├── main.py                 # Punto de entrada principal
├── sistema_experto.py      # Lógica del sistema experto
├── test_sistema_experto.py # Pruebas automatizadas
└── README.md               # Este archivo
```

## Uso
1. **Iniciar el Sistema:** Ejecuta `main.py` desde la terminal.
2. **Cargar Base de Conocimiento:** Selecciona el archivo `base_conocimiento.json`.
3. **Introducir Datos:** Completa los campos requeridos en la interfaz.
4. **Obtener Resultados:** Haz clic en "Analizar" para ver las recomendaciones.

## Contribución
Si deseas contribuir a este proyecto, sigue estos pasos:
1. Haz un *fork* del repositorio.
2. Crea una rama con tu nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz *commit* (`git commit -am 'Añade nueva funcionalidad'`).
4. Sube tus cambios (`git push origin feature/nueva-funcionalidad`).
5. Abre un *Pull Request*.


