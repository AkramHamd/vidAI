import re
import uuid

def sanitize_filename(filename):
    """
    Sanitize the filename by removing or replacing characters that are not allowed
    in file names. This function also truncates the filename to a maximum length to
    ensure it does not exceed filesystem limits.
    """
    # Remove or replace invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '', filename)
    # Replace spaces with underscores
    sanitized = sanitized.replace(' ', '_')
    # Truncate to the first 100 characters to avoid long filenames
    sanitized = sanitized[:100]
    # Ensure the filename is not empty
    sanitized = sanitized if sanitized else "unnamed"
    return sanitized

def generate_temp_video_path(title):
    """
    Generates a path for saving a temporary video file with a sanitized title
    and a unique identifier.
    """
    sanitized_title = sanitize_filename(title)
    unique_id = str(uuid.uuid4())
    temp_video_path = f"./.temp/{sanitized_title}_{unique_id}.mp4"
    return temp_video_path
