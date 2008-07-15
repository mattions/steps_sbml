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