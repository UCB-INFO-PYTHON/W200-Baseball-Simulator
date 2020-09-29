# W200-Baseball-Simulator

Author: Amanda Smith\
Semester: Summer 2020\
Contact: amandasmith@ischool.berkeley.edu

**The game:**\ 
You’re the general manager for an MLB team, and it's not going well. Fans are losing hope and you are close to losing your job. The owner makes a snide remark that the team would probably do better if they batted while blindfolded. You decide it’s worth a shot. In this game, users will play as the MLB team of their choice and the goal is to score as many runs as possible. However, they have to bat while “blindfolded,” meaning the user will choose whether the player swings at or watches the pitch before it is thrown. Then, odds will determine whether it was a successful choice.

**File Structure:**\
Download the Smith_BaseballSim.py, help.txt, instructions.txt, and Baseball simulator.xlsx files from GitHub, into the same folder. Use the terminal to run Smith_BaseballSim.py. The additional files contain text for the intro and help screens, as well as the batter and team data to make the program run.

**How to play:**\
The main instructions are printed when the program loads on the welcome screen. The basic premise is that you will simulate a baseball game by choosing [s]wing or [w]atch before every pitch is thrown. The odds of making contact and to what extent are determined by actual MLB player results from 2003-2013 (not calculated by me). The main steps are:
1. Choose length of game (number of innings).
2. Select an MLB team to play as. As described in the game, please type the team without the city. To see a
list of all teams, access the [h]elp screen.
3. Choose your lineup (between 5 and 9 players) from players with at least 50 plate appearances.
4. Enter a name for your opponent.
5. The game will start and simulate the top of the inning for the other team.
6. Select [s]wing or [w]atch for each pitch.
a. The count will update after each pitch.
b. When the player either makes contact, strikes out, or walks, a description of the outcome will
print.
c. The field will print with updated runner positions at the start of each at bat.
7. Play until you run out of innings.
a. If the game is tied at the end, you can choose to extend it one inning at a time.
8. View score and player stats.
All inputs are coded so the user can always access the [h]elp or [q]uit options. While error checking, I set up as many defaults as possible so that in case of user error, the game can continue. For example, the game will default to 9 innings, the Orioles, and the first 9 batters listed.


**Reflection:**\
I chose this project topic because not only do I find baseball data interesting, it's also really accessible and prolific. I wanted to take advantage of the specificity of the game as an opportunity to work on coding a somewhat repetitive experience that still produced unique, fresh outcomes.

Overall, I'm happy with the customization and options I created. I was able to include the option of selecting any MLB team and using unique odds for every player, and different outcomes include walk, strike out, out in play, single, double, triple, home run. I was also able to create unique out scenarios—is the lead runner or the batter out in the play? If first base is empty on a walk, the other runners won’t move, etc. If I had more time I would add more user options like bunt or steal. I would also let users pick an MLB opponent from the dataset of pitchers, and find unique odds for each batter/pitcher matchup.

Modularizing my code was difficult because I found a lot of scenarios were unique to specific cases. I also think I stuck too closely to my original pseudocode (which was written with a poorer understanding of how classes work and interact) which contributed to lengthy/inefficient code. My program ended up a lot longer than I anticipated and I can’t tell how much of that was because I “took the scenic route” for some of my functions. I worked on this by looking for code that was repeated throughout my program and writing new functions for it, even if it seemed short. This was how I got the check_count(), send_to_dugout(), update_stats(), and clear_bases() functions. I’m also proud of my help_quit() function, which allows for repeat requests for the help or quit options.
