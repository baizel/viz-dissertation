import os
import string


class PseudoAlgorithm:
    def __init__(self, fileName: string):
        self.__file = fileName
        self.__jsonAlgo = self.__read(fileName)

    def __read(self, fileName) -> dict:
        """
        Function to split Pseudo algorithm from txt file to a json object
        """

        returnData = {"lines": []}
        baseDir = os.path.dirname(os.path.realpath(__file__))
        fileReader = open(os.path.join(baseDir + "/txt/", fileName), encoding="utf8")
        for line in fileReader:
            result = line.split("//")
            lineData = {"line": self.remWhiteSpaceAtEnd(result[0].strip("\n")) + " <span class=data></span>" + "\n"}
            if len(result) > 1:
                lineData["exp"] = result[1]
            returnData['lines'].append(lineData)
        return returnData

    def remWhiteSpaceAtEnd(self, txt):
        if len(txt) != 0:
            split = 0
            for i in range(len(txt) - 1, 0, -1):
                split = i
                if txt[i] != " ":
                    break
            return txt[0:split + 1]
        return txt

    def getJsonAlgo(self):
        return self.__jsonAlgo
