from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image

def gerar_cartelas(nome_arquivo, total_cartelas=1000, numeros_por_cartela=10):
    # Configurações do documento (paisagem)
    doc = SimpleDocTemplate(nome_arquivo, pagesize=landscape(A4))
    styles = getSampleStyleSheet()
    
    # Estilo personalizado para o cabeçalho
    estilo_header = ParagraphStyle(
        'Header',
        parent=styles['Normal'],
        fontSize=12,  # Fonte maior
        alignment=0,  # Alinhamento à esquerda
        leading=16,  # Espaçamento entre linhas aumentado
        textColor=colors.black,  # Cor do texto
        spaceAfter=6  # Espaço após cada parágrafo
    )
    
    elementos = []
    numeros = list(range(1, total_cartelas * numeros_por_cartela + 1))

    def criar_cartela(id_cartela, nums):
        # Carregar a logo
        logo = Image("logo_creche.png", width=100, height=50)  # Ajuste o tamanho conforme necessário

        # Texto do cabeçalho
        texto_cabecalho = [
            [Paragraph("<b>CRECHE TIA MARIAZINHA - PÁSCOA 2025</b>", estilo_header)],
            [Paragraph("Prêmio: Linda Cesta de Páscoa • Valor: R$2,00", estilo_header)],
            [Paragraph(f"Sorteio: 16/04/2025 • <font color=darkred>Cartela {id_cartela} de {total_cartelas}</font>", estilo_header)]
        ]

        # Tabela do cabeçalho com logo e texto
        tabela_header = Table([
            [logo, Table(texto_cabecalho, colWidths=[350])]  # Logo à esquerda, texto à direita
        ], colWidths=[100, 450])  # Largura da logo e do texto
        
        tabela_header.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),  # Borda preta
            ('BACKGROUND', (0,0), (-1,-1), colors.lightgrey),  # Fundo cinza claro
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),  # Alinhar à esquerda
            ('PADDING', (0,0), (-1,-1), 10),  # Espaçamento interno aumentado
        ]))

        # Tabela de números (10 números por cartela)
        dados = [["Número", "Nome", "Telefone"]] + [[str(n), "", ""] for n in nums]
        tabela_numeros = Table(dados, 
                             colWidths=[80, 150, 170],  # Colunas mais largas
                             rowHeights=[20]*11)  # 10 números + cabeçalho
        
        tabela_numeros.setStyle(TableStyle([
            ('FONTSIZE', (0,0), (-1,-1), 10),  # Fonte ligeiramente maior
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),  # Cabeçalho cinza claro
            ('TEXTCOLOR', (0,0), (-1,0), colors.black),  # Texto preto
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.lightgrey),  # Grid mais suave
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.whitesmoke]),  # Linhas zebradas
        ]))

        return [tabela_header, Spacer(1, 15), tabela_numeros]

    # Layout de 2 cartelas por página (paisagem)
    for i in range(0, total_cartelas, 2):
        cartela_esq = criar_cartela(i+1, numeros[i*10:(i+1)*10])
        cartela_dir = criar_cartela(i+2, numeros[(i+1)*10:(i+2)*10]) if i+1 < total_cartelas else []
        
        # Remover o espaçamento entre as cartelas
        pagina = Table([[cartela_esq, cartela_dir]], 
                     colWidths=[400, 400],  # Largura igual para ambas as cartelas
                     spaceAfter=20)  # Espaço maior entre páginas
        
        elementos.append(pagina)
        if i+2 < total_cartelas:
            elementos.append(PageBreak())

    # Gerar o PDF
    doc.build(elementos)

# Executar
gerar_cartelas("cartelas_rifa.pdf")