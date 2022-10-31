from functools import partial
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics, viewsets
from rest_framework.response import Response

from quizes.models import (
    Variant,
    Question,
    Quiz,
    Result
)
from .serializers import (
    VariantSerializer,
    QuestionSerializer,
    QuizSerializer,
    ResultSerializer
)


class VariantsViewSet(viewsets.ViewSet):
    def create(self, request):
        serial = VariantSerializer(data=request.data, many=True)
        serial.is_valid(raise_exception=True)
        serial.save()
        return Response({'status': serial.data})

    def update(self, request, pk=None):
        serializer = VariantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': True})
        return Response({'status': False})

    def destroy(self, request, pk=None):
        question = get_object_or_404(Variant, pk=pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionsViewSet(viewsets.ViewSet):
    def list(self, request, slug=None):
        queryset = Question.objects.filter(quiz__slug=slug)
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serial = QuestionSerializer(data=request.data, many=True)
        serial.is_valid(raise_exception=True)
        serial.save()
        return Response({'status': serial.data})

    def update(self, request, pk=None):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': True})
        return Response({'status': False})

    def destroy(self, request, pk=None):
        question = get_object_or_404(Question, pk=pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuizList(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuizDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class ResultsViewSet(viewsets.ViewSet):
    def list(self, request, slug=None):
        queryset = Result.objects.filter(quiz__slug=slug)
        serializer = ResultSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, slug=None):
        result = Result.objects.create(
            result=request.data['result'],
            max_result=request.data['max_result'],
            user=request.user,
            quiz=get_object_or_404(Quiz, slug=slug)
        )
        return Response({'result': model_to_dict(result)})
