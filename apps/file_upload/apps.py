"""FILE UPLOAD MODULE"""
from django.apps import AppConfig


class FileUploadConfig(AppConfig):
    """Config for uploading files"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.file_upload'
