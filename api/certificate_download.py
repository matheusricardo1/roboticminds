import os
from django.conf import settings
from django.http import FileResponse
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io


def get_user_data(user_id):
    # Simulação de dados do usuário (substituir com sua lógica real)
    return {
        'full_name': 'John Doe',
        'cpf': '123.456.789-00'
    }



def create_certificate_image():
    # Caminho para a imagem base
    image_path = os.path.join(settings.STATICFILES_DIRS[0], 'certificates', 'base_certificate.jpg')
    image = Image.open(image_path)
    
    try:
        # Salvar a imagem em um buffer
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        buffer.seek(0)
        
        # Criar uma resposta de arquivo para download
        response = FileResponse(buffer, as_attachment=True, filename='certificate.jpg')
        
        return response
        
    except OSError as e:
        print(f"OSError: {e}")
        return None


def create_certificate_pdf(image_buffer):
    # Criar um buffer para o PDF
    pdf_buffer = io.BytesIO()
    
    # Configurar o canvas do PDF
    c = canvas.Canvas(pdf_buffer, pagesize=A4)
    
    # Definir as coordenadas de onde a imagem será desenhada
    c.drawImage(image_buffer, 0, 0, width=A4[0], height=A4[1])
    
    c.showPage()
    c.save()
    
    pdf_buffer.seek(0)
    return pdf_buffer

