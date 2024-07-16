
class Human:


    def __init__(self, name, sex, age):
        self.name = name
        self.sex = sex
        self.age = age
        self.birthday = 2024-age

    def say_hi(self):
        print("Hi, my name is", self.name)

    def run(self):
        print("I am running")

    def job(self):
        if self.age > 18:
            print("I am a adult, i  can work")
        else:
            print("I am a child, i can't work")


class Tester(Human):
    def __init__(self, name, sex, age, tech):
        super().__init__(name, sex, age)
        self.tech = tech

    def skill(self):
        print("I can do", self.tech)

if __name__ == '__main__':
    human = Human("Tom", "male", 28)
    tester = Tester("Jom", "male", 18, 'python')
    print(human.name, human.sex, human.age, human.birthday)
    human.say_hi()
    human.run()
    human.job()
    print('###################')
    print(tester.name, tester.sex, tester.age, tester.birthday)
    tester.say_hi()
    tester.run()
    tester.job()
    tester.skill()