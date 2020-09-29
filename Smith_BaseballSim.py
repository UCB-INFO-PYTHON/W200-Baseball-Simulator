import random
import pandas as pd
import sys

# To bold text in certain print statements.
start = "\033[1m"
end = "\033[0;0m"

class Files:
    """
    Class to load data into the program.

    Attributes:
        welcome (txt): Welcome screen text.
        help (txt): Help screen text.
        data (xlsx): Batter odds data.
    """
    def __init__(self, players="Baseball simulator.xlsx", welcome_file=\
                "instructions.txt", help_file="help.txt"):
        """
        Constructor for Files class.

        Parameters:
            players (xlsx): Name of batter odds spreadsheet
            welcome_file (txt): Name of welcome text file.
            help_file (txt): Name of help text file.
        """
        file = open(welcome_file)
        welcome = file.read()
        file.close()
        self.welcome = welcome
        file2 = open(help_file)
        help = file2.read()
        file2.close()
        self.help = help
        excel_file = players
        data = pd.read_excel(excel_file)
        self.data = data

    def __repr__(self):
        """Returns names of each file in class."""
        return ("{welcome file: " + str(self.welcome) + ", help file: " + \
                str(self.help) + ", data file: " + str(self.data) + "}")

class Pitcher:
    """
    This is a class for throwing pitches.

    Attributes:
        name (str): The name of the pitcher.
    """

    def __init__(self, name, field):
        """The constructor for Pitcher class."""
        self.name = name
        field.bullpen.append(self)

    def __repr__(self):
        """Returns Pitcher: Name."""
        return ("{Pitcher: " + self.name + "}")

    def throw_pitch(self, atbat):
        """
        The function to create a pitch using a random number generator.

        Parameters:
            atbat (obj): An instance of the AtBat class.

        Returns:
            (str): "Ball" or "Strike"
        """
        pitch = random.randrange(0,2)
        if pitch == 0:
            return 'Ball'
        else:
            return 'Strike'


class Batter:
    """
    Class to create MLB players capable of batting and running bases.

    Attributes:
        name (str): Player's name.
        atbats (int): Number of plate appearances that end in a hit or out.
        hits (int): Number of hits player has.
        rbis (int): Number of runs batted in by player.
        odds (dict): Player-specific odds of different at bat outcomes.
    """

    def __init__(self, name, single, double, triple, hr, walk, k, hbp, oip):
        """
        Constructor function for Batter class.

        Parameters:
            name (str): Batter name.
            single (float): % of batter's at bats that end in a single.
            double (float): % of batter's at bats that end in a double.
            triple (float): % of batter's at bats that end in a triple.
            hr (float): % of batter's at bats that end in a home run.
            walk (float): % of batter's at bats that end in a walk.
            k (float): % of batter's at bats that end in a strike out.
            hbp (float): % of batter's at bats ending in hit by the pitch.
            oip (float): % of batter's at bats ending in an out during a play.
        """
        self.name = name
        self.atbats = 0
        self.hits = 0
        self.rbis = 0
        self.odds = {
            "1B" : single,
            "2B" : double,
            "3B" : triple,
            "HR" : hr,
            "BB" : walk,
            "HBP" : hbp,
            "OIP" : oip,
            "K" : k,
            # The total of potential outcomes if a batter swings.
            "SWING" : single
                      + double
                      + triple
                      + hr
                      + oip
                      + k
        }

    def __repr__(self):
        """Returns batter name (str)."""
        return self.name


