library(dplyr)
library(ggplot2)

bkv <- 2792
solucoes <- c(4861.0, 4425.0, 4310.0, 4310.0)
desvios <- c(((solucoes[1] -bkv)/bkv), ((solucoes[2] -bkv)/bkv),((solucoes[3] -bkv)/bkv),((solucoes[4] -bkv)/bkv))

do.call(rbind, Map(data.frame, desvios=desvios, nro_iteracoes=nro_iteracoes)) %>%
  ggplot(aes(x = nro_iteracoes, y=desvios))+ geom_line()+ 
  geom_point(aes(colour= as.factor(nro_iteracoes),  group=1))+
  geom_text(aes(label = round(desvios, 4), colour= as.factor(desvios)),
            vjust = "inward", hjust = "inward",
            show.legend = FALSE) +
  labs(x = "nro_iteracoes", y = "Desvio relativo ao BKV")+ 
  theme(panel.background = element_blank(), legend.position = "none")+
  scale_y_continuous(breaks = desvios) 


times <- c(49102.4, 99670.49, 193752.17, 293276.42)
do.call(rbind, Map(data.frame, times=times, nro_iteracoes=nro_iteracoes)) %>%
  ggplot(aes(x = nro_iteracoes, y=times))+ geom_line()+ 
  geom_point(aes(colour= as.factor(nro_iteracoes),  group=1))+
  geom_text(aes(label = round(nro_iteracoes, 4), colour= as.factor(nro_iteracoes)),
            vjust = "inward", hjust = "inward",
            show.legend = FALSE) +
  labs(x = "nro_iteracoes", y = "Tempo de execução em milissegundos")+ 
  theme(panel.background = element_blank(), legend.position = "none")+
  scale_y_continuous(breaks = times) 
