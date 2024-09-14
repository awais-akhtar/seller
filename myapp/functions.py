import requests
from bs4 import BeautifulSoup
import json
import re
import uuid

class UniqueIDGenerator:
    def generate_unique_id(self):
        unique_id = uuid.uuid4().int % 10000300
        return str(unique_id).zfill(12)

def likee_profile_info(likeeid):
    url = f'https://likee.video/@{likeeid}?lang=en'
    # Headers to simulate a request from a web browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Send a request to the URL
    response = requests.get(url, headers=headers)

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    # with open('abc.html','w',encoding='utf-8') as f:
    #     f.write(str(soup))
    # Convert the soup object to a string for regex processing
    html_content = str(soup)

    # Extract the profile image URL using regex
    img_url_pattern = re.search(r'https://img\.like\.video/[^\s"]+', html_content)
    if img_url_pattern:
        # Clean the URL by removing any query parameters
        profile_image_url = img_url_pattern.group(0).split('?')[0]
    else:
        profile_image_url = 'N/A'

    # Extract the profile details from the meta description using regex
    meta_description_tag = soup.find('meta', {'name': 'description'})
    if meta_description_tag:
        meta_description_content = meta_description_tag.get('content', '')
        followers_pattern = re.search(r'(\d+\.?\d*[mk]?) followers', meta_description_content, re.IGNORECASE)
        likes_pattern = re.search(r'(\d+\.?\d*[mk]?) likes', meta_description_content, re.IGNORECASE)
        
        followers = followers_pattern.group(1) if followers_pattern else 'N/A'
        likes = likes_pattern.group(1) if likes_pattern else 'N/A'
    else:
        followers = 'N/A'
        likes = 'N/A'

    # Extract the profile name from the title tag
    profile_name_tag = soup.find('meta', {'name': 'title'})
    if profile_name_tag:
        profile_name_content = profile_name_tag.get('content', 'N/A')
        profile_name = re.sub(r'\(@[^)]+\) Official \| Likee', '', profile_name_content).strip()
    else:
        profile_name = 'N/A'

    # Extract the username from the URL
    username = '@' + url.split('@')[-1].split('?')[0]

    # Extract the bio from the hidden <h3> tag
    bio_tag = soup.find('h3', style='display: none;')
    if bio_tag:
        bio = bio_tag.text.strip()
    else:
        bio = 'N/A'


    # Return the extracted data as a dictionary
    return {
        'Profile_Name': profile_name,
        'Username': username,
        'Followers': followers,
        'Likes': likes,
        'Image_URL': profile_image_url,
        'Bio': bio
    }

# # Example usage
# profile_info = likee_profile_info(166629854)
# print(profile_info)

def process_avatar_url(avatar_url):
    # Remove 'https:\u002F\u002F' from the start and add 'https://'
    if avatar_url.startswith('https:\\u002F\\u002F'):
        avatar_url = 'https://' + avatar_url[len('https:\\u002F\\u002F'):]
    # Replace '\u002F' with '/'
    avatar_url = avatar_url.replace('u002F', '')
    avatar_url = avatar_url.replace('\\', '/')
    return avatar_url

