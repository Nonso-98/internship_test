from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .Serializer import UserSerializer
from .models import User
from datetime import datetime
import requests


class UserListView(APIView):

    def get(self, request):
        name = request.GET.get("name")

        if not name:
            return Response(
                {"status": "error", "message": "Name is required"},
                status=400
            )

        if not isinstance(name, str):
            return Response(
                {"status": "error", "message": "Name must be a string"},
                status=422
            )

        try:
            res = requests.get(f"https://api.genderize.io/?name={name}")
            data = res.json()

            gender = data.get("gender")
            probability = float(data.get("probability", 0))
            sample_size = data.get("count", 0)

            if gender is None or sample_size == 0:
                return Response(
                    {
                        "status": "error",
                        "message": "No prediction available for the provided name"
                    },
                    status=404
                )

            is_confident = probability >= 0.7 and sample_size >= 100

            processed_at = datetime.utcnow().isoformat() + "Z"

            return Response({
                "status": "success",
                "data": {
                "name": name,
                "gender": gender,
                "probability": probability,
                "sample_size": sample_size,
                "is_confident": is_confident,
                "processed_at": processed_at

                }
            })

        except Exception:
            return Response(
                {"status": "error", "message": "External API error"},
                status=502
            )
