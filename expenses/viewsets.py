from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Expense
from .serializers import ExpenseSerializer


class ExpenseViewSet(ModelViewSet):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()

    def list(self, request):
        queryset = Expense.objects.all().order_by("-date_added")
        serializer = ExpenseSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Expense.objects.all()
        expense = get_object_or_404(queryset, pk=pk)
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)
