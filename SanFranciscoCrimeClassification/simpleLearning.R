# The amount of data available is very large
# You cannot train with the full data set => you need to be selective

setwd("C:/Users/anilkag/Desktop/personalWork/Machine Learning/Competitions/SanFranciscoCrimeClassification")
data = read.csv("train.csv", header=TRUE)							# read the raw data

sampledData = data[sample(nrow(data), 100000), ]
sampledData = subset(sampledData, select = c(1,2,4,5)) #6 is for resolution
sampledData$Dates = as.numeric( as.Date(sampledData$Dates, format='%m/%d/%Y') - as.Date('2000-01-01') )
sampledData$Category = factor(sampledData$Category)
#sampledData$Resolution = factor(sampledData$Resolution)
train = sampledData[1:10000,  ]
test 	= sampledData[10001:100000,]

model = glm(Category ~., family=binomial(link='logit'), data=train,  control= list(maxit=50))	# train the logistic regression model
#model$xlevels[["Resolution"]] <- union (model$xlevels[["Resolution"]], levels(test$Resolution))

summary(model)														# summary of the model (properties of different cols wrt decision)
anova(model, test="Chisq")

#results = predict(model, newdata = subset(test, select=c(1,3,4,5)), type='response')
results = predict(model, newdata = subset(test, select=c(1,3,4)), type='response')
results = ifelse(results > 0.5,1,0)
misClasificError = mean(results != test$Category)
print(paste('Accuracy',1-misClasificError))


actualTest = read.csv("test.csv", header=TRUE)
actualTest = subset(actualTest , select = c(1,3,4,5))
actualTest$Dates = as.numeric( as.Date(actualTest$Dates, format='%m/%d/%Y') - as.Date('2000-01-01') )

results = predict(model, newdata=actualTest, type='response')
results = ifelse(results > 0.5, 1, 0)
output =  cbind(PassengerId = actualTest$PassengerId, Survived = results)
write.csv(data.frame(output), "output.csv", row.names=FALSE)
