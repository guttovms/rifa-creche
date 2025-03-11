from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image

def gerar_cartelas(nome_arquivo, total_cartelas=1, numeros_por_cartela=10):

    doc = SimpleDocTemplate(nome_arquivo, pagesize=A4)
    styles = getSampleStyleSheet()
    
    cor_vermelha = colors.Color(224/255, 82/255, 82/255)

    estilo_header = ParagraphStyle(
        'Header',
        parent=styles['Normal'],
        fontSize=12,
        alignment=0,
        leading=14,
        textColor=colors.black,
        spaceAfter=6
    )

    estilo_destacado = ParagraphStyle(
        'Destacado',
        parent=styles['Normal'],
        fontSize=12,
        alignment=0,
        leading=14,
        textColor=cor_vermelha, 
        spaceAfter=6
    )
    
    elementos = []
    numeros = list(range(1, total_cartelas * numeros_por_cartela + 1))

    for id_cartela in range(1, total_cartelas + 1):
        try:
            logo = Image("logo_creche.png", width=100, height=50)
        except Exception as e:
            print(f"Erro ao carregar a logo: {e}")
            logo = None

        texto_cabecalho = [
            [Paragraph("<b>CRECHE TIA MARIAZINHA - PÁSCOA 2025</b>", estilo_destacado)], 
            [Paragraph("Vamos sortear uma linda cesta. No valor de R$2,00.", estilo_header)],
            [Paragraph(f"O Sorteio acontecerá no dia 16/04/2025. Cartela {id_cartela} de {total_cartelas}.", estilo_header)]  
        ]

        tabela_cabecalho = Table([
            [logo, Table(texto_cabecalho, colWidths=[350])]
        ], colWidths=[100, 350])
        
        tabela_cabecalho.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('PADDING', (0, 0), (-1, -1), 10),
        ]))
        elementos.append(tabela_cabecalho)
        elementos.append(Spacer(1, 12))

        inicio = (id_cartela - 1) * numeros_por_cartela
        fim = inicio + numeros_por_cartela
        numeros_cartela = numeros[inicio:fim]

        dados = [["Número", "Nome Completo", "Telefone de Contato"]]
        for numero in numeros_cartela:
            dados.append([str(numero), "", ""])

        tabela = Table(dados, colWidths=[100, 200, 150], rowHeights=30)
        tabela.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        elementos.append(tabela)

        if id_cartela < total_cartelas:
            elementos.append(PageBreak())

    doc.build(elementos)

gerar_cartelas("cartelas_rifa.pdf")
