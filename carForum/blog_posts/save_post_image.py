from flask import current_app

def save_post_image(pic_upload, username):
    import uuid
    from PIL import Image
    import os

    filename = pic_upload.filename
    ext_type = filename.split('.')[-1]
    storage_filename = f"{username}_{uuid.uuid4().hex}.{ext_type}"

    filepath = os.path.join(current_app.root_path, 'static/post_images', storage_filename)

    output_size = (800, 600)  # Larger size for post images
    image = Image.open(pic_upload)
    image.thumbnail(output_size)
    image.save(filepath)

    return storage_filename