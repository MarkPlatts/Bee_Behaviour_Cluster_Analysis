library(ggplot2)
library(here)

segment_length <- 150
n_clusters <- 5

path <- paste0("Data/length", segment_length, "/")
df <- read.csv(paste0(path, "xy_voted_", n_clusters, "_clusters.csv"))
ggplot(data = df, aes(x = Experiment, fill = as.factor(cluster_won))) + 
  geom_bar(position = "fill") + 
  coord_flip()



