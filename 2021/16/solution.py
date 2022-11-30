import os
from typing import Any
from support import timing, check_result

CTBL = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def to_bit(input: str) -> str:
    return "".join([CTBL[a] for a in input.strip()])
    # f"{int(a, 16):04b}"


def read_file(filename: str) -> str:
    path = os.path.dirname(__file__) + "\\" + filename
    return open(path).read()


def to_dec(bin: str) -> int:
    return int(bin, 2)


def get_packets(hex: str):
    binary = to_bit(hex)

    def read_bits(i: int, length: int) -> tuple[int, str]:
        chunk = binary[i : i + length]
        i += length
        return i, chunk

    def read_bits_dec(i: int, length: int) -> tuple[int, int]:
        i, chunk = read_bits(i, length)
        return i, to_dec(chunk)

    def parse_packet(i: int) -> tuple[int, dict[str, Any]]:
        i, packet_version = read_bits_dec(i, 3)
        i, packet_type_id = read_bits_dec(i, 3)

        if packet_type_id == 4:
            bit_groups: list[str] = []
            while True:
                i, chunk = read_bits(i, 5)
                bit_groups.append(chunk[1:])
                if chunk[0] == "0":
                    break
            literal_value = to_dec("".join(bit_groups))
            return i, {
                "packet_version": packet_version,
                "packet_type_id": packet_type_id,
                "value": literal_value,
            }

        # every othewer is operatortype k
        else:
            i, length_type_id = read_bits(i, 1)
            length_type_id = int(length_type_id)
            if length_type_id == 0:
                i, packet_length = read_bits_dec(i, 15)
                j = i
                i = i + int(packet_length)
                packets: list[dict[str, Any]] = []
                while j < i:
                    j, packet = parse_packet(j)
                    packets.append(packet)

                return i, {
                    "packet_version": packet_version,
                    "packet_type_id": packet_type_id,
                    #  "length_type_id": length_type_id,
                    #  "packet_length": packet_length,
                    "packets": packets,
                }

            elif length_type_id == 1:
                i, subpacket_count = read_bits_dec(i, 11)
                subpacket_count = int(subpacket_count)
                subpackets = []
                for _ in range(subpacket_count):
                    i, packet = parse_packet(i)
                    subpackets.append(packet)

                return i, {
                    "packet_version": packet_version,
                    "packet_type_id": packet_type_id,
                    #  "length_type_id": length_type_id,
                    #  "subpacket_count": subpacket_count,
                    "packets": subpackets,
                }

        raise AssertionError()

    return parse_packet(0)[1]


def part1(hex: str) -> int:
    todo = [get_packets(hex)]
    total = 0
    while todo:
        packet = todo.pop()
        for k, v in packet.items():
            if k == "packet_version":
                total += int(v)
            elif k == "packets":
                todo.extend(v)

    return total


def multiplication(input: list[int]) -> int:
    total = 1
    for i in input:
        total *= i
    return total


op = {
    # type=
    0: sum,
    1: multiplication,
    2: min,
    3: max,
    5: lambda x: 1 if x[0] > x[1] else 0,
    6: lambda x: 1 if x[0] < x[1] else 0,
    7: lambda x: 1 if x[0] == x[1] else 0,
}


def part2(hex: str) -> int:
    def compute(packet) -> int:
        packet_id: int = packet["packet_type_id"]
        values: list[int] = []

        if packet_id != 4 and "packets" in packet:
            for literal_packet in packet["packets"]:
                if literal_packet["packet_type_id"] == 4:
                    val: int = literal_packet["value"]
                    values.append(val)
                else:
                    values.append(compute(literal_packet))
        else:
            for subpacket in packet["packets"]:
                values.append(compute(subpacket))

        if packet_id in op and len(values) > 0:
            val = op[packet_id](values)
            return val

        raise AssertionError()

    return compute(get_packets(hex))


@timing("total")
def main() -> int:
    puzzle = read_file("puzzle.input")

    check_result(6, part1("D2FE28"))
    check_result(9, part1("38006F45291200"))
    check_result(14, part1("EE00D40C823060"))
    check_result(16, part1("8A004A801A8002F478"))
    check_result(12, part1("620080001611562C8802118E34"))
    check_result(23, part1("C0015000016115A2E0802F182340"))
    check_result(31, part1("A0016C880162017C3686B18A3D4780"))
    check_result(852, part1(puzzle))

    check_result(3, part2("C200B40A82"))
    check_result(54, part2("04005AC33890"))
    check_result(7, part2("880086C3E88112"))
    check_result(9, part2("CE00C43D881120"))
    check_result(1, part2("D8005AC2A8F0"))
    check_result(0, part2("F600BC2D8F"))
    check_result(0, part2("9C005AC2F8F0"))
    check_result(1, part2("9C0141080250320F1802104A08"))
    check_result(19348959966392, part2(puzzle))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
