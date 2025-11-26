import fitz

def extract_text_from_pdf_path(pdf_path: str):
    doc = fitz.open(pdf_path)
    texto_completo = []

    for pagina in doc:
        blocos = pagina.get_text("blocks")

        # Ordenar blocos pela posição (y, x)
        blocos_ordenados = sorted(blocos, key=lambda b: (b[1], b[0]))

        texto_pagina = "\n".join(
            [bloco[4] for bloco in blocos_ordenados if bloco[6] == 0]
        )

        texto_completo.append(texto_pagina)

    doc.close()

    pdf_content = "".join(texto_completo)
    return pdf_content
