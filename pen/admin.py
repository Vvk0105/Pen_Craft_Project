from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserReg,Master,WritingSubmission,FeedbackDetails,Complaint,ChatMessage

admin.site.register(UserReg)
admin.site.register(Master)
admin.site.register(WritingSubmission)
admin.site.register(FeedbackDetails)
admin.site.register(Complaint)
admin.site.register(ChatMessage)