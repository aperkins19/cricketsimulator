import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time

# captaincy approach transitions between defensive, neutral and aggressive in a stochastic markov chain.


def extract_team(team):
    index = np.arange(11)
    df = pd.DataFrame(columns=['Name','Batting', 'Bowling', 'Bowling Style'], index=index)
    skills = []
    for k,dicts in dict.items():
        player = []
        player.append(k)
        for t,v in dicts.items():
            player.append(v)
        skills.append(player)
    for i in range(11):
        df.iloc[i,0] = skills[i][0]
        df.iloc[i,1] = skills[i][1]
        df.iloc[i,2] = skills[i][2]
    return df

def build_team(team):
    df = pd.DataFrame(np.zeros((11, 5)), columns=['Name', 'Batting', 'Bowling', 'Yet to bat', 'Bowling Style'])
    for r in range(len(team)):
        df.loc[r, 'Name' ] = team[r][0]
        df.loc[r, 'Batting' ] = team[r][1]
        df.loc[r, 'Bowling' ] = team[r][2]
        df.loc[r, 'Bowling Style'] = team[r][3]
    return df


def outcome(bowler, batsman, pitch_quality, ball_condition):
    """ returns a random number scaled to the difference in the skill of the players. More difficulty_for_batsman == transforms the graph to the right, more difficult = greater numbers
    ideally, the max range of both the mean and std of the Normal Distribution should be 2. Pitch should matter half as much as the bowling. difficultly for batsman: 1.4.
    Should pitch_quality be factor? or an addition. Addition is easier to begin with. max Pitch quality = 0.5.
    """
    pitch_factor = (5 - pitch_quality)/100
    #print('pitch factor ' + str(pitch_factor))

    ball_factor = ((((ball_condition - 5  )**2   ) -7  ) /2.5)  /30
    #print('ball factor ' + str(ball_factor))

    skill_diff = (bowler-batsman)/50

    #print('mean = '+str(5 * (1 + pitch_factor + skill_diff + ball_factor )))
    loc = 5 * (1 + pitch_factor + skill_diff + ball_factor)

    ball = np.random.normal(loc = loc, scale = 1.2)
    return ball

def delivery(bowler, batsman,pitch_quality, ball_condition, ON_strike, batsman_a, batsman_b):
    ball = outcome(bowler, batsman,pitch_quality, ball_condition)
    #print(ball)
    l = ball
    if ball > 7.5:
        #out
        score = 0
        out = 1

    elif ball > 4:
        #dot
        score = 0
        out = 0

    elif ball > 3.5:
        #single
        score = 1
        out = 0
        #swap batsman
        ON_strike = change_ends(ON_strike, batsman_a, batsman_b)

    elif ball > 2.75:
        #two
        score = 2
        out = 0

    elif ball > 2.5:
        #three
        score = 3
        out = 0
        ON_strike = change_ends(ON_strike, batsman_a, batsman_b)

    elif ball > 0.5:
        #four
        score = 4
        out = 0

    else:
        #six
        score = 6
        out = 0

    if read_out == 1:
        live_text(score,out)

    return score, out, l, ON_strike


def new_batsman(batting_team, batting_score_sheet):
    look_for_next = 2
    counter = 0
    #while you haven't found a waiting batsman
    while look_for_next == 2:
        #go through list
        if batting_team.loc[counter,'Yet to bat'] == 0:
            look_for_next = 0

            #enter batsman into batting sheet
            batting_score_sheet.loc[counter, 'Name'] = batting_team.loc[counter, 'Name']
            #mark batsman down as batting
            batting_team.loc[counter,'Yet to bat'] = 1

            batsmans_index = counter

        else:
            counter = counter + 1

    return batting_score_sheet, batsmans_index

def facing_batsman(ON_strike, batsman_a, batsman_b, batting_team):
    if ON_strike == 'batsman_a':
        name = batting_team.loc[batsman_a, 'Name']
        bat = batting_team.loc[batsman_a, 'Batting']
    elif ON_strike == 'batsman_b':
        name = batting_team.loc[batsman_b, 'Name']
        bat = batting_team.loc[batsman_b, 'Batting']
    return name, bat

def change_ends(ON_strike, batsman_a, batsman_b):
    if ON_strike == 'batsman_a':
        ON_strike = 'batsman_b'
    elif ON_strike == 'batsman_b':
        ON_strike = 'batsman_a'
    return ON_strike


def over_change_bowler(in_the_attack):
    if in_the_attack == 'bowler_a':
        in_the_attack = 'bowler_b'
    elif in_the_attack == 'bowler_b':
        in_the_attack = 'bowler_a'
    return in_the_attack

