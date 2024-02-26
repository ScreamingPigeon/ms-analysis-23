library(ez)
library(ggplot2)
library(plyr)
library(reshape2)
library(pbkrtest)
library(multcomp)
library(Hmisc)
library(readxl)
library(tidyverse)
library(stringr)
library(fs)
library(writexl)
library(xlsx)
library(openxlsx)
library(arrow)
library(tibble)
library(data.table)


participant <- dir_ls("C:\\Users\\Chang\\Documents\\researchstuff\\MS\\MS activities\\106")
test = "C:\\Users\\Chang\\Documents\\researchstuff\\MS\\MS activities\\106\\CHI2021 106B1_T2.csv"
big = data.frame()
big
resultant <- function(path){
  dataf = read.csv(path)
  dataf <- dataf[,-c(1)]
  xyz <- dataf[,1:3]
  t <- dataf[,4]
  resultant <- sqrt((xyz[,1]^2) + (xyz[,2]^2) + (xyz[,3]^2))
  #print(length(resultant))
  dataf$resultant <- resultant
  #print(nrow(dataf))
  dataf
}

combine <- map_dfr(
  .x = participant, 
  .f = \(path) resultant(
    path = path))
combine <- as.data.frame(combine)

ggplot(data = combine, mapping = aes(x = t, y = resultant, group = 1)) + geom_line(colour = 'red', alpha = 0.5)
resultant(test)

nrow(combine)
typeof(combine)
