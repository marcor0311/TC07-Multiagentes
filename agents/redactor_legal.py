"""
agents/redactor_legal.py

• Compone un resumen legal final a partir de contratos, jurisprudencia y legislación.
• Genera un PDF de una sola página con ReportLab.
"""

from datetime import datetime


def redactar_respuesta_legal(contexto: dict[str, list[str]], anio_inicio: int, anio_fin: int) -> str:
    if not (isinstance(anio_inicio, int) and isinstance(anio_fin, int) and anio_inicio <= anio_fin):
        return "No se indicaron años válidos."

    def filtrar_por_anio(datos: list[str]) -> list[str]:
        return [d for d in datos if any(str(a) in d for a in range(anio_inicio, anio_fin + 1))]

    def extraer_info_contrato(texto: str) -> str:
        lineas = texto.split('\n')
        anio = next((l.replace('Año: ','') for l in lineas if l.startswith('Año:')), None)
        contraparte = next((l.replace('Empresa Contraparte: ','') for l in lineas if l.startswith('Empresa Contraparte:')), None)
        resumen = next((l.replace('Resumen: ','') for l in lineas if l.startswith('Resumen:')), None)
        monto = next((l.replace('Monto: ','') for l in lineas if l.startswith('Monto:')), None)
        duracion = next((l.replace('Duración: ','') for l in lineas if l.startswith('Duración:')), None)
        alcance = next((l.replace('Alcance: ','') for l in lineas if l.startswith('Alcance:')), None)
        partes = []
        if anio:
            partes.append(f"Año: {anio}")
        if contraparte:
            partes.append(f"Empresa: {contraparte}")
        if resumen:
            partes.append(f"Resumen: {resumen}")
        if monto:
            partes.append(f"Monto: {monto}")
        if duracion:
            partes.append(f"Duración: {duracion}")
        if alcance:
            partes.append(f"Alcance: {alcance}")
        return "<br/>".join(partes) if partes else texto[:120]

    def extraer_info_juris(texto: str) -> str:
        lineas = texto.split('\n')
        tribunal = next((l.replace('Tribunal: ','') for l in lineas if l.startswith('Tribunal:')), None)
        resumen = next((l.replace('Resumen: ','') for l in lineas if l.startswith('Resumen:')), None)
        anio = next((l.replace('Año: ','') for l in lineas if l.startswith('Año:')), None)
        partes = []
        if tribunal:
            partes.append(f"Tribunal: {tribunal}")
        if resumen:
            partes.append(f"Resumen: {resumen}")
        if anio:
            partes.append(f"Año: {anio}")
        return "<br/>".join(partes) if partes else texto[:120]

    contratos = filtrar_por_anio(contexto.get("contrato", []))
    jurisprudencia = filtrar_por_anio(contexto.get("jurisprudencia", []))
    legislacion = filtrar_por_anio(contexto.get("legislacion", []))

    contratos_unicos = list(dict.fromkeys([extraer_info_contrato(c) for c in contratos]))
    jurisprudencia_unicos = list(dict.fromkeys([extraer_info_juris(j) for j in jurisprudencia]))

    def formatear_ley(texto: str) -> str:
        lineas = texto.split('\n')
        datos = {}
        for linea in lineas:
            if ":" in linea:
                clave, valor = linea.split(":", 1)
                datos[clave.strip()] = valor.strip()
        return (
            f"• Ley: {datos.get('Ley', 'Desconocida')}\n"
            f"  Artículo: {datos.get('Artículo', '?')}\n"
            f"  Tema: {datos.get('Tema', 'N/A')}\n"
            f"  Norma Aplicada: {datos.get('Norma_Aplicada', 'N/A')}\n"
            f"  Año: {datos.get('Año', '?')}\n"
            f"  Resumen: {datos.get('Resumen', '')}\n"
            f"  Análisis: Esta disposición legal introduce implicaciones sustantivas para la gestión corporativa, requiriendo atención particular para asegurar el cumplimiento normativo y prevenir riesgos regulatorios."
        )

    legislacion_unicos = list(dict.fromkeys([formatear_ley(l) for l in legislacion]))

    resumen = f"""
INFORME LEGAL AUTOMATIZADO – CACTI S.A.

Generado por: Catalunya Consulting
Bufete de abogados orientado al derecho empresarial

Informe para: Cacti S.A.
Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

Periodo de análisis: {anio_inicio} a {anio_fin}

CONTRATOS ({len(contratos)}):
(Se presenta un análisis extendido y detallado de los contratos relevantes para la empresa en el periodo indicado)
{chr(10).join(f"• {c}" for c in contratos_unicos) or "• No se encontraron contratos relevantes."}

JURISPRUDENCIA RELEVANTE ({len(jurisprudencia)}):
(Se presenta un análisis extendido y detallado de la jurisprudencia relevante para la empresa en el periodo indicado)
{chr(10).join(f"• {j}" for j in jurisprudencia_unicos) or "• No se encontró jurisprudencia relevante."}

Consideraciones legales:
{chr(10).join(legislacion_unicos) or "• No se encontró legislación relevante."}

Este informe ha sido generado automáticamente y resume información legal y financiera para el periodo seleccionado.

Recomendación final:
A partir del análisis detallado de los contratos, la jurisprudencia y la legislación relevante, se recomienda a la dirección de Cacti S.A. considerar cuidadosamente el impacto práctico de cada obligación contractual, precedente judicial y disposición normativa en la toma de decisiones empresariales. Profundizar en la comprensión de los riesgos, oportunidades y tendencias identificadas permitirá anticipar escenarios, fortalecer la gestión legal y optimizar la estrategia corporativa. Ante dudas específicas, se sugiere consultar con el equipo legal para adaptar las acciones a la realidad normativa y jurisprudencial vigente.
"""

    try:
        import os
        from openai import OpenAI

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        respuesta_ia = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres un asesor jurídico especializado en derecho corporativo."},
                {"role": "user", "content": f"""A continuación se te presentan tres bloques de contenido legal extraídos del análisis de una empresa:

CONTRATOS:
{chr(10).join(contratos_unicos)}

JURISPRUDENCIA:
{chr(10).join(jurisprudencia_unicos)}

LEGISLACIÓN:
{chr(10).join(legislacion_unicos)}

Redacta una sección titulada 'Resumen u Observaciones de Catalunya Consulting' que:
- Sintetice los hallazgos clave de los tres bloques.
- Proponga observaciones analíticas y estratégicas.
- Emita recomendaciones adaptadas a la empresa Cacti S.A., desde la perspectiva de un equipo consultor legal.

Usa un estilo claro, profesional y estratégico."""}
            ],
            temperature=0.7
        )
        resumen += "\n\nRESUMEN U OBSERVACIONES DE CATALUNYA CONSULTING:\n"
        resumen += respuesta_ia.choices[0].message.content.strip()
    except Exception as e:
        resumen += f"\n\nRESUMEN U OBSERVACIONES DE CATALUNYA CONSULTING:\n Error: {str(e)}"
        print("Error al generar la sección de observaciones:", e)

    return resumen

