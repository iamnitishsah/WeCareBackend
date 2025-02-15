from rest_framework import serializers

class ReportUploadSerializer(serializers.Serializer):
    report_date = serializers.DateField()
    report_type = serializers.CharField(max_length=255)
    report_file = serializers.FileField()
