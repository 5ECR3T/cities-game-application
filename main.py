from tkinter import *
from tkinter import messagebox
from datetime import date

import random
import sqlite3
import os
import pygame
import webbrowser

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()

k_catch = pygame.mixer.music.load(f'music\\sample3.mp3')
k_catch = pygame.mixer.music.play(-1)

s_catch = pygame.mixer.Sound(f'music\\sample.mp3')

root=Tk()
root.geometry('1080x720')
root.title('Cities game')
root.iconbitmap(f'images\\city.ico')
root.resizable(False,False)
root['bg']='white'

bg_img=PhotoImage(file=f'images\\3.png')
bg_label=Label(image=bg_img)
bg_label.place(x=0, y=0, relheight=1, relwidth=1)

program_version='Build version 1.00'

rules='''
- Починається гра з будь-якого міста.\n\
\n\
- Кожен з учасників гри по "колу" називає реальне місто, назва якого починається\n на букву, якою закінчується попередня назва міста. \n(Наприклад: МосквА-АнапА-АгріджентО-ОмсьК-КраснодаР-\nРостов-на-ДонУ-УльМ-МалЕ-ЄкатеринбурГ-ГаагА-АдеН-НовгороД).\n\
\n\
- Забороняється повторення міст.\n\
\n\
- Назв міст на на м'який знак та букву и немає. Через це пропускаємо цю букву і гравець повинен назвати місто на букву що стоїть перед ь або и.\n\
\n\
- Гра завершується коли гравець не в силах більше згадати назву міста.
'''

authors='''
Кирилескул Гліб\n
Воробйов Даниїл\n
Боярко Даниїл\n
Кобзарь Олександр\n
Тихохід Євгеній\n
Мінжулін Євгеній\n
Ковальський Роман'''


def music_pause():
    s_catch.play()
    pygame.mixer.music.pause()

def music_unpause():
    s_catch.play()
    pygame.mixer.music.unpause()

def menu_hide():
    butt1.pack_forget()
    butt2.pack_forget()
    butt3.pack_forget()
    butt4.pack_forget()

def menu_show():
    butt1.pack(padx=10,pady=(100, 10))
    butt2.pack(padx=10,pady=10)
    butt3.pack(padx=10,pady=10)
    butt4.pack(padx=10,pady=10)

def gmail():
    s_catch.play()
    webbrowser.open_new(r"mailto:city.gamess0.2@gmail.com")

def inst():
    s_catch.play()
    webbrowser.open_new(r"https://www.instagram.com/city_game_0.2/")

def telega():
    s_catch.play()
    webbrowser.open_new(r"https://t.me/citygamel")

def donat_now():
    s_catch.play()
    webbrowser.open_new(r"https://www.donationalerts.com/r/glebychh")

def rule_button():
    s_catch.play()
    messagebox.showinfo(title='Cities game', message=rules)

def close():
    s_catch.play()
    root.destroy()

