import sys
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLabel, QComboBox, QPushButton, QTextEdit, 
                             QGroupBox, QScrollArea, QFrame, QProgressBar,
                             QTabWidget, QListWidget, QListWidgetItem, QMessageBox,
                             QCheckBox, QSpinBox, QSlider)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon
from sistema_experto import SistemaExpertoDL

class StyledComboBox(QComboBox):
    """ComboBox con estilo personalizado"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QComboBox {
                background-color: #f8f9fa;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                min-height: 20px;
            }
            QComboBox:hover {
                border-color: #007bff;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #6c757d;
                width: 0px;
                height: 0px;
            }
        """)

class StyledButton(QPushButton):
    """Botón con estilo personalizado"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
            QPushButton:disabled {
                background-color: #6c757d;
                color: #ced4da;
            }
        """)

class QuestionGroup(QGroupBox):
    """Grupo de pregunta con estilo personalizado"""
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.setStyleSheet("""
            QGroupBox {
                background-color: #ffffff;
                border: 2px solid #e9ecef;
                border-radius: 12px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
                color: #495057;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                background-color: #ffffff;
            }
        """)

class ResultCard(QFrame):
    """Tarjeta para mostrar resultados"""
    def __init__(self, resultado, parent=None):
        super().__init__(parent)
        self.resultado = resultado
        self.setup_ui()
        
    def setup_ui(self):
        self.setFrameStyle(QFrame.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 16px;
                margin: 8px 0px;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Header con técnica y confianza
        header_layout = QHBoxLayout()
        
        tecnica_label = QLabel(self.resultado['tecnica'])
        tecnica_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #212529;")
        tecnica_label.setWordWrap(True)
        
        confianza = self.resultado['confianza'] * 100
        confianza_label = QLabel(f"{confianza:.1f}%")
        confianza_label.setStyleSheet(f"""
            font-size: 14px; 
            font-weight: bold; 
            color: {'#28a745' if confianza > 80 else '#ffc107' if confianza > 60 else '#dc3545'};
            background-color: {'#d4edda' if confianza > 80 else '#fff3cd' if confianza > 60 else '#f8d7da'};
            border-radius: 12px;
            padding: 4px 12px;
        """)
        
        header_layout.addWidget(tecnica_label)
        header_layout.addWidget(confianza_label)
        layout.addLayout(header_layout)
        
        # Justificación
        justificacion_label = QLabel(self.resultado['justificacion'])
        justificacion_label.setStyleSheet("font-size: 14px; color: #6c757d; margin-top: 8px;")
        justificacion_label.setWordWrap(True)
        layout.addWidget(justificacion_label)
        
        # Regla ID
        regla_label = QLabel(f"Regla aplicada: #{self.resultado['regla_id']}")
        regla_label.setStyleSheet("font-size: 12px; color: #adb5bd; margin-top: 8px;")
        layout.addWidget(regla_label)
        
        self.setLayout(layout)

class InterfazSistemaExperto(QMainWindow):
    """Interfaz gráfica principal del sistema experto"""
    
    def __init__(self):
        super().__init__()
        self.sistema = SistemaExpertoDL("base_conocimiento.json")
        self.hechos_actuales = {}
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Sistema Experto - Recomendación de Técnicas de Aprendizaje Profundo")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1000, 700)
        
        # Estilo general
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QLabel {
                color: #495057;
                font-size: 14px;
            }
            QProgressBar {
                border: 2px solid #dee2e6;
                border-radius: 5px;
                text-align: center;
                background-color: #e9ecef;
            }
            QProgressBar::chunk {
                background-color: #007bff;
                border-radius: 3px;
            }
        """)
        
        # Widget central con tabs
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        
        # Crear las pestañas
        self.setup_consulta_tab()
        self.setup_resultados_tab()
        self.setup_info_tab()
        
        # Mostrar pestaña de consulta por defecto
        self.tab_widget.setCurrentIndex(0)
        
    def setup_consulta_tab(self):
        """Configura la pestaña de consulta"""
        consulta_widget = QWidget()
        layout = QVBoxLayout()
        
        # Título
        titulo = QLabel("Sistema Experto - Recomendación de Técnicas de Aprendizaje Profundo")
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #212529; margin: 20px 0px;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        
        # Descripción
        descripcion = QLabel(
            "Complete el siguiente formulario con las características de su dataset "
            "y obtenga recomendaciones personalizadas de técnicas de aprendizaje profundo."
        )
        descripcion.setStyleSheet("font-size: 14px; color: #6c757d; margin-bottom: 30px;")
        descripcion.setWordWrap(True)
        descripcion.setAlignment(Qt.AlignCenter)
        layout.addWidget(descripcion)
        
        # Área de scroll para las preguntas
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        self.preguntas_layout = QVBoxLayout(scroll_widget)
        
        # Preguntas
        self.setup_preguntas()
        
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Botones
        botones_layout = QHBoxLayout()
        
        self.btn_limpiar = StyledButton("Limpiar Formulario")
        self.btn_limpiar.clicked.connect(self.limpiar_formulario)
        
        self.btn_analizar = StyledButton("Analizar y Recomendar")
        self.btn_analizar.clicked.connect(self.realizar_analisis)
        self.btn_analizar.setStyleSheet(self.btn_analizar.styleSheet() + """
            QPushButton {
                background-color: #28a745;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        
        botones_layout.addWidget(self.btn_limpiar)
        botones_layout.addWidget(self.btn_analizar)
        layout.addLayout(botones_layout)
        
        consulta_widget.setLayout(layout)
        self.tab_widget.addTab(consulta_widget, "🏠 Consulta")
        
    def setup_preguntas(self):
        """Configura todas las preguntas del formulario"""
        
        # 1. Tipo de datos
        grupo_tipo = QuestionGroup("1. Tipo de Datos")
        layout_tipo = QVBoxLayout()
        
        self.combo_tipo = StyledComboBox()
        self.combo_tipo.addItems([
            "Seleccione el tipo de datos...",
            "Imágenes (fotos, dibujos, etc.)",
            "Texto (documentos, mensajes, etc.)", 
            "Series Temporales (datos con orden temporal)",
            "Datos Tabulares (tablas, hojas de cálculo)",
            "Audio (sonidos, voz, música)"
        ])
        self.combo_tipo.currentIndexChanged.connect(self.on_tipo_datos_changed)
        
        layout_tipo.addWidget(QLabel("¿Qué tipo de datos tiene?"))
        layout_tipo.addWidget(self.combo_tipo)
        grupo_tipo.setLayout(layout_tipo)
        self.preguntas_layout.addWidget(grupo_tipo)
        
        # 2. Tamaño del dataset
        grupo_tamano = QuestionGroup("2. Tamaño del Dataset")
        layout_tamano = QVBoxLayout()
        
        self.combo_tamano = StyledComboBox()
        self.combo_tamano.addItems([
            "Seleccione el tamaño...",
            "Muy pequeño (menos de 1,000 muestras)",
            "Pequeño (1,000 - 10,000 muestras)",
            "Medio (10,000 - 100,000 muestras)", 
            "Grande (100,000 - 1,000,000 muestras)",
            "Muy grande (más de 1,000,000 muestras)"
        ])
        
        layout_tamano.addWidget(QLabel("¿Qué tamaño tiene su dataset?"))
        layout_tamano.addWidget(self.combo_tamano)
        grupo_tamano.setLayout(layout_tamano)
        self.preguntas_layout.addWidget(grupo_tamano)
        
        # 3. Recursos computacionales
        grupo_recursos = QuestionGroup("3. Recursos Computacionales")
        layout_recursos = QVBoxLayout()
        
        self.combo_recursos = StyledComboBox()
        self.combo_recursos.addItems([
            "Seleccione los recursos...",
            "Muy bajos (solo CPU básico)",
            "Bajos (CPU bueno, sin GPU)",
            "Medios (GPU básica o limitada)",
            "Altos (GPU buena, como RTX 3080/4090)",
            "Muy altos (múltiples GPUs, servidores)"
        ])
        
        layout_recursos.addWidget(QLabel("¿Qué recursos computacionales tiene disponibles?"))
        layout_recursos.addWidget(self.combo_recursos)
        grupo_recursos.setLayout(layout_recursos)
        self.preguntas_layout.addWidget(grupo_recursos)
        
        # 4. Tarea principal
        grupo_tarea = QuestionGroup("4. Tarea Principal (Opcional)")
        layout_tarea = QVBoxLayout()
        
        self.combo_tarea = StyledComboBox()
        self.combo_tarea.addItems([
            "Seleccione la tarea...",
            "Clasificación (categorizar en clases)",
            "Regresión (predecir valores numéricos)",
            "Segmentación (dividir en partes)",
            "Detección (encontrar objetos)",
            "Generación (crear nuevo contenido)",
            "Reconocimiento de voz"
        ])
        
        layout_tarea.addWidget(QLabel("¿Cuál es la tarea principal que quiere realizar?"))
        layout_tarea.addWidget(self.combo_tarea)
        grupo_tarea.setLayout(layout_tarea)
        self.preguntas_layout.addWidget(grupo_tarea)
        
        # 5. Preguntas específicas (se muestran dinámicamente)
        self.grupo_especifico = QuestionGroup("5. Características Específicas")
        self.layout_especifico = QVBoxLayout()
        self.grupo_especifico.setLayout(self.layout_especifico)
        self.grupo_especifico.setVisible(False)
        self.preguntas_layout.addWidget(self.grupo_especifico)
        
        # 6. Interpretabilidad
        grupo_interpretabilidad = QuestionGroup("6. Interpretabilidad (Opcional)")
        layout_interpretabilidad = QVBoxLayout()
        
        self.check_interpretabilidad = QCheckBox("¿Requiere que el modelo sea interpretable?")
        self.check_interpretabilidad.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                color: #495057;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #6c757d;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #007bff;
                border-radius: 3px;
                background-color: #007bff;
            }
        """)
        
        layout_interpretabilidad.addWidget(self.check_interpretabilidad)
        grupo_interpretabilidad.setLayout(layout_interpretabilidad)
        self.preguntas_layout.addWidget(grupo_interpretabilidad)
        
        # Espaciador
        self.preguntas_layout.addStretch()
        
    def setup_preguntas_especificas(self, tipo_datos):
        """Configura preguntas específicas según el tipo de datos"""
        # Limpiar layout anterior
        for i in reversed(range(self.layout_especifico.count())):
            widget = self.layout_especifico.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        if tipo_datos == "texto":
            self.grupo_especifico.setTitle("5. Características del Texto")
            
            label = QLabel("¿Qué longitud tienen sus textos?")
            self.layout_especifico.addWidget(label)
            
            self.combo_longitud = StyledComboBox()
            self.combo_longitud.addItems([
                "Seleccione la longitud...",
                "Corto (menos de 128 palabras/tokens)",
                "Medio (128-512 palabras/tokens)", 
                "Largo (más de 512 palabras/tokens)"
            ])
            self.layout_especifico.addWidget(self.combo_longitud)
            
        elif tipo_datos == "series_temporales":
            self.grupo_especifico.setTitle("5. Patrones Temporales")
            
            label = QLabel("¿Qué tipo de patrones temporales espera encontrar?")
            self.layout_especifico.addWidget(label)
            
            self.combo_patrones = StyledComboBox()
            self.combo_patrones.addItems([
                "Seleccione los patrones...",
                "Simples (patrones fáciles de identificar)",
                "Complejos (múltiples patrones entrelazados)",
                "Largos (dependencias de largo plazo)"
            ])
            self.layout_especifico.addWidget(self.combo_patrones)
            
        elif tipo_datos == "tabular":
            self.grupo_especifico.setTitle("5. Relaciones entre Variables")
            
            label = QLabel("¿Espera encontrar relaciones complejas entre las variables?")
            self.layout_especifico.addWidget(label)
            
            self.combo_relaciones = StyledComboBox()
            self.combo_relaciones.addItems([
                "Seleccione una opción...",
                "Sí, hay relaciones complejas y no lineales",
                "No, las relaciones son simples o lineales"
            ])
            self.layout_especifico.addWidget(self.combo_relaciones)
            
        elif tipo_datos == "audio":
            self.grupo_especifico.setTitle("5. Tipo de Audio")
            
            label = QLabel("¿Qué tipo de tarea desea realizar con el audio?")
            self.layout_especifico.addWidget(label)
            
            self.combo_tarea_audio = StyledComboBox()
            self.combo_tarea_audio.addItems([
                "Seleccione la tarea...",
                "Reconocimiento de voz",
                "Clasificación de sonidos",
                "Generación de audio",
                "Separación de fuentes"
            ])
            self.layout_especifico.addWidget(self.combo_tarea_audio)
        
        self.grupo_especifico.setVisible(True)
        
    def setup_resultados_tab(self):
        """Configura la pestaña de resultados"""
        resultados_widget = QWidget()
        layout = QVBoxLayout()
        
        # Título
        titulo = QLabel("Resultados de la Recomendación")
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #212529; margin: 20px 0px;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        
        # Resumen de características
        self.label_resumen = QLabel()
        self.label_resumen.setStyleSheet("font-size: 14px; color: #6c757d; margin-bottom: 20px;")
        self.label_resumen.setWordWrap(True)
        layout.addWidget(self.label_resumen)
        
        # Área de scroll para resultados
        self.scroll_resultados = QScrollArea()
        self.scroll_resultados.setWidgetResizable(True)
        self.widget_resultados = QWidget()
        self.layout_resultados = QVBoxLayout(self.widget_resultados)
        self.scroll_resultados.setWidget(self.widget_resultados)
        
        layout.addWidget(self.scroll_resultados)
        
        resultados_widget.setLayout(layout)
        self.tab_widget.addTab(resultados_widget, "📊 Resultados")
        
    def setup_info_tab(self):
        """Configura la pestaña de información del sistema"""
        info_widget = QWidget()
        layout = QVBoxLayout()
        
        # Título
        titulo = QLabel("Información del Sistema Experto")
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #212529; margin: 20px 0px;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        
        # Estadísticas
        stats_group = QuestionGroup("Estadísticas del Sistema")
        stats_layout = QVBoxLayout()
        
        stats_layout.addWidget(QLabel(f"Base de conocimiento: {self.sistema.archivo_base_conocimiento}"))
        stats_layout.addWidget(QLabel(f"Reglas cargadas: {len(self.sistema.reglas)}"))
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # Lista de reglas
        reglas_group = QuestionGroup("Reglas Disponibles")
        reglas_layout = QVBoxLayout()
        
        self.lista_reglas = QListWidget()
        for regla in self.sistema.reglas:
            item_text = f"Regla #{regla['id']}: {regla['recomendacion']}"
            item = QListWidgetItem(item_text)
            self.lista_reglas.addItem(item)
        
        reglas_layout.addWidget(self.lista_reglas)
        reglas_group.setLayout(reglas_layout)
        layout.addWidget(reglas_group)
        
        info_widget.setLayout(layout)
        self.tab_widget.addTab(info_widget, "ℹ️ Información")
        
    def on_tipo_datos_changed(self, index):
        """Maneja el cambio en el tipo de datos"""
        if index > 0:
            tipo_texto = self.combo_tipo.currentText()
            tipos = {
                "Imágenes (fotos, dibujos, etc.)": "imagenes",
                "Texto (documentos, mensajes, etc.)": "texto",
                "Series Temporales (datos con orden temporal)": "series_temporales",
                "Datos Tabulares (tablas, hojas de cálculo)": "tabular",
                "Audio (sonidos, voz, música)": "audio"
            }
            tipo_datos = tipos[tipo_texto]
            self.setup_preguntas_especificas(tipo_datos)
        else:
            self.grupo_especifico.setVisible(False)
            
    def limpiar_formulario(self):
        """Limpia todo el formulario"""
        self.combo_tipo.setCurrentIndex(0)
        self.combo_tamano.setCurrentIndex(0)
        self.combo_recursos.setCurrentIndex(0)
        self.combo_tarea.setCurrentIndex(0)
        self.check_interpretabilidad.setChecked(False)
        self.grupo_especifico.setVisible(False)
        
        QMessageBox.information(self, "Formulario Limpiado", 
                              "Todos los campos han sido restablecidos.")
        
    def recolectar_hechos(self):
        """Recolecta los hechos del formulario"""
        hechos = {}
        
        # Tipo de datos
        if self.combo_tipo.currentIndex() > 0:
            tipo_texto = self.combo_tipo.currentText()
            tipos = {
                "Imágenes (fotos, dibujos, etc.)": "imagenes",
                "Texto (documentos, mensajes, etc.)": "texto",
                "Series Temporales (datos con orden temporal)": "series_temporales",
                "Datos Tabulares (tablas, hojas de cálculo)": "tabular",
                "Audio (sonidos, voz, música)": "audio"
            }
            hechos["tipo_datos"] = tipos[tipo_texto]
        
        # Tamaño del dataset
        if self.combo_tamano.currentIndex() > 0:
            tamano_texto = self.combo_tamano.currentText()
            tamanos = {
                "Muy pequeño (menos de 1,000 muestras)": "muy_pequeno",
                "Pequeño (1,000 - 10,000 muestras)": "pequeno",
                "Medio (10,000 - 100,000 muestras)": "medio",
                "Grande (100,000 - 1,000,000 muestras)": "grande",
                "Muy grande (más de 1,000,000 muestras)": "muy_grande"
            }
            hechos["tamano_dataset"] = tamanos[tamano_texto]
        
        # Recursos computacionales
        if self.combo_recursos.currentIndex() > 0:
            recursos_texto = self.combo_recursos.currentText()
            recursos = {
                "Muy bajos (solo CPU básico)": "muy_bajo",
                "Bajos (CPU bueno, sin GPU)": "bajo",
                "Medios (GPU básica o limitada)": "medio",
                "Altos (GPU buena, como RTX 3080/4090)": "alto",
                "Muy altos (múltiples GPUs, servidores)": "muy_alto"
            }
            hechos["recursos_computacionales"] = recursos[recursos_texto]
        
        # Tarea principal
        if self.combo_tarea.currentIndex() > 0:
            tarea_texto = self.combo_tarea.currentText()
            tareas = {
                "Clasificación (categorizar en clases)": "clasificacion",
                "Regresión (predecir valores numéricos)": "regresion",
                "Segmentación (dividir en partes)": "segmentacion",
                "Detección (encontrar objetos)": "deteccion",
                "Generación (crear nuevo contenido)": "generacion",
                "Reconocimiento de voz": "reconocimiento_voz"
            }
            hechos["tarea"] = tareas[tarea_texto]
        
        # Preguntas específicas
        if self.grupo_especifico.isVisible():
            tipo_datos = hechos.get("tipo_datos", "")
            
            if tipo_datos == "texto" and hasattr(self, 'combo_longitud'):
                if self.combo_longitud.currentIndex() > 0:
                    longitud_texto = self.combo_longitud.currentText()
                    longitudes = {
                        "Corto (menos de 128 palabras/tokens)": "corto",
                        "Medio (128-512 palabras/tokens)": "medio",
                        "Largo (más de 512 palabras/tokens)": "largo"
                    }
                    hechos["longitud_texto"] = longitudes[longitud_texto]
                    
            elif tipo_datos == "series_temporales" and hasattr(self, 'combo_patrones'):
                if self.combo_patrones.currentIndex() > 0:
                    patrones_texto = self.combo_patrones.currentText()
                    patrones = {
                        "Simples (patrones fáciles de identificar)": "simples",
                        "Complejos (múltiples patrones entrelazados)": "complejos",
                        "Largos (dependencias de largo plazo)": "largos"
                    }
                    hechos["patrones_temporales"] = patrones[patrones_texto]
                    
            elif tipo_datos == "tabular" and hasattr(self, 'combo_relaciones'):
                if self.combo_relaciones.currentIndex() > 0:
                    relaciones_texto = self.combo_relaciones.currentText()
                    hechos["relaciones_no_lineales"] = relaciones_texto.startswith("Sí")
                    
            elif tipo_datos == "audio" and hasattr(self, 'combo_tarea_audio'):
                if self.combo_tarea_audio.currentIndex() > 0:
                    tarea_audio_texto = self.combo_tarea_audio.currentText()
                    if tarea_audio_texto == "Reconocimiento de voz":
                        hechos["tarea"] = "reconocimiento_voz"
        
        # Interpretabilidad
        if self.check_interpretabilidad.isChecked():
            hechos["requiere_interpretabilidad"] = True
        
        return hechos
        
    def realizar_analisis(self):
        """Realiza el análisis y muestra los resultados"""
        # Validar campos obligatorios
        if (self.combo_tipo.currentIndex() == 0 or 
            self.combo_tamano.currentIndex() == 0 or 
            self.combo_recursos.currentIndex() == 0):
            
            QMessageBox.warning(self, "Campos Incompletos", 
                              "Por favor complete los campos obligatorios:\n"
                              "- Tipo de datos\n"
                              "- Tamaño del dataset\n" 
                              "- Recursos computacionales")
            return
        
        # Mostrar progreso
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Progress bar indeterminado
        
        # Recolectar hechos
        self.hechos_actuales = self.recolectar_hechos()
        
        # Simular procesamiento (en una aplicación real, esto sería asíncrono)
        QTimer.singleShot(1000, self.procesar_analisis)
        
    def procesar_analisis(self):
        """Procesa el análisis después del delay simulado"""
        try:
            # Realizar inferencia
            recomendaciones = self.sistema.inferir(self.hechos_actuales)
            
            # Mostrar resultados
            self.mostrar_resultados(recomendaciones)
            
            # Cambiar a pestaña de resultados
            self.tab_widget.setCurrentIndex(1)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error durante el análisis:\n{str(e)}")
        finally:
            self.progress_bar.setVisible(False)
            
    def mostrar_resultados(self, recomendaciones):
        """Muestra los resultados en la pestaña correspondiente"""
        # Limpiar resultados anteriores
        for i in reversed(range(self.layout_resultados.count())):
            widget = self.layout_resultados.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Mostrar resumen de características
        resumen_texto = "Características analizadas:\n"
        for clave, valor in self.hechos_actuales.items():
            nombre_bonito = clave.replace('_', ' ').title()
            if isinstance(valor, bool):
                valor_str = "Sí" if valor else "No"
            else:
                valor_str = valor.replace('_', ' ').title()
            resumen_texto += f"• {nombre_bonito}: {valor_str}\n"
        
        self.label_resumen.setText(resumen_texto)
        
        # Mostrar recomendaciones
        if not recomendaciones:
            no_results_label = QLabel(
                "No se encontraron recomendaciones específicas para las características proporcionadas.\n\n"
                "Sugerencia: Intente ajustar algunos parámetros o consulte con un experto en aprendizaje profundo."
            )
            no_results_label.setStyleSheet("font-size: 16px; color: #6c757d; text-align: center; padding: 40px;")
            no_results_label.setAlignment(Qt.AlignCenter)
            self.layout_resultados.addWidget(no_results_label)
        else:
            # Título de recomendaciones
            titulo_recomendaciones = QLabel("Técnicas Recomendadas:")
            titulo_recomendaciones.setStyleSheet("font-size: 20px; font-weight: bold; color: #212529; margin: 20px 0px 10px 0px;")
            self.layout_resultados.addWidget(titulo_recomendaciones)
            
            # Mostrar cada recomendación
            for i, rec in enumerate(recomendaciones, 1):
                result_card = ResultCard(rec)
                self.layout_resultados.addWidget(result_card)
            
            # Recomendación principal
            recomendacion_principal = QLabel(f"🎯 Recomendación Principal: {recomendaciones[0]['tecnica']}")
            recomendacion_principal.setStyleSheet("font-size: 18px; font-weight: bold; color: #28a745; margin: 20px 0px; padding: 15px; background-color: #d4edda; border-radius: 8px;")
            recomendacion_principal.setAlignment(Qt.AlignCenter)
            self.layout_resultados.addWidget(recomendacion_principal)

def main():
    """Función principal para ejecutar la aplicación"""
    app = QApplication(sys.argv)
    
    # Establecer estilo de la aplicación
    app.setStyle('Fusion')
    
    # Crear y mostrar la ventana principal
    ventana = InterfazSistemaExperto()
    ventana.show()
    
    # Ejecutar la aplicación
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()