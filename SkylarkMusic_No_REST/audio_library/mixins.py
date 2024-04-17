

def get_path_upload_track(instance, file):
    return f'track/{instance.user.id}/{file}'


def get_path_upload_cover_track(instance, file):
    return f'track/cover/{instance.user.id}/{file}'
