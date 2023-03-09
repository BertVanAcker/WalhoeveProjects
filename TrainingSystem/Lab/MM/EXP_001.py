from WTS.Metamodel.WTS_MM import *


#set the employees
Lies = Employee(Name="Lies Mingneau",Role="Coordinator",Email="lies.mingneau@dewalhoeve.be")
Wim = Employee(Name="Wimpie",Role="Director",Email="Wimpie@dewalhoeve.be")
Pieter= Employee(Name="Pieter Buffel",Role="Begeleider",Email="pieter.buffel@dewalhoeve.be")
Emma= Employee(Name="Emma Tata",Role="Begeleider",Email="Emma.tata@dewalhoeve.be")

#set the Walhoeve Training System
wts = WTS(Name="WTS",Employees=[Lies,Wim,Pieter,Emma],currentBudget=10000)



#add trainings
t1 = Training(Name="Training 1", Price=100.0,Organization="B.MKR",Location="Keiem",Dates=["17/05/2023","19/08/2023"],Times=[7.6,3.8],Attendees=["Pieter Buffel"])
t2 = Training(Name="Training 2", Price=1200.0,Organization="PILZ",Location="Antwerpen",Dates=["21/10/2023"],Times=[7.6],Attendees=["Pieter Buffel","Lies Mingneau","Wimpie"])
t3 = Training(Name="Training 3", Price=20.0,Organization="CAVA",Location="Keiem",Dates=["31/10/2023"],Times=[2],Attendees=["Lies Mingneau"])
t4 = Training(Name="Training 4", Price=2000.0,Organization="B.MKR",Location="Keiem",Dates=["17/05/2023","19/08/2024"],Times=[7.6,7.6],Attendees=["Lies Mingneau"])
t5 = Training(Name="Training 5", Price=20.0,Organization="CAVA",Location="Keiem",Dates=["4/09/2023"],Times=[2],Attendees=["Emma Tata"])
t6 = Training(Name="Training 6", Price=660.0,Organization="CAVA",Location="Keiem",Dates=["4/10/2023"],Times=[5],Attendees=["Emma Tata","Pieter Buffel"],Scope="External")
wts.addTraining(t1)
wts.addTraining(t2)
wts.addTraining(t3)
wts.addTraining(t4)
wts.addTraining(t5)
wts.addTraining(t6)



#----------EXPERIMENTATION------------
print(wts.getTrainingKPIPerUser("Lies Mingneau","2023"))
print(wts.getTrainingKPIPerUser("Pieter Buffel","2023"))
print(wts.getTrainingKPIPerUser("Wimpie","2023"))

print(wts.getTrainingKPIPerFunction("Begeleider","2023"))

print(wts.getOverallKPI(year="2023"))

print(wts.getKPI_User(user="Lies Mingneau",year="2023"))
print(wts.getKPI_User(user="Pieter Buffel",year="2023"))
print(wts.getKPI_User(user="Emma Tata",year="2023"))

print(wts.getKPI_Function(function="Begeleider",year="2023"))