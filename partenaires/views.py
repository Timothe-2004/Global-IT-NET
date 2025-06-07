from rest_framework import generics
from .models import Partenaire
from .serializers import PartenaireSerializer

class PartenaireListCreateView(generics.ListCreateAPIView):
    queryset = Partenaire.objects.all()
    serializer_class = PartenaireSerializer

class PartenaireRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Partenaire.objects.all()
    serializer_class = PartenaireSerializer
