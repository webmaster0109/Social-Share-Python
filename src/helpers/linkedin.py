from django.contrib.auth import get_user_model
import requests

def get_linkedin_user_details(user):
  try:
    linkedin_social = user.socialaccount_set.get(provider='linkedin')
  except:
    raise Exception('Linkedin is not connected on this user.')
  return linkedin_social

def get_share_headers(linkedin_social):
  tokens = linkedin_social.socialtoken_set.all()
  if not tokens.exists():
    raise Exception('Linkedin connection is invalid. Please Login Again.')
  
  token = tokens.first()
  
  return {
      "Authorization": f"Bearer {token.token}",
      "X-Restli-Protocol-Version": "2.0.0"
  }

def post_to_linkedin(user, text:str):
  User = get_user_model()
  if not isinstance(user, User):
    raise Exception('user must be a User instance')
  
  linkedin_social = get_linkedin_user_details(user)
  headers = get_share_headers(linkedin_social)
  endpoints = "https://api.linkedin.com/v2/ugcPosts"

  linkedin_user_id = linkedin_social.uid
  if not linkedin_user_id:
    raise Exception('Linkedin User ID is invalid')
  
  payload = {
      "author": f"urn:li:person:{linkedin_user_id}",
      "lifecycleState": "PUBLISHED",
      "specificContent": {
          "com.linkedin.ugc.ShareContent": {
              "shareCommentary": {
                  "text": f"{text}"
              },
              "shareMediaCategory": "NONE"
          }
      },
      "visibility": {
          "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
      }
  }
  
  response = requests.post(endpoints, json=payload, headers=headers)
  try:
    response.raise_for_status()
  except:
    raise Exception("Invalid posting to linkedin, try again.")
  
  return response