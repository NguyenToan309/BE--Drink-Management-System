import dataclasses

@dataclasses.dataclass
class Product:
    id: str  # UUID string
    name: str
    price: float
