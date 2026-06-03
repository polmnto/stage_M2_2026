rm(list=ls())
getwd()

library(tidyr)
library(ggplot2)
library(ggrepel)
library(ggpubr)

# Import and clean datasets-----
concordance = read.table("output/discordance_dataframe.csv", h = T, sep = "\t")
height = read.table("output/height_dataframe.csv", h = T, sep = "\t", dec = ".")
dstat = read.table("output/quartet_support_Dstat.csv", h = T, sep = "\t", dec = ",")
dstat = dstat[,c(1:7,13)]  
colnames(dstat)[colnames(dstat) == "node_ID"] = "node"
dstat$node = as.factor(dstat$node)
levels(dstat$node) = c('9','10','11','12','13','14','15','16','17','18',
                       '19','20','21','22','23','24','25','26','27') #adapt this part for the nodes you are interested in

node_age = read.table("input/node_age.csv", h = T, sep = "\t", dec = ".")
node_age = node_age[c(8:26),]

## Convert into tidy format
conco_tidy = pivot_longer(concordance, cols = 2:1600, names_to = "gene", values_to = "concordance")
haut_tidy = pivot_longer(height, cols = 2:1600, names_to = "gene", values_to = "height")

## Merge datasets
df_merged = merge(conco_tidy, haut_tidy, by = c("node", "gene"))

#Group D1 and D2 nodes together
df_merged$concordance_grouped = df_merged$concordance
df_merged$concordance_grouped[df_merged$concordance == "D1"] = "D"
df_merged$concordance_grouped[df_merged$concordance == "D2"] = "D"

## Remove NAs
df_merged = subset(df_merged, concordance != 'N')
df_merged = na.omit(df_merged)

## Rename nodes
df_merged$node = as.factor(df_merged$node)
levels(df_merged$node) = c('9','10','11','12','13','14','15','16','17','18',
                           '19','20','21','22','23','24','25','26','27')


# Height index that allow to detect gene flow------
H_stat = c()  #vector with height index
nb_D_nodes = c()  #vector with the number of discordant nodes
nb_D_nodes_INF = c()  #vector with the number of discordant nodes with a height below the height mode of the concordant ones

for(i in levels(as.factor(df_merged$node))){
  subset_i = subset(df_merged, node == i)
  dst = density(subset_i$height[subset_i$concordance_grouped == "C"])
  H_C = dst$x[dst$y == max(dst$y)]
  tot_D_nodes = nrow(subset(subset_i, concordance_grouped == "D"))
  hD_inf_C = nrow(subset(subset_i, concordance_grouped == "D" & height < H_C))
  H = hD_inf_C / tot_D_nodes
  H_stat = append(H_stat, H)  
  nb_D_nodes = append(nb_D_nodes, tot_D_nodes)
  nb_D_nodes_INF = append(nb_D_nodes_INF, hD_inf_C)
}

## Create dataframe
node = dstat$node
Dstat = dstat$Dstat
age = node_age$age
q1 = dstat$q1

df_Hstat = data.frame(node, q1, Dstat, H_stat, nb_D_nodes_INF, nb_D_nodes, age)

df_Hstat$discordance_rate = 1 - df_Hstat$q1

## Remove nodes with less than 5% discordancee (q1 > 0.95)
df_Hstat = subset(df_Hstat, q1 < 0.95)


# Figure H ~ D-------

# Just for information, the horizontal lines plotted here correspond to :
#   - continuous : the expected mean H index under the null hypothesis
#   - dashed : the 95th percentile of H under the null hypothesis (i.e. the 5% significance threshold)
#   - dotted : the 99th percentile of H under the null hypothesis (i.e. the 1% significance threshold)
# 
# All those values were computed doing 1000 simulations of 1600 gene trees with three species 
# under the MultiSpecies Coalesent without any gene flow (= null hypothesis).

ggplot(df_Hstat, aes(y = H_stat, x = abs(Dstat))) +
  geom_hline(yintercept = 0.1215315, col = "#474747", linewidth = 0.7) +
  geom_hline(yintercept = 0.1801961, col = "#474747", linetype = "dashed", linewidth = 0.7) +
  geom_hline(yintercept = 0.2104132, col = "#474747", linetype = "dotted", linewidth = 0.7) +
  geom_point(aes(size = discordance_rate, col = age)) +
  geom_text_repel(aes(label = node), size = 5.1, point.padding = 0.5) +
  ylim(c(0,NA)) +
  labs(y = "H index", x = "| D stat |", size = "Discordance", col = "Age (Ma)") +
  scale_colour_gradientn(colours=c("#580585fa", "orange")) + 
  theme_bw()
