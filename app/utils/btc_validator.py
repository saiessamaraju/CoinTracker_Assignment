import re


def is_valid_btc_address(address: str) -> bool:
    """
    Performs basic syntactic validation for Bitcoin addresses.

    Supports:
    - Legacy addresses (P2PKH / P2SH starting with '1' or '3')
    - Native SegWit addresses (bech32 starting with 'bc1')

    Note:
    This validation checks format only. It does not verify checksum
    correctness or on-chain existence, which are intentionally deferred
    to external blockchain providers.
    """
    # Guard against non-string inputs to avoid regex errors
    # and enforce a predictable function contract.
    if not isinstance(address, str):
        return False

    # Legacy Bitcoin address format:
    # - Starts with '1' or '3'
    # - Base58 characters excluding visually ambiguous ones
    # - Typical length range: 26–35 characters
    legacy = r"^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$"

    # Native SegWit (bech32) address format:
    # - Always starts with 'bc1'
    # - Lowercase alphanumeric characters
    # - Length varies based on witness version and program size
    segwit = r"^(bc1)[a-z0-9]{39,59}$"

    # Return True if the address matches any supported Bitcoin format
    return bool(re.match(legacy, address) or re.match(segwit, address))
