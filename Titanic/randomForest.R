setwd("C:/Users/anilkag/Desktop/personalWork/Machine Learning/Competitions/Titanic")

library(randomForest)
set.seed(415)

data = read.csv("train.csv", header=TRUE)							# read the raw data

# add new feature
data$Name = as.character(data$Name)
data$Title <- sapply(data$Name, FUN=function(x) {strsplit(x, split='[,.]')[[1]][2]})
data$Title <- sub(' ', '', data$Title)
data$Title[data$Title %in% c('Mme', 'Mlle')] <- 'Mlle'
data$Title[data$Title %in% c('Capt', 'Don', 'Major', 'Sir')] <- 'Sir'
data$Title[data$Title %in% c('Dona', 'Lady', 'the Countess', 'Jonkheer')] <- 'Lady'
data$Title <- factor(data$Title)

data = subset(data, select = c(2,3,5,6,7,8,10,12,13))					# only select the cols required 

data[62, 8] = 'S'
data[830, 8] = 'S'

data$Fare[is.na(data$Fare)] = median(data$Fare, na.rm=TRUE)
AgeModel = rpart(Age ~ Pclass + Sex + SibSp + Parch + Fare + Embarked + Title, data=data[!is.na(data$Age), ], method="anova")
data$Age[is.na(data$Age)] = predict(AgeModel, data[is.na(data$Age), ])				# fill the missing values

model = randomForest(as.factor(Survived) ~ Pclass + Sex + Age + SibSp + Parch + Fare + Embarked + Title, data=data , importance=TRUE, ntree=2000)	# train the logistic regression model
varImpPlot(model)

actualTest = read.csv("test.csv", header=TRUE)
actualTest$Name = as.character(actualTest$Name)
actualTest$Title <- sapply(actualTest$Name, FUN=function(x) {strsplit(x, split='[,.]')[[1]][2]})
actualTest$Title <- sub(' ', '', actualTest$Title)
actualTest$Title[actualTest$Title %in% c('Mme', 'Mlle')] <- 'Mlle'
actualTest$Title[actualTest$Title %in% c('Capt', 'Don', 'Major', 'Sir')] <- 'Sir'
actualTest$Title[actualTest$Title %in% c('Dona', 'Lady', 'the Countess', 'Jonkheer')] <- 'Lady'
actualTest$Title <- factor(actualTest$Title)

actualTest = subset(actualTest , select = c(1,2,4,5,6,7,9,11,12))
actualTest$Age[is.na(actualTest$Age)] = predict(AgeModel, actualTest[is.na(actualTest$Age), ])	
actualTest$Fare[is.na(actualTest$Fare)] = median(actualTest$Fare, na.rm=TRUE)
actualTest$Age[ actualTest$Age < 1] = 1

levels(actualTest$Title) = levels(data$Title)

results = predict(model, actualTest)
output =  data.frame(PassengerId = actualTest$PassengerId, Survived = results)
write.csv(output, "randomForestOuptut.csv", row.names=FALSE)
