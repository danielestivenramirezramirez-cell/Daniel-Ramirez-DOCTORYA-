class ExternalPaymentGateway:
    def execute_transaction(self, amount_in_cents: int, account: str) -> bool:
        print(f"Procesando pago externo de {amount_in_cents} centavos para {account}")
        return True

class PaymentAdapter:
    def __init__(self, external_gateway: ExternalPaymentGateway):
        self.external_gateway = external_gateway

    def pay(self, amount: float, user_email: str) -> str:
        cents = int(amount * 100)
        success = self.external_gateway.execute_transaction(cents, user_email)
        if success:
            return f"Pago de ${amount} procesado exitosamente mediante Adapter."
        return "Error al procesar el pago."