def start():
    s_catch.play()

    def game_hide():
        label3.pack_forget()
        entry1.pack_forget()
        butt5.place_forget()
        butt6.pack_forget()
        butt7.pack_forget()
    
    def write():
        result=open(file='score.txt', mode='a+', encoding='UTF-8')
        result.writelines(f'{date.today()}      {score[-1]}\n')
        result.close()

    menu_hide()

    os.system(f'del Temp\\* /Q')
    os.system(f'copy example.db Temp\\')

    con = sqlite3.connect(f'Temp\\example.db')
    cur=con.cursor()

    label3=Label(text='Введіть місто',font=('OCR-A BT',20), background='#dae6f2', foreground='black')
    label3.pack(anchor=CENTER, padx=10, pady=(50, 10))
    entry1=Entry(width=20,font=('OCR-A BT',25), background='white', foreground='black',)
    entry1.pack(anchor=CENTER, padx=10,pady=10)

    last=[]
    score=[0]
    temp=[]
    attempts=[0]

    def next():
        s_catch.play()

        def check_user():
            if city[-1] == 'Ь' or city[-1] == 'И' or city[-1] == 'ь' or city[-1] == 'и':
                i=-2
            else:
                i=-1
            return i
        
        def check_ai():
            if city_ai[-1] == 'Ь' or city_ai[-1] == 'И' or city_ai[-1] == 'ь' or city_ai[-1] == 'и':
                i=-2
            else:
                i=-1
            return i

        city=str(entry1.get()).title()
        if last==[] or last[-1] == city[0].title():
            cur.execute(f'''SELECT * FROM base WHERE name="{city}"''')
            try:
                if city == cur.fetchall()[0][0]:
                    cur.execute(f'''DELETE FROM base WHERE name="{city}"''')
                    con.commit()
                    last.append(city[int(check_user())].upper())
                    score.append(score[-1]+1)
                    try:
                        cur.execute(f'''SELECT * FROM base WHERE name LIKE "{last[-1]}%"''')
                        temp.append(cur.fetchall())
                        city_ai=str(temp[0][random.randint(0, len(temp[0])-1)][0])
                        temp.clear()
                        last.append(city_ai[int(check_ai())].upper())
                        label3.configure(text=f"Комп'ютер: {city_ai}")
                    except:
                        messagebox.showinfo(title='Cities game',message=f'Ви виграли\nВаш рахунок {score[-1]}')
                        write()
                        game_hide()
                        menu_show()
            except IndexError:
                messagebox.showinfo(title='Cities game',message='В нашій базі даних немає такого міста')
        else:
            messagebox.showinfo(title='Cities game',message=f'Ваше місто починається на {last[-1]}')
        entry1.delete(0,END)
        
    def help():
        s_catch.play()
        if last == []:
            entry1.delete(0,END)
            cur.execute(f'''SELECT * FROM base''')
            raint=len(cur.fetchall())-1
            cur.execute(f'''SELECT * FROM base''')
            entry1.insert(0, cur.fetchall()[random.randint(0,raint)][0])
            attempts.append(attempts[-1]+1)
            if attempts[-1] >= 3:
                butt5['state'] = DISABLED
        else:
            entry1.delete(0,END)
            cur.execute(f'''SELECT * FROM base WHERE name LIKE "{last[-1]}%"''')
            raint=len(cur.fetchall())-1
            cur.execute(f'''SELECT * FROM base WHERE name LIKE "{last[-1]}%"''')
            entry1.insert(0, cur.fetchall()[random.randint(0,raint)][0])
            attempts.append(attempts[-1]+1)
            if attempts[-1] >= 3:
                butt5['state'] = DISABLED

    def loseplayer():
        s_catch.play()
        messagebox.showinfo(title='Cities game', message=f'Ви програли\nВаш рахунок {score[-1]}')
        write()
        game_hide()
        menu_show()
            
    butt5=Button(text='💡',font=('Arial',30), background='gray', command=help, foreground='yellow')
    butt5["border"] = "5"
    butt5.place(x=750, y=240, width=70, height=70)
    butt6=Button(text='Відповісти', font=('Arial',14), command=next, width=30, height=2, background='gray', foreground='white')
    butt6["border"] = "5"
    butt6.pack(anchor=CENTER, padx=10, pady=(30, 10))
    butt7=Button(text='Здатися', font=('Arial',14),command=loseplayer, width=30, height=2, background='gray', foreground='white')
    butt7["border"] = "5"
    butt7.pack(anchor=CENTER, padx=10, pady=10)
    
def score_history():
    s_catch.play()
    menu_hide()
    line=[]
    try:
        result=open(file='score.txt', mode='r', encoding='UTF-8')
        long=len(result.readlines())
        result.close()
    except:
        pass
    try:
        with open(file='score.txt', mode='r', encoding='UTF-8') as result:
            for i in range(long):
                line.append(result.readline())
            result.close()
    except:
        pass

    def back():
        s_catch.play()
        label4.pack_forget()
        butt8.pack_forget()
        menu_show()

    label4=Label(font=('OCR-A BT',14), background='#dae6f2', foreground='black')
    label4.pack(anchor=CENTER, padx=10,pady=(50, 10))
    try:
        if len(line) == 1:
            label4.configure(text=(f'{line[-1]}'))
        elif len(line) == 2:
            label4.configure(text=(f'{line[-1]}\n{line[-2]}'))
        elif len(line) == 3:
            label4.configure(text=(f'{line[-1]}\n{line[-2]}\n{line[-3]}'))
        elif len(line) == 4:
            label4.configure(text=(f'{line[-1]}\n{line[-2]}\n{line[-3]}\n{line[-4]}'))
        else:
            label4.configure(text=(f'{line[-1]}\n{line[-2]}\n{line[-3]}\n{line[-4]}\n{line[-5]}\n'))
    except IndexError:
        label4.configure(text="Немає даних")
        

    butt8=Button(text='Назад', font=('Arial',14), command=back, width=30, height=2, background='gray', foreground='white')
    butt8["border"] = "5"
    butt8.pack(anchor=CENTER, padx=10, pady=(50, 10))