class AtBat:
    """
    Class to create a new at bat for a batter, manage the count, and handle
    the batter's odds for each outcome.

    Attributes:
        batter (obj): The Batter object at bat.
        status (str): Indicates if the at bat is in progress and the outcome.
        balls (int): Pitch count, balls.
        strikes (int): Pitch count, strikes.
    """

    def __init__(self, batter, field):
        """
        Constructor for AtBat class.

        Parameters:
            batter (obj): Instance from Batter class.
            field (obj): Instance from Field class.
        """
        self.batter = batter
        self.status = "Batting"
        self.balls = 0
        self.strikes = 0
        # Set the batters base equal to 0 (at the plate).
        field.bases[batter] = 0
        # Remove the batter from the dugout so they have no duplicates.
        field.dugout.remove(batter)

    def __repr__(self):
        """Returns the count of the at bat: 'X balls, Y strikes.'"""
        return (str(atbat.balls) + " balls, " + str(atbat.strikes) +
              " strikes.\n")

    def check_count(self):
        """Checks the pitch count and updates status if necessary."""
        if self.strikes >= 3:
            self.status = "Strike out"
        elif self.balls >= 4:
            self.status = "Walk"

    def swing(self):
        """
        Function to determine the outcome when a batter swings at a pitch.

        Returns:
            self.status (str): "Batting" if the at bat still in progress, or
            a new outcome.
        """
        # Potentials are floats between 0 and the total of all swing options.
        x = random.uniform(0,self.batter.odds["SWING"])
        # Check to see where x falls among the options.
        # Update the count and status accordingly.
        if x <= self.batter.odds["K"]:
            self.strikes += 1
            self.status = "Batting"
            prints = ["Whiff! That's a strike.", "A swing and a miss. Strike!"]
            print(random.choice(prints))
            self.check_count()
        elif x <= self.batter.odds["K"]\
                + self.batter.odds["OIP"]:
            self.status = "Out in play"
        elif x <= self.batter.odds["K"]\
                + self.batter.odds["OIP"]\
                + self.batter.odds["HR"]:
            self.status = "Home run"
        elif x <= self.batter.odds["K"]\
                + self.batter.odds["OIP"]\
                + self.batter.odds["HR"]\
                + self.batter.odds["1B"]:
            self.status = "Single"
        elif x <= self.batter.odds["K"]\
                + self.batter.odds["OIP"]\
                + self.batter.odds["HR"]\
                + self.batter.odds["1B"]\
                + self.batter.odds["2B"]:
            self.status = "Double"
        else:
            self.status = "Triple"
        return self.status

    def watch(self, pitch):
        """
        Function to determine the outcome when a batter watches the pitch.

        Parameters:
            pitch (str): The return a Pitcher.throw_pitch(AtBat)

        Returns:
            self.status (str): "Batting" if the at bat still in progress, or
            a new outcome.
        """
        if pitch == "Ball":
            prints = ["Good eye! It was a ball.", "Ball! Good job.",
                      "Way to hold - ball!"]
            print(random.choice(prints))
            self.balls += 1
            self.check_count()
        else:
            prints = ["Strike!", "Darn, you watched a perfect strike!",
                      "Right down the middle - strike!"]
            print(random.choice(prints))
            self.strikes += 1
            self.check_count()
        return self.status

    def send_to_dugout(self, runner, field):
        """Function to remove runner from field and add to dugout."""
        field.dugout.append(runner)
        del field.bases[runner]

    def update_stats(self, scoreboard, hit, out, at_bat):
        """
        Updates player stats and scoreboard based on outcome.

        Parameters:
            scoreboard (obj): Instance from Scoreboard class.
            hit (bool): True if there was a hit.
            out (bool): True if there was an out.
            at_bat (bool): True if counts as an at bat.
        """
        if hit == True:
            self.batter.hits += 1
        if out == True:
            scoreboard.outs += 1
        if at_bat == True:
            self.batter.atbats +=1

    def outcome_machine(self, field, scoreboard):
        """
        Function that updates player stats, the scoreboard, and the field
        based on the outcome of the at bat.

        Parameters:
            field (obj): Instance from Field class.
            scoreboard (obj): Instance from Scoreboard class.
        """
        if self.status == "Strike out":
            self.update_stats(scoreboard, False, True, True)
            self.send_to_dugout(self.batter, field)
            print("\nThat's 3. " + self.batter.name + " strikes out.")
        elif self.status == "Walk":
            # Check to see if there is a runner on first already.
            no_first = True
            for item in field.bases:
                if field.bases[item] != 1:
                    no_first = True
                    continue
                else:
                    no_first = False
                    break
            # If no one on first, the batter gets a base but runners stay put.
            if no_first == True:
                field.bases[self.batter] += 1
                print("\nThat's 4 balls. " + self.batter.name + " takes the" +
                      " empty spot at first base.")
            # If a runner is already on first, everyone moves one base.
            else:
                print("\nThat's 4 balls - take a walk.")
                field.advance_runners(1, scoreboard, self.batter, True)
        elif self.status == "Single":
            print(self.batter.name + " gets a single through the infield!")
            self.update_stats(scoreboard, True, False, True)
            field.advance_runners(1, scoreboard, self.batter)
        elif self.status == "Double":
            print(self.batter.name + " finds a gap and hits a double!")
            self.update_stats(scoreboard, True, False, True)
            field.advance_runners(2, scoreboard, self.batter)
        elif self.status == "Triple":
            print(self.batter.name + " hits it to the fence for a triple!")
            self.update_stats(scoreboard, True, False, True)
            field.advance_runners(3, scoreboard, self.batter)
        elif self.status == "Home run":
            print(self.batter.name + " sends it out of the park! HOME RUN!")
            self.update_stats(scoreboard, True, False, True)
            field.advance_runners(4, scoreboard, self.batter)
        elif self.status == "Out in play":
            self.update_stats(scoreboard, False, True, True)
            # To determine which runner is out in the play.
            whos_out = random.randrange(0,3)
            # If the batter is the only runner, they hit into an out at first.
            if len(field.bases) < 2 or scoreboard.outs == 3:
                print(self.batter.name + " hits into an out at first.")
                self.send_to_dugout(self.batter, field)
            # If the random number is 2, the out is at first.
            elif whos_out > 1:
                print(self.batter.name + " hits into an out at first, but" +
                      " the runners advance.")
                field.advance_runners(1, scoreboard, self.batter)
                self.send_to_dugout(self.batter, field)
            # It's more likely in baseball to get the lead runner.
            # If random number is 0 or 1, the lead runner (not batter) is out.
            else:
                print(self.batter.name + " hits into a play, and the lead" +
                      " runner is out.")
                lead_runner = max(field.bases, key=field.bases.get)
                self.send_to_dugout(lead_runner, field)
                field.advance_runners(1, scoreboard, self.batter)


