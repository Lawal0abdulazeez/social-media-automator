# Main script execution logic
from . import data_source, content_adapter, social_poster, media_handler

def run_automation():
    """Main function to run the social media automation workflow."""
    print("Starting social media automation workflow...")
    
    post_data = data_source.get_todays_post()
    
    if not post_data:
        print("No post scheduled for today. Exiting.")
        return

    print(f"Found post for today: {post_data.get('Main Content')[:50]}...")
    
    main_content = post_data.get("Main Content")
    media_url = post_data.get("Media")
    
    # 1. Download Media
    media_path = media_handler.download_media(media_url)
    if not media_path:
        print("Failed to download media. Aborting post.")
        return

    # 2. Adapt for Twitter
    #twitter_content = content_adapter.adapt_for_twitter(main_content)
    
    # Post to Twitter
    #twitter_success = social_poster.TwitterPoster().post(twitter_content, media_path)
    #print(f"Twitter Post Success: {twitter_success}")
    
    # Post to LinkedIn
    #linkedin_success = social_poster.LinkedInPoster().post(main_content, media_path)
    #print(f"LinkedIn Post Success: {linkedin_success}")

    # Post to Facebook
    facebook_success = social_poster.FacebookPoster().post(main_content, media_path)
    print(f"Facebook Post Success: {facebook_success}")

    # 4. Cleanup downloaded media
    media_handler.cleanup(media_path)

    print("Workflow finished.")

if __name__ == "__main__":
    run_automation()


