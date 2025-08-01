from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError

User = settings.AUTH_USER_MODEL
print(User)

class Post(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  content = models.TextField()
  share_on_linkedin = models.BooleanField(default=False)
  shared_at_linkedin = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
  updated_at = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def clean(self, *args, **kwargs):
    super().clean(*args, **kwargs)
    if len(self.content) < 5:
      raise ValidationError({
         "content": "Content is too short, at least 5 characters are required"
      })
    elif self.share_on_linkedin and not self.can_share_on_linkedin:
      raise ValidationError({
         "share_on_linkedin": "Post is already shared on linkedin"
      })

  def save(self, *args, **kwargs):
    if self.share_on_linkedin and self.can_share_on_linkedin:
        print("sharing on linkedin")
        self.shared_at_linkedin = timezone.now()
    else:
        print("not sharing on linkedin")
      
    self.share_on_linkedin = False
    super(Post, self).save(*args, **kwargs)
  
  @property
  def can_share_on_linkedin(self):
    return not self.shared_at_linkedin

