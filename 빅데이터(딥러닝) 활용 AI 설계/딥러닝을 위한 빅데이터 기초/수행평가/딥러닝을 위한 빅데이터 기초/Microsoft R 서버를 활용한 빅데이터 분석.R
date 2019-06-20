# [Microsoft R 서버를 활용한 빅데이터 분석]
# mpg 데이터를 이용해서 분석 문제를 해결해보세요. 
# 
library(ggplot2)
library(dplyr)
# • Q1. mpg 데이터의 class는 "suv", "compact" 등 자동차를 특징에 따라 일곱 종류로 분류한 변수입니다. 어떤 차종의 연비가 높은지 비교해보려고 합니다. class별 cty 평균을 구해보세요.
mpg.copy <- mpg
mpg.copy %>% 
  group_by(class) %>% 
  summarise(mean.cty = mean(cty))

# • Q2. 앞 문제의 출력 결과는 class 값 알파벳 순으로 정렬되어 있습니다. 어떤 차종의 도시 연비가 높은지 쉽게 알아볼 수 있도록 cty 평균이 높은 순으로 정렬해 출력하세요. 
mpg.copy %>% 
  group_by(class) %>% 
  summarise(mean.cty = mean(cty)) %>% 
  arrange(desc(mean.cty))

# • Q3. 어떤 회사 자동차의 hwy(고속도로 연비)가 가장 높은지 알아보려고 합니다. hwy 평균이 가장 높은 회사 세 곳을 출력하세요. 
mpg.copy %>% 
  group_by(manufacturer) %>% 
  summarise(mean.hwy = mean(hwy)) %>% 
  arrange(desc(mean.hwy)) %>% 
  head(3)

# • Q4. 어떤 회사에서 "compact"(경차) 차종을 가장 많이 생산하는지 알아보려고 합니다. 각 회사별 "compact" 차종 수를 내림차순으로 정렬해 출력하세요. 
mpg.copy %>% 
  filter(class == "compact") %>% 
  group_by(manufacturer) %>% 
  summarise(cnt.compact = n()) %>% 
  arrange(desc(cnt.compact))
