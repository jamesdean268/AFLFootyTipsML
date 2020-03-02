import unittest

# Class to test
from src.HelloWorld import HelloWorld

class HelloWorld_Test(unittest.TestCase):
    """
    The basic class that inherits unittest.TestCase
    """
    def test_SetName_NameIsSet_EqualsHelloName(self):
        # Arrange
        person = HelloWorld()
        # Act
        person.setName('James') 
        # Assert
        self.assertEqual('Hello, James', person.name)

    def test_GetName_NameIsSetAndReturned_EqualsHelloName(self):
        # Arrange
        person = HelloWorld()
        # Act
        person.setName('James') 
        hello = person.getHello()
        # Assert
        self.assertEqual('Hello, James', hello)

