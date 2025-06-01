from bs4 import BeautifulSoup
import re

# Charger le HTML
with open("debug.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

with open("traitement_folios.html", "w", encoding="utf-8") as out:
    # Préparer résumé STR par SHIFT
    resume = {}
    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) < 3:
            continue

        folio_text = cells[0].get_text(strip=True)
        if not re.match(r"38\d{4}", folio_text):
            continue

        full_row_html = ''.join(str(td) for td in cells)
        if "PARC / CAVALIER" not in full_row_html or "STR" not in full_row_html:
            continue

        shift_text = cells[1].get_text(strip=True)
        shift = next((code for code in ["S1", "S2", "S3", "JD", "JV"] if code in shift_text), "?")
        numbers = re.findall(r"STR\s*<\/td>\s*<td[^>]*>\s*(\d+)\s*<\/td>\s*<td[^>]*>\s*(\d+)", full_row_html)
        if numbers:
            n1, n2 = map(int, numbers[0])
            total = n1
            gemfos = n1 - n2
            if shift not in resume:
                resume[shift] = []
            resume[shift].append((gemfos, total))

    # Écrire le résumé
    out.write("<html><body><h2>Résumé PARC / CAVALIER STR</h2>")
    out.write("<table border='1' style='border-collapse: collapse;'>")
    out.write("<tr><th>SHIFT</th><th>STR GEMFOS</th><th>STR TOTAL</th></tr>")
    for shift, valeurs in resume.items():
        sum_gemfos = sum(v[0] for v in valeurs)
        sum_total = sum(v[1] for v in valeurs)
        out.write(f"<tr><td>{shift}</td><td>{sum_gemfos}</td><td>{sum_total}</td></tr>")
    out.write("</table>")

    # Deuxième partie : NAVIRE
    out.write("<h2>Résumé NAVIRE</h2>")
    out.write("<table border='1' style='border-collapse: collapse;'>")
    out.write("<tr><th>SHIFT</th><th>Portique</th><th>Navire</th></tr>")

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
                    (cell.get_text(strip=True) for cell in cells[2:] if re.match(r"^[A-Z ]{4,}$", cell.get_text(strip=True))),
                    "?"
                )
                out.write(f"<tr><td>{shift}</td><td>{portique}</td><td>{navire_cell}</td></tr>")
                break  # Une seule ligne par portique
    out.write("</table></body></html>")