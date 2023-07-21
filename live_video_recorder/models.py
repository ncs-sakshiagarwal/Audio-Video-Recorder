from django.conf import settings
from django.db import models




class RecordedVideo(models.Model):
    video = models.FileField(upload_to="recordings/")
    created_at = models.DateTimeField(auto_now_add=True)


class AudioRecording(models.Model):
    audio = models.FileField(upload_to='audio_recordings/')
    created_at = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    question_text = models.CharField(max_length=5000)
    def __str__(self):
            return self.question_text
    
class Response(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='responses'
    )
    RESPONSE_TYPES = [
        ('video', 'Video'),
        ('audio', 'Audio'),
    ]
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response_type=models.CharField(max_length=10, choices=RESPONSE_TYPES)
    response_text = models.CharField(max_length=100)
    response_media = models.FileField(upload_to="recordings/")


class UserProfile(models.Model):
    user = models.OneToOneField( settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='userprofile')
    role = models.ForeignKey('Role',  on_delete=models.CASCADE)
  
    
class Role(models.Model):
    name  = models.CharField(max_length=100)
    def __str__(self):
            return self.name
    