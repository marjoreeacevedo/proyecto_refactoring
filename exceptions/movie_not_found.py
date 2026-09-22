"""La película buscada no existe en OMDB."""


class MovieNotFoundError(Exception):
    """OMDB respondió Response=False para el título pedido."""
