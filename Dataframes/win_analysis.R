library (dplyr)
library (readxl)
library (tidyverse)
library (ggplot2)
library(hrbrthemes)

#DATA IMPORTATION                               

all_data = read.csv("C:/Users/josep/Dropbox/Joseph/AgroParisTech/IODAAAAA/Othello_ML/Dataframes/1675265393_final_df.csv", 
                    na = "null", colClasses = c('factor', 'character','character','numeric','character'))

min_max = read.csv("D:/MCTS_generated_games/Dataframes Othello/1675093333_final_df - Copy.csv", 
                   na = "null", colClasses = c('factor', 'character','character','numeric','character'))



all_data_wins = all_data %>%  
                  mutate ( win = case_when(
                            `AI.player` == "0" & substring(`final.score`,2,3) < substring(`final.score`,6,7) ~ 1,
                            `AI.player` == "O" & substring(`final.score`,2,3) > substring(`final.score`,6,7) ~ 1,
                            `AI.player` == "" & substring(`final.score`,2,3) > substring(`final.score`,6,7) ~ 1,
                            `AI.player` == "0" & substring(`final.score`,2,3) > substring(`final.score`,6,7) ~ 0,
                            `AI.player` == "O" & substring(`final.score`,2,3) < substring(`final.score`,6,7) ~ 0,
                            `AI.player` == "" & substring(`final.score`,2,3) < substring(`final.score`,6,7) ~ 0,
                            substring(`final.score`,2,3) == substring(`final.score`,6,7)  ~ 1
                            )
                  )

min_max_wins = min_max %>%  
  mutate ( win = case_when(
    `AI.player` == "0" & substring(`final.score`,2,3) < substring(`final.score`,6,7) ~ 1,
    `AI.player` == "O" & substring(`final.score`,2,3) > substring(`final.score`,6,7) ~ 1,
    `AI.player` == "" & substring(`final.score`,2,3) > substring(`final.score`,6,7) ~ 1,
    `AI.player` == "0" & substring(`final.score`,2,3) > substring(`final.score`,6,7) ~ 0,
    `AI.player` == "O" & substring(`final.score`,2,3) < substring(`final.score`,6,7) ~ 0,
    `AI.player` == "" & substring(`final.score`,2,3) < substring(`final.score`,6,7) ~ 0,
    substring(`final.score`,2,3) == substring(`final.score`,6,7)  ~ 1
  )
  )


print(levels(all_data_wins$Game.type))
print(levels(min_max_wins$Game.type))
# GRAPHS

## Alpha Beta
all_data_alpha = all_data_wins [grepl("^alpha",all_data_wins$Game.type),]
win_alpha_glob = as.numeric(colSums(all_data_alpha[6])/count(all_data_alpha))
time_alpha = as.numeric(colSums(all_data_alpha[4])/count(all_data_alpha))

### Depth 1
data_alpha_depth_1 = all_data_alpha [grepl( "depth 1",all_data_alpha$Game.type),]
win_alpha_depth_1 = as.numeric(colSums(data_alpha_depth_1[6])/count(data_alpha_depth_1))
time_alpha_depth_1 = as.numeric(colSums(data_alpha_depth_1[4])/count(data_alpha_depth_1))

### Depth 2
data_alpha_depth_2 = all_data_alpha [grepl( "depth 2",all_data_alpha$Game.type),]
win_alpha_depth_2 = as.numeric(colSums(data_alpha_depth_2[6])/count(data_alpha_depth_2))
time_alpha_depth_2 = as.numeric(colSums(data_alpha_depth_2[4])/count(data_alpha_depth_2))

### Depth 3
data_alpha_depth_3 = all_data_alpha [grepl( "depth 3",all_data_alpha$Game.type),]
win_alpha_depth_3 = as.numeric(colSums(data_alpha_depth_3[6])/count(data_alpha_depth_3))
time_alpha_depth_3 = as.numeric(colSums(data_alpha_depth_3[4])/count(data_alpha_depth_3))


## Min max
all_data_min = min_max_wins [grepl("min",min_max_wins$Game.type),]
win_min_glob = as.numeric(colSums(all_data_min[6])/count(all_data_min))
time_min = as.numeric(colSums(all_data_min[4])/count(all_data_min))

### depth 1
data_min_depth_1 = all_data_min[grepl("depth 1",all_data_min$Game.type),]
win_min_depth_1 = as.numeric(colSums(data_min_depth_1[6])/count(data_min_depth_1))
time_min_depth_1 = as.numeric(colSums(data_min_depth_1[4])/count(data_min_depth_1))


### depth 2
data_min_depth_2 = all_data_min[grepl("depth 2",all_data_min$Game.type),]
win_min_depth_2 = as.numeric(colSums(data_min_depth_2[6])/count(data_min_depth_2))
time_min_depth_2 = as.numeric(colSums(data_min_depth_2[4])/count(data_min_depth_2))

### depth 3
data_min_depth_3 = all_data_min[grepl("depth 3",all_data_min$Game.type),]
win_min_depth_3 = as.numeric(colSums(data_min_depth_3[6])/count(data_min_depth_3))
time_min_depth_3 = as.numeric(colSums(data_min_depth_3[4])/count(data_min_depth_3))


## MCTS
all_data_mcts = all_data_wins [grepl("^mcts",all_data_wins$Game.type),]
win_mcts = as.numeric(colSums(all_data_mcts[6])/count(all_data_mcts))
time_mcts = as.numeric(colSums(all_data_mcts[4])/count(all_data_mcts))

## PLOTS

# Mean time of execution
data_times <- data.frame(
  name=c(1,2,3) ,  
  value_alpha=c(time_alpha_depth_1,time_alpha_depth_2,time_alpha_depth_3),
  value_min=c(time_min_depth_1,time_min_depth_2,time_min_depth_3),
  value_mcts=c(time_mcts)
)

a = ggplot(data_times, aes(x=name)) + 
  geom_line(data = data_times, aes(y= value_alpha, color='Alpha Beta') ) +
  geom_line(data = data_times, aes(y= value_min, color="Min Max")) +
  labs(title= 'Time complexity of the different algorithms', x = 'Depth', y='Time (ms)')

a + labs(colour = "Algorithms")

# Mean time of execution
data_win <- data.frame(
  name=c(1,2,3),  
  value_alpha=c(win_alpha_depth_1,win_alpha_depth_2,win_alpha_depth_3),
  value_min=c(win_min_depth_1,win_min_depth_2,win_min_depth_3),
  value_mcts=c(win_mcts, win_mcts, win_mcts)
)

a = ggplot(data_win, aes(x=name)) + 
  geom_line(data = data_win, aes(y= value_alpha, color='Alpha Beta') ) +
  geom_line(data = data_win, aes(y= value_min, color="Min Max")) +
  geom_line(data = data_win, aes(y= value_mcts, color="MCTS")) +
  labs(title= 'Win pourcentage of the different algorithms', x = 'Depth', y='Time (ms)')

a + labs(colour = "Algorithms")






