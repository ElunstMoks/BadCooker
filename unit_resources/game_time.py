from typing import Self
import constraints

class GameTime(int):
    DAILY_TIME = 1000

    def __new__(cls, *args, **kwargs):
        """
        >>> repr(GameTime(120))
        GameTime(120)

        >>> GameTime(2000)
        Traceback (most recent call last):
        TypeError: GameTime(2000) not in valid range

        >>> GameTime(-800)
        Traceback (most recent call last):
        TypeError: GameTime(-800) not in valid range
        """
        new = cls(*args, **kwargs)
        if new not in range(cls.DAILY_TIME // -2, cls.DAILY_TIME):
            raise TypeError(f"{new!r} not in valid range")
        return new

    def __add__(self, other: int) -> Self:
        """
        adds extra time to a player's current game day

        >>> game_time = GameTime(120)
        >>> game_time += 170
        >>> repr(game_time)
        GameTime(290)
        >>> game_time += 800
        >>> repr(game_time)
        GameTime(1000)
        >>> game_time += -150
        >>> repr(game_time)
        GameTime(850)
        """
        if other < 0:
            return self - -other
        return min(super().__add__(other), GameTime.DAILY_TIME)

    def __sub__(self, other: int) -> Self:
        """
        reduces time of a player's game day

        >>> game_time = GameTime(100)
        >>> game_time -= 120
        >>> repr(game_time)
        GameTime(-20)
        >>> game_time -= 600
        Traceback (most recent call last):
        constraints.TimeDefecit: it's brings you to unallowed tiedness level
        >>> game_time -= -60
        >>> repr(game_time)
        GameTime(40)
        """
        if other < 0:
            return self + other
        if self + GameTime.DAILY_TIME // 2 < other:
            raise constraints.TimeDefecit()
        return super().__sub__(other)

    def __mul__(self, other) -> Self:
        return NotImplemented

    def __divmod__(self, other) -> Self:
        return NotImplemented

    def __str__(self) -> str:
        """
        a string displaying a current game time for the game interface

        >>> GameTime(120)
        120 🕗
        """
        color = "magenta" if self.with_tiedness else "black"
        return f"[bold {color}]{super().__str__()}[/] :clock:"

    def __repr__(self) -> str:
        """
        >>> repr(GameTime(120))
        GameTime(120)
        """
        return f"{self.__class__.__name__}({super().__str__()})"

    @property
    def with_tiedness(self) -> bool:
        """
        checks where's a player is 'tied', tiedness is represented as a negative game time

        >>> GameTime(120).with_tiedness
        False
        >>> GameTime(0).with_tiedness
        False
        >>> GameTime(-80).with_tiedness
        True
        """
        return self <= 0
