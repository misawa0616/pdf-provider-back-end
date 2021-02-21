from django.contrib import admin
from django.urls import path
from pdf_manage import views


urlpatterns = [
    path('pdf_tester/', views.PdfTester.as_view())
]
