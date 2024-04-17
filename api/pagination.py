from rest_framework.pagination import PageNumberPagination

class UserAPIPagination(PageNumberPagination):
    
    def __init__(self, page_size=2):
        page_size = page_size # Itens por página 

    page_size_query_param = 'page_size'  # Parâmetro opcional na solicitação para alterar o tamanho da página
    max_page_size = 50  # Tamanho máximo da página para evitar abusos