def generar_pdf(resumen: str, nombre_archivo: str = "respuesta_legal.pdf") -> None:
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    from reportlab.lib.units import inch
    from reportlab.lib import colors

    doc = SimpleDocTemplate(nombre_archivo, pagesize=LETTER,
                            rightMargin=40, leftMargin=40,
                            topMargin=40, bottomMargin=40)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Justify", alignment=TA_LEFT, fontSize=8, leading=10))
    styles.add(ParagraphStyle(name="SectionTitle", alignment=TA_LEFT, fontSize=10, leading=12, textColor=colors.HexColor('#003366'), spaceAfter=2, spaceBefore=6, fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name="Header", alignment=TA_CENTER, fontSize=13, leading=15, textColor=colors.HexColor('#003366'), fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name="Footer", alignment=TA_CENTER, fontSize=7, leading=9, textColor=colors.grey))

    # Extraer secciones del resumen
    secciones = {}
    actual = None
    for linea in resumen.strip().split('\n'):
        if linea.strip().startswith("INFORME LEGAL"):
            actual = "header"
            secciones[actual] = linea.strip()
        elif linea.strip().startswith("Periodo de análisis"):
            actual = "periodo"
            secciones[actual] = linea.strip()
        elif linea.strip().startswith("CONTRATOS"):
            actual = "contratos"
            secciones[actual] = linea.strip()
        elif linea.strip().startswith("JURISPRUDENCIA"):
            actual = "jurisprudencia"
            secciones[actual] = linea.strip()
        elif linea.strip().startswith("Consideraciones legales"):
            actual = "legislacion"
            secciones[actual] = linea.strip()
        elif linea.strip().startswith("Este informe"):
            actual = "footer"
            secciones[actual] = linea.strip()
        elif linea.strip().startswith("Generado por"):
            actual = "subheader"
            secciones[actual] = linea.strip()
        elif linea.strip().startswith("RESUMEN U OBSERVACIONES DE CATALUNYA CONSULTING"):
            actual = "observaciones"
            secciones[actual] = linea.strip()
        elif actual:
            secciones[actual] += "\n" + linea.strip()

    def truncar_seccion(texto: str, max_items: int = 6) -> str:
        lineas = [l for l in texto.split("\n") if l.strip().startswith("• ")]
        if not lineas:
            return texto
        return "\n".join(lineas[:max_items])

    story = []
    # Header
    story.append(Paragraph("INFORME LEGAL Y FINANCIERO AUTOMATIZADO", styles["Header"]))
    story.append(Spacer(1, 2))
    if "periodo" in secciones:
        story.append(Paragraph(secciones["periodo"], styles["Justify"]))
        story.append(Spacer(1, 2))
    if "subheader" in secciones:
        for line in secciones["subheader"].split("\n"):
            if line.strip():
                story.append(Paragraph(line.strip(), styles["Justify"]))
                story.append(Spacer(1, 2))
    # Línea divisoria (horizontal, fina)
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#003366')))
    story.append(Spacer(1, 4))
    # Contratos
    if "contratos" in secciones:
        story.append(Paragraph("Contratos relevantes", styles["SectionTitle"]))
        for line in truncar_seccion(secciones["contratos"]).split("\n"):
            if line.strip():
                story.append(Paragraph(line, styles["Justify"]))
                story.append(Spacer(1, 2))
    # Jurisprudencia
    if "jurisprudencia" in secciones:
        story.append(Paragraph("Jurisprudencia relevante", styles["SectionTitle"]))
        for line in truncar_seccion(secciones["jurisprudencia"]).split("\n"):
            if line.strip():
                story.append(Paragraph(line, styles["Justify"]))
                story.append(Spacer(1, 2))
    # Legislación
    if "legislacion" in secciones:
        story.append(Paragraph("Legislación relevante", styles["SectionTitle"]))
        leyes = secciones["legislacion"].split("• ")
        for ley in leyes:
            if not ley.strip():
                continue
            for linea in ley.strip().split("<br/>"):
                if linea.strip():
                    story.append(Paragraph(linea.strip(), styles["Justify"]))
            story.append(Spacer(1, 6))
    # Observaciones de Catalunya Consulting
    if "observaciones" in secciones:
        story.append(Paragraph("Análisis estratégico y recomendaciones personalizadas para Cacti S.A.", styles["SectionTitle"]))
        for line in secciones["observaciones"].split("\n")[1:]:
            line = line.strip()
            if not line:
                continue
            if line.startswith("## ") or line.startswith("#### ") or (line.startswith("**") and line.endswith("**")) or (line.endswith(":") and not line.startswith("-")):
                clean_line = line.replace("## ", "").replace("#### ", "").replace("**", "").strip(":").strip()
                story.append(Spacer(1, 2))
                story.append(Paragraph(clean_line, styles["SectionTitle"]))
            else:
                clean_line = line.replace("**", "").replace("--", "").strip()
                story.append(Paragraph(clean_line, styles["Justify"]))
                story.append(Spacer(1, 2))
    # Footer
        story.append(Spacer(1, 3))
        story.append(Paragraph(
            "Este informe ha sido generado con RAGs (Retrieval-Augmented Generation). "
            "Es indispensable que se consulte con Catalunya Consulting para validar la información "
            "y tomar decisiones estratégicas. La Inteligencia Artificial es el futuro del management legal, "
            "pero no sustituye el asesoramiento profesional que Catalunya Consulting ofrece a sus clientes. "
            "Es una herramienta que complementa la experiencia y el conocimiento de los abogados.",
            styles["Footer"]
        ))
    # Línea final (horizontal, fina)
    story.append(Spacer(1, 1))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#003366')))
    doc.build(story)
    print(f"PDF generado correctamente: {nombre_archivo}")