def get_bowler(in_the_attack, bowler_a, bowler_b):
    #gets stats of the bowler
    if in_the_attack == 'bowler_a':
        name = bowler_a.loc['Name']
        bowl = bowler_a.loc['Bowling']
        type = bowler_a.loc['Bowling Style']
    elif in_the_attack == 'bowler_b':
        name = bowler_b.loc['Name']
        bowl = bowler_b.loc['Bowling']
        type = bowler_b.loc['Bowling Style']
    return name, bowl, type

def get_bowling_attack(bowling_team):
    bowling_attack = bowling_team['Bowling'] > 4
    return bowling_attack

def get_change_of_bowling(bowler_a, bowler_b, bowling_attack):
    # makes list of available bowlers not including bowler a or b
    bowlers = bowling_attack['Name'] != bowler_a['Name'] and bowler_b['Name']
    print(bowlers)
    #randomly decides which bowler to change - captain decides later
    change = np.random.choice(['bowler_a', 'bowler_b'])

    #if change == 'bowler_a':
    #    bowler_a =

    #print the name of the bowler




def innings(bowler, pitch_quality, batting_team, bowling_team, live_text, pitch_deterioration_rate):

    #initialise innings

    #reset yet to bat columns

    for r in range(len(batting_team)):
        batting_team.loc[r, 'Yet to bat' ] = 0

    basic_score_sheet = pd.DataFrame(columns = ['Score','Wickets in hand'])
    batting_score_sheet = pd.DataFrame(np.zeros((11, 6)), columns = ['Name', 'Runs','Out', 'Balls Faced', '4s', '6s'])
    ball = 0
    wickets_in_hand = 10
    ball_condition = 10

    batting_score_sheet, batsman_a = new_batsman(batting_team, batting_score_sheet)
    batting_score_sheet, batsman_b = new_batsman(batting_team, batting_score_sheet)

    bowling_attack = get_bowling_attack(bowling_team)

    #bowiling team
    # 1st bowling pair is just the bottom
    bowler_a = bowling_team.loc[10]
    bowler_b = bowling_team.loc[9]


    # ON_strike holds the index of the batsman_a/b
    ON_strike = 'batsman_a'

    in_the_attack = 'bowler_a'

    if read_out == 1:
        print(' ')
        print('Opening the batting, ' + batting_score_sheet.loc[0,'Name'] + ' & '+ batting_score_sheet.loc[1,'Name'])
        print('')
        bwl_n, bwl, bwl_t = get_bowler(in_the_attack, bowler_a, bowler_b)
        print('Opening the bowling, ' + bwl_n + ' bowling '+ bwl_t)

    #run innings

    l_list=[]

    while wickets_in_hand > 0:
        #which batsman is facing -  get their stats
        ball = ball + 1
        bt_n, bat = facing_batsman(ON_strike, batsman_a, batsman_b, batting_team)
        bwl_n, bwl, bwl_t = get_bowler(in_the_attack, bowler_a, bowler_b)

        get_change_of_bowling(bowler_a, bowler_b, bowling_attack)

        score, out, l, ON_strike = delivery(bowler, bat, pitch_quality, ball_condition, ON_strike, batsman_a, batsman_b)

        l_list.append(l)
        basic_score_sheet.loc[ball] = (score + out)
        ball_condition = ball_condition - 0.02083
        pitch_quality = pitch_quality - 0.004

        if ball == 480:
            ball_condition = 10
            print("New ball taken.")


        #update batsman's tally
        if ON_strike == 'batsman_a':
            batting_score_sheet.loc[batsman_a, 'Balls Faced'] = batting_score_sheet.loc[batsman_a, 'Balls Faced'] + 1
        elif ON_strike == 'batsman_b':
            batting_score_sheet.loc[batsman_b, 'Balls Faced'] = batting_score_sheet.loc[batsman_b, 'Balls Faced'] + 1

        if score != 0:
            if ON_strike == 'batsman_a':
                batting_score_sheet.loc[batsman_a, 'Runs'] = batting_score_sheet.loc[batsman_a, 'Runs'] + score
                if score == 4:
                    batting_score_sheet.loc[batsman_a, '4s'] = batting_score_sheet.loc[batsman_a, '4s'] + 1
                elif score == 6:
                    batting_score_sheet.loc[batsman_a, '6s'] = batting_score_sheet.loc[batsman_a, '6s'] + 1

            elif ON_strike == 'batsman_b':
                batting_score_sheet.loc[batsman_b, 'Runs'] = batting_score_sheet.loc[batsman_b, 'Runs'] + score
                if score == 4:
                    batting_score_sheet.loc[batsman_b, '4s'] = batting_score_sheet.loc[batsman_b, '4s'] + 1
                elif score == 6:
                    batting_score_sheet.loc[batsman_b, '6s'] = batting_score_sheet.loc[batsman_b, '6s'] + 1

        if out == 1:
            wickets_in_hand = wickets_in_hand - 1
            batsman_no = 10-wickets_in_hand

            if wickets_in_hand > 0:
                if ON_strike == 'batsman_a':
                    batting_score_sheet, batsman_a = new_batsman(batting_team, batting_score_sheet)
                    if read_out == 1:
                        print('New batsman: '+ batting_score_sheet.loc[batsman_a,'Name'])

                elif ON_strike == 'batsman_b':
                    batting_score_sheet, batsman_b = new_batsman(batting_team, batting_score_sheet)
                    if read_out == 1:
                        print('New batsman: '+ batting_score_sheet.loc[batsman_b,'Name'])

        if read_out == 1:
            if ball % 6 == 0:
                print('')
                print('End of over: '+ str(int(ball/6)))
                print('Score: '+ str(sum(basic_score_sheet['Score'])) + '/'+str(10-wickets_in_hand))
                print(batting_score_sheet.loc[batsman_a,'Name']  + ': ' + str(int(batting_score_sheet.loc[batsman_a,'Runs'])) + ', ' + batting_score_sheet.loc[batsman_b,'Name'] +': ' +  str(int(batting_score_sheet.loc[batsman_b, 'Runs'])))
                print('')
                in_the_attack = over_change_bowler(in_the_attack)

        time.sleep(5)

    if live_text == 1:
        print('')
        print('End of the innings:')
        print('All out for '+ str(sum(basic_score_sheet['Score'])))
        print('pitch_quality '+ str(round(pitch_quality)))
        print('')
        print('Overs: '+str(ball/6))
        print(basic_score_sheet['Score'].value_counts())
        print(' ')
    return batting_score_sheet, pitch_quality


