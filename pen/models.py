from django.db import models
from django.utils import timezone
# Create your models here.
from django.contrib.auth.models import User

class UserReg(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Profile', default='profile/default.jpg')
    qualification = models.CharField(max_length=100,default='Not Provided')
    phone_number = models.CharField(max_length=20,default='Not Provided')
    address = models.CharField(max_length=255,default='Not Provided')
    location = models.CharField(max_length=100,default='Not Provided')
    state = models.CharField(max_length=100,default='Not Provided')
    city = models.CharField(max_length=100,default='Not Provided')

    def __str__(self):
        return self.user.username
    


class Master(models.Model):
    username = models.CharField(max_length=150, default='name')
    email = models.EmailField(default='example@example.com')
    phone = models.CharField(max_length=50, default='Not Provided')
    address = models.CharField(max_length=255, default='Not Provided')
    qual = models.CharField(max_length=100, default='Not Provided')
    field = models.CharField(max_length=100, default='Default Value')
    img = models.ImageField(upload_to='Profile')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(default='Not Provided')

    def delete(self, *args, **kwargs):
        user = self.user
        super().delete(*args, **kwargs)
        user.delete()

    def __str__(self):
        return self.user.username

class WritingSubmission(models.Model):
    CATEGORY_CHOICES = [    
        ('Literature-Story', 'Literature-Story'),
        ('Poem', 'Poem'),
        ('Novel', 'Novel'),
        ('Article', 'Article'),
        ('Journals', 'Journals'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)



    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('open', 'Open'),
        ('completed', 'Completed'),
    )


    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class FeedbackDetails(models.Model):
    submission = models.ForeignKey(WritingSubmission, on_delete=models.CASCADE)
    spelling_mark = models.FloatField(default=0)  # Changed to FloatField
    plagiarism_mark = models.FloatField(default=0)  # Changed to FloatField
    grammar_mark = models.FloatField(default=0)  # Changed to FloatField
    total_mark = models.FloatField(default=0)  # Changed to FloatField
    reviewed_by = models.CharField(max_length=150, default='') 

    def __str__(self):
        return self.submission.title
    
    def reviewed_by_user(self):
        try:
            user = User.objects.get(username=self.reviewed_by)
            return user
        except User.DoesNotExist:
            return None
    

class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    complaint_against = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint by {self.user.username} against {self.complaint_against} on {self.created_at}"
    

class ChatMessage(models.Model):
    sender_user = models.ForeignKey(UserReg, null=True, blank=True, on_delete=models.CASCADE, related_name='sent_messages')
    receiver_user = models.ForeignKey(UserReg, null=True, blank=True, on_delete=models.CASCADE, related_name='received_messages')
    sender_master = models.ForeignKey(Master, null=True, blank=True, on_delete=models.CASCADE, related_name='sent_messages')
    receiver_master = models.ForeignKey(Master, null=True, blank=True, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.message
