import json
import os
import string


class Algorithm:
    def __init__(self, fileName: string):
        self.__file = fileName
        self.__jsonAlgo = self.__read(fileName)

    def __read(self, fileName) -> dict:
        """
        Function to split pesudo algorthim from txt file to a json object
        """

        d = {"lines": []}
        baseDir = os.path.dirname(os.path.realpath(__file__))
        o = open(os.path.join(baseDir + "/txt/", fileName))
        for line in o:
            res = line.split("//")
            data = {"line": self.remWhiteSpaceAtEnd(res[0].strip("\n")) + " <span class=data></span>" + "\n"}
            if len(res) > 1:
                data["exp"] = res[1]
            d['lines'].append(data)
        return d

    def remWhiteSpaceAtEnd(self, txt):
        if len(txt) != 0:
            split = 0
            for i in range(len(txt)-1,0,-1):
                split = i
                if txt[i] != " ":
                    break
            return txt[0:split+1]
        return txt

    def getJsonAlgo(self):
        return self.__jsonAlgo
