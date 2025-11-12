from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import re

app = FastAPI(title="Address Line Splitter API")


class AddressInput(BaseModel):
    address: str


class AddressOutput(BaseModel):
    address_line_1: str
    address_line_2: str
    address_line_3: str
    original_address: str


def split_address_equally(address: str) -> Dict[str, str]:
    """
    Split addresses into 3 equally distributed lines based on character count.
    """
    # Clean up the address
    address = ' '.join(address.split())  # Normalize whitespace

    if not address:
        return {
            "address_line_1": "",
            "address_line_2": "",
            "address_line_3": ""
        }

    # Calculate target length for each line
    total_length = len(address)
    target_length = total_length // 3

    # Split by common delimiters first
    parts = re.split(r'[,;]', address)
    parts = [part.strip() for part in parts if part.strip()]

    # If we have natural parts, try to distribute them
    if len(parts) >= 3:
        return distribute_parts(parts, 3)

    # Otherwise, split by words
    words = address.split()

    if len(words) < 3:
        # If less than 3 words, pad with empty strings
        while len(words) < 3:
            words.append("")
        return {
            "address_line_1": words[0],
            "address_line_2": words[1],
            "address_line_3": words[2]
        }

    # Distribute words across 3 lines
    lines = ["", "", ""]
    current_line = 0

    for word in words:
        # Add word to current line
        if lines[current_line]:
            lines[current_line] += " " + word
        else:
            lines[current_line] = word

        # Check if we should move to next line
        if current_line < 2:
            # Calculate remaining text
            remaining_words = words[words.index(word) + 1:]
            remaining_text = " ".join(remaining_words)
            remaining_lines = 3 - current_line - 1

            # Move to next line if current line is long enough
            if len(lines[current_line]) >= target_length and remaining_lines > 0:
                if len(remaining_text) >= remaining_lines * 10:  # Ensure minimum content for remaining lines
                    current_line += 1

    return {
        "address_line_1": lines[0],
        "address_line_2": lines[1],
        "address_line_3": lines[2]
    }


def distribute_parts(parts: List[str], num_lines: int) -> Dict[str, str]:
    """
    Distribute address parts across specified number of lines.
    """
    lines = ["", "", ""]

    if len(parts) == num_lines:
        # Perfect match - one part per line
        for i in range(num_lines):
            lines[i] = parts[i] if i < len(parts) else ""
    else:
        # Distribute parts as evenly as possible
        total_length = sum(len(part) for part in parts)
        target_length = total_length // num_lines

        current_line = 0
        current_length = 0

        for part in parts:
            if lines[current_line]:
                lines[current_line] += ", " + part
                current_length += len(part) + 2
            else:
                lines[current_line] = part
                current_length = len(part)

            # Move to next line if current is full enough
            if current_line < num_lines - 1:
                remaining_parts = parts[parts.index(part) + 1:]
                if remaining_parts and current_length >= target_length:
                    current_line += 1
                    current_length = 0

    return {
        "address_line_1": lines[0],
        "address_line_2": lines[1],
        "address_line_3": lines[2]
    }


@app.get("/")
def root():
    return {
        "message": "Address Line Splitter API",
        "endpoints": {
            "/split": "POST - Split address into 3 lines",
            "/docs": "Interactive API documentation"
        }
    }


@app.post("/split", response_model=AddressOutput)
def split_address(input_data: AddressInput):
    """
    Split a single address line into 3 equally distributed lines.
    """
    try:
        result = split_address_equally(input_data.address)
        return AddressOutput(
            address_line_1=result["address_line_1"],
            address_line_2=result["address_line_2"],
            address_line_3=result["address_line_3"],
            original_address=input_data.address
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Example usage and testing
if __name__ == "__main__":
    import uvicorn

    # Test examples
    test_addresses = [
        "123 Main Street, Apartment 4B, Springfield, IL 62701, United States",
        "Plot No. 45, Sector 12, Near City Mall, Gurgaon, Haryana 122001",
        "Flat 301, Krishna Towers, MG Road, Bangalore 560001",
        "123 Short St",
        "Building A, Floor 3, Office 302, Tech Park, Whitefield, Bangalore, Karnataka, India 560066"
    ]

    print("Testing address splitting:\n")
    for addr in test_addresses:
        result = split_address_equally(addr)
        print(f"Original: {addr}")
        print(f"Line 1: {result['address_line_1']}")
        print(f"Line 2: {result['address_line_2']}")
        print(f"Line 3: {result['address_line_3']}")
        print("-" * 50)

    # Run the API
    uvicorn.run(app, host="0.0.0.0", port=8000)