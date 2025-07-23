from django.core.exceptions import ValidationError

def validate_file_size(file):
    max_size_kb = 100

    if file.size > max_size_kb * 1000:
        raise ValidationError(f'Image cannot be larger than {max_size_kb}KB!')