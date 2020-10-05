from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import (
    AcademySerializer, CertificateSerializer,
    GetCohortSerializer, UserSerializer
)
from .models import Academy, CohortUser, Certificate, Cohort
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status


@api_view(['GET'])
@permission_classes([AllowAny])
def get_cohorts(request):
    items = Cohort.objects.all()

    upcoming = request.GET.get('upcoming', None)
    if upcoming is not None:
        now = timezone.now()
        items = items.filter(kickoff_date__gte=now)

    academy = request.GET.get('academy', None)
    if academy is not None:
        items = items.filter(academy__slug__in=academy.split(","))

    location = request.GET.get('location', None)
    if location is not None:
        items = items.filter(academy__slug__in=academy.split(","))

    items = items.order_by('kickoff_date')
    serializer = GetCohortSerializer(items, many=True)
    return Response(serializer.data)


# Create your views here.
class AcademyView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        items = Academy.objects.all()
        serializer = AcademySerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AcademySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CohortUserView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        items = CohortUser.objects.all()
        serializer = UserSerializer(items, many=True)
        return Response(serializer.data)


class CohortView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        items = Cohort.objects.all()

        upcoming = request.GET.get('upcoming', None)
        if upcoming is not None:
            now = timezone.now()
            items = items.filter(kickoff_date__gte=now)

        academy = request.GET.get('academy', None)
        if academy is not None:
            items = items.filter(academy__slug__in=academy.split(","))

        serializer = GetCohortSerializer(items, many=True)
        return Response(serializer.data)


class CertificateView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        items = Certificate.objects.all()
        serializer = CertificateSerializer(items, many=True)
        return Response(serializer.data)
