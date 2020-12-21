df <- read.csv('../Data/BERT_out.csv')  # 0 indexed
labels <- read.csv('../Data/labels.csv')

library(ggplot2)

ggplot(df) +
  geom_point(aes(x = pred, obs, color = as.factor(obs)))


# xy <- as.data.frame(tsne(as.matrix(df), max_iter = 300))  # takes a while
colnames(xy) <- c('x','y')

ggplot(xy) + 
  geom_point(aes(x, y, color = as.factor(df$obs)))

# df$miss <- df$pred != df$obs
# df$hit <- df$pred == df$obs
