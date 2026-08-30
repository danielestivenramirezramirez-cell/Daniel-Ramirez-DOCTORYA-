from abc import ABC, abstractmethod

class PricingStrategy(ABC):
    @abstractmethod
    def calculate_price(self, base_price: float) -> float:
        pass

class GeneralConsultationStrategy(PricingStrategy):
    def calculate_price(self, base_price: float) -> float:
        return base_price

class SpecialistConsultationStrategy(PricingStrategy):
    def calculate_price(self, base_price: float) -> float:
        return base_price * 1.5

class EmergencyConsultationStrategy(PricingStrategy):
    def calculate_price(self, base_price: float) -> float:
        return base_price * 2.0