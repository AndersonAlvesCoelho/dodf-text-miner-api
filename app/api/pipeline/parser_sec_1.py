import re
import unicodedata


TITLE_REGEX = r'^[A-ZÁÉÍÓÚÃÕÂÊÔÇ ]{2,}\s+N[º°oO\.]?\s*[\d\.\/-]+(?:,\s*DE\s+[^\n]+)?'
TITLE_PATTERN = re.compile(TITLE_REGEX)

META_REGEX = re.compile(
    r'^(?P<tipo>[A-ZÁÉÍÓÚÃÕÂÊÔÇ ]+)\s+N[º°oO\.]?\s*(?P<numero>[\d\.\/-]+)'
    r'(?:,\s*DE\s*(?P<data>[^\n]+))?',
    re.UNICODE
)

ORG_REGEX = re.compile(
    r'\b(GABINETE|SECRETARIA|MINISTÉRIO|SUPERINTENDÊNCIA|PREFEITURA|GOVERNO|CÂMARA|ASSEMBLEIA|TRIBUNAL|PROCURADORIA)[^\n]{0,80}',
    re.IGNORECASE
)


# PROCESSAR ATO
def process_act(title, content_lines):
    meta = META_REGEX.match(title)

    tipo = meta.group("tipo").strip() if meta else None
    numero = meta.group("numero").strip() if meta else None
    data_raw = meta.group("data").strip() if meta and meta.group("data") else None

    ano = None
    if data_raw:
        ano_match = re.search(r'\b(19|20)\d{2}\b', data_raw)
        if ano_match:
            ano = int(ano_match.group(0))

    content_text = "\n".join(content_lines).strip()
    org_match = ORG_REGEX.search(content_text)
    orgao = org_match.group(0).strip() if org_match else None

    return {
        "tipo": tipo,
        "numero": numero,
        "data": data_raw,
        "ano": ano,
        "orgao": orgao,
        "titulo": title,
        "conteudo": content_text
    }


# EXTRAÇÃO COMPLETA 
def extract_section_I(section_text):
    """
    Recebe a string da seção I e retorna uma lista de dicts com metadados.
    """
    lines = section_text.split("\n")
    acts = []
    current_title = None
    current_content = []

    for line in lines:
        stripped = line.strip()

        if TITLE_PATTERN.match(stripped):
            # salva anterior
            if current_title:
                acts.append(process_act(current_title, current_content))

            current_title = stripped
            current_content = []
            continue

        if current_title:
            current_content.append(line)

    if current_title:
        acts.append(process_act(current_title, current_content))

    return acts
