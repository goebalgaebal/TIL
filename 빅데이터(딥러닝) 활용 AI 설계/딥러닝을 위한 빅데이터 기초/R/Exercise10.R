library(rJava)
library(KoNLP)
library(stringr)

library(RWeka)
library(tm)

mytextlocation <- "논문/"
#파일들을 모두 가져와서 corpus 생성
mypaper <- VCorpus(DirSource(mytextlocation))
mypaper

#mycourpus : mypaper에서 숫자 data를 없앤 Corpus data
mycorpus <- tm_map(mypaper, removeNumbers)
mycorpus


#특수 문자와 영단어 제거
for(i in 1: length(mycorpus)){
  mycorpus[[i]]$content <- str_replace_all(mycorpus[[i]]$content, "[a-zA-Z]|\\(|\\)|‘|’|·|－", "")
}


bigramTokenizer <-function(x) 
  NGramTokenizer(x, Weka_control(
    min = 2, max = 2))

trigramTokenizer <-function(x) 
  NGramTokenizer(x, Weka_control(
    min = 3, max = 3))

mycorpus.bigram.tdm <- TermDocumentMatrix(mycorpus, control = list(tokenize = bigramTokenizer))
mycorpus.bigram.tdm
bigramlist <- apply(mycorpus.bigram.tdm[,], 1, sum)
sort(bigramlist, decreasing = TRUE) %>%  head(10)
#것으로 나타났다       본 연구는   본 연구에서는       이 연구는     마을 공동체         수 있는       수 있었다 
#             7               7               6               6               5               5               5 
#어떠한 영향을       이를 위해       공익 연계 
#           5               5               4

myreplacecorpus <- mycorpus
for(i in 1:length(mycorpus)){
  myreplacecorpus[[i]]$content <- str_replace_all(mycorpus[[i]]$content, "본 연구[[:alpha:]]{1,}|이 연구[[:alpha:]]{1,}", "본 연구는")
  myreplacecorpus[[i]]$content <- str_replace_all(myreplacecorpus[[i]]$content, "수 있[[:alpha:]]{1,}", "수 있었다")
}

mycorpus.bigram.tdm <- TermDocumentMatrix(myreplacecorpus, control = list(tokenize = bigramTokenizer))
bigramlist <- apply(mycorpus.bigram.tdm[,], 1, sum)
sort(bigramlist, decreasing = TRUE) %>%  head(10)
# 본 연구는       수 있었다 것으로 나타났다     마을 공동체   어떠한 영향을       이를 위해       공익 연계 
#       22              20               7               5               5               5               4 
#구분한 후           년 월     만족을 얻을 
#       4               4               4





mycorpus.trigram.tdm <- TermDocumentMatrix(mycorpus, control = list(tokenize = trigramTokenizer))
mycorpus.trigram.tdm
trigramlist <- apply(mycorpus.trigram.tdm[,], 1, sum)
sort(trigramlist, decreasing = TRUE) %>% head(10)
#만족을 얻을 수           얻을 수 있다       확인할 수 있었다 경우 기업공익 적합도는           년 월 일부터 
#            4                      4                      4                      3                      3 
#가치지향은 마을 공동체       것이다 이를 위해     규범 변화에 미치는 긍정적인 경우 기업공익 기반으로 본 연구에서는 
#                    2                      2                      2                      2                      2
