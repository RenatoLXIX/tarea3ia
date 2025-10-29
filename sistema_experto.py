class SistemaExpertoDL:
    def __init__(self):
        self.reglas = self._cargar_reglas()
        self.hechos = {}
    
    def _cargar_reglas(self):
        """Define las reglas del sistema experto"""
        return [
            {
                "id": 1,
                "condiciones": {
                    "tipo_datos": "imagenes",
                    "tamano_dataset": "grande",
                    "recursos_computacionales": "alto"
                },
                "recomendacion": "CNN (Redes Neuronales Convolucionales)",
                "justificacion": "Las CNN son ideales para procesamiento de imagenes con datasets grandes y recursos computacionales adecuados.",
                "confianza": 0.95
            },
            {
                "id": 2,
                "condiciones": {
                    "tipo_datos": "imagenes",
                    "tamano_dataset": "pequeno",
                    "recursos_computacionales": "bajo"
                },
                "recomendacion": "Transfer Learning con modelos pre-entrenados (ResNet, VGG)",
                "justificacion": "Para datasets pequeños, el transfer learning permite aprovechar modelos pre-entrenados con menos recursos.",
                "confianza": 0.90
            },
            {
                "id": 3,
                "condiciones": {
                    "tipo_datos": "texto",
                    "tarea": "clasificacion",
                    "longitud_texto": "corto"
                },
                "recomendacion": "BERT o Transformers para clasificacion de texto",
                "justificacion": "Los transformers son state-of-the-art para procesamiento de lenguaje natural.",
                "confianza": 0.92
            },
            {
                "id": 4,
                "condiciones": {
                    "tipo_datos": "texto",
                    "tarea": "generacion",
                    "recursos_computacionales": "alto"
                },
                "recomendacion": "GPT o modelos de lenguaje grandes",
                "justificacion": "Para generacion de texto se requieren modelos autoregresivos como GPT.",
                "confianza": 0.88
            },
            {
                "id": 5,
                "condiciones": {
                    "tipo_datos": "series_temporales",
                    "patrones_temporales": "complejos"
                },
                "recomendacion": "LSTM o GRU",
                "justificacion": "Las redes recurrentes son efectivas para capturar dependencias temporales.",
                "confianza": 0.85
            },
            {
                "id": 6,
                "condiciones": {
                    "tipo_datos": "series_temporales",
                    "patrones_temporales": "largos"
                },
                "recomendacion": "Transformers para series temporales",
                "justificacion": "Los transformers pueden capturar dependencias de largo plazo mejor que LSTM.",
                "confianza": 0.82
            },
            {
                "id": 7,
                "condiciones": {
                    "tipo_datos": "tabular",
                    "relaciones_no_lineales": True,
                    "tamano_dataset": "grande"
                },
                "recomendacion": "Redes Neuronales Fully Connected",
                "justificacion": "Para datos tabulares con relaciones complejas y datasets grandes.",
                "confianza": 0.80
            },
            {
                "id": 8,
                "condiciones": {
                    "tipo_datos": "tabular",
                    "relaciones_no_lineales": False,
                    "tamano_dataset": "pequeno"
                },
                "recomendacion": "Gradient Boosting (XGBoost, LightGBM) o MLP simple",
                "justificacion": "Para datasets pequeños sin relaciones complejas, metodos clasicos pueden ser suficientes.",
                "confianza": 0.75
            },
            {
                "id": 9,
                "condiciones": {
                    "tipo_datos": "audio",
                    "tarea": "reconocimiento_voz"
                },
                "recomendacion": "CNN + RNN o Transformers para audio",
                "justificacion": "Combinacion de CNN para caracteristicas espectrales y RNN/Transformers para secuencias temporales.",
                "confianza": 0.88
            },
            {
                "id": 10,
                "condiciones": {
                    "requiere_interpretabilidad": True,
                    "tipo_datos": "cualquiera"
                },
                "recomendacion": "Modelos con atencion o SHAP/LIME para interpretabilidad",
                "justificacion": "Se priorizan tecnicas que permiten explicar las decisiones del modelo.",
                "confianza": 0.70
            }
        ]
    
    def _preguntar_opciones(self, pregunta, opciones, obligatorio=True):
        """Hace una pregunta con opciones especificas"""
        print(f"\n{pregunta}")
        for i, opcion in enumerate(opciones, 1):
            print(f"  {i}. {opcion}")
        
        while True:
            try:
                respuesta = input(f"\nSeleccione una opcion (1-{len(opciones)}): ").strip()
                if not respuesta and not obligatorio:
                    return None
                
                indice = int(respuesta) - 1
                if 0 <= indice < len(opciones):
                    return opciones[indice]
                else:
                    print(f"ERROR: Por favor, seleccione un numero entre 1 y {len(opciones)}")
            except ValueError:
                print("ERROR: Por favor, ingrese un numero valido")
    
    def _preguntar_si_no(self, pregunta):
        """Hace una pregunta de si/no"""
        while True:
            respuesta = input(f"\n{pregunta} (s/n): ").strip().lower()
            if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
                return True
            elif respuesta in ['n', 'no']:
                return False
            else:
                print("ERROR: Por favor, responda 's' para si o 'n' para no")
    
    def recolectar_hechos_interactivo(self):
        """Recolecta los hechos preguntando uno por uno"""
        hechos = {}
        
        print("\n" + "="*60)
        print("ANALISIS DE SU DATASET - PREGUNTAS INTERACTIVAS")
        print("="*60)
        
        # 1. Tipo de datos
        print("\nPREGUNTA 1: TIPO DE DATOS")
        tipo_opciones = [
            "Imagenes (fotos, dibujos, etc.)",
            "Texto (documentos, mensajes, etc.)", 
            "Series Temporales (datos con orden temporal)",
            "Datos Tabulares (tablas, hojas de calculo)",
            "Audio (sonidos, voz, musica)"
        ]
        tipo_valores = ["imagenes", "texto", "series_temporales", "tabular", "audio"]
        
        respuesta = self._preguntar_opciones("Que tipo de datos tiene?", tipo_opciones)
        hechos["tipo_datos"] = tipo_valores[tipo_opciones.index(respuesta)]
        
        # 2. Tamaño del dataset
        print("\nPREGUNTA 2: TAMAÑO DEL DATASET")
        tamano_opciones = [
            "Muy pequeño (menos de 1,000 muestras)",
            "Pequeño (1,000 - 10,000 muestras)",
            "Medio (10,000 - 100,000 muestras)", 
            "Grande (100,000 - 1,000,000 muestras)",
            "Muy grande (mas de 1,000,000 muestras)"
        ]
        tamano_valores = ["muy_pequeno", "pequeno", "medio", "grande", "muy_grande"]
        
        respuesta = self._preguntar_opciones("Que tamaño tiene su dataset?", tamano_opciones)
        hechos["tamano_dataset"] = tamano_valores[tamano_opciones.index(respuesta)]
        
        # 3. Recursos computacionales
        print("\nPREGUNTA 3: RECURSOS COMPUTACIONALES")
        recursos_opciones = [
            "Muy bajos (solo CPU basico)",
            "Bajos (CPU bueno, sin GPU)",
            "Medios (GPU basica o limitada)",
            "Altos (GPU buena, como RTX 3080/4090)",
            "Muy altos (multiples GPUs, servidores)"
        ]
        recursos_valores = ["muy_bajo", "bajo", "medio", "alto", "muy_alto"]
        
        respuesta = self._preguntar_opciones("Que recursos computacionales tiene disponibles?", recursos_opciones)
        hechos["recursos_computacionales"] = recursos_valores[recursos_opciones.index(respuesta)]
        
        # 4. Tarea principal
        print("\nPREGUNTA 4: TAREA PRINCIPAL")
        tarea_opciones = [
            "Clasificacion (categorizar en clases)",
            "Regresion (predecir valores numericos)",
            "Segmentacion (dividir en partes)",
            "Deteccion (encontrar objetos)",
            "Generacion (crear nuevo contenido)",
            "Reconocimiento de voz"
        ]
        tarea_valores = ["clasificacion", "regresion", "segmentacion", "deteccion", "generacion", "reconocimiento_voz"]
        
        respuesta = self._preguntar_opciones("Cual es la tarea principal que quiere realizar?", tarea_opciones, obligatorio=False)
        if respuesta:
            hechos["tarea"] = tarea_valores[tarea_opciones.index(respuesta)]
        
        # 5. Preguntas especificas segun tipo de datos
        if hechos["tipo_datos"] == "texto":
            print("\nPREGUNTA ESPECIFICA: LONGITUD DEL TEXTO")
            longitud_opciones = [
                "Corto (menos de 128 palabras/tokens)",
                "Medio (128-512 palabras/tokens)", 
                "Largo (mas de 512 palabras/tokens)"
            ]
            longitud_valores = ["corto", "medio", "largo"]
            
            respuesta = self._preguntar_opciones("Que longitud tienen sus textos?", longitud_opciones, obligatorio=False)
            if respuesta:
                hechos["longitud_texto"] = longitud_valores[longitud_opciones.index(respuesta)]
        
        elif hechos["tipo_datos"] == "series_temporales":
            print("\nPREGUNTA ESPECIFICA: PATRONES TEMPORALES")
            patrones_opciones = [
                "Simples (patrones faciles de identificar)",
                "Complejos (multiples patrones entrelazados)",
                "Largos (dependencias de largo plazo)"
            ]
            patrones_valores = ["simples", "complejos", "largos"]
            
            respuesta = self._preguntar_opciones("Que tipo de patrones temporales espera encontrar?", patrones_opciones, obligatorio=False)
            if respuesta:
                hechos["patrones_temporales"] = patrones_valores[patrones_opciones.index(respuesta)]
        
        elif hechos["tipo_datos"] == "tabular":
            print("\nPREGUNTA ESPECIFICA: RELACIONES ENTRE VARIABLES")
            relaciones_opciones = [
                "Si, hay relaciones complejas y no lineales",
                "No, las relaciones son simples o lineales"
            ]
            
            respuesta = self._preguntar_opciones("Espera encontrar relaciones complejas entre las variables?", relaciones_opciones, obligatorio=False)
            if respuesta:
                hechos["relaciones_no_lineales"] = respuesta.startswith("Si")
        
        # 6. Interpretabilidad
        print("\nPREGUNTA FINAL: INTERPRETABILIDAD")
        interpretabilidad_opciones = [
            "Si, es importante entender como el modelo toma decisiones",
            "No, el rendimiento es mas importante que la explicabilidad"
        ]
        
        respuesta = self._preguntar_opciones("Requiere que el modelo sea interpretable?", interpretabilidad_opciones, obligatorio=False)
        if respuesta:
            hechos["requiere_interpretabilidad"] = respuesta.startswith("Si")
        
        return hechos
    
    def inferir(self, hechos_usuario):
        """Ejecuta el motor de inferencia"""
        self.hechos = hechos_usuario
        recomendaciones = []
        
        print(f"\nAnalizando caracteristicas del dataset...")
        
        for regla in self.reglas:
            if self._evaluar_condiciones(regla["condiciones"]):
                recomendaciones.append({
                    "tecnica": regla["recomendacion"],
                    "justificacion": regla["justificacion"],
                    "confianza": regla["confianza"],
                    "regla_id": regla["id"]
                })
        
        # Ordenar por confianza
        recomendaciones.sort(key=lambda x: x["confianza"], reverse=True)
        return recomendaciones
    
    def _evaluar_condiciones(self, condiciones):
        """Evalúa si se cumplen todas las condiciones de una regla"""
        for clave, valor in condiciones.items():
            if clave not in self.hechos:
                return False
            if self.hechos[clave] != valor:
                return False
        return True
    
    def mostrar_resultados(self, recomendaciones, hechos):
        """Muestra los resultados de forma clara"""
        print("\n" + "="*60)
        print("RESULTADOS DE LA RECOMENDACION")
        print("="*60)
        
        print(f"\nCARACTERISTICAS ANALIZADAS:")
        for clave, valor in hechos.items():
            nombre_bonito = clave.replace('_', ' ').title()
            if isinstance(valor, bool):
                valor_str = "Si" if valor else "No"
            else:
                valor_str = valor.replace('_', ' ').title()
            print(f"   - {nombre_bonito}: {valor_str}")
        
        print(f"\nTECNICAS RECOMENDADAS:")
        
        if not recomendaciones:
            print("\nNo se encontraron recomendaciones especificas para las caracteristicas proporcionadas.")
            print("Sugerencia: Intente ajustar algunos parametros o consulte con un experto en aprendizaje profundo.")
            return
        
        for i, rec in enumerate(recomendaciones, 1):
            print(f"\n{i}. {rec['tecnica']}")
            print(f"   Confianza: {rec['confianza']*100:.1f}%")
            print(f"   Justificacion: {rec['justificacion']}")
            print(f"   Regla aplicada: #{rec['regla_id']}")
        
        print(f"\nRECOMENDACION PRINCIPAL: {recomendaciones[0]['tecnica']}")