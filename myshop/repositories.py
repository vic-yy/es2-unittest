from abc import ABC, abstractmethod
from .products import Product

class ProductRepository(ABC):
    @abstractmethod
    def get_by_id(self, product_id: int) -> Product: ...
    @abstractmethod
    def save(self, product: Product) -> None: ...