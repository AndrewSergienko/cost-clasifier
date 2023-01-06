from bankapi.monobank.models import MonobankApiManager


def create_monobank_manager(token: str, *args, **kwargs) -> MonobankApiManager:
    return MonobankApiManager(token=token)

