import sys
from typing import NamedTuple

from support import InputReader, asserter, timing


class Character(NamedTuple):
    hp: int
    dmg: int
    mp: int = 0


def parse(input: str) -> Character:
    return Character(*[int(x.split(": ")[1]) for x in input.strip().splitlines()])


class Game:
    def __init__(
        self, enemy_hp: int, enemy_dmg: int, player_hp: int, player_mp: int
    ) -> None:
        self.active_spells: list[int] = [0] * len(SPELLBOOK)
        self.used_spells: list[int] = []

        self.mana_cost = 0
        self.turn_id = 0
        self.enemy_hp = enemy_hp
        self.enemy_dmg = enemy_dmg
        self.player_hp = player_hp
        self.player_mp = player_mp
        self.player_armor: int = 0

    def __repr__(self):
        return (
            f"{self.turn_id} cost={self.mana_cost} hp={self.player_hp} "
            f"mp={self.player_mp} enemy_hp={self.enemy_hp}"
        )

    def next(self):
        n = Game(self.enemy_hp, self.enemy_dmg, self.player_hp, self.player_mp)
        n.active_spells = self.active_spells.copy()
        n.used_spells = self.used_spells.copy()
        n.mana_cost = self.mana_cost
        n.turn_id = self.turn_id + 1
        n.player_armor = self.player_armor
        return n


class Spell(NamedTuple):
    def name(self) -> str:
        return self.__class__.__name__


class MagicMissile(Spell):
    mp = 53
    dmg = 4
    max_turns = 0

    def cast(self, state: Game, **_) -> bool:
        state.enemy_hp -= self.dmg
        return False


class Drain(Spell):
    mp = 73
    dmg = 2
    max_turns = 0

    def cast(self, state: Game, **_) -> bool:
        state.enemy_hp -= self.dmg
        state.player_hp += 2
        return False


class Shield(Spell):
    mp = 113
    max_turns = 6

    def cast(self, state: Game, *, turn: int = 0) -> bool:
        if turn == self.max_turns:
            state.player_armor += 7
        elif turn == 1:
            state.player_armor -= 7
        return True


class Poison(Spell):
    mp = 173
    dmg = 3
    max_turns = 6

    def cast(self, state: Game, **_) -> bool:
        state.enemy_hp -= self.dmg
        return True


class Recharge(Spell):
    mp = 229
    max_turns = 5

    def cast(self, state: Game, **_) -> bool:
        state.player_mp += 101
        return True


SPELLBOOK = [MagicMissile(), Drain(), Shield(), Poison(), Recharge()]


def simulate(enemy: Character, player: Character, difficulty: int = 0) -> int:
    queue: list[Game] = [Game(enemy.hp, enemy.dmg, player.hp, player.mp)]
    best = sys.maxsize

    def player_turn(state: Game) -> list[Game]:
        cand = []

        state.player_hp -= difficulty

        for spell_id, spell in enumerate(SPELLBOOK):
            # is the next spell still active?
            if state.active_spells[spell_id] > 0:
                continue

            n = state.next()
            # player has enough mp?
            if n.player_mp < spell.mp:
                continue

            n.player_mp -= spell.mp
            n.mana_cost += spell.mp
            if best < n.mana_cost:
                continue

            if spell.max_turns == 0:
                # instant effect
                spell.cast(n)
            else:
                # cast lingering effect
                n.active_spells[spell_id] = spell.max_turns

            n.used_spells.append(spell_id)
            cand.append(n)
        return cand

    def enemy_turn(state: Game) -> Game:
        n = state.next()
        n.player_hp -= max(1, n.enemy_dmg - n.player_armor)
        return n

    def round_start(state: Game) -> None:
        for spell_id, turns_left in enumerate(state.active_spells):
            if turns_left > 0 and SPELLBOOK[spell_id].cast(state, turn=turns_left):
                state.active_spells[spell_id] -= 1

    while queue:
        state = queue.pop()

        if state.player_hp <= 0 or state.player_mp <= 20:
            continue

        round_start(state)

        if state.enemy_hp <= 0:
            best = min(state.mana_cost, best)
            continue

        if state.turn_id % 2 == 0:
            queue.extend(player_turn(state))
        else:
            queue.append(enemy_turn(state))

    return best


@asserter
def part1(enemy: Character, player: Character) -> int:
    return simulate(enemy, player)


@asserter
def part2(enemy: Character, player: Character) -> int:
    return simulate(enemy, player, 1)


@timing("day22")
def main() -> int:
    i = InputReader(2015, 22).raw

    p1 = Character(10, 0, 250)
    example1 = Character(13, 8, 0)
    example2 = Character(14, 8, 0)

    p2 = Character(50, 0, 500)
    puzzle = parse(i("puzzle"))

    def s1() -> None:
        assert part1(example1, p1)(226)
        assert part1(example2, p1)(641)
        assert part1(puzzle, p2)(1824)

    def s2() -> None:
        assert part2(puzzle, p2)(1937)

    match sys.argv:
        case [_, "1"]:
            s1()
        case [_, "2"]:
            s2()
        case _:
            s1()
            s2()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
