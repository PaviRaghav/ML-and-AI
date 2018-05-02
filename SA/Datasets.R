setwd("/Users/pavithraraghavan/Documents/Sentiment_Analysis")
#=========1st dataset => train.csv

#=========2nd dataset => train.csv, amazon_cells_labelled.txt
temp1 <- read.csv("Datasets/train.csv", header=TRUE)
head(temp1)
unique(temp1$Sentiment) #0 negative #1 positive
nrow(temp1[temp1$Sentiment==0,]) #negative 43532
nrow(temp1[temp1$Sentiment==1,]) #positive 56457

temp2 <- read.table("Datasets/amazon_cells_labelled.txt", header=FALSE, sep="|")
head(temp2)
unique(temp2$V2) #0 negative #1 positive
colnames(temp2) <- c("SentimentText","Sentiment")
dataset2 <- as.data.frame(rbind(temp1[,c("Sentiment", "SentimentText")],temp2))
nrow(dataset2[dataset2$Sentiment==0,]) #negative 87420
nrow(dataset2[dataset2$Sentiment==1,]) #positive 113306
#shuffle
dataset_2 <- dataset2[sample(nrow(dataset2)),]
dataset2 <- dataset_2
write.csv(dataset2, file="Final_datasets/Dataset_2.csv", row.names = FALSE, quote = TRUE)


#=========3rd dataset => train.csv, amazon_cells_labelled.txt, imdb_labelled.txt
temp1 <- dataset2
head(temp1)
unique(temp1$Sentiment) #0 negative #1 positive
nrow(temp1[temp1$Sentiment==0,]) #negative 87420
nrow(temp1[temp1$Sentiment==1,]) #positive 113306

temp2 <- read.table("Datasets/imdb_labelled.txt", header=FALSE, sep="|")
head(temp2,6)
unique(temp2$V2) #0 negative #1 positive
colnames(temp2) <- c("SentimentText","Sentiment")
dataset2 <- as.data.frame(rbind(temp1[,c("Sentiment", "SentimentText")],temp2))
nrow(dataset2[dataset2$Sentiment==0,]) #negative 87712
nrow(dataset2[dataset2$Sentiment==1,]) #positive 113546
dataset_2 <- dataset2[sample(nrow(dataset2)),]
dataset2 <- dataset_2
write.csv(dataset2, file="Final_datasets/Dataset_3.csv", row.names = FALSE, quote = TRUE)


#=========4th dataset => train.csv, amazon_cells_labelled.txt, imdb_labelled.txt, train_new.txt
temp1 <- dataset2
head(temp1)
unique(temp1$Sentiment) #0 negative #1 positive
nrow(temp1[temp1$Sentiment==0,]) #negative 87712
nrow(temp1[temp1$Sentiment==1,]) #positive 113546

temp2 <- read.table("Datasets/train_new.txt", header=FALSE, sep="|")
head(temp2,6)
unique(temp2$V1) #0 negative #1 positive
colnames(temp2) <- c("Sentiment","SentimentText")
dataset2 <- as.data.frame(rbind(temp1[,c("Sentiment", "SentimentText")],temp2))
nrow(dataset2[dataset2$Sentiment==0,]) #negative 91560
nrow(dataset2[dataset2$Sentiment==1,]) #positive 116032
dataset_2 <- dataset2[sample(nrow(dataset2)),]
dataset2 <- dataset_2
write.csv(dataset2, file="Final_datasets/Dataset_4.csv", row.names = FALSE, quote = TRUE)


#=========5th dataset => train.csv, amazon_cells_labelled.txt, imdb_labelled.txt, train_new.txt, tweets.csv
temp1 <- dataset2
head(temp1)
unique(temp1$Sentiment) #0 negative #1 positive
nrow(temp1[temp1$Sentiment==0,]) #negative 91560
nrow(temp1[temp1$Sentiment==1,]) #positive 116032
#0 negative #1 positive #2 neutral

temp2 <- read.csv("Datasets/tweets.csv", header=TRUE)
head(temp2,6)
unique(temp2$airline_sentiment) #negative, positive, neutral
#remove @* from tweets
gsub("[^\\s]*@[^\\s]*", "", temp2$text, perl=T) -> temp2$SentimentText
#
ifelse(temp2$airline_sentiment=="positive", 1, (ifelse(temp2$airline_sentiment=="negative", 0,2)))  -> temp2$Sentiment
dataset2 <- as.data.frame(rbind(temp1[,c("Sentiment", "SentimentText")],temp2[,c("Sentiment", "SentimentText")]))
nrow(dataset2[dataset2$Sentiment==0,]) #negative 109916
nrow(dataset2[dataset2$Sentiment==1,]) #positive 120758
nrow(dataset2[dataset2$Sentiment==2,]) #neutral 6198
dataset_2 <- dataset2[sample(nrow(dataset2)),]
dataset2 <- dataset_2
write.csv(dataset2, file="Final_datasets/Dataset_5.csv", row.names = FALSE, quote = TRUE)

#=========6th dataset => train.csv, amazon_cells_labelled.txt, imdb_labelled.txt, train_new.txt, tweets.csv, yelp_labelled.txt
temp1 <- dataset2
head(temp1)
unique(temp1$Sentiment) #0 negative #1 positive #2neutral
nrow(temp1[temp1$Sentiment==0,]) #negative 109916
nrow(temp1[temp1$Sentiment==1,]) #positive 120758
nrow(temp1[temp1$Sentiment==1,]) #positive 6198

temp2 <- read.table("Datasets/yelp_labelled.txt", header=FALSE, sep="|")
head(temp2,6)
unique(temp2$V2) #0 negative #1 positive
colnames(temp2) <- c("SentimentText","Sentiment")
dataset2 <- as.data.frame(rbind(temp1[,c("Sentiment", "SentimentText")],temp2[,c("Sentiment", "SentimentText")]))
nrow(dataset2[dataset2$Sentiment==0,]) #negative 110166
nrow(dataset2[dataset2$Sentiment==1,]) #positive 120946
nrow(dataset2[dataset2$Sentiment==2,]) #neutral 6198
dataset_2 <- dataset2[sample(nrow(dataset2)),]
dataset2 <- dataset_2
write.csv(dataset2, file="Final_datasets/Dataset_6.csv", row.names = FALSE, quote = TRUE)


temp2 <- read.csv("Final_datasets/Dataset_6.csv", header=TRUE)
temp2$Sentiment_New <- gsub("@[^\\s]*", "", temp2$SentimentText, perl=T) 
temp2$SentimentNew <-  gsub("[^[:alnum:][:space:]']", "", temp2$Sentiment_New)
dataset2 <- temp2[,c("Sentiment","SentimentNew")]
colnames(dataset2) <- c("Sentiment","SentimentText")
write.csv(dataset2, file="Final_datasets/Dataset_Bayes.csv", row.names = FALSE, quote = TRUE)

