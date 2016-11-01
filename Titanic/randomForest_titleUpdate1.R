setwd("C:/Users/anilkag/Desktop/personalWork/Machine Learning/Competitions/Titanic")

library(rpart)
library(rpart.plot)
library(randomForest)
library(ggplot2)

set.seed(1)
train <- read.csv("train.csv", stringsAsFactors=FALSE)
test  <- read.csv("test.csv",  stringsAsFactors=FALSE)

extractFeatures <- function(data) {
  features <- c("Pclass",
                "Age",
                "Sex",
                "Parch",
                "SibSp",
                "Fare",
                "Embarked",
                "Name")
  fea <- data[,features]
  fea$Age[is.na(fea$Age)] <- -1
  fea$Fare[is.na(fea$Fare)] <- median(fea$Fare, na.rm=TRUE)
  fea$Embarked[fea$Embarked==""] = "S"
  fea$Sex      <- as.factor(fea$Sex)
  fea$Embarked <- as.factor(fea$Embarked)

  fea$Title <- sapply(fea$Name, FUN=function(x) {strsplit(x, split='[,.]')[[1]][2]})
  fea$Title <- sub(' ', '', fea$Title)
  fea$Title[fea$Title %in% c('Mme', 'Mlle')] <- 'Mlle'
  fea$Title[fea$Title %in% c('Capt', 'Don', 'Major', 'Sir')] <- 'Sir'
  fea$Title[fea$Title %in% c('Dona', 'Lady', 'the Countess', 'Jonkheer')] <- 'Lady'
  fea$Title <- as.factor(fea$Title)

  return(fea)
}

rf <- randomForest(extractFeatures(train), as.factor(train$Survived), ntree=100, importance=TRUE)
submission <- data.frame(PassengerId = test$PassengerId)
submission$Survived <- predict(rf, extractFeatures(test))
write.csv(submission, file = "1_random_forest_r_submission.csv", row.names=FALSE)

imp <- importance(rf, type=1)
featureImportance <- data.frame(Feature=row.names(imp), Importance=imp[,1])

p <- ggplot(featureImportance, aes(x=reorder(Feature, Importance), y=Importance)) +
     geom_bar(stat="identity", fill="#53cfff") +
     coord_flip() + 
     theme_light(base_size=20) +
     xlab("") +
     ylab("Importance") + 
     ggtitle("Random Forest Feature Importance\n") +
     theme(plot.title=element_text(size=18))

ggsave("2_feature_importance.png", p)

#FareModel = rpart(Fare ~ Pclass + Sex + SibSp + Parch + Age + Embarked, data=data[!is.na(data$Fare), ], method="anova")
#AgeModel = rpart(Age ~ Pclass + Sex + SibSp + Parch + Embarked + Title, data=data[!is.na(data$Age), ], method="anova")
#data$Fare[is.na(data$Fare)] = predict(FareModel, data[is.na(data$Fare), ])
#data$Age[is.na(data$Age)] = predict(AgeModel, data[is.na(data$Age), ])				# fill the missing values

#levels(actualTest$Title) = levels(data$Title)

