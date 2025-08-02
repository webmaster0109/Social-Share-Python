from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError

from helpers import linkedin

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
    if self.share_on_linkedin:
       self.verify_can_share_on_linkedin()

  def save(self, *args, **kwargs):
    if self.share_on_linkedin:
      self = self.perform_share_on_linkedin(save=False)
    super().save(*args, **kwargs)
  
  def perform_share_on_linkedin(self, save=False):
      self.share_on_linkedin = False
      try:
          linkedin.post_to_linkedin(self.user, self.content)
      except:
          raise ValidationError({
              "content": "Could not share to Linkedin"
          })
      self.shared_at_linkedin = timezone.now()
      if save:
        self.save()
      return self
  
  def verify_can_share_on_linkedin(self):
    # run validation error if content is too short
    if len(self.content) < 5:
      raise ValidationError({
         "content": "Content is too short, at least 5 characters are required"
      })
    # run validation errors if attempting to share on linkedin
    if self.shared_at_linkedin:
      raise ValidationError({
        "content": "Post is already shared on linkedin"
      })
    
    try:
        # share on linkedin
        linkedin.get_linkedin_user_details(self.user)
    except linkedin.UserNotConnectedToLinkedin:
        # run validation error if user is not connected
        raise ValidationError({
          "user": "You must connect to Linkedin before sharing to Linkedin"
        })
    except Exception as e:
        # run validation error
        raise ValidationError({
          "user": f"Linkedin Error: {e}"
        })