class Field:
    """
    Class to manage location of players.

    Attributes:
        dugout (list): Holds Batter objects not on base.
        bullpen (list): Holds Pitcher objects not currently pitching.
        bases (dict): Keys are Batter objects, value is base they are on.
    """

    def __init__(self):
        """Constructor for Field class; creates an empty field."""
        self.dugout = []
        self.bullpen = []
        self.bases = {}

    def __repr__(self):
        """Returns (str) # of batters in dugout and # on base."""
        print(str(len(self.dugout)) + " batters in the dugout.")
        print(str(len(self.bases)) + " batters on base.")

    def print_field(self, bases, scoreboard):
        """
        Function to print visual representation of the base runners and inning.

        Parameters:
            bases (dict): self.bases dictionary.
            scoreboard (obj): Instance of Scoreboard class.
        """
        # Define variables we'll be using.
        home = False
        first = False
        second = False
        third = False
        # Check dictionary and assign runners to the variable matching value.
        # This was how I got around dictionaries being unordered.
        for runner in bases:
            if bases[runner] == 0:
                home = runner
            elif bases[runner] == 1:
                first = runner
            elif bases[runner] == 2:
                second = runner
            elif bases[runner] == 3:
                third = runner
            else:
                continue
        # Print the top border, inning number and outs above the field.
        print("_" * 80)
        print(start + "\nInning: " + end + str(scoreboard.inning))
        print(start + "Outs: " + end + str(scoreboard.outs) + "\n")
        # The field is printed in 9 rows.
        for r in range(0, 9):
            # The first row holds 2nd base.
            if r == 0:
                # If someone is on second, print row with their name.
                if second != False:
                    print('{:^80s}'.format(start + "2nd: " + end + \
                          second.name))
                # Otherwise, print 2nd as empty.
                else:
                    print('{:^80s}'.format(start + "2nd: " + end))
            # Row holding 3rd and 1st base.
            elif r == 4:
                if third != False and first != False:
                    print('{:<72s}'.format(start + "3rd: " + end + third.name)\
                         + '{:>0s}'.format(start + "1st: " + end + first.name))
                elif third != False:
                    print('{:<80s}'.format(start + "3rd: " + end + third.name)\
                         + '{:>0s}'.format(start + "1st: " + end))
                elif first != False:
                    print('{:<72s}'.format(start + "3rd: " + end) + '{:>0s}'.\
                          format(start + "1st: " + end + first.name))
                else:
                    print('{:<80s}'.format(start + "3rd: " + end) + '{:>0s}'.\
                          format(start + "1st: " + end))
            # Home plate row.
            elif r == 8:
                print('{:^80s}'.format(start + "Up next: " + end + self.dugout\
                      [0].name))
            # Other rows are blank for spacing.
            else:
                print()
        print("_" * 80)

    def advance_runners(self, value, scoreboard, batter, walk=False):
        """
        Function move runners around the bases.

        Parameters:
            value (int): Number of bases everyone needs to move.
            scoreboard (obj): Instance of Scoreboard class.
            batter (obj): Instance of Batter class; batter who triggered
                          movement.
            walk (bool): True if the Batter walked.
        """
        to_remove = []
        for base in self.bases:
            self.bases[base] += value
            # If they reach 4, they scored.
            if self.bases[base] > 3:
                scoreboard.runs += 1
                print(".\n.\n.\n" + base.name + " scores!")
                # If they reached 4 and it is not from a walk, the batter gets
                # an RBI.
                if walk == False:
                    batter.rbis += 1
                # Add runners who scored back to dugout.
                self.dugout.append(base)
                to_remove.append(base)
        # Go back through runners who scored and delete them from bases.
        # This is a seperate part because the length of the dict can't change
        # during the loop above.
        for item in to_remove:
            del self.bases[item]

    def clear_bases(self):
        """Function to remove all runners from bases and add them to dugout."""
        to_remove = []
        for base in self.bases:
            self.dugout.append(base)
            to_remove.append(base)
        for item in to_remove:
            del self.bases[item]

