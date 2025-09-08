import datetime
import random
import string


def generate_filename(length: int = 12) -> str:

    # Get the current date in YYYYMMDD format
    current_date = datetime.date.today().strftime("%d%m%Y")

    # Generate a random string of the specified length
    random_string = "".join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )

    # Combine the date, random string, and extension
    filename = f"{current_date}_{random_string}"
    return filename
