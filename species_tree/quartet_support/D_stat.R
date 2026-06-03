library(argparse)

parser = ArgumentParser()
parser$add_argument("-i", "--input")
parser$add_argument("-o", "--output")
args = parser$parse_args()

#import table
data = read.table(args$input, h = T, sep = ";", dec = ".")

#D stat calculation
data$Dstat = (data$q2 - data$q3) / (data$q2 + data$q3)

#export table
write.table(x = data, file = args$output, quote = F, sep = "\t", dec = ",", row.names =  F)
