#Q1. mytext에 저장된 단어를 2단어씩 연결하여 출력 
#The United/ United States/ States comprises/.../United States
mytext <- "The United States comprises fifty states. In the United States, each state has its own laws. However, federal law overrides state law in the United States."

library(stringr)

mywrod <- unlist(str_extract_all(mytext, boundary("word")))
myword

myword.2gram <- c()
for(i in 1:length(myword) - 1){
  myword.2gram[i] <- paste(myword[c(i, i+1)], collapse = " ")
}
myword.2gram
# [1] "The United"       "United States"    "States comprises"
# [4] "comprises fifty"  "fifty states"     "states In"       
# [7] "In the"           "the United"       "United States"   
# [10] "States each"      "each state"       "state has"       
# [13] "has its"          "its own"          "own laws"        
# [16] "laws However"     "However federal"  "federal law"     
# [19] "law overrides"    "overrides state"  "state law"       
# [22] "law in"           "in the"           "the United"      
# [25] "United States"   

#Q2. kaggle Titanic train.csv의 Name에서 명칭 추출 후,
#   시각화와 범주형으로 치환
library(readxl)
raw_titanic <- read.csv("Data/titanic.csv")
titanic <- raw_titanic
length(titanic$Name)

library(stringr)
title <- str_match_all(titanic$Name, "[[:space:]]([[:alpha:]]{2,})\\.")
title <- lapply(title, function(x){x[,2]})
title <- as.data.frame(unlist(title))
colnames(title) <- "Title"
title

titanic <- cbind(titanic, title)
title.top5 <- sort(table(titanic$Title), decreasing = T) %>% 
  head(5)
title.top5
#  Mr   Miss    Mrs Master     Dr 
#517    182    125     40      7

#시각화
library(ggplot2)
ggplot(as.data.frame(title.top5), aes(x = Var1, y = Freq)) + 
  geom_col() +
  labs(x = "Title" ) +
  geom_text(aes(label = Freq), vjust = -0.5) +
  theme(plot.title = element_text(hjust = 0.5))


#Title 범주화
library(dplyr)
titanic <-  mutate(titanic, Title.num = ifelse(Title == "Mr", 1,
                        ifelse(Title == "Miss", 2,
                               ifelse(Title == "Mrs", 3,
                                      ifelse(Title == "Master", 4,
                                             ifelse(Title == "Dr", 5, 6))))))
table(titanic$Title.num)
#   1   2   3   4   5   6 
#517 182 125  40   7  20