from collections.abc import Callable


class GroupValidationError(Exception):
    pass

class Group[T]:
    def __init__(self, s: list[T], op: Callable[[T,T],T]):
        if not self.verify(s,op):
            raise(GroupValidationError)

        self.s = s
        self.op = op
        self.identity = self.findIdentity(s,op)

    @classmethod
    def findIdentity(cls, s: list[T], op: Callable[[T, T], T]) -> T:
        for element in s:
            if all(op(element, other) == other and op(other, element) == other for other in s):
                return element
        raise (ValueError)

    @classmethod
    def closureUnderIdentity(cls, s: list[T], op: Callable[[T, T], T]) -> bool:
        try:
            cls.findIdentity(s,op)
            return True
        except ValueError:
            return False

    @classmethod
    def closureUnderOperation(cls, s: list[T], op: Callable[[T, T], T]) -> bool:
        return all(op(a,b) in s for a in s for b in s)

    @classmethod
    def isAssociative(cls, s: list[T], op: Callable[[T,T], T]) -> bool:
        return all(op(op(a,b),c) == op(a,op(b,c))
                   for a in s
                   for b in s
                   for c in s)

    @classmethod
    def closureUnderInverses(cls, s: list[T], op: Callable[[T, T], T]) -> bool:
        try:
            identity = cls.findIdentity(s,op)
        except ValueError:
            return False

        return all(any(op(a,b) == identity and op(b,a) == identity for b in s) for a in s)

    @classmethod
    def verify(cls, s: list, op: Callable[[T, T], T]) -> bool:
        return (
            cls.closureUnderOperation(s, op)
            and cls.isAssociative(s, op)
            and cls.closureUnderIdentity(s, op)
            and cls.closureUnderInverses(s, op)
        )

try:
    group = Group([0,1,2,3], lambda x,y: (x+y) % 4)
except GroupValidationError:
    print("Couldn't make group from axioms")
