import re

def extract_sections(text: str):
    pattern = r"(SEÇÃO\s+[IVX]+)"
    partes = re.split(pattern, text)
    extract_sections = []
    for i in range(1, len(partes), 2):
        titulo = partes[i].strip()
        conteudo = partes[i+1].strip() if i+1 < len(partes) else ""
        # --- FILTROS IMPORTANTES ---
        
        # remover seções muito pequenas (sumário/capa)
        if len(conteudo) < 500:
            continue
        # ignorar sumário
        if conteudo[:50].upper().startswith("SUMÁRIO"):
            continue
        
        # evitar duplicações vazias ou irrelevantes
        if "PAG." in conteudo[:80]:
            continue
        # manter apenas SEÇÃO I, II e III
        if titulo not in ["SEÇÃO I", "SEÇÃO II", "SEÇÃO III"]:
            continue
        extract_sections.append({
            "secao": titulo,
            "conteudo": conteudo
        })

    return extract_sections