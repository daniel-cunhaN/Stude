import base64

def img_to_base64(path):
    """Converte uma imagem em string base64 para uso em HTML."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()
