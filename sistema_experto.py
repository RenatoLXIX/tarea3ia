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
                "justificacion": "Las CNN son ideales para procesamiento de imágenes con datasets grandes y recursos computacionales adecuados.",
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
                "recomendacion": "BERT o Transformers para clasificación de texto",
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
                "justificacion": "Para generación de texto se requieren modelos autoregresivos como GPT.",
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
                "justificacion": "Para datasets pequeños sin relaciones complejas, métodos clásicos pueden ser suficientes.",
                "confianza": 0.75
            },
            {
                "id": 9,
                "condiciones": {
                    "tipo_datos": "audio",
                    "tarea": "reconocimiento_voz"
                },
                "recomendacion": "CNN + RNN o Transformers para audio",
                "justificacion": "Combinación de CNN para características espectrales y RNN/Transformers para secuencias temporales.",
                "confianza": 0.88
            },
            {
                "id": 10,
                "condiciones": {
                    "requiere_interpretabilidad": True,
                    "tipo_datos": "cualquiera"
                },
                "recomendacion": "Modelos con atención o SHAP/LIME para interpretabilidad",
                "justificacion": "Se priorizan técnicas que permiten explicar las decisiones del modelo.",
                "confianza": 0.70
            }
        ]
    
    def mostrar_opciones(self):
        """Muestra las opciones disponibles para cada característica"""
        print("\n" + "="*60)
        print("SISTEMA EXPERTO - RECOMENDACIÓN DE TÉCNICAS DL")
        print("="*60)
        
        print("\nOPCIONES DISPONIBLES:")
        print("\n1. TIPO DE DATOS:")
        print("   - imagenes")
        print("   - texto") 
        print("   - series_temporales")
        print("   - tabular")
        print("   - audio")
        
        print("\n2. TAMAÑO DEL DATASET:")
        print("   - muy_pequeno (menos de 1,000 muestras)")
        print("   - pequeno (1,000 - 10,000 muestras)")
        print("   - medio (10,000 - 100,000 muestras)")
        print("   - grande (100,000 - 1,000,000 muestras)")
        print("   - muy_grande (más de 1,000,000 muestras)")
        
        print("\n3. RECURSOS COMPUTACIONALES:")
        print("   - muy_bajo (CPU básico)")
        print("   - bajo (CPU bueno)")
        print("   - medio (GPU básica)")
        print("   - alto (GPU buena)")
        print("   - muy_alto (múltiples GPUs)")
        
        print("\n4. TAREA PRINCIPAL:")
        print("   - clasificacion")
        print("   - regresion")
        print("   - segmentacion")
        print("   - deteccion")
        print("   - generacion")
        print("   - reconocimiento_voz")
        
        print("\n5. LONGITUD DEL TEXTO (solo para datos de texto):")
        print("   - corto (menos de 128 tokens)")
        print("   - medio (128-512 tokens)")
        print("   - largo (más de 512 tokens)")
        
        print("\n6. PATRONES TEMPORALES (solo para series temporales):")
        print("   - simples")
        print("   - complejos")
        print("   - largos")
        
        print("\n7. RELACIONES NO LINEALES (solo para datos tabulares):")
        print("   - true (sí)")
        print("   - false (no)")
        
        print("\n8. ¿REQUIERE INTERPRETABILIDAD?")
        print("   - true (sí)")
        print("   - false (no)")
    
    def recolectar_hechos(self):
        """Recolecta los hechos del usuario mediante la consola"""
        hechos = {}
        
        print("\n" + "-"*60)
        print("INGRESE LAS CARACTERÍSTICAS DE SU DATASET")
        print("-"*60)
        
        # Tipo de datos (obligatorio)
        while True:
            tipo = input("\nTipo de datos: ").strip().lower()
            if tipo in ["imagenes", "texto", "series_temporales", "tabular", "audio"]:
                hechos["tipo_datos"] = tipo
                break
            else:
                print("❌ Opción inválida. Use: imagenes, texto, series_temporales, tabular, audio")
        
        # Tamaño del dataset (obligatorio)
        while True:
            tamano = input("Tamaño del dataset: ").strip().lower()
            if tamano in ["muy_pequeno", "pequeno", "medio", "grande", "muy_grande"]:
                hechos["tamano_dataset"] = tamano
                break
            else:
                print("❌ Opción inválida. Use: muy_pequeno, pequeno, medio, grande, muy_grande")
        
        # Recursos computacionales (obligatorio)
        while True:
            recursos = input("Recursos computacionales: ").strip().lower()
            if recursos in ["muy_bajo", "bajo", "medio", "alto", "muy_alto"]:
                hechos["recursos_computacionales"] = recursos
                break
            else:
                print("❌ Opción inválida. Use: muy_bajo, bajo, medio, alto, muy_alto")
        
        # Tarea principal (opcional)
        tarea = input("Tarea principal (opcional, Enter para omitir): ").strip().lower()
        if tarea and tarea in ["clasificacion", "regresion", "segmentacion", "deteccion", "generacion", "reconocimiento_voz"]:
            hechos["tarea"] = tarea
        
        # Campos específicos según tipo de datos
        if hechos["tipo_datos"] == "texto":
            longitud = input("Longitud del texto (corto/medio/largo, opcional): ").strip().lower()
            if longitud in ["corto", "medio", "largo"]:
                hechos["longitud_texto"] = longitud
        
        elif hechos["tipo_datos"] == "series_temporales":
            patrones = input("Patrones temporales (simples/complejos/largos, opcional): ").strip().lower()
            if patrones in ["simples", "complejos", "largos"]:
                hechos["patrones_temporales"] = patrones
        
        elif hechos["tipo_datos"] == "tabular":
            relaciones = input("¿Relaciones no lineales? (true/false, opcional): ").strip().lower()
            if relaciones in ["true", "false"]:
                hechos["relaciones_no_lineales"] = relaciones == "true"
        
        # Interpretabilidad
        interpretabilidad = input("¿Requiere interpretabilidad? (true/false, opcional): ").strip().lower()
        if interpretabilidad in ["true", "false"]:
            hechos["requiere_interpretabilidad"] = interpretabilidad == "true"
        
        return hechos
    
    def inferir(self, hechos_usuario):
        """Ejecuta el motor de inferencia"""
        self.hechos = hechos_usuario
        recomendaciones = []
        
        print(f"\n🔍 Analizando con hechos: {hechos_usuario}")
        
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
        print("📊 RESULTADOS DE LA RECOMENDACIÓN")
        print("="*60)
        
        print(f"\nCaracterísticas analizadas:")
        for clave, valor in hechos.items():
            print(f"  • {clave.replace('_', ' ').title()}: {valor}")
        
        print(f"\n🔧 TÉCNICAS RECOMENDADAS:")
        
        if not recomendaciones:
            print("\n❌ No se encontraron recomendaciones específicas para las características proporcionadas.")
            print("   Intente ajustar los parámetros o consulte con un experto en aprendizaje profundo.")
            return
        
        for i, rec in enumerate(recomendaciones, 1):
            print(f"\n{i}. {rec['tecnica']}")
            print(f"   📈 Confianza: {rec['confianza']*100:.1f}%")
            print(f"   💡 Justificación: {rec['justificacion']}")
            print(f"   🔗 Regla aplicada: #{rec['regla_id']}")