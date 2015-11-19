#Begin class Variable
class Variable:
    def __init__(self, Name='0', Type=int, Address='0', Dimension='0'):
        self.Name = Name
        self.Type = Type
        self.Address = Address
        self.Dimension = Dimension

    def __str__(self):
        return "{}\t{}\t{}\t{}".format(str(self.Name), str(self.Type), str(self.Address), str(self.Dimension))
#End class Variable

from quadrupleGenerator import quadruple

#Begin class procedureDirectory
class procedureDirectory:
    constants = {}     #stores the value of constants

    def __init__(self, identifier, parent=None):
        self.identifier = identifier    #directory identifier
        self.parent = parent    #pointer to the directory's parent
        self.parameters = []    #current directory's parameter table
        self.variables = {}     #current directory's variable table
        self.directories = {}   #current directory's children
        self.Type = None
        self.startAddress = 0

        #Note: works with preincrement, so variables start one index below specification
        if parent:
            self.nextIntVarAddress = 9999           #10,000 - 10,999
            self.nextDoubleVarAddress = 10999       #11,000 - 11,999
            self.nextStringVarAddress = 11999       #12,000 - 12,999
            self.nextIntTempAddress = 12999         #13,000 - 13,999
            self.nextDoubleTempAddress = 13999      #14,000 - 14,999
            self.nextStringTempAddress = 14999      #15,000 - 15,999
            self.nextBoolTempAddress = 15999        #16,000 - 16,999

        else:
            self.nextIntVarAddress = 2999           #3,000 - 3,999
            self.nextDoubleVarAddress = 3999        #4,000 - 4,999
            self.nextStringVarAddress = 4999        #5,000 - 5,999

            self.nextIntTempAddress = 5999          #6,000 - 6,999
            self.nextDoubleTempAddress = 6999       #7,000 - 7,999
            self.nextStringTempAddress = 7999       #8,000 - 8,999
            self.nextBoolTempAddress = 8999         #9,000 - 9,999

        #Note: zero-const is zero and all variables and constants are numbered with preincrement
        self.nextIntConst = -1                      #0 - 999
        self.nextDoubleConst = 999                  #1,000 - 1,999
        self.nextStringConst = 1999                 #2,000 - 2,999
        self.add_const(int, 0)


    def __str__(self):
        return self.to_string()

    def to_string(self,):
        string = str(self.identifier) + "{\n"

        if(self.variables):
            string = string + "variables:\n"
            for identifier in self.variables:
                string = string + str(self.variables[identifier])
                #Append the constant value to constant variables
                try:
                    string = string + " := " + str(procedureDirectory.constants[identifier])
                except KeyError:
                    # print ("warning: constant key error")
                    pass
                string = string + "\n"

        if(self.directories):
            string = string + "\ndirectories:\n"
            for identifier in self.directories:
                string = string + str(self.directories[identifier])
        string = string + "}\n\n"

        string = string + "Starting Address: " + str(self.startAddress) + "\n\n"
        return string

    def getReturnVariable(self):
        return Variable("retVar", self.Type, 17000)

    def get_variable(self, identifier):
        currDir = self
        while currDir:
            if identifier in currDir.variables:
                return currDir.variables[identifier]
            currDir = currDir.parent
        return None

    def add_variable(self, identifier, variableType, variableDimensions, variableClass = "variable"):
        if identifier in self.variables:
            print ("Error! Variable \"{}\" already exists in current scope as \"{}\"!".format(str(identifier), str(self.variables[identifier])))
            return False
        else:
            self.variables[identifier] = Variable(identifier, variableType, self.next_address(variableClass, variableType), variableDimensions)
            if(variableDimensions):
                if variableType is int:
                    self.nextIntVarAddress += variableDimensions - 1
                elif variableType is float:
                    self.nextDoubleVarAddress += variableDimensions - 1
                elif variableType is str:
                    self.nextStringVarAddress += variableDimensions - 1

            return True

    def add_temp(self, variableType):
        variableClass = "temporal"
        if variableType is int:
            identifier = "T{}".format(self.nextIntTempAddress+1)
        elif variableType is float:
            identifier = "T{}".format(self.nextDoubleTempAddress+1)
        elif variableType is str:
            identifier = "T{}".format(self.nextStringTempAddress+1)
        elif variableType is bool:
            identifier = "T{}".format(self.nextBoolTempAddress+1)
        if self.add_variable(identifier, variableType, 0, variableClass):
            return self.get_variable(identifier)
        else:
            return False

    def add_const(self, variableType, variableValue):
        """ Adds a constant to the Procedure Directory.
        Constants are always added to the global Procedure Directory.

        Return: "Variable" referencing the constant value, or false if an error occurred.
        """
        variableClass = "constant"

        identifier = str(variableValue)
        #if the constant already exists, return
        if self.get_variable(identifier):
            return self.get_variable(identifier)

        #else:
        #find global directory
        currDir = self
        while currDir.parent:
            currDir = currDir.parent
        #currDir is now the global directory
        #add constant to the global directory
        if currDir.add_variable(identifier, variableType, 0, variableClass):
            procedureDirectory.constants[identifier] = variableValue
            return self.get_variable(identifier)


    def next_address(self, variableClass, variableType):
        if variableClass == "variable":
            if variableType is int:
                self.nextIntVarAddress += 1
                return self.nextIntVarAddress
            elif variableType is float:
                self.nextDoubleVarAddress += 1
                return self.nextDoubleVarAddress
            elif variableType is str:
                self.nextStringVarAddress += 1
                return self.nextStringVarAddress
        elif variableClass == "temporal":
            if variableType is int:
                self.nextIntTempAddress += 1
                return self.nextIntTempAddress
            elif variableType is float:
                self.nextDoubleTempAddress += 1
                return self.nextDoubleTempAddress
            elif variableType is str:
                self.nextStringTempAddress += 1
                return self.nextStringTempAddress
            elif variableType is bool:
                self.nextBoolTempAddress += 1
                return self.nextBoolTempAddress
        elif variableClass == "constant":
            if variableType is int:
                self.nextIntConst += 1
                return self.nextIntConst
            elif variableType is float:
                self.nextDoubleConst += 1
                return self.nextDoubleConst
            elif variableType is str:
                self.nextStringConst += 1
                return self.nextStringConst

    def rem_variable(self, identifier):
        if identifier in self.variables:
            del self.variables[identifier]
            return True
        else:
            return False

    def list_all_variables(self):
        currDirr = self
        string = ""
        while(currDirr):
            string = string + str(currDirr.identifier) + "{\n"
            if(currDirr.variables):
                for identifier in currDirr.variables:
                    string = string + str(currDirr.variables[identifier]) + "\n"
            string = string + "}\n"
            currDirr = currDirr.parent
        return string

    def get_all_variables(self):
        currDir = self
        allVariables = []
        for var in procedureDirectory.constants:
            if not var in allVariables:
                allVariables.append(var)
        return allVariables

    def get_directory(self, identifier):
        currDir = self
        while currDir:
            if identifier in currDir.directories:
                return currDir.directories[identifier]
            currDir = currDir.parent
        return None

    def add_directory(self, identifier):
        if identifier in self.directories:
            print ("Error! Directory \"{}\" already exists in scope: \"{}\"!".format(str(identifier), str(self.identifier)))
            return False
        else:
            self.directories[identifier] = procedureDirectory(identifier, self)
            return True

    def rem_directory(self, identifier):
        if identifier in self.directories:
            del self.directories[identifier]
            return True
        else:
            return False

    def getConstantDeclarations(self):
        constantDeclarations = []
        for var in self.get_all_variables():
            var = self.get_variable(var)
            if var.Address <= self.nextStringConst:
                constantDeclarations.append(quadruple("CNT", var, Variable(0), var))

        string = ""
        for const in constantDeclarations:
            const.printFormat = "Constants"
            string += '{}\n'.format(str(const))
        return string

#End class procedureDirectory

#Test routine
if __name__ == '__main__':
    glob = procedureDirectory("global");
    glob.add_variable("foo", int)
    glob.add_variable("bar", int)

    glob.add_directory("method 1")
    glob = glob.get_directory("method 1")
    glob.add_variable("var", str)
    glob.add_variable("foo", int)
    glob = glob.parent

    glob.add_directory("method 2")
    glob = glob.get_directory("method 2")
    glob.add_variable("var", float)
    glob.add_variable("bar", int)
    glob = glob.parent

    glob.add_directory("method 1")

    print (glob)
    print (glob.get_directory("method 1").list_all_variables())
    print (glob.get_directory("method 2").list_all_variables())
    print ('global foo is: ', glob.get_variable("foo"))
    print ('method 1 foo is: ',glob.get_directory("method 1").get_variable("foo"))
    print ('method 2 foo is: ', glob.get_directory("method 2").get_variable("foo"))
