import abc
from typing import TypeAlias, Any
import time
import enum

class Computation:
    @abc.abstractmethod
    def solve(self, *args, **kwargs):
        pass

ResultDict: TypeAlias = dict[str, Any]


class QuadraticTypeEnum(enum.StrEnum):
    ONE_ROOT = 'one_root'
    TWO_ROOT = 'two_root'
    COMPLEX_ROOT = 'complex_roots'

class QuadraticComputation(Computation):
    def solve(self, a: float, b:float, c: float) -> ResultDict:
        start_time = time.time()
        result: ResultDict = {}

        roots = {}
        solve_type = QuadraticTypeEnum.COMPLEX_ROOT
        message = "Комплексные корни"

        D = b**2-4*a*c

        if D > 0:
            x1 = (-b + D**0.5) / (2*a)
            x2 = (-b - D**0.5) / (2*a)
            solve_type = QuadraticTypeEnum.TWO_ROOT
            result['message'] = 'Два корня'
            result['roots'] = [x1, x2]
        elif D == 0:
            solve_type = QuadraticTypeEnum.ONE_ROOT
            result['roots'] = [(-b) / (2*a)]
            result['message'] = 'Один корнь'
        else:
            real = -b / (2*a)
            imag = -D**0.5/(2*a)
            result['roots'] [f"{real}+{imag}i", f"{real}-{imag}i"]

        result = {
            'descrimenant': D,
            'type': solve_type,
            'time_ms': (time.time() - start_time) * 1000
        }
            
        return result


factory = {
    "quadratic": QuadraticComputation,
}

if __name__ == '__main__':
    calc_class = factory['quadratic']

    params = {
        "a": 2,
        "b": -4,
        "c": -6
    }
    result = calc_class().solve(**params)

    print(result)