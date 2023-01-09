library (dplyr)
library (readxl)
library (tidyverse)

all_data = read.csv("C:/Users/joseph/Dropbox/Joseph/AgroParisTech/IODAAAAA/Othello_ML/Dataframes/1672340024_final_df.csv", 
                    na = "null", colClasses = c('factor', 'character','character','numeric','character'))

all_data_wins = all_data %>%  
                  mutate ( win = case_when(
                            `AI.player` == "0" & substring(`final.score`,2,3) < substring(`final.score`,6,7) ~ 1,
                            `AI.player` == "O" & substring(`final.score`,2,3) > substring(`final.score`,6,7) ~ 1,
                            `AI.player` == "" & substring(`final.score`,2,3) > substring(`final.score`,6,7) ~ 1,
                            `AI.player` == "0" & substring(`final.score`,2,3) > substring(`final.score`,6,7) ~ 0,
                            `AI.player` == "O" & substring(`final.score`,2,3) < substring(`final.score`,6,7) ~ 0,
                            `AI.player` == "" & substring(`final.score`,2,3) < substring(`final.score`,6,7) ~ 0
                            )
                  )

all_data_mcts = all_data_wins [all_data_wins$`Game.type` == "mcts vs random",]
all_data_alpha = all_data_wins [grepl("^alpha beta vs random",all_data_wins$Game.type),]
all_data_min = all_data_wins [grepl("^min max vs random",all_data_wins$Game.type),]
all_data_random = all_data_wins [all_data_wins$Game.type == "random vs random",]

#####

all_data_mcts_good = read.csv("C:/Users/joseph/Dropbox/Joseph/AgroParisTech/IODAAAAA/Othello_ML/Dataframes/1672430492_games_data-mcts-test.csv", 
                    na = "null", colClasses = c('factor', 'character','character','numeric','character'))

all_data_mcts_good = all_data_mcts_good %>%  
  mutate ( win = case_when(
    `AI.player` == "0" & substring(`final.score`,2,3) < substring(`final.score`,6,7) ~ 1,
    `AI.player` == "O" & substring(`final.score`,2,3) > substring(`final.score`,6,7) ~ 1,
    `AI.player` == "" & substring(`final.score`,2,3) > substring(`final.score`,6,7) ~ 1,
    `AI.player` == "0" & substring(`final.score`,2,3) > substring(`final.score`,6,7) ~ 0,
    `AI.player` == "O" & substring(`final.score`,2,3) < substring(`final.score`,6,7) ~ 0,
    `AI.player` == "" & substring(`final.score`,2,3) < substring(`final.score`,6,7) ~ 0,
    substring(`final.score`,2,3) == substring(`final.score`,6,7) ~ 1
  )
  )

win_pourc = as.numeric(colSums(all_data_mcts_good[6])/count(all_data_mcts_good))

###

data_mcts_mac = read.csv("C:/Users/joseph/Downloads/1672460512_games_data-mcts-test-mac.csv", 
                              na = "null", colClasses = c('factor', 'character','character','numeric','character'))

data_mcts_mac = data_mcts_mac %>%  
  mutate ( win = case_when(
    `AI.player` == "0" & substring(`final.score`,2,3) < substring(`final.score`,6,7) ~ 1,
    `AI.player` == "O" & substring(`final.score`,2,3) > substring(`final.score`,6,7) ~ 1,
    `AI.player` == "" & substring(`final.score`,2,3) > substring(`final.score`,6,7) ~ 1,
    `AI.player` == "0" & substring(`final.score`,2,3) > substring(`final.score`,6,7) ~ 0,
    `AI.player` == "O" & substring(`final.score`,2,3) < substring(`final.score`,6,7) ~ 0,
    `AI.player` == "" & substring(`final.score`,2,3) < substring(`final.score`,6,7) ~ 0,
    substring(`final.score`,2,3) == substring(`final.score`,6,7) ~ 1
  )
  )

win_pourc_100_2 = as.numeric(colSums(data_mcts_mac[6])/count(data_mcts_mac))


