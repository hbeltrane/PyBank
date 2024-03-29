from dataclasses import dataclass, field
from datetime import datetime

from model.customer import Customer
from model.product import Product


@dataclass(kw_only=True, slots=True)
class Account:
    acc_number: str
    acc_type_id: int
    balance: float
    transfer_amount: float
    transfer_quantity: int
    customer_id: int
    open_date: datetime
    agent_id: str
    acc_type: Product = field(init=False)
    customer: Customer = field(init=False, default=None)

    def __post_init__(self):
        self.acc_type = Product(self.acc_type_id)

    def set_customer(self, customer):
        self.customer = customer
