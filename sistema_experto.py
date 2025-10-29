import json
import os

class SistemaExpertoDL:
    def __init__(self, archivo_base_conocimiento="base_conocimiento.json"):
        self.archivo_base_conocimiento = archivo_base_conocimiento
        self.reglas = self._cargar_reglas_desde_json()
        self.hechos = {}
    
    def _cargar_reglas_desde_json(self):
        """Carga las reglas desde un archivo JSON externo"""
        try:
            if not os.path.exists(self.archivo_base_conocimiento):
                raise FileNotFoundError(f"No se encontro el archivo: {self.archivo_base_conocimiento}")
            
            with open(self.archivo_base_conocimiento, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
            
            if "reglas" not in datos:
                raise ValueError("El archivo JSON no contiene la clave 'reglas'")
            
            print(f"Base de conocimiento cargada: {len(datos['reglas'])} reglas")
            return datos["reglas"]
            
        except Exception as e:
            print(f"Error cargando la base de conocimiento: {e}")
            print("Usando reglas por defecto...")
            return self._cargar_reglas_por_defecto()
    
    def _cargar_reglas_por_defecto(self):
        """Reglas por defecto en caso de error"""
        return [
            {
                "id": 0,
                "condiciones": {"tipo_datos": "imagenes"},
                "recomendacion": "CNN (Redes Neuronales Convolucionales)",
                "justificacion": "Recomendacion por defecto para imagenes.",
                "confianza": 0.5
            }
        ]
    
    def guardar_reglas_en_json(self):
        """Guarda las reglas actuales en el archivo JSON"""
        try:
            datos = {"reglas": self.reglas}
            with open(self.archivo_base_conocimiento, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=2, ensure_ascii=False)
            print(f"Base de conocimiento guardada en: {self.archivo_base_conocimiento}")
            return True
        except Exception as e:
            print(f"Error guardando la base de conocimiento: {e}")
            return False
    
    def agregar_regla(self, condiciones, recomendacion, justificacion, confianza):
        """Agrega una nueva regla a la base de conocimiento"""
        nuevo_id = max([regla["id"] for regla in self.reglas]) + 1 if self.reglas else 1
        
        nueva_regla = {
            "id": nuevo_id,
            "condiciones": condiciones,
            "recomendacion": recomendacion,
            "justificacion": justificacion,
            "confianza": confianza
        }
        
        self.reglas.append(nueva_regla)
        return self.guardar_reglas_en_json()
    
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
        print(f"Hechos proporcionados: {hechos_usuario}")
        
        for regla in self.reglas:
            if self._evaluar_condiciones(regla["condiciones"]):
                recomendaciones.append({
                    "tecnica": regla["recomendacion"],
                    "justificacion": regla["justificacion"],
                    "confianza": regla["confianza"],
                    "regla_id": regla["id"]
                })
                print(f"Regla #{regla['id']} aplicada: {regla['recomendacion']}")
        
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