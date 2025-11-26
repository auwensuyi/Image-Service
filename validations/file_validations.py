ALLOWED_EXTS = {"jpg", "jpeg", "png", "webp", "gif", "bmp", "tiff", "ico"}
ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
    "image/bmp",
    "image/tiff",
    "image/x-icon",
}


class FileValidations:
    @staticmethod
    def is_valid_extension(filename: str) -> bool:
        ext = filename.rsplit(".", 1)[-1].lower()
        return ext in ALLOWED_EXTS

    @staticmethod
    def is_valid_mime(mime_type: str) -> bool:
        return mime_type in ALLOWED_MIME_TYPES

    @staticmethod
    def validate(file) -> bool:
        """Validate both extension and content type."""
        filename = file.filename
        mime_type = file.content_type

        return (
            FileValidations.is_valid_extension(filename)
            and FileValidations.is_valid_mime(mime_type)
        )
