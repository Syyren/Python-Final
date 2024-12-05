#you didn't see this one

def forg(exponent : int = 10):
    string = "<img src='https://media.tenor.com/tS4120QBuugAAAAj/frog-spin-frog.gif'></img>"
    for i in range(exponent):
        string += string
    return string