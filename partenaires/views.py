from rest_framework import generics
from backend.permissions import IsAdminOrReadOnly
from .models import Partenaire
from .serializers import PartenaireSerializer

class PartenaireListCreateView(generics.ListCreateAPIView):
    """
    Vue pour lister et créer des partenaires.
    - READ (list): Public (AllowAny)
    - CREATE: Admin uniquement
    """
    queryset = Partenaire.objects.all()
    serializer_class = PartenaireSerializer
    permission_classes = [IsAdminOrReadOnly]

class PartenaireRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vue pour récupérer, modifier et supprimer un partenaire.
    - READ (retrieve): Public (AllowAny)
    - UPDATE/DELETE: Admin uniquement
    """
    queryset = Partenaire.objects.all()
    serializer_class = PartenaireSerializer
    permission_classes = [IsAdminOrReadOnly]
