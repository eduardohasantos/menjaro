from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from textwrap import wrap
from io import BytesIO

def gerar_pdf_noticia(noticia):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    largura, altura = A4

    y = altura - 2*cm

    # TÍTULO
    p.setFont("Helvetica-Bold", 16)
    p.drawString(2*cm, y, noticia.titulo)
    y -= 1*cm

    # CONTEÚDO
    p.setFont("Helvetica", 12)
    linhas = wrap(noticia.conteudo, 90)

    for linha in linhas:
        if y < 2*cm:  # quebra de página
            p.showPage()
            p.setFont("Helvetica", 12)
            y = altura - 2*cm
        p.drawString(2*cm, y, linha)
        y -= 0.5*cm

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer
