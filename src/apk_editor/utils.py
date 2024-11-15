from pathlib import Path
import subprocess
import requests


def is_java_installed() -> bool:
    try:
        subprocess.run(
            ["java", "-version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except FileNotFoundError:
        return False


def download_file(url, path: Path):
    """
    Downloads a file from the given URL and saves it to the specified Path.

    Parameters:
        url (str): The URL of the file to download.
        path (Path): A Path object representing where the file will be saved.

    Returns:
        bool: True if the download is successful, False otherwise.
    """
    try:
        # Ensure the parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        with requests.get(url, stream=True) as response:
            response.raise_for_status()  # Raise an HTTPError if the HTTP request failed
            with path.open(
                "wb"
            ) as file:  # Use Path's open method for writing binary data
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # Filter out keep-alive chunks
                        file.write(chunk)
        print(f"File downloaded successfully: {path}")
        return True
    except requests.RequestException as e:
        print(f"An error occurred while downloading the file: {e}")
        return False
