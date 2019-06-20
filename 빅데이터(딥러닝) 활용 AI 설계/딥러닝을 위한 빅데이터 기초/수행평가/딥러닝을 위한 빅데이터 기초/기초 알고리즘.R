# [기초 알고리즘]
# mpg 데이터를 이용해서 분석 문제를 해결해보세요.
# mpg 데이터는 연비를 나타내는 변수가 hwy(고속도로 연비), cty(도시 연비) 두 종류로 분리되어 있습니다. 두 변수를 각각 활용하는 대신 하나의 통합 연비 변수를 만들어 분석하려고 합니다. 

library(ggplot2) # 내장된 mpg 데이터를 활용하기 위해 package 사용
library(dplyr)

# • Q1. mpg 데이터 복사본을 만들고, cty와 hwy를 더한 '합산 연비 변수'를 추가하세요. 
mpg.copy <- mpg
mpg.copy <- mpg.copy %>% 
  mutate(tot = cty + hwy)

# • Q2. 앞에서 만든 '합산 연비 변수'를 2로 나눠 '평균 연비 변수'를 추가세요. 
mpg.copy <- mpg.copy %>% 
  mutate(mean.tot = tot / 2)

# • Q3. '평균 연비 변수'가 가장 높은 자동차 3종의 데이터를 출력하세요. 
mpg.copy %>% 
  arrange(desc(mean.tot)) %>% 
  head(3)
