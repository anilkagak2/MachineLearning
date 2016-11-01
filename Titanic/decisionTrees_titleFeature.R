setwd("C:/Users/anilkag/Desktop/personalWork/Machine Learning/Competitions/Titanic")

library(rpart)
library(rattle)
library(rpart.plot)
library(RColorBrewer)

data = read.csv("train.csv", header=TRUE)							# read the raw data
# add new feature
data$Name = as.character(data$Name)
data$Title <- sapply(data$Name, FUN=function(x) {strsplit(x, split='[,.]')[[1]][2]})
data$Title <- sub(' ', '', data$Title)
data$Title[data$Title %in% c('Mme', 'Mlle')] <- 'Mlle'
data$Title[data$Title %in% c('Capt', 'Don', 'Major', 'Sir')] <- 'Sir'
data$Title[data$Title %in% c('Dona', 'Lady', 'the Countess', 'Jonkheer')] <- 'Lady'
data$Title <- factor(data$Title)

data = subset(data, select = c(2,3,5,6,7,8,10,12))					# only select the cols required 

FareModel = rpart(Fare ~ Pclass + Sex + SibSp + Parch + Age + Embarked, data=data[!is.na(data$Fare), ], method="anova")
AgeModel = rpart(Age ~ Pclass + Sex + SibSp + Parch + Embarked + Title, data=data[!is.na(data$Age), ], method="anova")
data$Fare[is.na(data$Fare)] = predict(FareModel, data[is.na(data$Fare), ])
data$Age[is.na(data$Age)] = predict(AgeModel, data[is.na(data$Age), ])				# fill the missing values

train = data[1:891,  ]

#model = rpart(Survived ~ ., data=train, method='class')
model = rpart(Survived ~ Pclass + Sex + Age + Embarked + Title, data=train, method='class')	# train the logistic regression model
plot(model)
fancyRpartPlot(model)
summary(model)														# summary of the model (properties of different cols wrt decision)

actualTest = read.csv("test.csv", header=TRUE)

actualTest = subset(actualTest , select = c(1,2,4,5,6,7,9,11))
actualTest$Age[is.na(actualTest$Age)] = predict(AgeModel, actualTest[is.na(actualTest$Age), ])	
actualTest$Fare[is.na(actualTest$Fare)] = predict(FareModel, actualTest[is.na(data$Fare), ]) 
actualTest$Age[ actualTest$Age < 1] = 1

#levels(actualTest$Title) = levels(data$Title)

results = predict(model, newdata=actualTest, type="class")
output =  data.frame(PassengerId = actualTest$PassengerId, Survived = results)
write.csv(output, "decisionTreeOuptut_Title.csv", row.names=FALSE)