def fetch_tiktok_data(tiktok_id):
    # URL of the TikTok profile
    url = f'https://www.tiktok.com/@{tiktok_id}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Dictionary to store extracted data
    tiktok_data = {}

    # Send a request to the URL
    response = requests.get(url, headers=headers)

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Locate the script tag containing the data
    script_tag = soup.find('script', {'id': '__UNIVERSAL_DATA_FOR_REHYDRATION__'})

    if script_tag:
        # Extract the JSON content from the script tag
        long_text = script_tag.string

        # Define pattern to extract shareMeta dictionary
        pattern = r'"shareMeta":\{.*?\}'

        # Find the first match of the pattern in the long text
        match = re.search(pattern, long_text)

        if match:
            # Extract shareMeta JSON data
            share_meta_json = match.group(0)
            share_meta_dict = json.loads(f'{{{share_meta_json}}}')['shareMeta']

            # Extract profile name
            try:
                profile_name = share_meta_dict.get('title', 'N/A')
                tiktok_data['profile_name'] = profile_name
            except KeyError:
                tiktok_data['profile_name'] = 'Profile Name not found'

            # Extract username
            username = url.split('@')[-1]
            tiktok_data['username'] = username

            # Extract bio details
            try:
                bio = share_meta_dict.get('desc', 'N/A')

                # Extract followers, likes, following from bio text
                followers_pattern = re.search(r'(\d+\.?\d*[mk]?) Followers', bio)
                likes_pattern = re.search(r'(\d+\.?\d*[mk]?) Likes', bio)
                following_pattern = re.search(r'(\d+\.?\d*[mk]?) Following', bio)

                followers = followers_pattern.group(1) if followers_pattern else 'N/A'
                likes = likes_pattern.group(1) if likes_pattern else 'N/A'
                following = following_pattern.group(1) if following_pattern else 'N/A'

                tiktok_data['followers'] = followers
                tiktok_data['likes'] = likes
                tiktok_data['following'] = following
            except AttributeError:
                tiktok_data['bio_details'] = 'Bio details not found'

            # Extract signature
            try:
                signature_pattern = r'"signature":"([^"]*)"'
                signature_match = re.search(signature_pattern, long_text)

                if signature_match:
                    signature = signature_match.group(1)
                    tiktok_data['signature'] = signature.replace('\\n', '')
                else:
                    tiktok_data['signature'] = 'No signature found'
            except AttributeError:
                tiktok_data['signature'] = 'Signature not found'

            # Extract biolink
            try:
                biolink_pattern = r'"bioLink":\{"link":"([^"]*)".*?\}'
                biolink_match = re.search(biolink_pattern, long_text)

                if biolink_match:
                    biolink_url = biolink_match.group(1)
                    tiktok_data['biolink'] = biolink_url
                else:
                    tiktok_data['biolink'] = 'No specific bio link found'
            except AttributeError:
                tiktok_data['biolink'] = 'Bio link not found'

            # Extract video count
            try:
                video_count_pattern = r'"videoCount":(\d+)'
                video_count_match = re.search(video_count_pattern, long_text)

                if video_count_match:
                    video_count = video_count_match.group(1)
                    tiktok_data['video_count'] = video_count
                else:
                    tiktok_data['video_count'] = 'No video count found'
            except AttributeError:
                tiktok_data['video_count'] = 'Video count not found'

            # Extract uniqueId and nickname
            try:
                unique_id_pattern = r'"uniqueId":"([^"]*)"'
                nickname_pattern = r'"nickname":"([^"]*)"'

                unique_id_match = re.search(unique_id_pattern, long_text)
                nickname_match = re.search(nickname_pattern, long_text)

                if unique_id_match:
                    unique_id = unique_id_match.group(1)
                    tiktok_data['unique_id'] = unique_id
                else:
                    tiktok_data['unique_id'] = 'No unique ID found'

                if nickname_match:
                    nickname = nickname_match.group(1)
                    tiktok_data['nickname'] = nickname
                else:
                    tiktok_data['nickname'] = 'No nickname found'
            except AttributeError:
                tiktok_data['unique_id'] = 'Unique ID or nickname not found'
            # Extract avatarThumb URL
            try:
                avatar_pattern = r'"avatarLarger":"([^"]*)"'
                avatar_match = re.search(avatar_pattern, long_text)

                if avatar_match:
                    avatar_url = avatar_match.group(1)
                    # print(process_avatar_url(avatar_url))
                    tiktok_data['avatar_url'] = process_avatar_url(avatar_url)
                else:
                    tiktok_data['avatar_url'] = 'Avatar URL not found'
            except AttributeError:
                tiktok_data['avatar_url'] = 'Avatar URL not found'
        
        else:
            tiktok_data['error'] = 'No data found'
    else:
        tiktok_data['error'] = 'Profile data not found'
    
    return tiktok_data

