# from rest_framework import generics
# from .models import FAQ
# from .serializers import FAQSerializer
#
# class FAQListCreateAPIView(generics.ListCreateAPIView):
#     queryset = FAQ.objects.all()
#     serializer_class = FAQSerializer
#
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         # Pass the language parameter to the serializer context
#         context['lang'] = self.request.query_params.get('lang', 'en')
#         return context
#


from rest_framework import generics, status
from rest_framework.response import Response
from .models import FAQ
from .serializers import FAQSerializer, FAQCreateUpdateSerializer
from django.views.decorators.csrf import csrf_exempt





class FAQListCreateAPIView(generics.ListCreateAPIView):
    queryset = FAQ.objects.all()
    permission_classes = ()
    authentication_classes = ()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return FAQCreateUpdateSerializer
        return FAQSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lang'] = self.request.query_params.get('lang', 'en')
        return context


class FAQRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.all()
    permission_classes = ()
    authentication_classes = ()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return FAQCreateUpdateSerializer
        return FAQSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lang'] = self.request.query_params.get('lang', 'en')
        return context