class Scoreboard:
    """
    Class to manage game stats, batting order and the opponent.

    Attributes:
        outs (int): Number of outs in current inning.
        runs (int): Runs scored by user's team.
        opponentruns (int): Runs scored by opposing team.
        opponent (str): Name of opposing team.
        home (str): Name of home team.
        inning (int): Current inning of game.
        max (int): User defined length of game (in innings).
    """

    def __init__(self, game):
        """Constructor for Scoreboard class."""
        self.outs = 0
        self.runs = 0
        self.opponentruns = 0
        self.opponent = ''
        self.home = ''
        self.inning = 1
        # Error check user input for the length of the game.
        try:
            self.max = int(game.help_quit("How many innings do you want to" +
                           " play? "))
        except ValueError:
            print("That's not a valid number. Let's go with 9.")
            self.max = 9

    def __repr__(self):
        """Returns score of the game (Opponent: runs, User: runs)"""
        return (self.opponent + ': ' + str(self.opponentruns) + "\n" +
                self.home + ': ' + str(self.runs))

    def default_order(self, field, lineup):
        """
        Sets the order to the first 9 players in case of user error.

        Parameters:
            field (obj): Instance of Field class.
            lineup (lst): List of player objects based on MLB data.
        """
        print("We're going to default to the first nine players...")
        field.dugout = []
        order_list = [0,1,2,3,4,5,6,7,8]
        for number in order_list:
            field.dugout.append(lineup[int(number)])

    def batting_order(self, lineup, field, game):
        """
        Allows the user to select which players they want on their team.

        Parameters:
            lineup (lst): List of player objects based on MLB data.
            field (obj): Instance of Field class.
            game (obj): Instance of Engine class.
        """
        # Show the user player options.
        for player in lineup:
            print('{:^80s}'.format(f"{str(lineup.index(player))}: " +
                  f"{player.name}"))
        order = game.help_quit("\nTime to pick the batting order. Using the" +\
                               " numbers above, enter the order you \nwould" +\
                               " like players to bat as a set of numbers" +\
                               " separated by commas. Choose \nbetween 5 and" +
                               " 9 batters. Example: 1,5,10,7,2\n")
        order_list = order.split(",")
        # Check number of players.
        if len(order_list) < 5:
            print("You did not select enough players. You need at" +
                        " least 5.")
            self.default_order(field, lineup)
        elif len(order_list) > 9:
            print("You selected more than 9 batters.")
            self.default_order(field, lineup)
        # Check for duplicates.
        elif len(order_list) != len(set(order_list)):
            print("There was a duplicate somewhere. We'll set you up with " + \
                  "the first 9 batters.")
            self.default_order(field, lineup)
        else:
            # Try and append them all to dugout.
            try:
                for number in order_list:
                    field.dugout.append(lineup[int(number)])
            # Check for validity of choices.
            except IndexError:
                print("You typed a number outside the range of potential " + \
                      "batters. We'll set you up with the first 9 batters.")
                self.default_order(field, lineup)
            # Check for valid characters.
            except ValueError:
                print("It looks like you typed an invalid character. We'll " +\
                      "set you up with the first 9 batters.")
                self.default_order(field, lineup)
        # Show user their lineup.
        count = 1
        print("\nGreat job coach! Here's your lineup:")
        for x in field.dugout:
            print(str(count) + ". " + x.name)
            count += 1

    def other_team(self):
        """
        Simulates opposing team's performance at top of each inning.

        Returns:
            (str): The 'opponent' scored 'x' runs at the top of inning '#.'
        """
        x = random.uniform(0,1)
        # Odds: https://gregstoll.com/~gregstoll/baseball/runsperinning.html
        if x <= .7315:
            return ("The " + self.opponent + " scored 0 runs at the" +
                   " top of inning " + str(self.inning) + ".")
        elif x <= .8782:
            self.opponentruns += 1
            return ("The " + self.opponent + " scored 1 run at the" +
                   " top of inning " + str(self.inning) + ".")
        elif x <= .9455:
            self.opponentruns += 2
            return ("The " + self.opponent + " scored 2 runs at the" +
                   " top of inning " + str(self.inning) + ".")
        else:
            self.opponentruns += 3
            return ("The " + self.opponent + " scored 3 runs at the" +
                   " top of inning " + str(self.inning) + ".")

    def box_score(self, players):
        """
        Prints the box score (each player's stats).

        Parameters:
            players (obj): List of Batter objects.
        """
        print(start + "\nBox score:" + end)
        for player in players:
            print(player.name + ", " + str(player.hits) + " for " + \
                  str(player.atbats) + ", " + str(player.rbis) + " RBIs")

    def pick_opponent(self, game):
        """Let's user name the opposing team; checks for unique string."""
        self.opponent = str(game.help_quit("\nOne more thing! Enter a name" +
                                             " for the opposing team: "))
        if self.opponent == self.home:
            print(f"You can't choose the same name as your team. We'll " +
                      f"rename your opponent the Anti-{self.opponent}.")
            self.opponent = "Anti-" + self.opponent

    def extra_innings(self, game):
        """Asks user if they want to extend the game in case of tie."""
        if self.inning == self.max and self.runs == self.opponentruns:
            extras = game.help_quit("\nYou're out of innings and it's tied." +\
                                    " Do you want to play one more inning? " +\
                                    "[y] or [n]: ")
            if extras == 'y':
                self.max +=1

