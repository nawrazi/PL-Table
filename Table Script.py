from tkinter import Tk, Label, Canvas, NW, messagebox, Button, PhotoImage
from bs4 import BeautifulSoup
from requests import get, exceptions
from PIL import ImageTk, Image
from threading import Thread
from sys import exit
from time import sleep
from darkdetect import isDark


def watermark():
    global waterRoot, screenHeight, screenWidth
    waterRoot = Tk()

    screenWidth = waterRoot.winfo_screenwidth()
    screenHeight = waterRoot.winfo_screenheight()

    pillowImage = Image.open("img/watermark.png")
    imageWidth, imageHeight = pillowImage.size

    xPosition = (screenWidth // 2) - (imageWidth // 2)
    yPosition = (screenHeight // 2) - (imageHeight // 2) - int(0.05787*screenHeight)

    canvas = Canvas(waterRoot, width = 487, height = 487, bg = "white", highlightthickness = 0)
    canvas.pack()
    canvas.master.overrideredirect(True)
    canvas.master.geometry(f'+{xPosition}+{yPosition}')
    canvas.master.wm_attributes("-transparentcolor", "white")
    canvas.master.wm_attributes("-alpha", 0.6)
    canvas.master.wm_attributes("-topmost", True)
    canvas.master.lift()

    photoImage = ImageTk.PhotoImage(pillowImage)
    canvas.create_image(10, 10, anchor = NW, image = photoImage)

    waterRoot.mainloop()


def scrape():
    URL = 'https://www.goal.com/en/premier-league/table/2kwbbcootiqqgmrzs6o5inle5'
    try:
        webpage = get(URL).text
    except exceptions.RequestException:
        networkError()

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

    return zip(pos_list, name_list, mp_list, points_list, gd_list)


def table():
    final_table = scrape()
    newLine = '\n'
    windowText = dict()

    windowText['header'] = f"{' '*7}TEAM{' '*37}MP{' '*13}PTS{' '*11}GD{newLine*2}"

    windowText['pos'], windowText['names'], windowText['mp'], windowText['pts'], windowText['gd'] = (str() for _ in range(5))

    for pos, name, mp, pts, gd in final_table:
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
    xPosition = (screenWidth-430)//4
    yPosition = (screenHeight-740)//4
    tableRoot.geometry(f'+{xPosition}+{yPosition}')

    header = Label(tableRoot, text=windowText['header'], justify='left', font=('Century Gothic Bold',11))
    header.place(x=5, y=15)

    pos = Label(tableRoot, text=windowText['pos'], justify='left', font=('Century Gothic',10))
    pos.place(x=5, y=50)

    names = Label(tableRoot, text=windowText['names'], justify='left', font=('Century Gothic',10))
    names.place(x=35, y=50)

    mp = Label(tableRoot, text=windowText['mp'], justify='left', font=('Century Gothic',10))
    mp.place(x=225, y=50)

    pts = Label(tableRoot, text=windowText['pts'], justify='left', font=('Century Gothic',10))
    pts.place(x=295, y=50)

    gd = Label(tableRoot, text=windowText['gd'], justify='left', font=('Century Gothic',10))
    gd.place(x=360, y=50)


    def darkMode():
        tableRoot.configure(bg='#121212')
        header.configure(fg='#FFFFFF', bg='#121212')
        pos.configure(fg='#FFFFFF', bg='#121212')
        names.configure(fg='#FFFFFF', bg='#121212')
        mp.configure(fg='#FFFFFF', bg='#121212')
        pts.configure(fg='#FFFFFF', bg='#121212')
        gd.configure(fg='#FFFFFF', bg='#121212')

    if isDark():
        darkMode()

    destroyWatermark()

    tableRoot.mainloop()


def networkError():
    sleep(1)
    destroyWatermark()

    errorRoot = Tk()
    errorRoot.overrideredirect(True)
    errorRoot.geometry('400x130')

    screenWidth = errorRoot.winfo_screenwidth()
    screenHeight = errorRoot.winfo_screenheight()
    xPosition = (screenWidth - 400)//2
    yPosition = (screenHeight - 200)//2
    errorRoot.geometry(f'+{xPosition}+{yPosition}')

    errorString = "Failed To Establish Connection. Check Your Network."
    errorMessage = Label(errorRoot, text=errorString, justify='center', font=('Century Gothic',11))
    errorMessage.place(x=8, y=30)

    exit_button = Button(errorRoot, text="EXIT", command=errorRoot.destroy, font=('Century Gothic',9))
    exit_button.place(x=185, y = 90)
    # img = PhotoImage(file="img/exit_black.png")
    # exitButton = Button(errorRoot, image=img, borderwidth=0, command=errorRoot.destroy)
    # exitButton.place(x=173, y=70)

    if isDark():
        errorRoot.configure(bg='#121212')
        errorMessage.configure(fg='#ffffff', bg='#121212')

        exit_button.configure(fg='#ffffff', bg='#121212')
        # imgW = PhotoImage(file="img/exit_white.png")
        # exitButton.configure(image=imgW, bg='#121212')

    errorRoot.mainloop()

    exit()


def destroyWatermark():
    waterRoot.after(0, waterRoot.destroy)



if __name__ == '__main__':
    waterMark = Thread(target = watermark)
    table = Thread(target = table)
    waterMark.start()
    table.start()
