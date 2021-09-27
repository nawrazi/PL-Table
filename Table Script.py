from tkinter import *
from bs4 import BeautifulSoup
from requests import get
from PIL import ImageTk, Image
from threading import Thread
from sys import exit
from time import sleep
from tkinter.messagebox import showerror


def watermark():
    global waterRoot, screenHeight, screenWidth
    waterRoot = Tk()
    screenWidth = waterRoot.winfo_screenwidth()
    screenHeight = waterRoot.winfo_screenheight()
    pictureWidth = int(screenWidth / 2) - int(487 / 2)
    pictureHeight = int(screenHeight / 2) - int(487 / 2) - int(0.05787*screenHeight)
    canvas = Canvas(waterRoot, width = 487, height = 487, bg = 'white', highlightthickness = 0)
    canvas.pack()
    canvas.master.overrideredirect(True)
    canvas.master.geometry('+%d+%d' %(pictureWidth,pictureHeight))
    canvas.master.wm_attributes("-transparentcolor", "white")
    canvas.master.wm_attributes("-alpha", 0.4)
    canvas.master.wm_attributes("-topmost", True)
    canvas.master.lift()
    img = ImageTk.PhotoImage(Image.open("C:\Storage\Code\Python\PL Table\PC App\Window App\Table 2.0\img\watermark.png"))
    canvas.create_image(10, 10, anchor = NW, image = img)

    waterRoot.mainloop()


def scrape():
    URL = 'https://www.goal.com/en/premier-league/table/2kwbbcootiqqgmrzs6o5inle5'
    try:
        web_html = get(URL).text
    except Exception:
        networkError()

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

    return final_table


def table():
    final_table = scrape()

    final_string_title = ''
    final_string_mp = ''
    final_string_names = ''
    final_string_pts = ''
    final_string_gd = ''
    windowText = {}

    final_string_title += ' '*7
    final_string_title += 'TEAM'
    final_string_title += ' '*36
    final_string_title += 'MP'
    final_string_title += ' '*11
    final_string_title += 'PTS'
    final_string_title += ' '*11
    final_string_title += 'GD'
    final_string_title += '\n'*2
    windowText['title']=final_string_title

    for num in range(len(final_table['names'])):
        final_string_names += ' '*(3 - (len(final_table['positions'][num])))
        final_string_names += final_table['positions'][num]
        final_string_names += '.'
        final_string_names += ' '*2
        final_string_names += final_table['names'][num]
        final_string_names += ' '*(19 - len(final_table['names'][num]))
        final_string_names += '\n'*2
        windowText['names']=final_string_names

        final_string_mp += final_table['mp'][num]
        final_string_mp += '\n'*2
        windowText['mp']=final_string_mp
        final_string_pts += final_table['pts'][num]
        final_string_pts += '\n'*2
        windowText['pts']=final_string_pts
        final_string_gd += final_table['gd'][num]
        final_string_gd += '\n'*2
        windowText['gd']=final_string_gd

    tableRoot = Tk()
    tableRoot.title('Table')
    tableRoot.iconbitmap(r'C:\Storage\Code\Python\PL Table\PC App\Window App\Table 2.0\img\logo.ico')
    tableRoot.resizable(False, False)
    tableRoot.geometry('430x740')
    yPosition = (screenHeight-740)/4
    xPosition = (screenWidth-430)/16
    tableRoot.geometry('+200+%d' %yPosition)

    title = Label(tableRoot, text=windowText['title'], justify='left', font=('Arial Bold',11))
    title.place(x=5, y=15)

    names = Label(tableRoot, text=windowText['names'], justify='left', font=('Arial',11))
    names.place(x=5, y=50)

    mp = Label(tableRoot, text=windowText['mp'], justify='left', font=('Arial',11))
    mp.place(x=225, y=50)

    pts = Label(tableRoot, text=windowText['pts'], justify='left', font=('Arial',11))
    pts.place(x=295, y=50)

    gd = Label(tableRoot, text=windowText['gd'], justify='left', font=('Arial',11))
    gd.place(x=363, y=50)

    destroyWatermark()

    tableRoot.mainloop()


def destroyWatermark():
    waterRoot.after(0, waterRoot.destroy)


def networkError():
    sleep(1)
    showerror("Error", "Check Your Network")
    destroyWatermark()
    exit()


if __name__ == '__main__':
    waterMark = Thread(target = watermark)
    table = Thread(target = table)
    waterMark.start()
    table.start()
