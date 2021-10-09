from tkinter import Tk, Label, Canvas, NW, Button, PhotoImage
from bs4 import BeautifulSoup
from requests import get, exceptions
from PIL import ImageTk, Image
from threading import Thread
from sys import exit
from time import sleep
from darkdetect import isDark
from json import dumps, loads
from os import mkdir, system


def watermark():
    global waterRoot, screenHeight, screenWidth
    waterRoot = Tk()

    screenWidth = waterRoot.winfo_screenwidth()
    screenHeight = waterRoot.winfo_screenheight()

    pillowImage = Image.open('img/watermark.png')
    imageWidth, imageHeight = pillowImage.size

    xPosition = (screenWidth // 2) - (imageWidth // 2)
    yPosition = (screenHeight // 2) - (imageHeight // 2) - int(0.05787*screenHeight)

    canvas = Canvas(waterRoot, width=487, height=487, bg='white', highlightthickness=0)
    canvas.pack()
    canvas.master.overrideredirect(True)
    canvas.master.geometry(f"+{xPosition}+{yPosition}")
    canvas.master.wm_attributes('-transparentcolor', 'white')
    canvas.master.wm_attributes('-alpha', 0.6)
    canvas.master.wm_attributes('-topmost', True)
    canvas.master.lift()

    photoImage = ImageTk.PhotoImage(pillowImage)
    canvas.create_image(10, 10, anchor=NW, image=photoImage)

    waterRoot.mainloop()


def scrape():
    try:
        scrapeOnline()
    except exceptions.RequestException as noConnection:
        sleep(1)
        try:
            scrapeOffline()
        except FileNotFoundError as noCache:
            failure()


def scrapeOnline():
    URL = "https://www.goal.com/en/premier-league/table/2kwbbcootiqqgmrzs6o5inle5"

    webpage = get(URL, timeout=6).text

    soup = BeautifulSoup(webpage, 'lxml')

    pos_list, name_list, mp_list, points_list, gd_list = (list() for _ in range(5))

    teams = soup.find_all('tr', class_ = ('p0c-competition-tables__row p0c-competition-tables__row--rank-status p0c-competition-tables__row--rank-status-1',
                                          'p0c-competition-tables__row p0c-competition-tables__row--rank-status p0c-competition-tables__row--rank-status-2',
                                          'p0c-competition-tables__row p0c-competition-tables__row--rank-status p0c-competition-tables__row--rank-status-',
                                          'p0c-competition-tables__row p0c-competition-tables__row--rank-status p0c-competition-tables__row--rank-status-relegation'))

    for team in teams:
        position = (team.find('td')).text.strip()
        pos_list.append(position)

        name = (team.find('td', class_='p0c-competition-tables__team')).text.strip()
        name_list.append(name)

        matches_played = (team.find('td', class_='p0c-competition-tables__matches-played')).text.strip()
        mp_list.append(matches_played)

        points = (team.find('td', class_='p0c-competition-tables__pts')).text.strip()
        points_list.append(points)

        goal_diff = (team.find('td', class_='p0c-competition-tables__goals-diff')).text.strip()
        gd_list.append(goal_diff)

    final_table = {
        'pos': pos_list,
        'names': name_list,
        'mp': mp_list,
        'pts': points_list,
        'gd': gd_list
    }

    def saveCache():
        try:
            mkdir('cache')
        except FileExistsError:
            pass

        data = dumps(final_table)
        try:
            with open('cache/cache.json','r+') as cache:
                cache.write(data)
        except FileNotFoundError as noCacheToRead:
            with open('cache/cache.json','w+') as cache:
                cache.write(data)
                system('attrib +h cache/cache.json')

    saveCache()
    table(zip(*final_table.values()))


def scrapeOffline():
    with open('cache/cache.json', 'r') as cache:
        cached_table = loads(cache.read())

    table(zip(*cached_table.values()), False)


def table(table, online=True):
    newLine = '\n'
    windowText = dict()

    windowText['header'] = f"{' '*7}TEAM{' '*37}MP{' '*13}PTS{' '*11}GD{newLine*2}"

    windowText['pos'], windowText['names'], windowText['mp'], windowText['pts'], windowText['gd'] = (str() for _ in range(5))

    for pos, name, mp, pts, gd in table:
        windowText['pos'] += f"{' '*(3 - len(pos))}{pos}.{newLine*2}"
        windowText['names'] += f"{name}{newLine*2}"
        windowText['mp'] += f"{mp}{newLine*2}"
        windowText['pts'] += f"{pts}{newLine*2}"
        windowText['gd'] += f"{gd}{newLine*2}"


    tableRoot = Tk()
    tableRoot.title('Table')
    tableRoot.iconbitmap(r'img/logo.ico')
    tableRoot.resizable(False, False)
    tableRoot.geometry('430x740')
    tableRoot.attributes('-topmost',True)
    xPosition = (screenWidth-430)//4
    yPosition = (screenHeight-740)//4
    tableRoot.geometry(f"+{xPosition}+{yPosition}")

    header = Label(tableRoot, text=windowText['header'], justify='left', font=('Century Gothic Bold',11))
    header.place(x=5, y=15)

    pos = Label(tableRoot, text=windowText['pos'], justify='left', font=('Century Gothic',10))
    pos.place(x=5, y=50)

    names = Label(tableRoot, text=windowText['names'], justify='left', font=('Century Gothic',10))
    names.place(x=35, y=50)

    mp = Label(tableRoot, text=windowText['mp'], justify='left', font=('Century Gothic',10))
    mp.place(x=225, y=50)

    pts = Label(tableRoot, text=windowText['pts'], justify='left', font=('Century Gothic',10))
    pts.place(x=296, y=50)

    gd = Label(tableRoot, text=windowText['gd'], justify='left', font=('Century Gothic',10))
    gd.place(x=360, y=50)

    status = Canvas(tableRoot, width=400, height=400, border=0, highlightthickness=0)
    status.place(x=410, y=720)
    status.create_oval(5, 5, 8, 8, fill='green' if online else 'red', width=0)

    def darkMode():
        tableRoot.configure(bg='#121212')
        header.configure(fg='#FFFFFF', bg='#121212')
        pos.configure(fg='#FFFFFF', bg='#121212')
        names.configure(fg='#FFFFFF', bg='#121212')
        mp.configure(fg='#FFFFFF', bg='#121212')
        pts.configure(fg='#FFFFFF', bg='#121212')
        gd.configure(fg='#FFFFFF', bg='#121212')
        status.configure(bg='#121212')

    if isDark():
        darkMode()

    destroyWatermark()

    tableRoot.mainloop()


def failure():
    errorRoot = Tk()
    errorRoot.overrideredirect(True)
    errorRoot.geometry('370x130')

    screenWidth = errorRoot.winfo_screenwidth()
    screenHeight = errorRoot.winfo_screenheight()
    xPosition = (screenWidth - 400)//2
    yPosition = (screenHeight - 200)//2
    errorRoot.geometry(f'+{xPosition}+{yPosition}')

    errorString = "Connect to network to load table."
    errorMessage = Label(errorRoot, text=errorString, justify='center', font=('Century Gothic',11))
    errorMessage.place(x=55, y=30)
    exit_button = Button(errorRoot, text='EXIT', command=errorRoot.destroy, font=('Century Gothic',11))
    exit_button.place(relx=0.45, y=80)

    def darkMode():
        errorRoot.configure(bg='#121212')
        errorMessage.configure(fg='#ffffff', bg='#121212')
        exit_button.configure(fg='#ffffff', bg='#121212')

    if isDark():
        darkMode()

    destroyWatermark()

    errorRoot.mainloop()

    exit()


def destroyWatermark():
    waterRoot.after(0, waterRoot.destroy)



if __name__ == '__main__':
    waterMark = Thread(target=watermark)
    scrape = Thread(target=scrape)
    waterMark.start()
    scrape.start()
