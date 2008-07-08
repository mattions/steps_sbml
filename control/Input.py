class Input(object):
    """
        Input we want to apply
    """
    def __init__(self, inputTimePoint, mol, quantity):
        self.__inputTimePoint = inputTimePoint
        self.__mol = mol
        self.__quantity = quantity

    def getInputTimePoint(self):
        return self.__inputTimePoint


    def getMol(self):
        return self.__mol


    def getQuantity(self):
        return self.__quantity


    def setInputTimePoint(self, value):
        self.__inputTimePoint = value


    def setMol(self, value):
        self.__mol = value


    def setQuantity(self, value):
        self.__quantity = value


    def delInputTimePoint(self):
        del self.__inputTimePoint


    def delMol(self):
        del self.__mol


    def delQuantity(self):
        del self.__quantity

    inputTimePoint = property(getInputTimePoint, setInputTimePoint, 
                              delInputTimePoint, "TimePoint of the Input")
    
    mol = property(getMol, setMol, delMol, "Mol")

    quantity = property(getQuantity, setQuantity, delQuantity, "Quantity")