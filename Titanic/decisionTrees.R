setwd("C:/Users/anilkag/Desktop/personalWork/Machine Learning/Competitions/Titanic")

library(rpart)
library(rattle)
library(rpart.plot)
library(RColorBrewer)

data = read.csv("train.csv", header=TRUE)							# read the raw data
data = subset(data, select = c(2,3,5,6,7,8,10,12))					# only select the cols required 
data$Age[is.na(data$Age)] = mean(data$Age, na.rm=TRUE)				# fill the missing values
data$Fare[is.na(data$Fare)] = mean(data$Fare, na.rm=TRUE)

train = data[1:891,  ]

model = rpart(Survived ~., data=train, method='class')	# train the logistic regression model
plot(model)
fancyRpartPlot(model)
summary(model)														# summary of the model (properties of different cols wrt decision)

actualTest = read.csv("test.csv", header=TRUE)
actualTest = subset(actualTest , select = c(1,2,4,5,6,7,9,11))
actualTest$Age[is.na(actualTest$Age)] = mean(actualTest$Age, na.rm=TRUE)
actualTest$Fare[is.na(actualTest$Fare)] = mean(actualTest$Fare, na.rm=TRUE)

results = predict(model, newdata=actualTest, type="class")
output =  data.frame(PassengerId = actualTest$PassengerId, Survived = results)
write.csv(output, "decisionTreeOuptut.csv", row.names=FALSE)
