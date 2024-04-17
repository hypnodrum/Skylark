from django.core.exceptions import ValidationError


def validate_size_image(file_obj):
    # 1024 * 1024 = 1MB
    file_size_limit = 2
    if file_obj.size > file_size_limit * 1024 * 1024:
        raise ValidationError(
            f'Image size must be less than {file_size_limit}MB'
        )
