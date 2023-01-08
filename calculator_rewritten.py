#########################################
# Calculator
###############
# The calculator has the options: +; -; *; /; ( )
#
#
#########################################

class Calculator:
    def __init__(self):
        """
        set available_operations and constants
        """
        self._constants = {
            "e": 2.718281828459045,
            "pi": 3.141592653589793,
            # "j": 1j,  # complex numbers are not a part of the calculator
        }
        self._operations = {
            # "__" marks a place for a required number
            # order to execute, 1 is the highest priority (the same value is not allowed)
            # "operation" : (operation_structure, order_to_execute, function)
            "+": ("_+_", 42, self.addition),
            "-": ("_-_", 41, self.subtraction),
            "*": ("_*_", 33, self.multiplication),
            "/": ("_/_", 32, self.division),
            "^": ("_^_", 27, self.exponentiation),
            "%": ("_%_", 31, self.modulo),
            "!": ("_!", 26, self.factorial),
            "sqrt": ("sqrt_", 21, self.sqrt),
            "root": ("_root_", 22, self.root),
            "sin": ("sin_", 23, self.sinus),
            "cos": ("cos_", 24, self.cosinus),
            "tan": ("tan_", 25, self.tangent),
        }

    def e(self) -> float:
        """
        :return: e
        """
        return self._constants["e"]

    def pi(self) -> float:
        """
        :return: pi
        """
        return self._constants["pi"]

    def addition(self, summand_1: float, summand_2: float) -> float:
        """
        add two numbers
        :param summand_1:
        :param summand_2:
        :return: the sum of both numbers
        """
        return summand_1 + summand_2

    def subtraction(self, minuend: float, subtrahend: float) -> float:
        """
        subtract two numbers
        :param minuend:
        :param subtrahend:
        :return: the differenz of both numbers
        """
        return minuend - subtrahend

    def multiplication(self, multiplier: float, multiplicand: float) -> float:
        """
        multiplicate number one with number two
        :param multiplier:
        :param multiplicand:
        :return: the product of both numbers
        """
        return multiplier * multiplicand

    def division(self, divident: float, divisor: float) -> float:
        """
        divide
        :param divident:
        :param divisor:
        :return: the quotient of both numbers
        """
        return divident / divisor

    def modulo(self, number_1: float, number_2: float) -> float:
        """
        number one mod number two
        :param number_1:
        :param number_2:
        :return: the modulo of number_1 % number_2
        """
        return number_1 % number_2

    def exponentiation(self, base: float, exponent: int) -> float:
        """
        2^3 = 2 * 2 * 2
        :param base:
        :param exponent:
        :return: the exponentiation of number_1 with number_2
        """
        result = 1
        for number_counter in range(exponent):
            result *= base
        return result

    def factorial(self, number: int) -> float:
        """
        3! = 1 * 2 * 3
        :param number:
        :return: the factorial of number
        """
        result = 1
        for number_counter in range(1, abs(number) + 1):
            result *= number_counter
        if number < 0:
            return 1 / result
        return result

    def sqrt(self, radicand: float) -> float:
        """
        add two numbers
        :param radicand:
        :return: the square root of number
        """
        return self.root(2, radicand)

    def root(self, degree: int, radicand: float) -> float:
        """
        give the root of the radicand
        :param degree:
        :param radicand:
        :return:
        """
        raise NotImplementedError("The function 'root' is not implemented.")

    def sinus(self, angle: float) -> float:
        """

        :param angle:
        :return:
        """
        angle = angle % (2 * self.pi())
        result = 0
        for n in range(10):
            result += self.exponentiation(-1, n) * self.exponentiation(angle, 2*n + 1) / self.factorial(2*n + 1)
        return result

    def cosinus(self, angle: float) -> float:
        """

        :param angle:
        :return:
        """
        return self.sinus(angle + (1/2 * self.pi()))

    def tangent(self, angle: float) -> float:
        """

        :param angle:
        :return:
        """
        return self.sinus(angle) / self.cosinus(angle)

    def calculate(self, term: str) -> float:
        """
        parse a term and calculate
        :param term: a string with a valid term
        :return: give the result as float
        """
        # fetch a not valid term
        if type(term) is not str:
            raise ValueError("The term have to be a string")

        # split term into smaller ones, with parenthesis
        open_par_count = 0  # counts how many parenthesis are currently open
        open_par_position = [0, 0]  # saves the position of the outermost parenthesis
        term = term.replace(" ", "")
        for index in range(len(term)):
            if term[index] == "(":
                open_par_count += 1
                # mark, where the outermost parenthesis is open
                if open_par_count == 1:
                    open_par_position[0] = index
            elif term[index] == ")":
                open_par_count -= 1
                # mark, where the outermost parenthesis is closed
                if open_par_count == 0:
                    open_par_position[1] = index
                    # calculate the parenthesis and replace it
                    return self.calculate(
                        term[:open_par_position[0]] +
                        str(self.calculate(term[(open_par_position[0]+1):open_par_position[1]])) +
                        term[(open_par_position[1]+1):]
                    )
        # no parenthesis in this term:

        term = term.replace("+-", "-").replace("--", "+")

        # get all different operations
        operations = []  # [(order, "operation")]
        for operation, structure_order_and_func in self._operations.items():
            operations.append((structure_order_and_func[1], operation))
        def sort_order(order_operation: tuple[int, str]) -> int:
            return order_operation[0]
        operations.sort(key=sort_order)
        for index, operation in enumerate(operations):
            operations[index] = operation[1]

        # split the term at all operations
        term_splitted = [0, "+",]
        buffer_term_char = ""
        negative_number = False
        for index, term_char in enumerate(term):
            if term_char.isnumeric():
                term_int = int(term_char)
                if type(term_splitted[-1]) is int:
                    term_splitted[-1] = term_splitted[-1] * 10 + term_int
                elif type(term_splitted[-1]) is float:
                    term_splitted[-1] = term_splitted[-1] + term_int / 10
                else:
                    term_splitted.append(term_int)
                if term_splitted[-1] != 0 and negative_number:
                    term_splitted[-1] = -term_splitted[-1]
                    negative_number = False
                continue

            elif term_char in (".",):
                if type(term_splitted[-1]) is int:
                    term_splitted[-1] = float(term_splitted[-1])
                elif type(term_splitted[-1]) is float:
                    raise ValueError("Can't create a number with two decimal dots")
                else:
                    term_splitted.append(0.0)
                continue

            elif term_char == "-" and type(term_splitted[-1]) not in (int, float):
                negative_number = True
                continue

            buffer_term_char += term_char
            if buffer_term_char in operations:  # here might be a problem when sinh would be used
                term_splitted.append(buffer_term_char)
                buffer_term_char = ""
            elif buffer_term_char in self._constants.keys():
                term_splitted.append(self._constants[buffer_term_char])
                buffer_term_char = ""
        if buffer_term_char != "":
            raise ValueError(f"This is not an valid operation '{buffer_term_char}'.")

        # execute the operations in order
        for operation in operations:
            while operation in term_splitted:
                # print(term_splitted)  # for finding errors
                # print("operation: " + operation)
                for index, term_piece in enumerate(term_splitted):
                    if term_piece == operation:
                        operation_structure = self._operations[operation][0]
                        numbers = []
                        if operation_structure.startswith("_"):
                            number = term_splitted[index-1]
                            if type(number) is float:
                                if number.is_integer():
                                    number = int(number)
                            elif type(number) is int:
                                pass
                            else:
                                raise ValueError(f"The operation {operation} have no enough values")
                            numbers.append(number)
                        if operation_structure.endswith("_"):
                            number = term_splitted[index+1]
                            if type(number) is float:
                                if number.is_integer():
                                    number = int(number)
                            elif type(number) is int:
                                pass
                            else:
                                raise ValueError(f"The operation {operation} have no enough values")
                            numbers.append(number)
                        term_splitted[index] = self._operations[operation][2](*numbers)
                        if operation_structure.endswith("_"):
                            term_splitted.pop(index+1)
                        if operation_structure.startswith("_"):
                            term_splitted.pop(index-1)
                        break

        return term_splitted[0]


if __name__ == "__main__":
    calculator = Calculator()
    input_calc = ""
    while input_calc not in ("exit", "quit"):
        input_calc = input("=")
        if input_calc in ("", "exit", "quit"):
            continue
        try:
            print(calculator.calculate(input_calc))
        except ValueError as error:
            print("invalid term\n" + str(error))