def settings():
    s_catch.play()
    menu_hide()
    def hide_settings():
        butt9.pack_forget()
        butt10.pack_forget()
        butt11.pack_forget()
        butt12.pack_forget()
        butt13.pack_forget()
    def show_settings():
        butt9.pack(padx=100, pady=(50, 10))
        butt10.pack(padx=10, pady=10)
        butt11.pack(padx=10, pady=10)
        butt12.pack(padx=10, pady=10)
        butt13.pack(padx=10, pady=10)
    def back():
        s_catch.play()
        hide_settings()
        menu_show()
    def author():
        s_catch.play()
        hide_settings()
        def author_back():
            s_catch.play()
            label5.pack_forget()
            butt14.pack_forget()
            show_settings()
        label5=Label(text=authors, font=('OCR-A BT',18), background='#dae6f2', foreground='black')
        label5.pack(anchor=CENTER, side="top", pady=10)
        butt14=Button(text='Назад', font=('Arial',14), command=author_back, width=30, height=2, background='gray', foreground='white')
        butt14["border"] = "5"
        butt14.pack(anchor=CENTER, padx=10, pady=10)
    def support():
        s_catch.play()
        hide_settings()
        def support_back():
            s_catch.play()
            butt15.pack_forget()
            butt16.pack_forget()
            butt17.pack_forget()
            butt18.pack_forget()
            show_settings()
        butt15=Button(text='Gmail', font=('Arial',14), command=gmail, width=30, height=2, background='gray', foreground='white')
        butt15["border"] = "5"
        butt15.pack(anchor=CENTER, padx=10, pady=(100, 10))
        butt16=Button(text='Instagram', font=('Arial',14), command=inst, width=30, height=2, background='gray', foreground='white')
        butt16["border"] = "5"
        butt16.pack(anchor=CENTER, padx=10, pady=(10, 10))
        butt17=Button(text='Telegram', font=('Arial',14), command=telega, width=30, height=2, background='gray', foreground='white')
        butt17["border"] = "5"
        butt17.pack(anchor=CENTER, padx=10, pady=(10, 10))
        butt18=Button(text='Назад', font=('Arial',14), command=support_back, width=30, height=2, background='gray', foreground='white')
        butt18["border"] = "5"
        butt18.pack(anchor=CENTER, padx=10, pady=(10, 10))
    def donate():
        s_catch.play()
        donat_now()
    def music():
        s_catch.play()
        hide_settings()
        def music_back():
            s_catch.play()
            butt19.pack_forget()
            butt20.pack_forget()
            butt21.pack_forget()
            show_settings()
        butt19=Button(text='Ввімкнути', font=('Arial',14), command=music_unpause, width=30, height=2, background='gray', foreground='white')
        butt19["border"] = "5"
        butt19.pack(anchor=CENTER, padx=10, pady=(100, 10))
        butt20=Button(text='Вимкнути', font=('Arial',14), command=music_pause, width=30, height=2, background='gray', foreground='white')
        butt20["border"] = "5"
        butt20.pack(anchor=CENTER, padx=10, pady=(10, 10))
        butt21=Button(text='Назад', font=('Arial',14), command=music_back, width=30, height=2, background='gray', foreground='white')
        butt21["border"] = "5"
        butt21.pack(anchor=CENTER, padx=10, pady=(10, 10))
    butt9=Button(text='Музика', font=('Arial',14), command=music, width=30, height=2, background='gray', foreground='white')
    butt9["border"] = "5"
    butt9.pack(anchor=CENTER, padx=100, pady=(50, 10))
    butt10=Button(text='Підтримати проєкт', font=('Arial',14), command=donate, width=30, height=2, background='gray', foreground='white')
    butt10["border"] = "5"
    butt10.pack(anchor=CENTER, padx=10, pady=10)
    butt11=Button(text='Тех.Підтримка', font=('Arial',14), command=support, width=30, height=2, background='gray', foreground='white')
    butt11["border"] = "5"
    butt11.pack(anchor=CENTER, padx=10, pady=10)
    butt12=Button(text='Автори', font=('Arial',14), command=author, width=30, height=2, background='gray', foreground='white')
    butt12["border"] = "5"
    butt12.pack(anchor=CENTER, padx=10, pady=10)
    butt13=Button(text='Назад', font=('Arial',14), command=back, width=30, height=2, background='gray', foreground='white')
    butt13["border"] = "5"
    butt13.pack(anchor=CENTER, padx=10, pady=10)
    


butt0=Button(text='❔',font=('Arial',21), command=rule_button, background='gray', foreground='white', width=3 )
butt0["border"] = "5"
butt0.pack(side="top", anchor=NE)

label2=Label(text=program_version,font=('OCR-A BT',14), background='#76a2c9', foreground='black')
label2.pack(side="bottom", anchor=NE)

label1=Label(text='CITIES GAME', font=('OCR-A BT',58), background='#dae6f2', foreground='black')
label1.pack(anchor=CENTER, side="top")

butt1=Button(text='Розпочати гру', font=('Arial',14), command=start, width=30, height=2, background='gray', foreground='white')
butt1["border"] = "5"
butt1.pack(anchor=CENTER, padx=10, pady=(100, 10))

butt2=Button(text='Історія рахунків', font=('Arial',14), command=score_history, width=30, height=2, background='gray', foreground='white')
butt2["border"] = "5"
butt2.pack(anchor=CENTER, padx=10, pady=10)

butt3=Button(text='Налаштування', font=('Arial',14), command=settings, width=30, height=2, background='gray', foreground='white')
butt3["border"] = "5"
butt3.pack(anchor=CENTER, padx=10, pady=10)

butt4=Button(text='Вихід ', font=('Arial',14), command=close, width=30, height=2, background='gray', foreground='white')
butt4["border"] = "5"
butt4.pack(anchor=CENTER, padx=10, pady=10)



root.mainloop()