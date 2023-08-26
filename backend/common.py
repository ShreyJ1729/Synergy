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
    .pip_install_from_requirements("requirements.txt")
    .run_commands(
        "apt-get update",
        "apt-get install -y git",
        "cd /root && git clone https://github.com/ggerganov/llama.cpp",
        "cd /root/llama.cpp && make",
    )
)

stub = Stub(
    image=image,
    mounts=mounts,
    name="synergy",
)
