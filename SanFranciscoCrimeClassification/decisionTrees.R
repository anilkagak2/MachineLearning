setwd("C:/Users/anilkag/Desktop/personalWork/Machine Learning/Competitions/SanFranciscoCrimeClassification")

library(rpart)
library(rattle)
library(rpart.plot)
library(RColorBrewer)

# The amount of data available is very large
# You cannot train with the full data set => you need to be selective
data = read.csv("train.csv", header=TRUE)							# read the raw data
sampledData = data[sample(nrow(data), 100000), ]
sampledData = subset(sampledData, select = c(1,2,4,5)) # is for resolution
sampledData$Dates = as.numeric( as.Date(sampledData$Dates, format='%m/%d/%Y') - as.Date('2000-01-01') )
sampledData$Category = factor(sampledData$Category)
#sampledData$Resolution = factor(sampledData$Resolution)
train = sampledData[1:10000,  ]
test 	= sampledData[10001:100000,]

model = rpart(Category ~., data=train, method='class')	# train the logistic regression model
plot(model)
fancyRpartPlot(model)
summary(model)														# summary of the model (properties of different cols wrt decision)

actualTest = read.csv("test.csv", header=TRUE)
actualTest = subset(actualTest, select = c(1,2,3,4))
results = predict(model, newdata=test, type="class")
output =  data.frame(PassengerId = actualTest$PassengerId, Category = results)
write.csv(output, "decisionTreeOuptut.csv", row.names=FALSE)
