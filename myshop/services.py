from .repositories import ProductRepository

class ProductNotFoundError(Exception):
    pass

class ProductService:
    def __init__(self, repo: ProductRepository, tax_rate: float = 0.10):
        self.repo = repo
        self.tax_rate = tax_rate

    def get_product(self, product_id: int):
        try:
            return self.repo.get_by_id(product_id)
        except KeyError as exc:
            raise ProductNotFoundError(product_id) from exc

    def set_price(self, product_id: int, new_price: float) -> None:
        if new_price < 0:
            raise ValueError("price cannot be negative")
        p = self.get_product(product_id)
        self.repo.save(p.with_price(new_price))

    # def final_price(self, product_id: int, discount: float = 0.0, include_tax: bool = True) -> float:
    #     if not (0.0 <= discount <= 1.0):
    #         raise ValueError("discount must be between 0 and 1")

    #     p = self.get_product(product_id)
    #     price = p.price

    #     tax_value = 0.0
    #     if include_tax:
    #         tax_value = price * self.tax_rate   # imposto aplicado no preço original (BUG)

    #     price = price * (1 - discount)          # aplica desconto no preço
    #     price = price + tax_value                # soma imposto calculado antes (não afetado pelo desconto)

    #     return round(price, 2)



    def final_price(self, product_id: int, discount: float = 0.0, include_tax: bool = True) -> float:
        if not (0.0 <= discount <= 1.0):
            raise ValueError("discount must be between 0 and 1")

        p = self.get_product(product_id)
        price = p.price

        price = price * (1 - discount)          # 1) desconto primeiro
        if include_tax:
            price = price * (1 + self.tax_rate) # 2) imposto sobre preço já com desconto

        return round(price, 2)

