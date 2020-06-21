"""Jest dana liczba 7 cyfrowa, jest parzysta, nie dzieli sie przez 7, zadna cyfra nie powtarza sie dwa razy.
Ile jest takich liczb"""


def how_many():
    list_value = []
    count = 0
    for i in range(1234567, 6543211): # range nie zawiera ostatniej liczby, wiec dodajemy o +1
        if i % 2 == 0 and i % 7 != 0 and len(set(str(i))) == len(str(i)):
            list_value.append(i)
            count += 1

    for i in list_value:
        print(i)

    print(count)
    
how_many()
