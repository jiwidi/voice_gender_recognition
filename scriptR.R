library(warbleR)
library(tuneR)
library(readr)    

args = commandArgs(trailingOnly=TRUE)

df <- read_csv(args[1])
selec = rep_len(1, nrow(df))
start= rep_len(0, nrow(df)) 
end = rep_len(Inf, nrow(df)) 
sound.files = df['sound.files']
dfS = data.frame(sound.files,selec,start,end)
a <- specan(X = dfS,parallel=8)
write.csv(file='audios_specan.csv', x=a)
result <-merge(df, a, by = "sound.files") 
write.csv(file='audios_dataset.csv', x=result)
  

