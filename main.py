from datetime import datetime
from graph.flujo import ejecutar_flujo_legal

def main() -> None:
    print("\nGenerador de resumen legal automatizado para Cacti S.A.")
    periodo = input("\nIndique el periodo de análisis.\nPuede ingresar un rango en formato '2020-2022' o un año específico como '2021'.\nLos años disponibles para análisis son: 2020, 2021, 2022, 2023, 2024, 2025.\n\nPeriodo: ").strip()
    if not periodo:
        print("\n Debe indicar un periodo válido.")
        return
    try:
        pregunta = "¿Cuál es el resumen legal del periodo indicado?"
        respuesta = ejecutar_flujo_legal(pregunta=pregunta, empresa="Cacti S.A.", periodo=periodo)
        if not respuesta or "No se encontró información" in respuesta:
            print("\n No se generó contenido relevante para el periodo indicado.")
        else:
            print("\n Respuesta del asistente:\n")
            print(respuesta)  # Mostrar todo el contenido sin truncarlo
    except Exception as e:
        print(f"\n Error en la ejecución: {e}")

if __name__ == "__main__":
    main()      