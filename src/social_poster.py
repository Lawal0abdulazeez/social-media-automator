# Classes for posting to each platform
# src/social_poster.py

import os
import tweepy
import requests
import json
from . import config

class SocialPoster:
    """Base class for social media posters."""
    def post(self, text: str, media_path: str) -> bool:
        """
        Posts content to a social media platform.
        
        Args:
            text (str): The text content of the post.
            media_path (str): The local file path to the media to be uploaded.
            
        Returns:
            bool: True if posting was successful, False otherwise.
        """
        raise NotImplementedError("Subclasses must implement this method.")


class TwitterPoster(SocialPoster):
    """Handles posting to Twitter (X)."""
    def __init__(self):
        try:
            # For posting tweets (v2)
            self.client = tweepy.Client(
                consumer_key=config.TWITTER_API_KEY,
                consumer_secret=config.TWITTER_API_SECRET,
                access_token=config.TWITTER_ACCESS_TOKEN,
                access_token_secret=config.TWITTER_ACCESS_TOKEN_SECRET
            )
            # For uploading media (v1.1)
            auth = tweepy.OAuth1UserHandler(
                consumer_key=config.TWITTER_API_KEY,
                consumer_secret=config.TWITTER_API_SECRET,
                access_token=config.TWITTER_ACCESS_TOKEN,
                access_token_secret=config.TWITTER_ACCESS_TOKEN_SECRET
            )
            self.api_v1 = tweepy.API(auth)
        except Exception as e:
            print(f"Error initializing Twitter client: {e}")
            self.client = None
            self.api_v1 = None

    def post(self, text: str, media_path: str) -> bool:
        if not self.client or not self.api_v1:
            print("Twitter client not initialized. Cannot post.")
            return False
            
        try:
            print("Uploading media to Twitter...")
            media = self.api_v1.media_upload(filename=media_path)
            media_id = media.media_id
            
            print("Posting tweet...")
            self.client.create_tweet(text=text, media_ids=[media_id])
            print("Successfully posted to Twitter.")
            return True
        except tweepy.errors.TweepyException as e:
            print(f"An error occurred with Twitter API: {e}")
            return False


class LinkedInPoster(SocialPoster):
    """Handles posting to LinkedIn."""
    def __init__(self):
        self.access_token = config.LINKEDIN_ACCESS_TOKEN
        self.author_urn = f"urn:li:person:{config.LINKEDIN_USER_ID}"
        self.api_base_url = "https://api.linkedin.com/v2"

    def post(self, text: str, media_path: str) -> bool:
        if not all([self.access_token, self.author_urn]):
            print("LinkedIn config missing. Cannot post.")
            return False

        try:
            # Step 1: Register the upload to get the upload URL
            print("Registering LinkedIn media upload...")
            register_headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            register_payload = {
                "registerUploadRequest": {
                    "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                    "owner": self.author_urn,
                    "serviceRelationships": [{"relationshipType": "OWNER", "identifier": "urn:li:userGeneratedContent"}]
                }
            }
            reg_res = requests.post(
                f"{self.api_base_url}/assets?action=registerUpload",
                headers=register_headers,
                json=register_payload
            )
            reg_res.raise_for_status()
            upload_data = reg_res.json()
            upload_url = upload_data['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
            asset_urn = upload_data['value']['asset']

            # Step 2: Upload the actual image file
            print("Uploading media to LinkedIn...")
            with open(media_path, 'rb') as f:
                upload_headers = {'Authorization': f'Bearer {self.access_token}'}
                up_res = requests.put(upload_url, headers=upload_headers, data=f)
                up_res.raise_for_status()

            # Step 3: Create the UGC (User Generated Content) Post
            print("Creating LinkedIn post...")
            post_headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json',
                'X-Restli-Protocol-Version': '2.0.0'
            }
            post_payload = {
                "author": self.author_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": text},
                        "shareMediaCategory": "IMAGE",
                        "media": [{"status": "READY", "media": asset_urn}]
                    }
                },
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
            }
            post_res = requests.post(f"{self.api_base_url}/ugcPosts", headers=post_headers, json=post_payload)
            post_res.raise_for_status()

            print("Successfully posted to LinkedIn.")
            return True
        except requests.exceptions.RequestException as e:
            print(f"An error occurred with LinkedIn API: {e}")
            if e.response:
                print(f"Response Body: {e.response.text}")
            return False

class FacebookPoster(SocialPoster):
    """Handles posting to a Facebook Page."""
    def __init__(self):
        self.page_id = config.FACEBOOK_PAGE_ID
        self.access_token = config.FACEBOOK_ACCESS_TOKEN
        self.api_base_url = "https://graph.facebook.com/v18.0"

    def post(self, text: str, media_path: str) -> bool:
        if not all([self.page_id, self.access_token]):
            print("Facebook config missing. Cannot post.")
            return False

        post_url = f"{self.api_base_url}/{self.page_id}/photos"
        params = {
            'caption': text,
            'access_token': self.access_token
        }
        
        try:
            print("Uploading media and posting to Facebook...")
            with open(media_path, 'rb') as f:
                files = {'source': f}
                response = requests.post(post_url, params=params, files=files)
                
                # This will raise an exception for bad status codes (4xx or 5xx)
                response.raise_for_status()
            
            print("Successfully posted to Facebook.")
            return True
        except requests.exceptions.RequestException as e:
            print(f"An error occurred with Facebook API: {e}")
            # --- START OF IMPROVEMENT ---
            # If the response object exists, print the detailed error from Facebook
            if e.response is not None:
                try:
                    error_details = e.response.json()
                    print("--- Facebook Error Details ---")
                    print(json.dumps(error_details, indent=2))
                    print("----------------------------")
                except json.JSONDecodeError:
                    print("Could not decode JSON from Facebook's error response.")
                    print(f"Response Body: {e.response.text}")
            # --- END OF IMPROVEMENT ---
            return False