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

    p.setFont("Helvetica-Bold", 16)

    # aumenta o limite de caracteres por linha para aproveitar toda a página
    titulo_linhas = wrap(noticia.titulo, 60)  

    for linha in titulo_linhas:
        p.drawString(2*cm, y, linha)
        y -= 0.8*cm  # mais espaçamento no título

    y -= 0.5*cm  # espaço extra após o título

    # ===== CONTEÚDO =====
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
