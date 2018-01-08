library(dplyr)
library(data.table)
library(tidyr)

determine_cluster <- function(x){
  if(any(is.na(x))) return(NA)
  max_x <- max(x)
  count_nmax <- sum(max_x == x)
  if (count_nmax == 1) return(names(x)[as.vector(x==max_x)])
  if (count_nmax > 1) return(NA)
}

calc_cluster_max_votes <- function(x){
  y <- x[, .N, by = .(coord_id, Cluster)]
  y = spread(y, key = Cluster, value = N, fill = 0)
  cluster_names <- names(y)[-1]
  y$cluster_won <- apply(y[,-1], MARGIN = 1, FUN = determine_cluster)
  y <- y[, .(coord_id, cluster_won)]
  return(y)
}

set.seed(1)
z <- data.table(
  data.frame(coord_index = seq(1:90),
             coords = rep(1:(90/3), each =3),
             cluster = sample(c("A","B","C"), 90, replace = TRUE))
)

perform_voting <- function(df){

  df <- df[, -1]
  df <- tbl_df(df)
  df <- unite(df, 'coord_id', 'x_mm', 'y_mm', sep = "_", remove = F)
  dt <- data.table(df)
  
  cluster_won <- calc_cluster_max_votes(dt)
  
  dt[, c("SegmentID", "Cluster") := NULL]
  
  dt <- unique(dt)
  dt <- merge(dt, cluster_won, by = "coord_id", join = "left", sort = FALSE)
}

segment_length <- 150
n_clusters <- 5

path <- paste0("C:/Users/Mark/Dropbox/RodentDataAnalytics-Bees Experiment/Australia Experiment/Data/length", segment_length, "/")
df <- read.csv(paste0(path, "segment_xys_with_clust_name_", n_clusters, "_clusters.csv"))

dt <- perform_voting(df)

write.csv(dt, paste0(path, "xy_voted_", n_clusters, "_clusters.csv"))

