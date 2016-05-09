from django.db import models
from django.contrib.auth.models import User
import os
# Create your models here.




class FileStorage(models.Model):
    user = models.ForeignKey(User,related_name='user_files',on_delete=models.CASCADE)
    file = models.FileField('File')
    public = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return os.path.basename(self.file.name)





class Note(models.Model):
    user = models.ForeignKey(User,related_name='user_notes',on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=True)
    body = models.TextField()
    title = models.CharField(max_length=25)
    subject = models.CharField(max_length=25)
    file = models.FileField('File',upload_to='notes')

    def filename(self):
        return os.path.basename(self.file.name)