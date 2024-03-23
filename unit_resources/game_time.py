from typing import Self, Optional
import constraints

class GameTime(int):
    DAILY_TIME = 1000

    def __new__(cls, value: int):
        """
        >>> GameTime(120)
        GameTime(120)

        >>> GameTime(2000)
        Traceback (most recent call last):
        TypeError: GameTime(2000) not in valid range

        >>> GameTime(-800)
        Traceback (most recent call last):
        TypeError: GameTime(-800) not in valid range
        """
        if value not in range(cls.DAILY_TIME // -2, cls.DAILY_TIME + 1):
            raise TypeError(f"{cls.__name__}({value}) not in valid range")
        return super().__new__(cls, value)

    def __add__(self, other: int) -> Self:
        """
        adds extra time to a player's current game day
        >>> game_time = GameTime(120)
        >>> game_time += 170
        >>> game_time
        GameTime(290)

        >>> game_time += 800
        >>> game_time
        GameTime(1000)

        >>> game_time += -150
        >>> game_time
        GameTime(850)
        """
        if other < 0:
            return self - -other
        return GameTime(min(super().__add__(other), GameTime.DAILY_TIME))

    def __sub__(self, other: int) -> Self:
        """
        reduces time of a player's game day
        >>> game_time = GameTime(100)
        >>> game_time -= 120
        >>> game_time
        GameTime(-20)

        >>> game_time -= 600 # doctest: +ELLIPSIS
        Traceback (most recent call last):
        constraints.TimeDefecit: ...

        >>> game_time -= -60
        >>> game_time
        GameTime(40)
        """
        if other < 0:
            return self + -other
        if self + GameTime.DAILY_TIME // 2 < other:
            raise constraints.TimeDefecit()
        return GameTime(super().__sub__(other))

    def __mul__(self, other) -> Self:
        return NotImplemented

    def __divmod__(self, other) -> Self:
        return NotImplemented

    def __str__(self) -> str:
        """
        a string displaying a current game time for the game interface
        >>> print(GameTime(120))
        [bold black]120[/] :seven o'clock:

        >>> print(GameTime(-10))
        [bold magenta]10[/]
        """
        indicator = self.tiredness or int(self)
        color = "magenta" if self.tiredness else "black"
        emoji = "seven o'clock" if not self.tiredness else None
        return f"[bold {color}]{indicator}[/]" + (f" :{emoji}:" if emoji else "")

    def __repr__(self) -> str:
        """
        >>> GameTime(120)
        GameTime(120)
        """
        return f"{self.__class__.__name__}({super().__repr__()})"

    @property
    def tiredness(self) -> Optional[int]:
        """
        a factor of game time's way below zero
        >>> GameTime(120).tiredness

        >>> GameTime(-60).tiredness
        60
        """
        if self >= 0:
            return None
        return int(self.negate())

    def negate(self) -> Self:
        """
        returns an exact tiredness, if player's time is positive or an exact positive time if this game time
        is represented in tiredness
        >>> GameTime(120).negate()
        GameTime(-120)

        >>> GameTime(-40).negate()
        GameTime(40)

        >>> GameTime(600).negate() # doctest: +ELLIPSIS
        Traceback (most recent call last):
        constraints.TimeDefecit: ...
        """
        if self > GameTime.DAILY_TIME // 2:
            raise constraints.TimeDefecit()
        return GameTime(super().__mul__(-1))

    def __int__(self) -> int:
        """
        integer representation of this game time
        >>> int(GameTime(120))
        120
        """
        return int(super().__repr__())

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=False, optionflags=doctest.ELLIPSIS | doctest.REPORT_ONLY_FIRST_FAILURE)
