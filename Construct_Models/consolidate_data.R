library(plyr)

data <- read.csv('RYANDATA.csv', stringsAsFactors = F)

data.complete <- data[(complete.cases(data$topic)),]
nrow(data.complete)
table(data.complete$topic)
unique(data.complete$topic)
#combine categories
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
data.complete$topic[grepl('UNIQUE',data.complete$topic)] <- NA

#some are too loosely defined
data.complete$topic[grepl('GAIT',data.complete$topic)] <- NA
data.complete$topic[grepl('METHOD', data.complete$topic)] <- NA
data.complete$topic[grepl('MATERIAL', data.complete$topic)] <- NA


#rename long names
data.complete$topic[grepl('CARDIO',data.complete$topic)] <- 'CARDIO'
data.complete$topic[grepl('TISSUE',data.complete$topic)] <- 'BIOMATERIAL'
data.complete$topic[grepl('CARDIO',data.complete$topic)] <- 'CARDIO'
data.complete$topic[grepl('CELL',data.complete$topic)] <- 'CELLULAR'
data.complete$topic[grepl('HAND',data.complete$topic)] <- 'HAND/FOOT'
data.complete$topic[grepl('TRAUMA',data.complete$topic)] <- 'IMPACT/TRAUMA'
data.complete$topic[grepl('ORTHO',data.complete$topic)] <- 'ORTHOPAEDICS'




# consolidate data ----
#save csv of changes above
table(data.complete$topic)
data.complete <- data.complete[(complete.cases(data.complete$topic)),]
nrow(data.complete)
write.csv(data.complete, file = 'RYANDATA_consolidated.csv')

## trim data ----
#laptop memory couldn't handle more than 400 per section
data.trim <- ddply(data.complete,.(topic), function(x) x[sample(nrow(x),400),])
table(data.trim$topic)
write.csv(data.trim, file = 'RYANDATA_trim.csv')
