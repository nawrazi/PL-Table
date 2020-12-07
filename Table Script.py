from bs4 import BeautifulSoup
import requests

URL = 'https://www.goal.com/en/premier-league/table/2kwbbcootiqqgmrzs6o5inle5'
web_html = requests.get(URL).text
soup = BeautifulSoup(web_html, 'lxml')

name_list = []
points_list = []
gd_list = []
mp_list = []
pos_list = []

teams = soup.find_all('tr', class_ = ('p0c-competition-tables__row p0c-competition-tables__row--rank-status p0c-competition-tables__row--rank-status-1',
                                      'p0c-competition-tables__row p0c-competition-tables__row--rank-status p0c-competition-tables__row--rank-status-2',
                                      'p0c-competition-tables__row p0c-competition-tables__row--rank-status p0c-competition-tables__row--rank-status-',
                                      'p0c-competition-tables__row p0c-competition-tables__row--rank-status p0c-competition-tables__row--rank-status-relegation'))
for team in teams:
    position = (team.find('td')).text.strip()
    pos_list.append(position)

    name = (team.find('td', class_='p0c-competition-tables__team')).text.strip()
    name_list.append(name)

    points = (team.find('td', class_='p0c-competition-tables__pts')).text.strip()
    points_list.append(points)

    goal_diff = (team.find('td', class_='p0c-competition-tables__goals-diff')).text.strip()
    gd_list.append(goal_diff)

    matches_played = (team.find('td', class_='p0c-competition-tables__matches-played')).text.strip()
    mp_list.append(matches_played)

final_table = {
'positions': pos_list,
'names': name_list,
'pts': points_list,
'gd': gd_list,
'mp': mp_list
}

print('\n' + ' '*5 + 'TEAM' + ' '*14 + 'MP' + ' '*3 + 'PTS' + ' '*3 + 'GD', end='\n'*2)

for num in range(len(name_list)):
    print(' '*(2 - (len(pos_list[num]))), final_table['positions'][num] + '.', # positions
          final_table['names'][num], # names
          ' '*(16 - len(name_list[num])), final_table['mp'][num], # matches played
          ' '*((2 - (len(mp_list[num]))) + 1), final_table['pts'][num], # points
          ' '*((2 - (len(points_list[num]))) + 2), final_table['gd'][num], # goal difference
          end='\n'*2)

input()
