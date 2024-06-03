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

    # 신고글 id, type, 유저가 모두 중복 되는지 체크
    def save(self):
        if Report.objects.filter(
            object_id=self.object_id,
            content_type=self.content_type,
            writer=self.writer
        ).exists():
            raise ValidationError('이미 신고한 글 입니다')
        super().save()