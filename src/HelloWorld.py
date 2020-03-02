# Basic HelloWorld Class to test the unittesting framework
class HelloWorld:
    name = ''

    def setName(self, user_name):
        self.name += 'Hello, ' 
        self.name += user_name

    def getHello(self):
        return self.name

# Execution of the class model for debugging purposes
if __name__ == '__main__':
    person = HelloWorld()
    person.setName('James')
    hello = person.getHello()
    print(hello)