import re
import unicodedata


# -------------------------------------------------------------------
# ===================== SEÇÃO II – EXTRAÇÃO ==========================
# -------------------------------------------------------------------

VERBS_LIST = [
    "NOMEAR","EXONERAR A PEDIDO","EXONERAR","DESIGNAR",
    "DISPENSAR","REMOVER","RECONDUZIR","RETIFICAR",
    "TORNAR SEM EFEITO","CONCEDER","PRORROGAR","CEDER"
]
VERBS_REGEX = "|".join(sorted(VERBS_LIST, key=lambda s: -len(s)))

# REGEX
name_re = re.compile(
    r"([A-ZÁÉÍÓÚÂÊÔÃÕÇ][A-ZÁÉÍÓÚÂÊÔÃÕÇ\.\-']+(?:\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ\.\-']+){1,6})"
)

mat_re = re.compile(
    r"matr[ií]cula[:\s]*([\d\.\-Xx]+)", flags=re.IGNORECASE
)

sigrh_re = re.compile(
    r"SIGRH[:\s]*([0-9]{4,12})", flags=re.IGNORECASE
)

sim_re = re.compile(
    r"(?:Símbolo|SIMBOLO|SÍMBOLO)[:\s]*([A-Z]{1,4}[-\s]?\d{1,3})",
    flags=re.IGNORECASE
)

org_keywords = [
    "Secretaria","Subsecretaria","Diretoria","Gerência","Gerencia",
    "Coordenação","Gabinete","Unidade","Conselho",
    "Administração Regional"
]
org_re = re.compile(
    r"(?:(?:da|do|das|dos)\s+)?("
    r"(?:" + r"|".join(org_keywords) + r")[^\.\,]{0,120})",
    flags=re.IGNORECASE
)


# --------------------- NORMALIZAÇÃO DE NOMES ---------------------
def title_case_name(s):
    s = s.strip()
    s = unicodedata.normalize('NFKD', s)
    parts = s.split()
    small = {"da","de","do","das","dos","e"}
    out = []
    for i, p in enumerate(parts):
        if p.lower() in small and i != 0:
            out.append(p.lower())
        else:
            out.append(p.capitalize())
    return " ".join(out).strip()


# ----------------------------- MAIN --------------------------------
def extract_section_II(section_text):
    """
    Recebe a string da seção II e retorna lista de nomeações/exonerações etc.
    """

    # Normalização
    t = re.sub(r"\r\n?", "\n", section_text)
    t = re.sub(r"\s+", " ", t)
    t = re.sub(rf"(?i)\b({VERBS_REGEX})\b", lambda m: "\n\n" + m.group(1).upper(), t)

    # Split por blocos
    blocks = [b.strip() for b in re.split(r"\n\s*\n", t) if b.strip()]

    entries = []

    for blk in blocks:
        m_ato = re.match(rf"^\s*({VERBS_REGEX})\b", blk, flags=re.IGNORECASE)
        if not m_ato:
            continue

        ato = m_ato.group(1).upper()
        content = blk[len(m_ato.group(0)):].strip()

        subblocks = re.split(
            r"(?<=\.)\s+|(?<=;)\s+",
            content
        )
        if not subblocks:
            subblocks = [content]

        for sb in subblocks:
            s = sb.strip()
            if not s:
                continue

            s_clean = re.sub(r"(?i)\bpor\s+estar\s+sendo\b[^\.,]*[\,]?", "", s).strip()

            names = name_re.findall(s_clean)

            if not names:
                continue

            for nm in names:
                pos = s_clean.find(nm)
                remaining = s_clean[pos + len(nm):].strip()

                matricula = None
                sigrh = None
                simbolos = []
                cargo = None
                orgao = None

                mm = mat_re.search(remaining)
                if mm:
                    matricula = mm.group(1).strip()

                ms = sigrh_re.findall(remaining)
                if ms:
                    sigrh = ms[0] if ato.startswith("EXONERAR") else ms[-1]

                sims = sim_re.findall(remaining)
                if sims:
                    simbolos = [re.sub(r"[\s]+","-",x).upper() for x in sims]

                org_matches = org_re.findall(s_clean)
                if org_matches:
                    last_org = org_matches[-1]
                    orgao = re.sub(r"^(da|do|das|dos)\s+", "", last_org.strip(), flags=re.IGNORECASE)

                clean_name = title_case_name(nm)

                simbolo_main = None
                if simbolos:
                    simbolos_norm = [re.sub(r"[^\w\-]","",s).upper() for s in simbolos]
                    simbolo_main = simbolos_norm[-1] if ato.startswith("NOMEAR") else simbolos_norm[0]

                entry = {
                    "uid": None,
                    "secao": "SEÇÃO II",
                    "ato": ato,
                    "nome": clean_name,
                    "matricula": matricula,
                    "sigrh": sigrh,
                    "simbolo": simbolo_main,
                    "cargo": cargo,
                    "orgao": orgao,
                    "raw": s_clean
                }

                uid_base = f"{ato}-{matricula or clean_name.replace(' ','_')}"
                entry["uid"] = re.sub(r"[^\w\-_]","", uid_base)[:80]

                entries.append(entry)

    # Deduplicação
    seen = set()
    final = []
    for e in entries:
        key = (e["ato"], e["nome"], e["matricula"])
        if key not in seen:
            seen.add(key)
            final.append(e)

    return final
