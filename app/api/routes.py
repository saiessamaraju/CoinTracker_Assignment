from flask import Blueprint, request, jsonify
from app.services.wallet_service import (
    add_wallet,
    list_wallets,
    get_wallet_details
)

# Blueprint for wallet-related API endpoints.
# Using a blueprint allows the API layer to remain modular and
# easily extensible as additional resources or versions are introduced.
api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/wallets", methods=["POST"])
def add_wallet_route():
    """
    Registers a new wallet address for tracking.

    This endpoint validates and persists a wallet address via the
    service layer. Business rules (e.g., duplicate detection or
    address validation) are intentionally enforced downstream to
    keep the HTTP layer thin and focused on request handling.
    """
    data = request.get_json()
    address = data.get("address")

    try:
        # Delegates wallet registration to the service layer to
        # ensure consistent validation and persistence behavior.
        return jsonify(add_wallet(address)), 201
    except ValueError as e:
        # Client-side error indicating invalid input or a failed
        # business validation (e.g., malformed address).
        return jsonify({"error": str(e)}), 400


@api.route("/wallets", methods=["GET"])
def list_wallets_route():
    """
    Returns all currently tracked wallet addresses.

    This endpoint provides a lightweight aggregation view and is
    optimized for fast reads without triggering any external
    synchronization or blockchain lookups.
    """
    return jsonify(list_wallets())


@api.route("/wallets/<address>", methods=["GET"])
def wallet_details_route(address):
    """
    Fetches aggregated details for a specific tracked wallet.

    Wallet data retrieval is performed on-demand to avoid unnecessary
    background processing and to ensure responses reflect the most
    recent blockchain state available at request time.
    """
    try:
        # Service-layer lookup ensures the wallet is tracked and
        # handles external API interactions in a controlled manner.
        return jsonify(get_wallet_details(address))
    except ValueError as e:
        # Returned when the requested wallet is not tracked or
        # cannot be resolved by the service layer.
        return jsonify({"error": str(e)}), 404
