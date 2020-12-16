library(plyr)
library(dplyr)

data <- read.csv('RYANDATA.csv', stringsAsFactors = F)

data.complete <- data[(complete.cases(data$Topics)),]
nrow(data.complete)
# table(data.complete$Topics)
# unique(data.complete$Topics)
#combine categories
data.complete$Topics[grepl('ANIMAL',data.complete$Topics)] <- 'COMPARATIVE'
data.complete$Topics[grepl('COMPARATIVE',data.complete$Topics)] <- 'COMPARATIVE'
data.complete$Topics[grepl('VETERINARY',data.complete$Topics)] <- 'COMPARATIVE'
data.complete$Topics[grepl('EVOLUTION', data.complete$Topics)] <- 'COMPARATIVE'
data.complete$Topics[grepl('COMPARATIVE', data.complete$Topics)] <- 'EVO COMP'
data.complete$Topics[grepl('DENTAL', data.complete$Topics)] <- 'HEAD'
data.complete$Topics[grepl('VISUAL', data.complete$Topics)] <- 'HEAD'
data.complete$Topics[grepl('WEARABLE', data.complete$Topics)] <- 'WEARABLES'
data.complete$Topics[grepl('ERGONOMICS', data.complete$Topics)] <- 'ERGONOMICS'
data.complete$Topics[grepl('OFTHEWEEK', data.complete$Topics)] <- 'PICKOFTHEWEEK'
data.complete$Topics[grepl('ROBOT', data.complete$Topics)] <- 'ROBOTICS'

#remove low-occurance categories
data.complete$Topics[grepl('BIOMECHANICS IN EDUCATION',data.complete$Topics)] <- NA
data.complete$Topics[grepl('DIGESTIVE',data.complete$Topics)] <- NA
data.complete$Topics[grepl('WHEELCHAIR',data.complete$Topics)] <- NA
data.complete$Topics[grepl('OBSTETRICS',data.complete$Topics)] <- NA
data.complete$Topics[grepl('REACHING',data.complete$Topics)] <- NA
data.complete$Topics[grepl('POSTURE',data.complete$Topics)] <- NA
data.complete$Topics[grepl('HAND',data.complete$Topics)] <- NA
data.complete$Topics[grepl('BOTANY',data.complete$Topics)] <- NA
data.complete$Topics[grepl('TRAUMA',data.complete$Topics)] <- NA
data.complete$Topics[grepl('UNIQUE',data.complete$Topics)] <- NA

#some are too loosely defined
data.complete$Topics[grepl('GAIT',data.complete$Topics)] <- NA
data.complete$Topics[grepl('METHOD', data.complete$Topics)] <- NA
data.complete$Topics[grepl('MATERIAL', data.complete$Topics)] <- NA


#rename long names
data.complete$Topics[grepl('CARDIO',data.complete$Topics)] <- 'CARDIO'
data.complete$Topics[grepl('TISSUE',data.complete$Topics)] <- 'BIOMATERIAL'
data.complete$Topics[grepl('CARDIO',data.complete$Topics)] <- 'CARDIO'
data.complete$Topics[grepl('CELL',data.complete$Topics)] <- 'CELLULAR'
data.complete$Topics[grepl('HAND',data.complete$Topics)] <- 'HAND FOOT'
data.complete$Topics[grepl('TRAUMA',data.complete$Topics)] <- 'IMPACT TRAUMA'
data.complete$Topics[grepl('ORTHO',data.complete$Topics)] <- 'ORTHOPAEDICS'

# keep topics with more 10 entries
df <- data.frame(table(data.complete$Topics))
keep_topics <- df$Var1[df$Freq > 10]
keep_topics <- droplevels(keep_topics)

data.complete <- data.complete %>% filter_at(vars(Topics), any_vars(. %in% keep_topics))

# consolidate data ----
#save csv of changes above
View(table(data.complete$Topics))
data.complete <- data.complete[(complete.cases(data.complete$Topics)),]
nrow(data.complete)
data.complete <- data.complete[,2:ncol(data.complete)]
write.csv(data.complete, file = 'RYANDATA_consolidated.csv', row.names = F)

## trim data ----
#laptop memory couldn't handle more than 400 per section
data.trim <- ddply(data.complete,.(Topics), function(x) x[sample(nrow(x),400),])
table(data.trim$Topics)
write.csv(data.trim, file = 'RYANDATA_trim.csv')
