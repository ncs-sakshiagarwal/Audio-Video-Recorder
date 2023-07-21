from django.contrib import admin
from .models import RecordedVideo, AudioRecording, Role, UserProfile
from .models import Question, Response
from django.contrib.auth.models import Permission


admin.site.register(RecordedVideo)
admin.site.register(AudioRecording)
admin.site.register(Question)
admin.site.register(Response)
admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(UserProfile)
