from dataclasses import dataclass

@dataclass(frozen=True)
class Product:
    id: int
    name: str
    price: float

    def with_price(self, new_price: float) -> "Product":
        if new_price < 0:
            raise ValueError("price cannot be negative")
        return Product(self.id, self.name, new_price)
