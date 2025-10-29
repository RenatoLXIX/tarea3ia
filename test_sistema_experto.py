import unittest
import json
import os
import tempfile
from sistema_experto import SistemaExpertoDL

class TestSistemaExpertoDL(unittest.TestCase):
    
    def setUp(self):
        """Configuración antes de cada prueba"""
        # Crear un archivo temporal de base de conocimiento para pruebas
        self.archivo_temp = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.datos_prueba = {
            "reglas": [
                {
                    "id": 1,
                    "condiciones": {
                        "tipo_datos": "imagenes",
                        "tamano_dataset": "grande"
                    },
                    "recomendacion": "CNN para prueba",
                    "justificacion": "Justificacion de prueba",
                    "confianza": 0.9
                },
                {
                    "id": 2,
                    "condiciones": {
                        "tipo_datos": "texto",
                        "tarea": "clasificacion"
                    },
                    "recomendacion": "BERT para prueba",
                    "justificacion": "Justificacion de prueba texto",
                    "confianza": 0.85
                },
                {
                    "id": 3,
                    "condiciones": {
                        "requiere_interpretabilidad": True
                    },
                    "recomendacion": "Modelo interpretable para prueba",
                    "justificacion": "Justificacion interpretabilidad",
                    "confianza": 0.7
                }
            ]
        }
        json.dump(self.datos_prueba, self.archivo_temp)
        self.archivo_temp.close()
        
    def tearDown(self):
        """Limpieza después de cada prueba"""
        if os.path.exists(self.archivo_temp.name):
            os.unlink(self.archivo_temp.name)
    
    def test_cargar_reglas_desde_json(self):
        """Prueba que las reglas se carguen correctamente desde JSON"""
        sistema = SistemaExpertoDL(self.archivo_temp.name)
        self.assertEqual(len(sistema.reglas), 3)
        self.assertEqual(sistema.reglas[0]["id"], 1)
        self.assertEqual(sistema.reglas[1]["recomendacion"], "BERT para prueba")
    
    def test_cargar_reglas_archivo_no_existe(self):
        """Prueba el comportamiento cuando el archivo no existe"""
        sistema = SistemaExpertoDL("archivo_que_no_existe.json")
        # Debería cargar reglas por defecto
        self.assertGreater(len(sistema.reglas), 0)
    
    def test_inferir_regla_simple(self):
        """Prueba la inferencia con una regla simple"""
        sistema = SistemaExpertoDL(self.archivo_temp.name)
        hechos = {
            "tipo_datos": "imagenes",
            "tamano_dataset": "grande"
        }
        recomendaciones = sistema.inferir(hechos)
        
        self.assertEqual(len(recomendaciones), 1)
        self.assertEqual(recomendaciones[0]["tecnica"], "CNN para prueba")
        self.assertEqual(recomendaciones[0]["confianza"], 0.9)
    
    def test_inferir_interpretabilidad(self):
        """Prueba la inferencia con requerimiento de interpretabilidad"""
        sistema = SistemaExpertoDL(self.archivo_temp.name)
        hechos = {
            "tipo_datos": "tabular",
            "requiere_interpretabilidad": True
        }
        recomendaciones = sistema.inferir(hechos)
        
        self.assertEqual(len(recomendaciones), 1)
        self.assertEqual(recomendaciones[0]["tecnica"], "Modelo interpretable para prueba")
        self.assertEqual(recomendaciones[0]["confianza"], 0.7)
    
    def test_inferir_varias_reglas(self):
        """Prueba la inferencia cuando múltiples reglas aplican"""
        # Crear base de conocimiento con reglas superpuestas
        datos_multiples = {
            "reglas": [
                {
                    "id": 1,
                    "condiciones": {"tipo_datos": "imagenes"},
                    "recomendacion": "Regla 1",
                    "justificacion": "Test",
                    "confianza": 0.8
                },
                {
                    "id": 2,
                    "condiciones": {"tamano_dataset": "grande"},
                    "recomendacion": "Regla 2",
                    "justificacion": "Test",
                    "confianza": 0.9
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(datos_multiples, f)
            temp_name = f.name
        
        try:
            sistema = SistemaExpertoDL(temp_name)
            hechos = {
                "tipo_datos": "imagenes",
                "tamano_dataset": "grande"
            }
            recomendaciones = sistema.inferir(hechos)
            
            self.assertEqual(len(recomendaciones), 2)
            # Deberían ordenarse por confianza
            self.assertEqual(recomendaciones[0]["confianza"], 0.9)
            self.assertEqual(recomendaciones[1]["confianza"], 0.8)
        finally:
            if os.path.exists(temp_name):
                os.unlink(temp_name)
    
    def test_inferir_sin_coincidencias(self):
        """Prueba la inferencia cuando no hay reglas que apliquen"""
        sistema = SistemaExpertoDL(self.archivo_temp.name)
        hechos = {
            "tipo_datos": "audio",  # No existe en las reglas de prueba
            "tamano_dataset": "pequeno"
        }
        recomendaciones = sistema.inferir(hechos)
        
        self.assertEqual(len(recomendaciones), 0)
    
    def test_evaluar_condiciones(self):
        """Prueba la evaluación de condiciones individuales"""
        sistema = SistemaExpertoDL(self.archivo_temp.name)
        
        # Condición que se cumple
        sistema.hechos = {"tipo_datos": "imagenes", "tamano_dataset": "grande"}
        self.assertTrue(sistema._evaluar_condiciones({"tipo_datos": "imagenes"}))
        
        # Condición que no se cumple
        self.assertFalse(sistema._evaluar_condiciones({"tipo_datos": "texto"}))
        
        # Condición con clave faltante
        self.assertFalse(sistema._evaluar_condiciones({"clave_inexistente": "valor"}))
    
    def test_agregar_regla(self):
        """Prueba agregar una nueva regla a la base de conocimiento"""
        sistema = SistemaExpertoDL(self.archivo_temp.name)
        cantidad_inicial = len(sistema.reglas)
        
        # Obtener el máximo ID actual
        max_id_actual = max([regla["id"] for regla in sistema.reglas])
        
        condiciones = {"tipo_datos": "audio", "tarea": "clasificacion"}
        resultado = sistema.agregar_regla(
            condiciones=condiciones,
            recomendacion="Nueva tecnica de prueba",
            justificacion="Justificacion de prueba",
            confianza=0.75
        )
        
        self.assertTrue(resultado)
        self.assertEqual(len(sistema.reglas), cantidad_inicial + 1)
        self.assertEqual(sistema.reglas[-1]["recomendacion"], "Nueva tecnica de prueba")
        # El siguiente ID debería ser max_id_actual + 1
        self.assertEqual(sistema.reglas[-1]["id"], max_id_actual + 1)
    
    def test_estructura_reglas_valida(self):
        """Prueba que las reglas tengan la estructura correcta"""
        sistema = SistemaExpertoDL(self.archivo_temp.name)
        
        for regla in sistema.reglas:
            self.assertIn("id", regla)
            self.assertIn("condiciones", regla)
            self.assertIn("recomendacion", regla)
            self.assertIn("justificacion", regla)
            self.assertIn("confianza", regla)
            self.assertIsInstance(regla["condiciones"], dict)
            self.assertIsInstance(regla["confianza"], (int, float))


class TestCasosDeUsoEspecificos(unittest.TestCase):
    """Pruebas con casos de uso específicos del dominio"""
    
    def setUp(self):
        # Verificar que el archivo de base de conocimiento existe
        if not os.path.exists("base_conocimiento.json"):
            self.skipTest("Archivo base_conocimiento.json no encontrado")
        self.sistema = SistemaExpertoDL("base_conocimiento.json")
    
    def test_caso_imagenes_grandes(self):
        """Prueba el caso de uso: imágenes grandes con recursos altos"""
        hechos = {
            "tipo_datos": "imagenes",
            "tamano_dataset": "grande",
            "recursos_computacionales": "alto"
        }
        recomendaciones = self.sistema.inferir(hechos)
        
        self.assertGreater(len(recomendaciones), 0)
        # Debería recomendar CNN
        tecnicas = [rec["tecnica"] for rec in recomendaciones]
        self.assertTrue(any("CNN" in tecnica for tecnica in tecnicas))
    
    def test_caso_texto_clasificacion(self):
        """Prueba el caso de uso: texto para clasificación"""
        hechos = {
            "tipo_datos": "texto",
            "tarea": "clasificacion",
            "longitud_texto": "corto"
        }
        recomendaciones = self.sistema.inferir(hechos)
        
        self.assertGreater(len(recomendaciones), 0)
        tecnicas = [rec["tecnica"] for rec in recomendaciones]
        self.assertTrue(any("BERT" in tecnica or "Transformer" in tecnica for tecnica in tecnicas))
    
    def test_caso_interpretabilidad(self):
        """Prueba el caso donde se requiere interpretabilidad"""
        hechos = {
            "tipo_datos": "tabular",
            "requiere_interpretabilidad": True
        }
        recomendaciones = self.sistema.inferir(hechos)
        
        self.assertGreater(len(recomendaciones), 0, 
                          "Debería encontrar al menos una recomendación para interpretabilidad")
        
        tecnicas = [rec["tecnica"] for rec in recomendaciones]
        # Verificar que alguna técnica menciona interpretabilidad, SHAP o LIME
        encontrado = any(
            "interpretabilidad" in tecnica.lower() or 
            "SHAP" in tecnica or 
            "LIME" in tecnica or
            "atencion" in tecnica.lower()
            for tecnica in tecnicas
        )
        self.assertTrue(encontrado, 
                       f"Ninguna técnica menciona interpretabilidad. Técnicas encontradas: {tecnicas}")
    
    def test_caso_series_temporales_complejas(self):
        """Prueba el caso de uso: series temporales con patrones complejos"""
        hechos = {
            "tipo_datos": "series_temporales",
            "patrones_temporales": "complejos"
        }
        recomendaciones = self.sistema.inferir(hechos)
        
        self.assertGreater(len(recomendaciones), 0)
        tecnicas = [rec["tecnica"] for rec in recomendaciones]
        self.assertTrue(any("LSTM" in tecnica or "GRU" in tecnica for tecnica in tecnicas))


class TestRendimientoSistema(unittest.TestCase):
    """Pruebas de rendimiento y casos edge"""
    
    def test_rendimiento_muchas_reglas(self):
        """Prueba el rendimiento con muchas reglas"""
        # Crear un archivo con muchas reglas
        muchas_reglas = {"reglas": []}
        for i in range(100):
            muchas_reglas["reglas"].append({
                "id": i + 1,
                "condiciones": {"tipo_datos": f"tipo_{i % 5}"},
                "recomendacion": f"Tecnica {i}",
                "justificacion": f"Justificacion {i}",
                "confianza": 0.5 + (i * 0.01)
            })
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(muchas_reglas, f)
            temp_name = f.name
        
        try:
            sistema = SistemaExpertoDL(temp_name)
            hechos = {"tipo_datos": "tipo_0"}
            recomendaciones = sistema.inferir(hechos)
            
            # Debería encontrar aproximadamente 20 reglas (100/5)
            self.assertGreater(len(recomendaciones), 10)
        finally:
            if os.path.exists(temp_name):
                os.unlink(temp_name)
    
    def test_hechos_vacios(self):
        """Prueba con hechos vacíos"""
        sistema = SistemaExpertoDL("base_conocimiento.json")
        recomendaciones = sistema.inferir({})
        self.assertEqual(len(recomendaciones), 0)


def ejecutar_pruebas_rapidas():
    """Función para ejecutar pruebas rápidas sin unittest"""
    print("Ejecutando pruebas rápidas...")
    
    # Prueba básica de carga
    sistema = SistemaExpertoDL("base_conocimiento.json")
    print(f"✓ Sistema cargado con {len(sistema.reglas)} reglas")
    
    # Prueba de inferencia básica
    hechos = {"tipo_datos": "imagenes", "tamano_dataset": "grande", "recursos_computacionales": "alto"}
    recomendaciones = sistema.inferir(hechos)
    print(f"✓ Inferencia básica: {len(recomendaciones)} recomendaciones")
    
    # Prueba de interpretabilidad
    hechos = {"tipo_datos": "tabular", "requiere_interpretabilidad": True}
    recomendaciones = sistema.inferir(hechos)
    print(f"✓ Prueba interpretabilidad: {len(recomendaciones)} recomendaciones")
    
    print("Todas las pruebas rápidas pasaron ✓")


if __name__ == '__main__':
    # Ejecutar pruebas rápidas primero
    try:
        ejecutar_pruebas_rapidas()
        print("\n" + "="*60)
    except Exception as e:
        print(f"Error en pruebas rápidas: {e}")
        print("\n" + "="*60)
    
    # Ejecutar todas las pruebas unitarias
    unittest.main(verbosity=2)