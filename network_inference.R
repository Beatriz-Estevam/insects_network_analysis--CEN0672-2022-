

### Loading csv into R
df = read_csv('grupo_-0.832778.csv')
head(df)

# Setting species column as df index
# removing species column from new df
df2 <- df[ -c(1)]
head(df2)

# add df species column as index to new df
rownames(df2) <- df$espécie
head(df2)

## Getting occurence stats 
library(cooccur)
# Find significant pairwise co-occurrences.
co <- print(cooccur(df2, spp_names = TRUE))

# Create a data frame of the nodes in the network. 
nodes <- data.frame(id = 1:nrow(df2),
                    label = rownames(df2),
                    color = '#ed72b2',
                    shadow = TRUE) 

# Create an edges dataframe from the significant pairwise co-occurrences.
edges <- data.frame(from = co$sp1, to = co$sp2,
                    color = ifelse(co$p_lt <= 0.50, '#B0B2C1', '#3C3F51'),
                    dashes = ifelse(co$p_lt <= 0.01, TRUE, FALSE))



## Plotting network
library(visNetwork)
visNetwork(nodes = nodes, edges = edges) %>% visIgraphLayout(layout = 'layout_with_kk')

