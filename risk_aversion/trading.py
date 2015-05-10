__author__ = 'shuxu'



class Trader:
    def __init__(self):
        pass



def main():
    data_array = list()
    response = open('../data/VIXCLS.csv')
    for line in response:
        data_array.append(line)

    for e in data_array:
        print e
    pass

if __name__ == "__main__":
    main()