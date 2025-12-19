import requests

# Base endpoint for querying Bitcoin address data.
# BlockCypher is used here for its simple REST interface
# and reliable address-level balance and transaction metadata.
BLOCKCHAIN_API = "https://api.blockcypher.com/v1/btc/main/addrs"


def get_wallet_info(address: str):
    """
    Retrieves on-chain wallet metadata for a given Bitcoin address.

    This function queries the BlockCypher public API to fetch
    the confirmed balance and total transaction count associated
    with the address.

    Assumptions:
    - Only confirmed (final) balances are considered.
    - Transaction count reflects on-chain activity and does not
      differentiate between incoming and outgoing transactions.

    Raises:
        requests.exceptions.RequestException:
            Propagated when network failures, timeouts,
            or non-2xx HTTP responses occur.
    """
    # Construct the full API endpoint for the given wallet address.
    url = f"{BLOCKCHAIN_API}/{address}"

    # A timeout is explicitly set to prevent the application from
    # hanging indefinitely on slow or unresponsive external services.
    response = requests.get(url, timeout=10)

    # Fail fast on non-success HTTP responses to ensure
    # upstream callers can handle error states consistently.
    response.raise_for_status()

    data = response.json()

    # Convert balance from satoshis to BTC for human-readable output,
    # keeping the API response consumer-friendly.
    return {
        "address": address,
        "balance_btc": data["final_balance"] / 1e8,
        "total_transactions": data["n_tx"]
    }
