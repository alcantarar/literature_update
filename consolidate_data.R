library(plyr)

<<<<<<< HEAD
data <- read.csv('/Users/ryanalcantara/Professional Drive/Subreddit/code_repo/literature_update/RYANDATA_consolidated.csv', stringsAsFactors = F)
=======
data <- read.csv('RYANDATA_consolidated.csv', stringsAsFactors = F)
>>>>>>> 0175f97eedb5f4b0683bb9fe69734a3789bac842

data.complete <- data[(complete.cases(data$topic)),]
nrow(data.complete)
table(data.complete$topic)

#combine categories
data.complete$topic[grepl('ORTHO',data.complete$topic)] <- 'ORTHOPAEDICS'
data.complete$topic[grepl('ANIMAL',data.complete$topic)] <- 'COMPARATIVE'
data.complete$topic[grepl('COMPARATIVE',data.complete$topic)] <- 'COMPARATIVE'
data.complete$topic[grepl('VETERINARY',data.complete$topic)] <- 'COMPARATIVE'
data.complete$topic[grepl('EVOLUTION', data.complete$topic)] <- 'COMPARATIVE'
data.complete$topic[grepl('COMPARATIVE', data.complete$topic)] <- 'EVO/COMP'
data.complete$topic[grepl('DENTAL', data.complete$topic)] <- 'HEAD'
data.complete$topic[grepl('VISUAL', data.complete$topic)] <- 'HEAD'

#remove low-occurance categories
data.complete$topic[grepl('BIOMECHANICS IN EDUCATION',data.complete$topic)] <- NA
data.complete$topic[grepl('DIGESTIVE',data.complete$topic)] <- NA
data.complete$topic[grepl('WHEELCHAIR',data.complete$topic)] <- NA
data.complete$topic[grepl('OBSTETRICS',data.complete$topic)] <- NA
data.complete$topic[grepl('REACHING',data.complete$topic)] <- NA
data.complete$topic[grepl('POSTURE',data.complete$topic)] <- NA
data.complete$topic[grepl('HAND',data.complete$topic)] <- NA
data.complete$topic[grepl('BOTANY',data.complete$topic)] <- NA
data.complete$topic[grepl('TRAUMA',data.complete$topic)] <- NA

table(data.complete$topic)
data.complete <- data.complete[(complete.cases(data.complete$topic)),]
nrow(data.complete)
write.csv(data.complete, file = 'RYANDATA_consolidated.csv')


data.trim <- ddply(data.complete,.(topic), function(x) x[sample(nrow(x),400),])
table(data.trim$topic)
write.csv(data.trim, file = 'RYANDATA_trim.csv')
