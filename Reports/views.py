from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.timezone import now
from bson import ObjectId
from .serializers import ReportUploadSerializer
from WeCare.settings import REPORTS_COLLECTION


class UploadReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReportUploadSerializer(data=request.data)

        if serializer.is_valid():
            file = request.FILES.get("report_file", None)
            if not file:
                return Response({"error": "No file uploaded."}, status=400)

            if file.content_type != "application/pdf":
                return Response({"error": "Only PDF files are allowed."}, status=400)

            filename = f"reports/{now().timestamp()}_{file.name}"
            file_path = default_storage.save(filename, file)

            report_data = {
                "_id": ObjectId(),
                "user_id": str(request.user.id) if request.user.is_authenticated else "anonymous",
                "report_date": serializer.validated_data["report_date"].isoformat(),
                "report_type": serializer.validated_data["report_type"],
                "file_url": default_storage.url(file_path),
                "uploaded_at": now().isoformat(),
            }

            REPORTS_COLLECTION.insert_one(report_data)
            report_data["_id"] = str(report_data["_id"])

            return Response({"message": "Report uploaded successfully", "report": report_data}, status=201)

        return Response(serializer.errors, status=400)


class GetReportsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = str(request.user.id) if request.user.is_authenticated else "anonymous"
        user_reports = REPORTS_COLLECTION.find({"user_id": user_id}).sort("uploaded_at", -1)

        reports = []
        for report in user_reports:
            reports.append({
                "report_id": str(report["_id"]),
                "report_date": report["report_date"],
                "report_type": report["report_type"],
                "file_url": report.get("file_url", None),
                "uploaded_at": report["uploaded_at"]
            })

        return Response({"reports": reports}, status=200)
