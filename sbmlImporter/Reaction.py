"""
 * Copyright (C) 2008 Jul - Michele Mattioni:
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, 
 * Boston, MA  02110-1301  USA
"""

class Reaction(object):
    def __init__(self):
        self.__name = ""
        self.__reacts = []
        self.__lhs = []
        self.__prods = []
        self.__rhs = []
        self.__kName = ""
        self.__kValue = 0

    def getKName(self):
        return self.__kName


    def getKValue(self):
        return self.__kValue


    def setKName(self, value):
        self.__kName = value


    def setKValue(self, value):
        self.__kValue = value



    def getName(self):
        return self.__name


    def setName(self, value):
        self.__name = value


    def getLhs(self):
        return self.__lhs


    def getRhs(self):
        return self.__rhs


    def setLhs(self, value):
        self.__lhs = value


    def setRhs(self, value):
        self.__rhs = value


    def delLhs(self):
        del self.__lhs


    def delRhs(self):
        del self.__rhs

    def getReacts(self):
        return self.__reacts


    def getProds(self):
        return self.__prods

    def setReacts(self, value):
        self.__reacts = value


    def setProds(self, value):
        self.__prods = value


    def delReacts(self):
        del self.__reacts


    def delProds(self):
        del self.__prods

    reacts = property(getReacts, setReacts, delReacts, "The reactants of the reaction")

    prods = property(getProds, setProds, delProds, "The products of the reaction")

    lhs = property(getLhs, setLhs, delLhs, "Left side STEPS")

    rhs = property(getRhs, setRhs, delRhs, "Right side STEPS")

    name = property(getName, setName, None, "Unique name of the reaction")

    kName = property(getKName, setKName, None, "The name of the costant")

    kValue = property(getKValue, setKValue, None, "The Value of the costant")
        
    

        