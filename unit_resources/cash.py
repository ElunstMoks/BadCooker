from typing import Self, Optional
import constraints

class Cash(int):
    def __new__(cls, value: int):
        """
        >>> Cash(40)
        Cash(40)
        """
        return super().__new__(cls, value)

    def __sub__(self, other) -> Self:
        """
        >>> cash = Cash(40)
        >>> cash
        Cash(40)

        >>> cash -= 20
        >>> cash
        Cash(20)

        >>> cash -= 30 # doctest: +ELLIPSIS
        Traceback (most recent call last):
        constraints.CashDefecit: ...

        >>> cash -= -10
        >>> cash
        Cash(30)
        """
        return self.spend(other, allow_debts=False)

    def spend(self, /, value: int, *, allow_debts: bool = False) -> Self:
        """
        reduces a player's cash
        allow_debts - if True disables the cash defecit constraint - player's cash now can be negative
        >>> cash = Cash(40)
        >>> cash
        Cash(40)

        >>> cash = cash.spend(20)
        >>> cash
        Cash(20)

        >>> cash.spend(30) # doctest: +ELLIPSIS
        Traceback (most recent call last):
        constraints.CashDefecit: ...

        >>> cash = cash.spend(30, allow_debts=True)
        >>> cash
        Cash(-10)

        >>> cash = cash.spend(-10)
        >>> cash
        Cash(0)
        """
        if value < 0:
            return self + -value
        if not allow_debts and super().__sub__(value) < 0:
            raise constraints.CashDefecit()
        return Cash(super().__sub__(value))

    def __add__(self, other: int) -> Self:
        """
        >>> cash = Cash(40)
        >>> cash
        Cash(40)

        >>> cash += 10
        >>> cash
        Cash(50)

        >>> cash += -20
        >>> cash
        Cash(30)
        """
        if other < 0:
            return self - -other
        return Cash(super().__add__(other))

    def __str__(self) -> str:
        """
        a string of player's cash for the game interface
        >>> print(Cash(40))
        [bold yellow]40[/] :coin:

        >>> print(Cash(-10))
        [bold magenta]-10[/] :coin:
        """
        color = "magenta" if self.debts else "yellow"
        return f"[bold {color}]{int(self)}[/] :coin:"

    def __repr__(self) -> str:
        """
        >>> Cash(40)
        Cash(40)
        """
        return f"{self.__class__.__name__}({super().__repr__()})"

    @property
    def debts(self) -> Optional[int]:
        if self >= 0:
            return None
        return -int(super().__repr__())

    def __int__(self) -> int:
        """
        integer representation of the cash
        >>> int(Cash(40))
        40
        """
        return int(super().__repr__())

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS | doctest.REPORT_ONLY_FIRST_FAILURE)
