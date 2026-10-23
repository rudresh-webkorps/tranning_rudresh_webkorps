class dog :
    speies ="canine"
    def __init__(self, name:str , age:float)->None:
        self.name = name
        self.age = age

    def bark(self):
        return f"{self.name} is barking"
d=dog("tommy", 3)
b=dog("buddy", 3)
# print (d . bark())
# print (d.speies)
# print (b.speies)

# now we will learn about types of class methord 
# 1. instance methord
# 2. class methord
# 3. static methord

class animal:

    animal_type = "mammal" # this is a class variable
    def __init__(self, name:str , breed:str)->None:
        self.name= name
        self.breed=breed
    #@instancemethord
    def speak(self):  # here in the inctance methord we uses self keyword to access the instance variable
        print(f"{self.name} barks")

    @classmethod 
    def set_info(cls, txt:str): #alternate intializer for the class methord we can use the class methord to create a new instance of the class
        name , breed = txt.split(",") #using cls in the class methord we can access the class variable and also we can create a new instance of the class using the class methord
        return cls(name, breed) # here we are returning the class object

    @staticmethod
    def info(): # in the static methord we can not access the instance variable and class variable but we can use it to perform some operation
        print("this is a static methord")

e= animal.set_info ("tommy, labrador") # here we are creating a new instance of the class using the class methord
#e.speak() # here we are calling the instance methord using the instance of the class
#e.info() # here we are calling the static methord using the instance of the class
#print(e.animal_type) # here we are accessing the class variable using the instance of the class


#encapusulation is the process of hiding the implementation details of a class and only exposing the necessary methods and properties to the outside world. 
# In python we can achieve encapsulation by using private variables and methods. 
# In python we can make a variable or method private by adding a double underscore before the variable or method name.

#we use the private protected and public in the inheritance

class car:
    def __init__(self, name:str, model:str)->None:
        self.name = name  #public
        self._model = model  #protected
        self.__speed = 0  # pribvter
         # this is a private variable but with the name mangaling each private 
       # variable is prefixed with _classname__variablename so in this case it will be _car__speed

#now its time to know, inheritance is the process of creating a new class from an existing class. 
# The new class is called the derived class and the existing class is called the base class. 
# The derived class inherits all the properties and methods of the base class. 
# In python we can achieve inheritance by passing the base class as a parameter to the derived class.

class cars:
    def __init__(self, name:str, model:str)->None:
        self.name = name
        self.model = model

    def start(self):
        print(f"{self.name} is starting")_optp

class maruti:
    def __init__(self, name:str, model:str)->None:
        self.name = name
        self.model = model

    def start(self):
        print(f"{self.name} is starting")

class honda():
    def __init__(self, name:str, model:str)->None:
        self.name = name
        self.model = model

    def start(self):
        print(f"{self.name} is starting")