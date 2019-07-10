from SupportMethods.Shuffler import Shuffler

class testShuffler():

    def RunTest(self):
        lists:list = [[12, 44, 56, 45, 34, 3], 
                     ['lol', 'no', 'what', 'ey', 'damn', 'trust'], 
                     [0.12, 2.4, 0.003, -0.167, -5.34, 3.0]]

        for index in range(len(lists)):
            print(lists[index])

        sler = Shuffler(lists)
        new_list = sler.ShuffleMultiList()
        sler.clear()

        for index in range(len(new_list)):
            print(new_list[index])



if __name__ == "__main__":
    testShuffler().RunTest()