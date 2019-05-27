#Q1.mysentences에서 stat~로 시작되는 표현 추출
R_wiki <- "R is a programming language and software environment for statistical computing and graphics supported by the R Foundation for Statistical Computing. The R language is widely used among statisticians and data miners for developing statistical software and data analysis. Polls, surveys of data miners, and studies of scholarly literature databases show that R's popularity has increased substantially in recent years.
R is a GNU package. The source code for the R software environment is written primarily in C, Fortran, and R. R is freely available under the GNU General Public License, and pre-compiled binary versions are provided for various operating systems. While R has a command line interface, there are several graphical front-ends available."

r_wiki_para <- strsplit(R_wiki, split = "\n")
r_wiki_sent <- strsplit(r_wiki_para[[1]], split = "\\. ")
mysentences <- unlist(r_wiki_sent)

mypattern <- gregexpr("(stat)[[:alpha:]]+", tolower(mysentences))
mypattern
# [[1]]
# [1]  58 127
# attr(,"match.length")
# [1] 11 11
# attr(,"index.type")
# [1] "chars"
# attr(,"useBytes")
# [1] TRUE
# 
# [[2]]
# [1] 37 82
# attr(,"match.length")
# [1] 13 11
# attr(,"index.type")
# [1] "chars"
# attr(,"useBytes")
# [1] TRUE
# 
# [[3]]
# [1] -1
# attr(,"match.length")
# [1] -1
# attr(,"index.type")
# [1] "chars"
# attr(,"useBytes")
# [1] TRUE
# 
# [[4]]
# [1] -1
# attr(,"match.length")
# [1] -1
# attr(,"index.type")
# [1] "chars"
# attr(,"useBytes")
# [1] TRUE
# 
# [[5]]
# [1] -1
# attr(,"match.length")
# [1] -1
# attr(,"index.type")
# [1] "chars"
# attr(,"useBytes")
# [1] TRUE
# 
# [[6]]
# [1] -1
# attr(,"match.length")
# [1] -1
# attr(,"index.type")
# [1] "chars"
# attr(,"useBytes")
# [1] TRUE
# 
# [[7]]
# [1] -1
# attr(,"match.length")
# [1] -1
# attr(,"index.type")
# [1] "chars"
# attr(,"useBytes")
# [1] TRUE
mystats <- regmatches(mysentences, mypattern)
unlist(mystats)
table(unlist(mystats))

#statistical   Statistical statisticians 
#         2             1             1 

#Q2. 가장 많이 사용된 단어?
mywords <- unlist(strsplit(mysentences, split = " "))
wordfreq <- tapply(rep(1, length(mywords)), mywords, sum)
wordfreq[order(-wordfreq)[1]]
#R 
#8 


#Q3. 총 몇 개의 알파벳 문자가 쓰였을까?
#특수문자 제거
myletters <- gsub("\\W", "", mywords)
myletters <- unlist(strsplit(myletters, split = ""))
table(myletters)
# a  b  c  C  d  e  f  F  g  G  h  i  k  l  L  m  n  N  o  p  P  r  R  s  S  t  T  u  U  v  w  W  y 
#71  7 18  2 25 61 13  2 14  3 14 50  1 29  1 14 44  2 34 16  2 46  9 49  1 45  2 16  2 10  6  1 12 
length(unique(myletters))
#대문자라면 33개

#총 글자수
sum(table(myletters))
#[1] 622

myletters <- tolower(myletters)
table(myletters)
# a  b  c  d  e  f  g  h  i  k  l  m  n  o  p  r  s  t  u  v  w  y 
#71  7 20 25 61 15 17 14 50  1 30 14 46 34 18 55 50 47 18 10  7 12 
length(unique(myletters)
#소문자라면 22개


#Q4. 가장 많이 사용된 알파벳 문자는?
letterfreq <- tapply(rep(1, length(myletters)), myletters, sum)
letterfreq[order(-letterfreq)[1]]
# a 
#71


df.letterfreq <- as.data.frame(table(unlist(myletters)))
df.letterfreq <- rename(df.letterfreq, "Alphabet" = "Var1")
df.letterfreq

df.letterfreq %>%  
  arrange(desc(Freq)) %>% 
  head(1)
#  Alphabet Freq
#1        a   71


#Q5. 4번 결과를 시각화
library(ggplot2)
ggplot(data = df.letterfreq, aes(x = reorder(Alphabet, Freq), y = Freq)) +
  geom_col()

