import requests
from bs4 import BeautifulSoup

from flask import render_template, request, url_for, session, redirect
from urlapp import app

import os

import sqlite3

db = "user.db"

app.secret_key = os.urandom(24)


@app.route('/')
def index():
    return render_template(
        'index_front.html'
    )

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template(
            'index_login.html'
        )

    else:
        name = request.form.get('username')
        psw = request.form.get('password')

        con = sqlite3.connect(db)
        cur = con.cursor()

        cur.execute('SELECT * FROM user_data WHERE (username, password)=(?,?)',[name, psw])

        key_data = cur.fetchall()

        if len(key_data) != 0:
            session['username'] = name

            return redirect(url_for(
                'mypage')
                
            )
        
        else:
            keymisserror = 'ログインできません'
            return render_template(
                'index_login.html',
                alreadyerror = keymisserror
            )


@app.route('/signup', methods=['GET', 'POST'])
def sighnup():  
    if request.method == 'POST':
        new_name = request.form.get("newusername")
        pws = request.form.get("newpassword")
        repws = request.form.get("repassword")

        con = sqlite3.connect(db)
        cur = con.cursor()

        cur.execute('SELECT * FROM user_data WHERE username=?',[new_name])
        ans = cur.fetchall()
        password = pws
        con.commit()
    
        # print(ans)

        if pws != repws or pws == '':
            misserror = "パスワードが一致しません"
            return render_template (
                'index_signup.html',
                misserror = misserror
            )
        
        elif pws == repws and len(ans)==0:
            con = sqlite3.connect(db)
            cur = con.cursor()

            password =  pws
            con.execute('INSERT INTO user_data(username, password) VALUES (?,?)', [new_name, password])

            con.commit()
            cur.close()
            con.close()

            return render_template(
                'index_login.html',
                new_name = new_name,
                password = password
            )
        
        elif len(ans) != 0:
            alreadyerror = "登録済みです"
            return render_template(
                'index_login.html',
                alreadyerror = alreadyerror
            )
        
    else:
        return render_template(
            'index_signup.html'
        )
            

@app.route('/guest', methods=['POST'])
def guest():
    return render_template(
        'index_gest.html'
    )

    

@app.route('/mypage', methods=['GET','POST'])
def mypage():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    if request.method == 'GET':
        

        con = sqlite3.connect(db)
        cur = con.cursor()
        result = cur.execute('SELECT title, urlname FROM bookmark WHERE username=?',(username,)).fetchall()
        cur.close()
        con.close()

        return render_template(
            'index_mypage.html',
            username = username,
            result = result
        )
    
    else:
        title = request.form.get('urlname')
        url = request.form.get('urlbody')

        con = sqlite3.connect(db)
        cur = con.cursor()

        con.execute('INSERT INTO bookmark(username, title, urlname) VALUES (?,?,?)', [username, title, url])

        cur.execute('SELECT title, urlname FROM bookmark WHERE username=?', (username,))
        result = cur.fetchall()

        con.commit()
        cur.close()
        con.close()
        


        return render_template(
            'index_mypage.html',
            username = username,
            result = result
        )


@app.route('/url_data', methods = ["GET","POST"])
def url_data():
    if 'username' not in session:
        return redirect(url_for('login'))


    if request.method == 'GET':
        return render_template(
            'index.html'
        )
        
    elif request.method == 'POST':
        url = request.form.get("urlname")
        if url:
            urlname = str(url)
            resupons = requests.get(urlname)
            resupons.encoding = resupons.apparent_encoding

            html = resupons.text
            soup = BeautifulSoup(html, "html.parser")
            result = soup.find("body").text
            image = soup.find_all("img")
            img_data = []

            for element in image:
                img = element.get("src")
                img_data.append(img)

            outurl = soup.find_all("a")
            outurl_data = []

            for delate in outurl:
                dela = delate.get("href")
                outurl_data.append(dela)

            return render_template(
                'index.html',
                edit = soup,
                text = result,
                img_data = img_data,
                outurl_data = outurl_data
            )
        
        else:
            finderro = "urlを読み取れませんでした"
            return render_template(
                'index.html',
                finderro = finderro
            )

@app.errorhandler(500)
def errprhandler(error):
    error = 'urlが見つかりません'
    return render_template(
        'index.html',
        finderro = error,
    ), 500



@app.route('/url_gest', methods = ["GET","POST"])
def url_gest():
    if request.method == 'GET':
        return render_template(
            'index_gest.html'
        )
        
    elif request.method == 'POST':
        url = request.form.get("urlname")
        if url:
            urlname = str(url)
            resupons = requests.get(urlname)
            resupons.encoding = resupons.apparent_encoding

            html = resupons.text
            soup = BeautifulSoup(html, "html.parser")
            result = soup.find("body").text
            image = soup.find_all("img")
            img_data = []

            for element in image:
                img = element.get("src")
                img_data.append(img)

            outurl = soup.find_all("a")
            outurl_data = []

            for delate in outurl:
                dela = delate.get("href")
                outurl_data.append(dela)

            return render_template(
                'index_gest.html',
                edit = soup,
                text = result,
                img_data = img_data,
                outurl_data = outurl_data
            )
        
        else:
            finderro = "urlを読み取れませんでした"
            return render_template(
                'index_gest.html',
                finderro = finderro
            )

@app.errorhandler(500)
def errprhandler(error):
    error = 'urlが見つかりません'
    return render_template(
        'index.html',
        finderro = error,
    ), 500

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

    
