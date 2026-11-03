from collections.abc import Callable

from fieldfit import Group, GroupValidationError


class FieldValidationError(Exception):
    pass

class Field[T]:
    def __init__(self, s: list[T], 
                 add_op: Callable[[T,T],T],
                 mul_op: Callable[[T,T],T]):
        if not self.verify(s,add_op,mul_op):
            raise FieldValidationError
        self.s = s
        self.add_op = add_op
        self.mul_op = mul_op

        self.zero = Group.findIdentity(s, add_op)
        self.nontrivials = [x for x in s if x != self.zero]
        self.one = Group.findIdentity(self.nontrivials, mul_op)

    @classmethod
    def isCommutative(cls, s: list[T], 
                      add_op: Callable[[T, T], T],
                      mul_op: Callable[[T,T ], T]):
        return all(mul_op(a,b) == mul_op(b,a) 
                   for a in s 
                   for b in s)


    @classmethod
    def isDistributive(cls, s: list[T], 
                       add_op: Callable[[T,T],T],
                       mul_op: Callable[[T,T],T]):
        return all(mul_op(add_op(a,b),c) == add_op(mul_op(a,c),mul_op(b,c)) 
                   for a in s 
                   for b in s 
                   for c in s)

    @classmethod
    def verify(cls, s: list[T],
               add_op: Callable[[T, T], T],
               mul_op: Callable[[T, T], T]):
        if not (Group.verify(s,add_op) 
                and cls.isCommutative(s,add_op,mul_op) 
                and cls.isDistributive(s,add_op, mul_op)):
            return False

        try:
            zero = Group.findIdentity(s, add_op)
        except GroupValidationError:
            return False

        nontrivials = [x for x in s if x != zero]

        if not nontrivials:
            return False

        if not (Group.verify(nontrivials, mul_op) 
                and cls.isCommutative(nontrivials, add_op, mul_op)):
            return False

        try:
            one = Group.findIdentity(nontrivials,mul_op)
            return zero != one
        except FieldValidationError:
            return False
        