from sistema_experto import SistemaExpertoDL

def mostrar_bienvenida():
    """Muestra el mensaje de bienvenida"""
    print("\n" + "="*60)
    print("SISTEMA EXPERTO - RECOMENDACION DE TECNICAS DE APRENDIZAJE PROFUNDO")
    print("="*60)
    print("\nBienvenido! Este sistema le ayudara a elegir la mejor tecnica de")
    print("aprendizaje profundo segun las caracteristicas de su dataset.")
    print("\nSolo responda las preguntas una por una cuando se le solicite.")

def main():
    sistema = SistemaExpertoDL("base_conocimiento.json")
    
    while True:
        mostrar_bienvenida()
        
        print("\nQue desea hacer?")
        print("1. Realizar una nueva consulta")
        print("2. Ver informacion del sistema")
        print("3. Salir del sistema")
        
        opcion = input("\nSeleccione una opcion (1-3): ").strip()
        
        if opcion == "1":
            print("\n" + "="*60)
            print("INICIANDO NUEVA CONSULTA")
            print("="*60)
            
            # Recolectar hechos de forma interactiva
            hechos = sistema.recolectar_hechos_interactivo()
            
            # Realizar inferencia
            recomendaciones = sistema.inferir(hechos)
            
            # Mostrar resultados
            sistema.mostrar_resultados(recomendaciones, hechos)
            
            # Preguntar si quiere otra consulta
            print("\n" + "-"*60)
            continuar = input("Desea realizar otra consulta? (s/n): ").strip().lower()
            if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
                print("\nGracias por usar el sistema experto!")
                break
                
        elif opcion == "2":
            print("\n" + "="*60)
            print("INFORMACION DEL SISTEMA")
            print("="*60)
            print(f"Base de conocimiento: {sistema.archivo_base_conocimiento}")
            print(f"Reglas cargadas: {len(sistema.reglas)}")
            print("\nReglas disponibles:")
            for regla in sistema.reglas:
                print(f"  - Regla #{regla['id']}: {regla['recomendacion']}")
            input("\nPresione Enter para continuar...")
                
        elif opcion == "3":
            print("\nHasta pronto!")
            break
            
        else:
            print("ERROR: Opcion invalida. Por favor, seleccione 1, 2 o 3.")
            input("Presione Enter para continuar...")

if __name__ == "__main__":
    main()