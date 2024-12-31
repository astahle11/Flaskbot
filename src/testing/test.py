import os
import zipfile


def unzip_cmder():
    user_profile = os.environ.get("USERPROFILE")
    extract_dir = os.path.join(user_profile, "cmder")
    

    # Path to the .7z file
    archive_path = r"bin/cmder_mini.zip"


    # Create the destination directory if it doesn't exist
    os.makedirs(extract_dir, exist_ok=True)

    with zipfile.ZipFile(archive_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    print(f"Contents extracted to {extract_dir}")


unzip_cmder()