def live_text(s,w):
    if w == 1:
        print('WICKET')
    else:
        if s == 0:
            print('.')
        else:
            print(s)

England = [
['Rory Burns', 10,  3, 'Offspin'],
['Dom Sibley', 10,  1, 'Offspin' ],
['Joe Denly', 9, 5, 'Offspin'],
['Joe Root', 9, 5, 'Offspin'],
['Ollie Pope', 8, 3, 'Offspin'],
['Ben Stokes', 8, 8, 'Pace'],
['Jos Buttler', 3, 1, 'Offspin'],
['Sam Curran', 3, 7, 'Pace'],
['Jack Leach', 2, 9, 'Leg spin'],
['Jofra Archer', 1, 9, 'Pace'],
['James Anderson', 1, 10, 'Pace'],
]


Australia = [
['Marcus Harris', 9, 3, 'Offspin'],
['David Warner', 10, 1,'Offspin'],
['Marnus Labuschagne', 9, 2, 'Offspin'],
['Steve Smith', 10,  2, 'Offspin'],
['Travis Head', 6, 2, 'Offspin'],
['Matt Wade' , 5, 3, 'Offspin'],
['Tim Paine', 4, 1, 'Pace'],
['Pat Cummins', 2, 7,'Pace'],
['Nathan Lyon', 3, 10, 'Offspin'],
['Mitchell Starc', 4, 8, 'Pace'],
['Josh Hazelwood', 2, 9, 'Pace'],
]

home_team = build_team(England)
away_team = build_team(Australia)

bowler = 5
pitch_quality = 10
pitch_deterioration_rate  = 0.000001
read_out = 1


scores = pd.DataFrame(np.zeros((2, 2)), columns=['First Innings', 'Second Innings'])

toss = np.random.rand()
if toss > 0.5:
    batting_team = home_team
    bowling_team = away_team
else:
    batting_team = away_team
    bowling_team = home_team

innings_list = []

score_sheet, pitch_quality = innings(bowler, pitch_quality, batting_team, bowling_team, read_out, pitch_deterioration_rate)


score_sheet, pitch_quality = innings(bowler, pitch_quality, batting_team, read_out, pitch_deterioration_rate)
innings_list.append(score_sheet)
scores.loc[0,'First Innings'] = sum(score_sheet['Runs'])
if read_out == 1:
    print('Innings: ' + str(1) + ' '+ str(int(sum(score_sheet['Runs']))) + '  overs  '+ str(int(sum(score_sheet['Balls Faced'])/6)))

