import os
from datetime import datetime
from uuid import uuid4
from django.contrib.auth.models import User


def default_upload_path(app_dir: str, user: User, filename: str) -> str:
    _, ext = os.path.splitext(filename)
    datetime_str = datetime.now().strftime("%d.%m.%Y_%H-%M-%S.%f")
    filename = f"{datetime_str}-{str(uuid4())}{ext}"
    return os.path.join(app_dir, user.username, filename)