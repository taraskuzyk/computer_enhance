from dataclasses import dataclass
from pathlib import Path

OP_CODES = {0b100010: "mov"}

REGISTERS = {
    0b0000: "AL",
    0b0001: "CL",
    0b0010: "DL",
    0b0011: "BL",
    0b0100: "AH",
    0b0101: "CH",
    0b0110: "DH",
    0b0111: "BH",
    0b1000: "AX",
    0b1001: "CX",
    0b1010: "DX",
    0b1011: "BX",
    0b1100: "SP",
    0b1101: "BP",
    0b1110: "SI",
    0b1111: "DI",
}


@dataclass
class DisassembledInstruction:
    mnemonic: str
    reg1: str
    reg2: str

    def __str__(self) -> str:
        return f"{self.mnemonic} {self.reg1}, {self.reg2}".lower()


@dataclass
class AssembledInstruction:
    op_code: int
    d: int
    w: int
    mod: int
    reg: int
    r_m: int

    def disassemble(self) -> DisassembledInstruction:
        return DisassembledInstruction(
            mnemonic=OP_CODES[self.op_code],
            reg1=REGISTERS[self.r_m + self.w * 8],
            reg2=REGISTERS[self.reg + self.w * 8],
        )


def get_bytes(file: Path) -> list[bytes]:
    with open(file, "rb") as file:
        lines = file.readlines()

    return lines


def get_instructions(binary: bytes) -> list[AssembledInstruction]:
    instructions_binary = [
        binary[index : index + 2] for index in range(0, len(binary), 2)
    ]
    return [
        AssembledInstruction(
            op_code=take(binary[0], 8, 2),
            d=take(binary[0], 2, 1),
            w=take(binary[0], 1, 0),
            mod=take(binary[1], 8, 6),
            reg=take(binary[1], 6, 3),
            r_m=take(binary[1], 3, 0),
        )
        for binary in instructions_binary
    ]


def take(byte: int, s: int, e: int) -> int:
    return byte >> e & (255 << (s - e) ^ 255)


if __name__ == "__main__":
    file_bytes = get_bytes(Path("listing_0038_many_register_mov"))
    instructions = get_instructions(file_bytes[0])
    disassembled_file_string = "\n".join(
        [str(instruction.disassemble()) for instruction in instructions]
    )
    print(disassembled_file_string)
