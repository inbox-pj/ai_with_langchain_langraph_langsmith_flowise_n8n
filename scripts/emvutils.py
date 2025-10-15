from typing import Dict, Union

def hexstr_to_bytes(hexstr: str) -> bytes:
    """Convert hex string to bytes, ignoring spaces."""
    return bytes.fromhex(hexstr.replace(" ", ""))

def is_cardholder_verification_supported(aip: bytes) -> bool:
    """
    Check if cardholder verification is supported in AIP (tag 82).
    Bit 5 of first byte (0x10) should be set.
    """
    if not aip or len(aip) < 1:
        return False
    return bool(aip[0] & 0x10)

def get_cvm_methods(cvm_list: bytes) -> list:
    """
    Parse CVM list (tag 8E) and return list of CVM codes.
    Each CVM entry is 2 bytes: [CVM code, Condition code]
    """
    if not cvm_list or len(cvm_list) < 2:
        return []
    return [cvm_list[i] for i in range(0, len(cvm_list), 2)]

def is_offline_pin_highest_priority(cvm_list: bytes) -> bool:
    """
    Check if offline PIN for CA (CVM code 0x01) is the highest priority in CVM list.
    """
    methods = get_cvm_methods(cvm_list)
    return methods and methods[0] == 0x01

def will_card_always_request_pin(card_tags: Dict[str, Union[str, bytes]]) -> bool:
    """
    Main function to validate if card will always request PIN.
    card_tags: dict with keys '82' (AIP) and '8E' (CVM list), values as hex strings or bytes.
    """
    aip = card_tags.get('82')
    cvm_list = card_tags.get('8E')

    # Convert hex strings to bytes if needed
    if isinstance(aip, str):
        aip = hexstr_to_bytes(aip)
    if isinstance(cvm_list, str):
        cvm_list = hexstr_to_bytes(cvm_list)

    cv_supported = is_cardholder_verification_supported(aip)
    offline_pin_priority = is_offline_pin_highest_priority(cvm_list)

    return cv_supported and offline_pin_priority

def explain_card_pin_requirement(card_tags: Dict[str, Union[str, bytes]]) -> str:
    aip = card_tags.get('82')
    cvm_list = card_tags.get('8E')
    if isinstance(aip, str):
        aip = hexstr_to_bytes(aip)
    if isinstance(cvm_list, str):
        cvm_list = hexstr_to_bytes(cvm_list)

    cv_supported = is_cardholder_verification_supported(aip)
    offline_pin_priority = is_offline_pin_highest_priority(cvm_list)

    explanation = []
    explanation.append(f"AIP (tag 82): {aip.hex().upper() if aip else 'Missing'}")
    explanation.append(f"CVM List (tag 8E): {cvm_list.hex().upper() if cvm_list else 'Missing'}")
    explanation.append(f"Cardholder verification supported in AIP: {'Yes' if cv_supported else 'No'}")
    explanation.append(f"Offline PIN for CA is highest priority in CVM list: {'Yes' if offline_pin_priority else 'No'}")
    explanation.append(f"Result: Card {'will' if cv_supported and offline_pin_priority else 'will NOT'} always request PIN for transaction.")
    return "\n".join(explanation)

def parse_tlv(hexstr: str) -> Dict[str, bytes]:
    """
    Parse a hex TLV string and return a dict of tag -> value (as bytes).
    Supports single-byte and double-byte tags, standard EMV TLV encoding.
    """
    data = bytes.fromhex(hexstr.replace(" ", ""))
    tlvs = {}
    i = 0
    while i < len(data):
        # Tag parsing
        tag = data[i]
        i += 1
        if (tag & 0x1F) == 0x1F:  # multi-byte tag
            tag = (tag << 8) | data[i]
            i += 1
        tag_hex = f"{tag:02X}" if tag <= 0xFF else f"{tag:04X}"
        # Length parsing
        length = data[i]
        i += 1
        if length & 0x80:
            num_bytes = length & 0x7F
            length = int.from_bytes(data[i:i+num_bytes], 'big')
            i += num_bytes
        # Value
        value = data[i:i+length]
        i += length
        tlvs[tag_hex] = value
    return tlvs

# Example usage and test cases
if __name__ == "__main__":
    # Example card data (replace with actual tag values from your cards)
    # cards = [
    #     {
    #         "name": "Card 1 (PIN always requested)",
    #         "82": "38 00",  # Bit 3 set (0x38 & 0x04 == 0x04)
    #         "8E": "01 00 02 00",  # First CVM code is 0x01 (offline PIN for CA)
    #     },
    #     {
    #         "name": "Card 2 (PIN not always requested)",
    #         "82": "30 00",  # Bit 3 not set (0x30 & 0x04 == 0x00)
    #         "8E": "02 00 01 00",  # First CVM code is 0x02 (not offline PIN for CA)
    #     },
    #     {
    #         "name": "Card 3 (PIN not highest priority)",
    #         "82": "38 00",  # Bit 3 set
    #         "8E": "02 00 01 00",  # First CVM code is 0x02
    #     },
    # ]
    #
    # for card in cards:
    #     print(f"--- {card['name']} ---")
    #     print(explain_card_pin_requirement(card))
    #     print()

    # --- EMV TLV string test ---
    emv_hex = "820219005F3401019F02060000000010005F2A0201245F3601029F0702FFC09F0D05FC78FCA8409F0E0500000000009F0F05FCF8FCF8705007496E74657261639F2608C2A967D4B19BA24E9F0607A00000027710109F360200E99F2701809F34030403029F1E08434D4A78353742579F10161502850400B100000000B280000000000000000000009F3901059F3303E0B8C89F1A0201249F350122950500800080009A032510109B02E8009C01209F3704749153DE9F21031212358407A00000027710109F4005F800F0F0019F150200009F4104000000079F1C08434D4A78353742575F280201249F5301FF9F09020001"
    tlvs = parse_tlv(emv_hex)
    card_tags = {"82": tlvs.get("82"), "8E": tlvs.get("8E")}
    print("--- Derived from EMV TLV ---")
    print(explain_card_pin_requirement(card_tags))
    print()
