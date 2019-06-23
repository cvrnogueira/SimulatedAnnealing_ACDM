library(dplyr)
library(ggplot2)

bkv <- 2792
solucoes <- c(4861.0, 4310.0, 4310.0)
desvios <- c(((solucoes[1] -bkv)/bkv), ((solucoes[2] -bkv)/bkv),((solucoes[3] -bkv)/bkv))
temperatura <- c(1, 0.1, 0.01)
do.call(rbind, Map(data.frame, desvios=desvios, temperatura=temperatura)) %>%
  ggplot(aes(x = temperatura, y=desvios))+ geom_line()+ 
  geom_point(aes(colour= as.factor(temperatura),  group=1))+
  geom_text(aes(label = round(desvios, 4), colour= as.factor(desvios)),
            vjust = "inward", hjust = "inward",
            show.legend = FALSE) +
  labs(x = "temperatura", y = "Desvio relativo ao BKV")+ 
  theme(panel.background = element_blank(), legend.position = "none")+
  scale_y_continuous(breaks = desvios) 


times <- c(49894.3, 74212.9, 99017.9)
do.call(rbind, Map(data.frame, times=times, temperatura=temperatura)) %>%
  ggplot(aes(x = temperatura, y=times))+ geom_line()+ 
  geom_point(aes(colour= as.factor(temperatura),  group=1))+
  geom_text(aes(label = round(temperatura, 4), colour= as.factor(temperatura)),
            vjust = "inward", hjust = "inward",
            show.legend = FALSE) +
  labs(x = "temperatura", y = "Tempo de execução em milissegundos")+ 
  theme(panel.background = element_blank(), legend.position = "none")+
  scale_y_continuous(breaks = times) 
