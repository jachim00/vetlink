"""Generuje 4 PDF dokumenty Vetlink-branded dla karty Burka."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os.path

OUT = os.path.dirname(os.path.abspath(__file__))

TEAL = HexColor('#0d9488')
TEAL_DARK = HexColor('#0e7490')
TEAL_LIGHT = HexColor('#ccfbf1')
SLATE_900 = HexColor('#0f172a')
SLATE_700 = HexColor('#334155')
SLATE_500 = HexColor('#64748b')
SLATE_300 = HexColor('#cbd5e1')
SLATE_100 = HexColor('#f1f5f9')
SLATE_50 = HexColor('#f8fafc')
EMERALD = HexColor('#10b981')
ROSE = HexColor('#f43f5e')

# Try to register a Polish-friendly font; fallback to Helvetica
FONT_REGULAR = 'Helvetica'
FONT_BOLD = 'Helvetica-Bold'
try:
    pdfmetrics.registerFont(TTFont('DejaVu', 'C:/Windows/Fonts/DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVu-Bold', 'C:/Windows/Fonts/DejaVuSans-Bold.ttf'))
    FONT_REGULAR = 'DejaVu'
    FONT_BOLD = 'DejaVu-Bold'
except Exception:
    try:
        pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
        pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:/Windows/Fonts/arialbd.ttf'))
        FONT_REGULAR = 'Arial'
        FONT_BOLD = 'Arial-Bold'
    except Exception:
        pass


def header_footer(canvas_obj, doc):
    """Brand header + footer drawn on every page."""
    c = canvas_obj
    w, h = A4

    # Header band
    c.setFillColor(TEAL)
    c.rect(0, h - 25 * mm, w, 25 * mm, fill=1, stroke=0)

    # Logo box
    c.setFillColor(white)
    c.roundRect(15 * mm, h - 22 * mm, 14 * mm, 14 * mm, 3 * mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    # Paw circles (simplified)
    c.circle(20 * mm, h - 13 * mm, 1.4 * mm, fill=1, stroke=0)
    c.circle(24 * mm, h - 11 * mm, 1.4 * mm, fill=1, stroke=0)
    c.circle(25 * mm, h - 15 * mm, 1.4 * mm, fill=1, stroke=0)
    c.circle(19 * mm, h - 16 * mm, 1.4 * mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.roundRect(20 * mm, h - 19 * mm, 5 * mm, 4 * mm, 1 * mm, fill=1, stroke=0)

    # Brand name
    c.setFont(FONT_BOLD, 18)
    c.setFillColor(white)
    c.drawString(34 * mm, h - 13 * mm, "Vetlink")
    c.setFont(FONT_REGULAR, 8)
    c.drawString(34 * mm, h - 17 * mm, "Karta zdrowia psa w 2 sekundy")

    # Right: doc title + date
    c.setFont(FONT_REGULAR, 9)
    c.setFillColor(white)
    c.drawRightString(w - 15 * mm, h - 12 * mm, doc.title)
    c.setFont(FONT_REGULAR, 7)
    c.drawRightString(w - 15 * mm, h - 17 * mm, "vetlink.eu")

    # Footer
    c.setStrokeColor(SLATE_300)
    c.setLineWidth(0.5)
    c.line(15 * mm, 18 * mm, w - 15 * mm, 18 * mm)

    c.setFont(FONT_REGULAR, 7)
    c.setFillColor(SLATE_500)
    c.drawString(15 * mm, 12 * mm, "Vetlink — system dostępu do danych medycznych zwierząt")
    c.drawCentredString(w / 2, 12 * mm, f"Strona {doc.page}")
    c.drawRightString(w - 15 * mm, 12 * mm, "Copyright © Cognify 2026")
    c.setFont(FONT_REGULAR, 6)
    c.setFillColor(SLATE_300)
    c.drawString(15 * mm, 8 * mm, "Dokument informacyjny — nie zastępuje konsultacji weterynaryjnej.")


def make_styles():
    s = getSampleStyleSheet()
    return {
        'title': ParagraphStyle('title', parent=s['Title'], fontName=FONT_BOLD, fontSize=22, textColor=SLATE_900, spaceAfter=4, alignment=TA_LEFT),
        'subtitle': ParagraphStyle('subtitle', parent=s['Normal'], fontName=FONT_REGULAR, fontSize=10, textColor=SLATE_500, spaceAfter=18, alignment=TA_LEFT),
        'h2': ParagraphStyle('h2', parent=s['Heading2'], fontName=FONT_BOLD, fontSize=12, textColor=TEAL_DARK, spaceBefore=12, spaceAfter=6),
        'body': ParagraphStyle('body', parent=s['Normal'], fontName=FONT_REGULAR, fontSize=10, textColor=SLATE_700, leading=14),
        'small': ParagraphStyle('small', parent=s['Normal'], fontName=FONT_REGULAR, fontSize=8, textColor=SLATE_500, leading=11),
        'note': ParagraphStyle('note', parent=s['Normal'], fontName=FONT_REGULAR, fontSize=9, textColor=SLATE_700, leading=13, leftIndent=8, rightIndent=8, spaceBefore=8, spaceAfter=8, backColor=TEAL_LIGHT, borderPadding=8),
    }


def info_table(rows, col_widths=(50 * mm, 110 * mm)):
    t = Table(rows, colWidths=col_widths, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), FONT_BOLD),
        ('FONTNAME', (1, 0), (1, -1), FONT_REGULAR),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), SLATE_500),
        ('TEXTCOLOR', (1, 0), (1, -1), SLATE_900),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LINEBELOW', (0, 0), (-1, -2), 0.3, SLATE_100),
    ]))
    return t


def build_doc(filename, title, body_fn):
    path = os.path.join(OUT, filename)
    doc = SimpleDocTemplate(path, pagesize=A4,
                            leftMargin=15 * mm, rightMargin=15 * mm,
                            topMargin=32 * mm, bottomMargin=22 * mm,
                            title=title)
    doc.title = title
    story = body_fn()
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"OK: {filename}")


# ============================================================
# DOC 1 — Wyniki morfologii
# ============================================================
def doc_morfologia():
    s = make_styles()
    story = [
        Paragraph("Wyniki morfologii krwi", s['title']),
        Paragraph("Pacjent: Burek (Golden retriever, 7 lat) · Mikroczip: 616 093 900 012 345 · Data badania: 22 kwietnia 2026", s['subtitle']),
        Paragraph("Dane lecznicy", s['h2']),
        info_table([
            ["Lecznica", "Vetlab Warszawa"],
            ["Lekarz prowadzący", "dr Tomasz Nowak"],
            ["Adres", "ul. Wiejska 12, 00-001 Warszawa"],
            ["Telefon", "+48 22 555 11 22"],
            ["Numer próbki", "VL-2026-04-22-1742"],
        ]),
        Paragraph("Profil hematologiczny", s['h2']),
    ]
    rows = [
        ["Parametr", "Wynik", "Norma", "Jednostka"],
        ["Erytrocyty (RBC)", "6,8", "5,5–8,5", "M/μl"],
        ["Hemoglobina (HGB)", "16,2", "12,0–18,0", "g/dl"],
        ["Hematokryt (HCT)", "47,3", "37–55", "%"],
        ["MCV", "69,5", "60–77", "fl"],
        ["MCH", "23,8", "19,5–24,5", "pg"],
        ["MCHC", "34,2", "32,0–36,0", "g/dl"],
        ["Płytki krwi (PLT)", "287", "200–500", "K/μl"],
        ["Leukocyty (WBC)", "9,4", "6,0–17,0", "K/μl"],
        ["Neutrofile", "62", "60–77", "%"],
        ["Limfocyty", "28", "12–30", "%"],
        ["Monocyty", "5", "3–10", "%"],
        ["Eozynofile", "4", "2–10", "%"],
        ["Bazofile", "1", "0–2", "%"],
    ]
    t = Table(rows, colWidths=(60 * mm, 30 * mm, 35 * mm, 35 * mm), hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), FONT_BOLD),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 1), (-1, -1), FONT_REGULAR),
        ('TEXTCOLOR', (0, 1), (-1, -1), SLATE_900),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.3, SLATE_300),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, SLATE_50]),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))
    story.append(Paragraph("Interpretacja", s['h2']),)
    story.append(Paragraph(
        "Wszystkie parametry hematologiczne mieszczą się w przedziale referencyjnym dla psów dorosłych. "
        "Nie obserwujemy cech anemii, infekcji ani zaburzeń krzepnięcia. "
        "Wyniki sugerują dobrą kondycję ogólną pacjenta, zgodną z wiekiem i rasą.",
        s['body']
    ))
    story.append(Paragraph(
        "Zalecenia: kontynuacja Lewotyroksyny 0,4 mg 1× dziennie rano. Kontrola za 6 miesięcy lub w razie pogorszenia stanu klinicznego.",
        s['note']
    ))
    return story


# ============================================================
# DOC 2 — Paszport zwierzęcia
# ============================================================
def doc_paszport():
    s = make_styles()
    story = [
        Paragraph("Paszport dla zwierzęcia towarzyszącego", s['title']),
        Paragraph("Numer paszportu: PL 16093900012345 · Wydany: 15 lipca 2018 · Ważny: bezterminowo", s['subtitle']),
        Paragraph("I. Dane właściciela", s['h2']),
        info_table([
            ["Imię i nazwisko", "Anna Kowalska"],
            ["Adres", "ul. Marszałkowska 15/22, 00-001 Warszawa, Polska"],
            ["Telefon", "+48 987 654 321"],
            ["Email", "anna.kowalska@example.com"],
        ]),
        Paragraph("II. Opis zwierzęcia", s['h2']),
        info_table([
            ["Imię", "Burek"],
            ["Gatunek", "Pies (Canis lupus familiaris)"],
            ["Rasa", "Golden retriever"],
            ["Płeć", "Samiec (kastrowany 12.06.2020)"],
            ["Data urodzenia", "15 maja 2018"],
            ["Maść", "Złota"],
        ]),
        Paragraph("III. Identyfikacja", s['h2']),
        info_table([
            ["Numer mikroczipu", "616 093 900 012 345"],
            ["Lokalizacja", "Lewa strona szyi"],
            ["Data implantacji", "20 lipca 2018"],
            ["Implantujący lekarz", "dr Tomasz Nowak"],
            ["Tag NFC Vetlink", "Aktywny od 15.04.2026"],
        ]),
        Paragraph("IV. Szczepienie przeciwko wściekliźnie", s['h2']),
    ]
    vac = [
        ["Data podania", "Producent / nazwa", "Numer serii", "Ważne do"],
        ["10.04.2026", "MSD / Nobivac Rabies", "A437B2026", "10.04.2027"],
        ["10.04.2025", "MSD / Nobivac Rabies", "A398B2025", "10.04.2026"],
        ["10.04.2024", "MSD / Nobivac Rabies", "A312B2024", "10.04.2025"],
    ]
    t = Table(vac, colWidths=(35 * mm, 60 * mm, 35 * mm, 30 * mm), hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), FONT_BOLD),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 1), (-1, -1), FONT_REGULAR),
        ('TEXTCOLOR', (0, 1), (-1, -1), SLATE_900),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.3, SLATE_300),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, SLATE_50]),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Paszport wystawiony zgodnie z Rozporządzeniem (UE) 2013/576 w sprawie przemieszczania o charakterze niehandlowym zwierząt domowych. "
        "Dokument cyfrowy w systemie Vetlink — zawsze dostępny po zeskanowaniu tagu NFC.",
        s['small']
    ))
    return story


# ============================================================
# DOC 3 — Opis RTG stawów biodrowych
# ============================================================
def doc_rtg():
    s = make_styles()
    story = [
        Paragraph("Opis badania radiologicznego", s['title']),
        Paragraph("Pacjent: Burek · Data badania: 22 stycznia 2026 · Numer skierowania: RTG-2026-01-22-0094", s['subtitle']),
        Paragraph("Dane badania", s['h2']),
        info_table([
            ["Lecznica", "Vetlab Warszawa"],
            ["Lekarz wykonujący", "dr Tomasz Nowak"],
            ["Adres", "ul. Wiejska 12, 00-001 Warszawa"],
            ["Telefon", "+48 22 555 11 22"],
            ["Aparat", "Cyfrowy detektor Carestream DRX-Evolution"],
            ["Projekcje", "VD pelvis (rozluźniona), kości udowe AP"],
        ]),
        Paragraph("Wskazania", s['h2']),
        Paragraph("Kontrola dysplazji stawów biodrowych u pacjenta z rozpoznaniem od 2022 r. "
                  "Pacjent przyjmuje Carprofen 50 mg 1× dziennie. Brak progresji klinicznej w ostatnich 6 miesiącach.", s['body']),
        Paragraph("Opis radiologiczny", s['h2']),
        Paragraph(
            "Staw biodrowy prawy: panewka prawidłowo wykształcona, głowa kości udowej osadzona symetrycznie. "
            "Norberg angle 102° (norma > 105°). Niewielkie spłycenie panewki bez zmian zwyrodnieniowych. "
            "Klasyfikacja FCI: B (na granicy normy). "
            "<br/><br/>"
            "Staw biodrowy lewy: panewka jak po stronie prawej. Norberg angle 100°. "
            "Drobne osteofity na brzegu panewki — bez progresji od poprzedniego badania (2025-07-15). "
            "Klasyfikacja FCI: B/C. "
            "<br/><br/>"
            "Kości miednicy i odcinka lędźwiowego kręgosłupa: bez zmian patologicznych. "
            "Spojenie łonowe symetryczne.",
            s['body']
        ),
        Paragraph("Wnioski", s['h2']),
        Paragraph(
            "Dysplazja stawów biodrowych — kategoria B (po prawej) i B/C (po lewej) wg FCI. "
            "Brak istotnej progresji w stosunku do badania z lipca 2025 r. "
            "Stan stabilny.",
            s['note']
        ),
        Paragraph("Zalecenia", s['h2']),
        Paragraph(
            "1. Kontynuacja Carprofen 50 mg 1× dziennie.<br/>"
            "2. Glukozamina + chondroityna 1× dziennie.<br/>"
            "3. Kontrola wagi (32 kg — w normie dla rasy).<br/>"
            "4. Umiarkowana aktywność fizyczna, unikanie skoków i biegania po śliskich powierzchniach.<br/>"
            "5. Kontrola RTG za 12 miesięcy lub w razie pogorszenia.",
            s['body']
        ),
    ]
    return story


# ============================================================
# DOC 4 — Polisa ubezpieczeniowa
# ============================================================
def doc_polisa():
    s = make_styles()
    story = [
        Paragraph("Polisa ubezpieczenia zdrowia zwierzęcia", s['title']),
        Paragraph("Numer polisy: PZU PET 1234567 · Data zawarcia: 10 stycznia 2026 · Okres ochrony: 10.01.2026 – 09.01.2027", s['subtitle']),
        Paragraph("Strony umowy", s['h2']),
        info_table([
            ["Ubezpieczyciel", "PZU SA · al. Jana Pawła II 24, 00-133 Warszawa"],
            ["Ubezpieczający", "Anna Kowalska · ul. Marszałkowska 15/22, Warszawa"],
            ["Nr klienta", "PZU-K-9847263"],
        ]),
        Paragraph("Zwierzę ubezpieczone", s['h2']),
        info_table([
            ["Imię", "Burek"],
            ["Gatunek/rasa", "Pies / Golden retriever"],
            ["Wiek", "7 lat"],
            ["Mikroczip", "616 093 900 012 345"],
        ]),
        Paragraph("Zakres ochrony", s['h2']),
    ]
    rows = [
        ["Świadczenie", "Suma ubezpieczenia", "Udział własny"],
        ["Wizyty weterynaryjne", "12 000 PLN / rok", "10%"],
        ["Zabiegi i operacje", "20 000 PLN / rok", "10%"],
        ["Hospitalizacja (do 30 dni)", "8 000 PLN / rok", "10%"],
        ["Badania diagnostyczne (RTG, USG, krew)", "4 000 PLN / rok", "0%"],
        ["Leczenie chorób przewlekłych", "10 000 PLN / rok", "20%"],
        ["Eutanazja i kremacja", "1 500 PLN / zdarzenie", "0%"],
    ]
    t = Table(rows, colWidths=(80 * mm, 50 * mm, 30 * mm), hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), FONT_BOLD),
        ('FONTNAME', (0, 1), (-1, -1), FONT_REGULAR),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 1), (-1, -1), SLATE_900),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.3, SLATE_300),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, SLATE_50]),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))
    story.append(Paragraph("Składka i sposób zapłaty", s['h2']))
    story.append(info_table([
        ["Składka roczna", "1 188 PLN"],
        ["Sposób płatności", "Miesięcznie 99 PLN, polecenie zapłaty"],
        ["Następna rata", "10.05.2026"],
    ]))
    story.append(Paragraph("Wyłączenia odpowiedzialności (skrót)", s['h2']))
    story.append(Paragraph(
        "Ochrona nie obejmuje: chorób rozpoznanych przed zawarciem umowy (z wyłączeniem dysplazji wpisanej do polisy), "
        "kastracji niezaleconej medycznie, hodowli i porodów, leczenia behawioralnego, kosmetyki, suplementów. "
        "Pełna lista wyłączeń: OWU PZU PET, §7.",
        s['small']
    ))
    story.append(Paragraph(
        "Dane medyczne pacjenta zsynchronizowane z systemem Vetlink. Likwidacja szkód: szybsza dzięki dostępowi do pełnej historii.",
        s['note']
    ))
    return story


if __name__ == '__main__':
    build_doc('Vetlink_morfologia_Burek.pdf', 'Wyniki morfologii — Burek', doc_morfologia)
    build_doc('Vetlink_paszport_Burek.pdf', 'Paszport zwierzęcia — Burek', doc_paszport)
    build_doc('Vetlink_RTG_Burek.pdf', 'Opis RTG stawów biodrowych — Burek', doc_rtg)
    build_doc('Vetlink_polisa_Burek.pdf', 'Polisa ubezpieczeniowa — Burek', doc_polisa)
    print("Wszystkie 4 dokumenty wygenerowane.")
