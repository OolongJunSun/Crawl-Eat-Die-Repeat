from typing import Union

def hex_to_bin(gene) -> str:
        scale = 16  # equals to hexadecimal
        n_bits = 4
        return bin(int(gene, scale))[2:].zfill(len(gene) * n_bits)

def normalize(char: str) -> float:
    return float(int(char, 2) / 2 ** len(char))

def scale(
    norm_value: Union[int, float],
    MAX: Union[int, float],
    MIN: Union[int, float]
) -> float:
    return float(max(MIN, norm_value * MAX))