class Engine:
    """
    Class for creating a game, making a roster, and managing user choices.

    Attributes:
        files (obj): Instance from Files class.
        field (obj): Instance from Field class.
        scoreboard (obj): Instance from Scoreboard class.
        lineup (lst): Empty list to hold players.
    """
    def __init__(self):
        """Constructor for Engine class."""
        self.files = Files()
        print(self.files.welcome)
        self.field = Field()
        self.scoreboard = Scoreboard(self)
        self.lineup = []

    def __repr__(self):
        """Returns game explanation."""
        return welcome

    def make_choice(self):
        """Asks user to decide what to do for next pitch; returns choice."""
        decision = self.help_quit("Incoming pitch... [s]wing or [w]atch: ")
        return decision

    def help_quit(self, question):
        """
        Allows user to always access the help or quit options during input.

        Paramters:
            question (str): Text of the input question.
        """
        # Ask for user input.
        user_input = input(question)
        # Whenever/while the input is h or q...
        while user_input == 'h' or user_input == 'q':
            if user_input == 'q':
                # Double check user wants to leave
                final_decision = input("\nAre you sure you want to quit the" +
                                       " game? [y] or [n]: ")
                if final_decision.lower() == 'y':
                    sys.exit(0)
                # If not, ask the input question again and restart loop.
                else:
                    user_input = input(question)
            elif user_input == 'h':
                print(self.files.help)
                leave = input("E[x]it the help screen.")
                # When they click 'x', ask input question again and restart.
                if leave == 'x':
                    user_input = input(question)
        # Return non-help or quit input as variable.
        return user_input

    def make_roster(self):
        """Scrape dataset to find potential players based on user input."""
        home_team = self.help_quit("\nWhich MLB team do you want to play as" +\
                                   "? Type a team name, without the city.\n" +\
                                   "Examples include 'Astros' and 'Red Sox." +\
                                   "'\n")
        # Filter to user's input.
        team_batters = self.files.data[self.files.data['Team'] == \
                       home_team.title()]
        # Check for error.
        if len(team_batters) < 5:
            print("Oops... Looks like there was a typo. We're going to " +
                 "default you to the Baltimore Orioles (sorry!). Enter 'q'" +\
                 " if you \nwant to quit and start over with a new selection.")
            home_team = "Orioles"
            team_batters = self.files.data[self.files.data['Team'] == \
                           home_team.title()]
        self.scoreboard.home = home_team.title()
        pitcher = Pitcher("Benny 'The Jet' Rodriguez", self.field)
        roster = {}
        # Append all players to the lineup.
        for index, row in team_batters.iterrows():
            name = 'obj_{}'.format(index)
            roster[name] = Batter(row['Name'], row['1B%'], row['2B%'], \
                           row['3B%'], row['HR%'], row['BB%'], row['K%'], \
                           row['HBP%'], row['OIP%'])
            self.lineup.append(roster[name])

    def play(self):
        """Function to play a full game."""
        self.make_roster()
        self.scoreboard.batting_order(self.lineup, self.field, self)
        current_pitcher = self.field.bullpen[0]
        self.scoreboard.pick_opponent(self)
        print("\nYou're all set, let's play!\n\n")
        # Checks length of game.
        while self.scoreboard.inning <= self.scoreboard.max:
            if self.scoreboard.inning > 1:
                print("\n" + '{:^80s}'.format("NEXT INNING.\n"))
            self.scoreboard.outs = 0
            # Let user know how other team did in top of inning and the score.
            print(self.scoreboard.other_team())
            print(self.scoreboard)
            while self.scoreboard.outs < 3:
                # At the start of every new batter, print field.
                self.field.print_field(self.field.bases, self.scoreboard)
                # Send a new batter to the plate.
                atbat = AtBat(self.field.dugout[0], self.field)
                print("\nBatter up! " + atbat.batter.name +
                      " is at the plate.")
                # Manage at bat.
                while atbat.status == "Batting":
                    print(str(atbat.balls) + " balls, " + str(atbat.strikes) +
                          " strikes.\n")
                    new_choice = self.make_choice()
                    if new_choice.lower() == 's':
                        atbat.swing()
                    elif new_choice.lower() == 'w':
                        atbat.watch(current_pitcher.throw_pitch(atbat))
                    else:
                        print("It looks like you didn't pick a valid option." +
                              " Let's try again!")
                atbat.outcome_machine(self.field, self.scoreboard)
            # Inning is over. Clear the bases for next inning and fix dugout.
            print("\n" + '{:^80s}'.format("3 OUTS"))
            self.field.clear_bases()
            self.scoreboard.extra_innings(self)
            self.scoreboard.inning += 1
        # Game is over.
        print("\n" + '{:^80s}'.format("GAME OVER."))
        print(start + "\nFinal score: \n" + end + str(self.scoreboard))
        self.scoreboard.box_score(self.field.dugout)

game = Engine()
game.play()
