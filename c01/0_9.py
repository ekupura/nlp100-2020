def main():
    # 00
    print("00:")
    print("stressed"[::-1])

    # 01
    print("01:")
    print("パタトクカシーー"[::2])

    # 02
    print("02:")
    print("".join([a + b for (a, b) in zip("パトカー", "タクシー")]))

    # 03
    print("03:")
    str03 = "Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."
    print([len(s) for s in str03.split(" ")])

    # 04
    print("04:")
    str04 = "Hi He Lied Because Boron Could Not Oxidize Fluorine. " \
            "New Nations Might Also Sign Peace Security Clause. Arthur King Can."
    single_list = [1, 5, 6, 7, 8, 9, 15, 16, 19]
    print([(s[0], str(i)) if i in single_list else (s[:2], str(i)) for i, s in enumerate(str04.split(" "), start=1)])

    # 05
    print("05:")
    str05 = "I am an NLPer"

    def generate_ngram(string, n=1, wordlevel=True):
        separated_string = string.split(" ") if wordlevel else [c for c in string]
        separator = ' ' if wordlevel else ''
        return [separator.join(separated_string[i:i+n]) for i in range(0, len(separated_string)-n+1)]
    print(generate_ngram(str05, n=2, wordlevel=True))
    print(generate_ngram(str05, n=2, wordlevel=False))

    # 06
    print("06:")
    set_x = set(generate_ngram("paraparaparadise", n=2, wordlevel=False))
    set_y = set(generate_ngram("paragraph", n=2, wordlevel=False))
    print(set_x | set_y)
    print(set_x & set_y)
    print(set_x - set_y)

    # 07
    print("07:")

    def func07(x, y, z):
        return "{}時の{}は{}".format(x, y, z)
    print(func07(12, "気温", 22.4))

    # 08
    print("08:")

    def cipher(string):
        return "".join([chr(219 - ord(c)) if c.islower() else c for c in string])
    print(cipher(str04))

    # 09
    print("09:")
    from random import sample
    str09 = "I couldn’t believe that I could actually understand what " \
            "I was reading : the phenomenal power of the human mind ."

    def func09(string):
        return " ".join([w[0] + "".join(sample(w[1:-1], len(w[1:-1]))) + w[-1] if len(w) > 4 else w
                         for w in string.split(" ")])
    print(func09(str09))

if __name__ == "__main__":
    main()