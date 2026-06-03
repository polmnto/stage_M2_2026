library(argparse)

parser = ArgumentParser()
parser$add_argument("-i", "--input")
parser$add_argument("-o", "--output")
args = parser$parse_args()

data = read.table(args$input, h = T, row.names = NULL)

data$row.names = NULL

write.table(x = data, file = args$output, quote = F, sep = " ", row.names =  F)
