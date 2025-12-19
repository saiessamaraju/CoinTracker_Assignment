from app.utils.btc_validator import is_valid_btc_address
from app.services.blockchain_service import get_wallet_info
from app.db.database import (
    add_wallet as db_add_wallet,
    wallet_exists,
    get_all_wallets
)


def add_wallet(address: str):
    """
    Registers a Bitcoin address for tracking.

    This function performs input validation and idempotency checks
    before persisting the wallet address. It enforces business rules
    at the service layer to keep API routes thin and predictable.

    Raises:
        ValueError:
            - If the address format is invalid
            - If the address is already being tracked
    """
    # Validate Bitcoin address format before any database interaction
    # to prevent storing malformed or unsupported addresses.
    if not is_valid_btc_address(address):
        raise ValueError("Invalid Bitcoin address")

    # Enforce uniqueness at the service layer to provide a clear,
    # user-friendly error instead of relying solely on database constraints.
    if wallet_exists(address):
        raise ValueError("Address already tracked")

    # Persist the wallet address once validation and duplication checks pass.
    db_add_wallet(address)

    # Return a minimal, explicit response indicating successful tracking.
    return {"status": "tracking", "address": address}


def list_wallets():
    """
    Retrieves all tracked Bitcoin wallet addresses.

    This method provides a lightweight summary view and does not
    perform any blockchain lookups, keeping the operation fast
    and suitable for frequent UI polling.
    """
    wallets = get_all_wallets()

    return {
        "wallets": wallets,
        "count": len(wallets)
    }


def get_wallet_details(address: str):
    """
    Fetches real-time blockchain data for a tracked Bitcoin address.

    The function ensures the wallet is registered locally before
    performing an external API call, preventing unnecessary
    outbound requests and enforcing application-level ownership.

    Raises:
        ValueError:
            If the wallet is not currently tracked.
    """
    # Ensure the address is registered locally before querying
    # external blockchain providers.
    if not wallet_exists(address):
        raise ValueError("Wallet not tracked")

    # Delegate blockchain interaction to the dedicated service layer,
    # maintaining a clean separation between persistence and I/O logic.
    return get_wallet_info(address)
