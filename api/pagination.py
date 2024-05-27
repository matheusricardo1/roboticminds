from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class UserAPIPagination(PageNumberPagination):
    
    def __init__(self, page_size=15):
        self.page_size = page_size # Itens por página 
  
    page_size_query_param = 'page_size'  # Parâmetro opcional na solicitação para alterar o tamanho da página
    max_page_size = 50  # Tamanho máximo da página para evitar abusos

    def get_paginated_response(self, data):
            return Response({
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'total_pages': self.page.paginator.num_pages,
                'results': data
            })

class CertificateAPIPagination(PageNumberPagination):
    
    def __init__(self, page_size=20):
        self.page_size = page_size 
  
    page_size_query_param = 'page_size'  
    max_page_size = 50 

    def get_paginated_response(self, data):
            return Response({
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'total_pages': self.page.paginator.num_pages,
                'results': data
            })