
# Homework Assignment 3 - String Encoding

## Overview
In this assignment, we expand Python's default string functionality by implementing a custom `String` class. This class retains the basic capabilities of the default Python string class while introducing advanced encoding and decoding features. Due to copyright constraints, no built-in libraries are used.

---

## Tasks
1. Implement a `String` class with behaviors similar to the Python `str` type:
   - Slicing, indexing, comparison, concatenation, repetition, iteration, length calculation, and methods like `count`, `isupper`, and `islower`.
2. Add custom exceptions:
   - `Base64DecodeError`
   - `CyclicCharsError`
   - `CyclicCharsDecodeError`
   - `BytePairError`
   - `BytePairDecodeError`
3. Implement encoding and decoding methods:
   - **Base64 Encoding and Decoding**.
   - **Cyclic Chars Encoding and Decoding**.
   - **Cyclic Bits Encoding and Decoding**.
   - **Byte Pair Encoding and Decoding**.
4. Add a histogram feature to count character categories.
5. Maintain a `rules` property for byte pair encoding.

---

## Code Files

### `String.py`
Defines the `String` class with the following functionalities:
1. **Basic String Operations**: Replicates essential behaviors of Python strings.
2. **Base64 Encoding and Decoding**:
   - Encodes strings using Base64 without padding (`=`).
   - Decodes Base64 strings back to their original form.
   - Example:
     ```python
     h = String("Hello World")
     h_base64 = h.base64()
     print(h_base64)  # Output: SGVsbG8gV29ybGQ
     print(h_base64.decode_base64())  # Output: Hello World
     ```
3. **Cyclic Chars Encoding and Decoding**:
   - Shifts characters cyclically within the printable ASCII range.
   - Raises `CyclicCharsError` for invalid strings.
4. **Cyclic Bits Encoding and Decoding**:
   - Performs circular bitwise shifts on the string's binary representation.
5. **Byte Pair Encoding and Decoding**:
   - Replaces frequent character pairs with unused characters based on priority groups.
   - Tracks replacements in the `rules` property.
   - Decoding reverses the process.
   - Example:
     ```python
     s = String("aaabdaaabac")
     encoded = s.byte_pair_encoding()
     print(encoded.val)  # Encoded string
     print(encoded.rules)  # Encoding rules
     print(encoded.decode_byte_pair().val)  # Decoded back to original
     ```
6. **Character Histogram**:
   - Counts characters across predefined categories (e.g., digits, uppercase, control codes).

---

## Implementation Notes
- All methods and properties adhere to the structure provided in the assignment description.
- No external libraries are used.
- Encoded outputs are validated against standard references where applicable.

---

## Example Testing

### Base64 Encoding and Decoding
```python
h = String("Hello World")
h_base64 = h.base64()
assert h_base64.val == "SGVsbG8gV29ybGQ"
assert h_base64.decode_base64().val == "Hello World"
```

### Cyclic Chars Encoding and Decoding
```python
s = String("Hello World")
cyclic_encoded = s.cyclic_chars(15)
cyclic_decoded = cyclic_encoded.decode_cyclic_chars(15)
assert cyclic_decoded.val == "Hello World"
```

### Byte Pair Encoding
```python
s = String("aaabdaaabac")
encoded = s.byte_pair_encoding()
print(encoded.val)  # Encoded string
print(encoded.rules)  # Encoding rules
assert encoded.decode_byte_pair().val == "aaabdaaabac"
```

### Histogram
```python
s = String("Hello123")
histogram = s.histogram_of_chars()
print(histogram)
```

---

## Submission Instructions
- Ensure your code is implemented in a single file named `String.py`.
- Avoid using any `import` statements.
- Test your implementation thoroughly to prevent runtime errors.

---

## Additional Tips
- Use the `rules` property for byte pair encoding and decoding.
- Follow the assignment's prototypes to avoid deductions.
- Validate results against references provided in the assignment description.

---

