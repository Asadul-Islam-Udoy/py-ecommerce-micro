from abc import ABC, abstractmethod

class PaymentInterface(ABC):

    @abstractmethod
    def create_payment(self, transaction):
        pass

    @abstractmethod
    def verify_payment(self, data):
        pass

    @abstractmethod
    def refund_payment(self, transaction):
        pass