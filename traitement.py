from bs4 import BeautifulSoup
import re

def run_traitement(html_file):
    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    result = {"parc": [], "navire": []}
    resume = {}

    # Traitement PARC / CAVALIER uniquement
    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) < 3:
            continue

        folio_text = cells[0].get_text(strip=True)
        if not re.match(r"38\d{4}", folio_text):
            continue

        full_row_html = ''.join(str(td) for td in cells)
        if "PARC / CAVALIER" not in full_row_html:
            continue

        shift_text = cells[1].get_text(strip=True)
        shift = next((code for code in ["S1", "S2", "S3", "JD", "JV"] if code in shift_text), "?")

        numbers = re.findall(r"STR\s*</td>\s*<td[^>]*>\s*(\d+)\s*</td>\s*<td[^>]*>\s*(\d+)", full_row_html)
        if numbers:
            n1, n2 = map(int, numbers[0])
            total = n1
            gemfos = n1 - n2
            resume.setdefault(shift, []).append((gemfos, total))

    for shift, valeurs in resume.items():
        sum_gemfos = sum(v[0] for v in valeurs)
        sum_total = sum(v[1] for v in valeurs)
        result["parc"].append({
            "shift": shift,
            "gemfos": sum_gemfos,
            "total": sum_total
        })

    # Traitement NAVIRE complet
    portiques_recherches = ["P08", "P09", "PS0", "PS1", "PS2", "PS3", "PS4", "PS5"]
    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) < 3:
            continue

        folio_text = cells[0].get_text(strip=True)
        if not re.match(r"38\d{4}", folio_text):
            continue

        shift_text = cells[1].get_text(strip=True)
        shift = next((code for code in ["S1", "S2", "S3", "JD", "JV"] if code in shift_text), "?")
        text_row = ''.join(cell.get_text(" ", strip=True) for cell in cells)

        for portique in portiques_recherches:
            if portique in text_row:
                navire_cell = next(
                    (cell.get_text(strip=True) for cell in cells[2:] if len(cell.get_text(strip=True)) > 3),
                    "?"
                )
                result["navire"].append({
                    "shift": shift,
                    "portique": portique,
                    "navire": navire_cell
                })
                break

    return result
