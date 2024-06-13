from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError


# Create your models here.
class Report(models.Model):
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')
    report_type = models.CharField(
        choices=(('UPDATE', 'UPDATE'), ('DELETE', 'DELETE'), ('REPORT', 'REPORT')),
        max_length=6
    )
    report_content = models.TextField()
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if Report.objects.filter(
                object_id=self.object_id,
                content_type=self.content_type,
                report_type=self.report_type,
                writer=self.writer
        ).exists():
            raise ValidationError("이미 같은 내용의 신고가 존재합니다.")
        super().save(*args, **kwargs)