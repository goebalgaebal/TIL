#Q1. r_wiki 데이터에서 "so" 추출
r_wiki <- "R is a programming language and software environment for statistical computing and graphics supported by the R Foundation for Statistical Computing. The R language is widely used among statisticians and data miners for developing statistical software and data analysis. Polls, surveys of data miners, and studies of scholarly literature databases show that R's popularity has increased substantially in recent years.
R is a GNU package. The source code for the R software environment is written primarily in C, Fortran, and R. R is freely available under the GNU General Public License, and pre-compiled binary versions are provided for various operating systems. While R has a command line interface, there are several graphical front-ends available."

str_extract_all(r_wiki, "(s|S)o", simplify = T)
#     [,1] [,2] [,3] [,4]
#[1,] "so" "so" "so" "so"

str_extract_all(r_wiki, "(s|S)o[[:alpha:]]{0,}", simplify = T)
#           [,1]       [,2]       [,3]     [,4]      
#[1,] "software" "software" "source" "software"

mypattern <- gregexpr("(s|S)o[[:alpha:]]{0,}", r_wiki) 
so.words <- regmatches(r_wiki, mypattern)
table(unlist(so.words))
#software   source 
#       3        1
