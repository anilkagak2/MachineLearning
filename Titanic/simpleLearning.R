setwd("C:/Users/anilkag/Desktop/personalWork/Machine Learning/Competitions/Titanic")
data = read.csv("train.csv", header=TRUE)							# read the raw data
data = subset(data, select = c(2,3,5,6,7,8,10,12))					# only select the cols required 
data$Age[is.na(data$Age)] = mean(data$Age, na.rm=TRUE)				# fill the missing values
actualTest$Fare[is.na(actualTest$Fare)] = mean(actualTest$Fare, na.rm=TRUE)

train 	= data[1:800,  ]
test 	= data[801:891,]

model = glm(Survived ~., family=binomial(link='logit'), data=train)	# train the logistic regression model
summary(model)														# summary of the model (properties of different cols wrt decision)
anova(model, test="Chisq")

results = predict(model, newdata = subset(test, select=c(2,3,4,5,6,7,8)), type='response')
results = ifelse(results > 0.5,1,0)
misClasificError = mean(results != test$Survived)
print(paste('Accuracy',1-misClasificError))


actualTest = read.csv("test.csv", header=TRUE)
actualTest = subset(actualTest , select = c(1,2,4,5,6,7,9,11))
actualTest$Age[is.na(actualTest$Age)] = mean(actualTest$Age, na.rm=TRUE)
actualTest$Fare[is.na(actualTest$Fare)] = mean(actualTest$Fare, na.rm=TRUE)

results = predict(model, newdata=actualTest, type='response')
results = ifelse(results > 0.5, 1, 0)
output =  cbind(PassengerId = actualTest$PassengerId, Survived = results)
write.csv(data.frame(output), "output.csv", row.names=FALSE)