score_sheet, pitch_quality = innings(bowler, pitch_quality, bowling_team, read_out, pitch_deterioration_rate)
innings_list.append(score_sheet)
scores.loc[1,'First Innings'] = sum(score_sheet['Runs'])
if read_out == 1:
    print('Innings: ' + str(2) + ' '+ str(int(sum(score_sheet['Runs']))) + '  overs  '+ str(int(sum(score_sheet['Balls Faced'])/6)))

#follow on
if scores.loc[1,'First Innings'] < (scores.loc[0,'First Innings']-200):
    score_sheet, pitch_quality = innings(bowler, pitch_quality, bowling_team, read_out, pitch_deterioration_rate)
    innings_list.append(score_sheet)
    scores.loc[1,'Second Innings'] = sum(score_sheet['Runs'])
    if read_out == 1:
        print('Innings: ' + str(4) + ' '+ str(int(sum(score_sheet['Runs']))) + '  overs  '+ str(int(sum(score_sheet['Balls Faced'])/6)))

    #follow on ending
    if (scores.loc[1,'Second Innings'] + scores.loc[1,'First Innings']) < scores.loc[0,'First Innings']:
        print('home team win by an innings and '+ str(scores.loc[0,'First Innings'] - (scores.loc[1,'Second Innings'] + scores.loc[1,'First Innings'])) + ' runs.')

    else:
        if (scores.loc[1,'Second Innings'] + scores.loc[1,'First Innings']) > scores.loc[0,'First Innings']:
            score_sheet, pitch_quality = innings(bowler, pitch_quality, batting_team, read_out, pitch_deterioration_rate)
            innings_list.append(score_sheet)
            scores.loc[0,'Second Innings'] = sum(score_sheet['Runs'])
            if read_out == 1:
                print('Innings: ' + str(3) + ' '+ str(int(sum(score_sheet['Runs']))) + '  overs  '+ str(int(sum(score_sheet['Balls Faced'])/6)))

            if (scores.loc[0,'Second Innings'] + scores.loc[0,'First Innings']) > (scores.loc[1,'Second Innings'] + scores.loc[1,'First Innings']):
                print('home team win by '+ str((scores.loc[0,'First Innings'] + scores.loc[0,'Second Innings']) - (scores.loc[1,'Second Innings'] + scores.loc[1,'First Innings'])) + ' runs.')

            if (scores.loc[0,'Second Innings'] + scores.loc[0,'First Innings']) < (scores.loc[1,'Second Innings'] + scores.loc[1,'First Innings']):
                print('Vistors win by '+ str((scores.loc[1,'First Innings'] + scores.loc[1,'Second Innings']) - (scores.loc[0,'Second Innings'] + scores.loc[0,'First Innings'])) + ' runs.')



else:
    #not follow on
    score_sheet, pitch_quality = innings(bowler, pitch_quality, batting_team, read_out, pitch_deterioration_rate)
    innings_list.append(score_sheet)
    scores.loc[0,'Second Innings'] = sum(score_sheet['Runs'])
    if read_out == 1:
        print('Innings: ' + str(3) + ' '+ str(int(sum(score_sheet['Runs']))) + '  overs  '+ str(int(sum(score_sheet['Balls Faced'])/6)))

    score_sheet, pitch_quality = innings(bowler, pitch_quality, bowling_team, read_out, pitch_deterioration_rate)
    innings_list.append(score_sheet)
    scores.loc[1,'Second Innings'] = sum(score_sheet['Runs'])
    if read_out == 1:
        print('Innings: ' + str(4) + ' '+ str(int(sum(score_sheet['Runs']))) + '  overs  '+ str(int(sum(score_sheet['Balls Faced'])/6)))

    if (scores.loc[0,'Second Innings'] + scores.loc[0,'First Innings']) > (scores.loc[1,'Second Innings'] + scores.loc[1,'First Innings']):
        print('home team win by '+ str((scores.loc[0,'First Innings'] + scores.loc[0,'Second Innings']) - (scores.loc[1,'Second Innings'] + scores.loc[1,'First Innings'])) + ' runs.')

    elif (scores.loc[0,'Second Innings'] + scores.loc[0,'First Innings']) < (scores.loc[1,'Second Innings'] + scores.loc[1,'First Innings']):
        print('The visitors win by '+ str((scores.loc[1,'First Innings'] + scores.loc[1,'Second Innings']) - (scores.loc[0,'Second Innings'] + scores.loc[0,'First Innings'])) + ' runs.')

#if read_out == 1:
print('')
print('')
print('')
print('')
print('Match Review')
print(' ')

for i in range(len(innings_list)):
    print(' ')
    print(innings_list[i])
    print(' ')

print('')
print('Final pitch condition: ' + str(round(pitch_quality,2)))

#plt.hist(scores, bins=50)
#plt.show()
