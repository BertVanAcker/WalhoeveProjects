import datetime

class WTS():
    """
            Module: Class representing the Walhoeve training system
             :param string Name: Name of the Lab
             :param list Employees: Registered employees of the Walhoeve
        """

    def __init__(self, Name="",Employees=[],Trainings=[],currentBudget=0.0):
        self.Name=Name
        self.EmployeeList=Employees
        self.TrainingList = Trainings
        self.currentBudget = currentBudget


    def addTraining(self,t):
        self.TrainingList.append(t)




    #--------------- ANALYSIS FUNCTIONS -------------------
    def getOverallKPI(self,year):
        internalBudget=0
        externalBudget=0
        trainingCount = [0,0]
        trainingTime = 0
        trainingTimeMonth = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        for training in self.TrainingList:
            trainingTime += training.getTotalTime(year)
            trainingTimeMonth = self.add_Custom(trainingTimeMonth,training.getTimePerMonth(year))
            if training.Scope=="Internal":
                internalBudget+=training.Price
                trainingCount[0]+=1
            elif training.Scope=="External":
                externalBudget+=training.Price
                trainingCount[1] += 1

        budgetLeft = self.currentBudget - (internalBudget + externalBudget)


        return self.currentBudget,budgetLeft, internalBudget, externalBudget, trainingCount,trainingTime,trainingTimeMonth

    def getKPI_User(self, user,year):
        internalBudget = 0
        externalBudget = 0
        trainingCount = [0, 0]
        trainingTime = 0
        trainingTimeMonth = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        for training in self.TrainingList:
            if user in training.AttendList:
                trainingTime += training.getTotalTime(year)
                trainingTimeMonth = self.add_Custom(trainingTimeMonth, training.getTimePerMonth(year))
                if training.Scope == "Internal":
                    internalBudget += training.Price
                    trainingCount[0] += 1
                elif training.Scope == "External":
                    externalBudget += training.Price
                    trainingCount[1] += 1

        return internalBudget+externalBudget, trainingCount, trainingTime, trainingTimeMonth

    def getKPI_Function(self, function,year):
        internalBudget = 0
        externalBudget = 0
        trainingCount = [0, 0]
        trainingTime = 0
        trainingTimeMonth = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        userList = []
        _user = None
        # look for user
        for employee in self.EmployeeList:
            if function == employee.Role:
                userList.append(employee)

        for training in self.TrainingList:
            if len(userList)!=0:
                for user in userList:
                    if user.Name in training.AttendList:
                        trainingTime += training.getTotalTime(year)
                        trainingTimeMonth = self.add_Custom(trainingTimeMonth, training.getTimePerMonth(year))
                        if training.Scope == "Internal":
                            internalBudget += training.Price
                            trainingCount[0] += 1
                        elif training.Scope == "External":
                            externalBudget += training.Price
                            trainingCount[1] += 1

        return internalBudget+externalBudget, trainingCount, trainingTime, trainingTimeMonth

    def getTrainingKPIPerUser(self,user,year):
        totalTrainingsTime = 0
        totalTrainingsBudget = 0
        _user=None
        #look for user
        for employee in self.EmployeeList:
            if user == employee.Name:
                _user=employee
        #Look for all trainings where the user is envolved
        if _user is not None:
            for training in self.TrainingList:
                if _user.Name in training.AttendList:
                    #check the training year
                    yearList = training.getTrainingYear()
                    if len(yearList)==1 and year==yearList[0]:
                        #SINGLE YEAR
                        totalTrainingsTime+= sum(training.TimingList)
                        totalTrainingsBudget+=training.Price
                    else:
                        #MULTI-YEAR\
                        totalTrainingsBudget += training.Price
                        for i in range(0,len(training.DateList),1):
                            if training.getYear(training.DateList[i]) == year:
                                totalTrainingsTime += training.TimingList[i]

        return totalTrainingsTime,totalTrainingsBudget

    def getTrainingKPIPerFunction(self, function, year):
        totalTrainingsTime = 0
        totalTrainingsBudget = 0

        userList=[]
        _user = None
        # look for user
        for employee in self.EmployeeList:
            if function == employee.Role:
                userList.append(employee)
        # Look for all trainings where the user is envolved
        if len(userList)!=0:
            for _user in userList:
                for training in self.TrainingList:
                    if _user.Name in training.AttendList:
                        # check the training year
                        yearList = training.getTrainingYear()
                        if len(yearList) == 1 and year == yearList[0]:
                            # SINGLE YEAR
                            totalTrainingsTime += sum(training.TimingList)
                            totalTrainingsBudget += training.Price
                        else:
                            # MULTI-YEAR\
                            totalTrainingsBudget += training.Price
                            for i in range(0, len(training.DateList), 1):
                                if training.getYear(training.DateList[i]) == year:
                                    totalTrainingsTime += training.TimingList[i]

        return totalTrainingsTime, totalTrainingsBudget

    def add_Custom(self,previous,new):
        zipped_list = zip(previous, new)
        return [sum(item) for item in zipped_list]





class Training():
    """
            Module: Class representing a employee
             :param string Name: Name of the User
             :param string Role: Role of the User
        """

    def __init__(self, Name="", Price=0.0,Organization="",Location="",Dates=[],Times=[], Attendees=[],Scope="Internal"):
        self.Name = Name
        self.Price = Price
        self.Organization = Organization
        self.Location = Location
        self.DateList = Dates
        self.TimingList = Times
        self.AttendList = Attendees
        self.Scope = Scope

        self.DateListInterpreted = []

    def interpretDates(self):

        for date in self.DateList:
            dateSplitted = date.split("/")
            day = dateSplitted[0]
            month = dateSplitted[1]
            year = dateSplitted[2]
            self.DateListInterpreted.append(datetime.datetime(year, month, day))

    def getTrainingYear(self):
        yearList = []
        for date in self.DateList:
            dateSplitted = date.split("/")
            year = dateSplitted[2]
            if year not in yearList:
                yearList.append(year)

        return yearList

    def getYear(self,date):

        dateSplitted = date.split("/")
        year = dateSplitted[2]
        return year

    def getMonth(self,date):

        dateSplitted = date.split("/")
        month = dateSplitted[1]
        return month

    def getTotalTime(self,year):
        totalTime = 0
        for i in range(0,len(self.DateList),1):
            if self.getYear(self.DateList[i]) == year:
                totalTime+=self.TimingList[i]
        return totalTime

    def getTimePerMonth(self,year):
        yearList = []
        Months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
        for month in Months:
            totalTime = 0
            for i in range(0,len(self.DateList),1):
                if self.getMonth(self.DateList[i]) == month and self.getYear(self.DateList[i]) == year:
                    totalTime+=self.TimingList[i]
            yearList.append(totalTime)
        return yearList




class Employee():
    """
            Module: Class representing a employee
             :param string Name: Name of the User
             :param string Role: Role of the User
        """

    def __init__(self, Name="", Role="",Email=""):
        self.Name = Name
        self.Role = Role
        self.email = Email

