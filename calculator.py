#########################################
# Calculator
###############
# The calculator has the options: +; -; *; /; ( )
#
#
#########################################

class Calculator():

    def __init__(self):
        import math

        self._constants = {
            "e": math.e,
            "pi": math.pi,
            "j": 1j
            }
        self._operations = {
            "+": "",
            "-": "",
            "*": "",
            "/": "",
            "^": "",
            # "!": "",
            # "%": "",
            "sqrt()": "",
            # "root(;)": "",
            "sin()": "",
            "cos()": "",
            "tan()": ""
            }

    # @staticmethod
    def calc(self, term="1+1"):
        import math
        result = 0
        if type(term) is not str:
            return result
        openparcont = 0  # open "(" will count
        openparlist = [0, 0]  # list to calculate the sub term separate
        # term = "0+" + term + "+0"
        term = term.replace(" ", "")
        termcalc = term

        # Parenthesis ( ) searching and separating for sub terms
        for i in range(len(term)):
            if term[i] == "(":
                openparcont += 1
                # mark, where the first parenthesis was open
                if openparcont == 1:
                    openparlist[0] = i
            elif term[i] == ")":
                openparcont += -1
                # if the first parenthesis was closed
                if openparcont == 0:
                    openparlist[1] = i

                    # This Part should be better
                    termcalc = term[:openparlist[0]]
                    term_sub = Calculator()
                    # if there is a function
                    if term[(openparlist[0]-4):openparlist[0]] == "sqrt":
                        termcalc = termcalc[:-4]
                        termcalc += str(math.sqrt(term_sub.calc(term[openparlist[0] + 1:openparlist[1]])))
                    ###
                    # #elif term[(openparlist[0]-4):openparlist[0]] == "root":
                    # #    termcalc = termcalc[:-4]
                    # #    termsub = term[openparlist[0] + 1:openparlist[1]].split(";")
                    # #    if len(termsub) == 1 or termsub[1] == "":
                    # #        termsub.append("0")
                    # #    termcalc += str(math.pow(1 / term_sub.calc(termsub[1]), term_sub.calc(termsub[0])))
                    ###
                    elif term[(openparlist[0]-3):openparlist[0]] == "sin":
                        termcalc = termcalc[:-3]
                        termcalc += str(math.sin(term_sub.calc(term[openparlist[0] + 1:openparlist[1]])))
                    elif term[(openparlist[0]-3):openparlist[0]] == "cos":
                        termcalc = termcalc[:-3]
                        termcalc += str(math.cos(term_sub.calc(term[openparlist[0] + 1:openparlist[1]])))
                    elif term[(openparlist[0]-3):openparlist[0]] == "tan":
                        termcalc = termcalc[:-3]
                        termcalc += str(math.tan(term_sub.calc(term[openparlist[0] + 1:openparlist[1]])))
                    else:
                        termcalc += str(term_sub.calc(term[openparlist[0] + 1:openparlist[1]]))
                    termcalc += term[openparlist[1]+1:]

        # #print(term)

        term = termcalc
        term = term.replace("+-", "-")
        term = term.replace("--", "+")

        # Split for the Addition
        termadd = term.split("+")
        for add in range(len(termadd)):
            if termadd[add].startswith("-"):
                termadd[add] = "0" + termadd[add]

            # Split for the Subtraction and join the string for  3*-2
            termsub = termadd[add].split("-")
            termsub.append("0")
            for sub in range(len(termsub)):
                if termsub[sub].endswith(("*", "/", "^")):
                    # endswith(SuffixOrTuple)
                    termsub[sub+1] = termsub[sub] + "-" + termsub[sub+1]
                    # Here the number's signs are taken into account
                    termsub[sub] = "0"

                # Split for the Multiplication
                termmul = termsub[sub].split("*")
                for mul in range(len(termmul)):

                    # Split for the Subtraction
                    termdiv = termmul[mul].split("/")
                    for div in range(len(termdiv)):

                        # Split for the Power
                        termpow = termdiv[div].split("^")

                        # begin to calculate

                        # power
                        while len(termpow) > 1:
                            termpow[0] = str((float(termpow[0]) ** float(termpow[1])))
                            termpow.pop(1)
                        termdiv[div] = termpow[0]
                    # division
                    while len(termdiv) > 1:
                        termdiv[0] = str(float(termdiv[0]) / float(termdiv[1]))
                        termdiv.pop(1)
                    termmul[mul] = termdiv[0]
                # multiplication
                while len(termmul) > 1:
                    termmul[0] = str(float(termmul[0]) * float(termmul[1]))
                    termmul.pop(1)
                termsub[sub] = termmul[0]
            # subtraction
            while len(termsub) > 1:
                termsub[0] = str(float(termsub[0]) - float(termsub[1]))
                termsub.pop(1)
            termadd[add] = termsub[0]
        # addition
        while len(termadd) > 1:
            termadd[0] = str(float(termadd[0]) + float(termadd[1]))
            termadd.pop(1)
        result = float(termadd[0])

        return result

    def calc_hex(self, term):
        pass


if __name__ == "__main__":
    calculator = Calculator()
    input_calc = input("=")
    while input_calc not in ("exit", "quit"):
        # here may the term edit
        try:
            print(calculator.calc(input_calc))
        except ValueError:
            print("invalid term")
        input_calc = input("=")
