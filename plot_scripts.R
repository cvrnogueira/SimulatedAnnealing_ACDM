
library(dplyr)
library(ggplot2)

bkv <- 2792
solucoes <- c(4308, 4289, 4273, 4022, 4314)
desvios <- c(((solucoes[1] -bkv)/bkv), ((solucoes[2] -bkv)/bkv),((solucoes[3] -bkv)/bkv),((solucoes[4] -bkv)/bkv),((solucoes[5] -bkv)/bkv))
dec_temperature <- c(0.6, 0.8, 0.92, 0.96, 0.99)

do.call(rbind, Map(data.frame, desvios=desvios, dec_temperature=dec_temperature)) %>%
ggplot(aes(x = dec_temperature, y=desvios))+ geom_line()+ 
  geom_point(aes(colour= as.factor(dec_temperature),  group=1))+
  geom_text(aes(label = round(dec_temperature, 4), colour= as.factor(dec_temperature)),
            vjust = "inward", hjust = "inward",
            show.legend = FALSE) +
  labs(x = "dec_temperature", y = "Desvio relativo ao BKV")+ 
  theme(panel.background = element_blank(), legend.position = "none")+
  scale_y_continuous(breaks = desvios) 




times <- c(8130.64, 17983.72, 47814.15, 96262.72, 395899.062)
do.call(rbind, Map(data.frame, desvios=times, dec_temperature=dec_temperature)) %>%
  ggplot(aes(x = dec_temperature, y=times))+ geom_line()+ 
  geom_point(aes(colour= as.factor(dec_temperature),  group=1))+
  geom_text(aes(label = round(dec_temperature, 4), colour= as.factor(dec_temperature)),
            vjust = "inward", hjust = "inward",
            show.legend = FALSE) +
  labs(x = "dec_temperature", y = "Tempo de execução em milissegundos")+ 
  theme(panel.background = element_blank(), legend.position = "none")+
  scale_y_continuous(breaks = times) 
  
