from modal import Stub, Image
import modal

mounts = [
    modal.Mount.from_local_file(
        ".env",
        "/root/.env",
    ),
]

image = (
    modal.Image.debian_slim()
    .apt_install("git", "ffmpeg")
    .pip_install(
        "openai",
        "python-dotenv",
        "https://github.com/openai/whisper/archive/v20230314.tar.gz",
        "ffmpeg-python",
        "numpy",
    )
)

stub = Stub(
    image=image,
    mounts=mounts,
    name="synergy",
)
