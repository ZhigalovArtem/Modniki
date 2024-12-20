from datetime import datetime
from flask import Flask, json, jsonify, render_template, request, redirect, url_for, session, flash
from flask_socketio import SocketIO, emit, join_room, leave_room
import db

app = Flask(__name__)
app.secret_key = 'supersecretkey'
socketio = SocketIO(app)
anketa = {}

@app.route('/') # Индекс
def start_page():
    print(session)
    db.create_tables()
    return render_template('index.html')

@app.route('/chooseClientOrStyle') # выбор роли (стилист\клиент)
def chooseClientOrStyle():
    return render_template('chooseClientOrStyle.html')

@app.route('/auth', methods=['POST', 'GET']) # авторизация
def auth_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        userInfo = db.get_user_info_by_email(email)
        print(userInfo)
        if userInfo:
            print('Правильное мыло')
            if password == userInfo.get('password'):
                print('Правильный пароль')
                session['email'] = email
                if userInfo['stylist'] == 0:
                    return redirect(url_for('lkCL'))  # При удачной авторизации перенаправляется в лк
                if userInfo['stylist'] == 1:
                    return redirect(url_for('lkST'))
            else:
                #flash(message='Неправильный пароль')
                print('Неправильный пароль')
        else:
            #flash(message='Такого пользователя не существует')
            print('Такого пользователя не существует')
    return render_template('auth.html')

@app.route('/registrationCL', methods=['GET', 'POST'])  # регистрация клиента
def registrationCL_page(): ########### ИСПРАВИТЬ #################
    if request.method == 'POST':
        #данные регистрации
        email = request.form.get('email')
        first_name = request.form.get('name')
        last_name = request.form.get('surname')
        password = request.form.get('password')
        birth_date = request.form.get('dob')
        isStylist = False
        level = 0

        #параметры пользователя
        height = request.form.get('height')
        weight = request.form.get('weight')
        chest_size = request.form.get('chest')
        ass_size = request.form.get('hips')
        waist_size = request.form.get('waist') # талия
        clothes_size = request.form.get('size')

        print(f'{email}, {first_name}, height: {height}')

        #retypedPassword = request.form.get('retypedPassword')
        userInfo = db.get_user_info_by_email(email)

        if userInfo is None:
            #if password == retypedPassword:

                db.add_user(first_name= first_name, last_name= last_name, email= email, password= password,
                             birth_date= birth_date, level= level, photo_path= '', stylist= isStylist)
                db.add_user_params(height, weight, chest_size, ass_size, waist_size, clothes_size, email)

                print('Регистрация успешна!')
                session['email'] = email
                return redirect(url_for('auth_page'))
                #return redirect(url_for('anket_gender'))  # Редирект на страницу выбра пола анкета
           #else:
                #flash(message='Пароли не совпадают')
        else:
            #flash(message='Эта почта уже используется')
            print('Эта почта уже используется')

    return render_template('registration.html')  # Возвращаем форму регистрации для GET-запроса

@app.route('/registrationST', methods=['GET', 'POST'])  # регистрация стилиста
def registrationST_page(): ###### исправить №№№№№№№№№
    if request.method == 'POST':
        #данные регистрации
        email = request.form.get('email')
        first_name = request.form.get('name')
        last_name = request.form.get('surname')
        password = request.form.get('password')
        #birth_date = request.form.get('birth_date')
        isStylist = True
        level = 1

        #Тут надо сделать загрузку файлов## на хуй посланы

        #retypedPassword = request.form.get('retypedPassword')
        userInfo = db.get_user_info_by_email(email)

        if userInfo is None:
            #if password == retypedPassword:
                db.add_user(first_name= first_name, last_name= last_name, email= email, 
                             birth_date='NULL', password= password, level= level, photo_path= '', stylist= isStylist)
                flash('Регистрация успешна!')
                return redirect(url_for('auth_page'))
                #return redirect(url_for('start_page'))  # Редирект на страницу входа после регистрации ???
           #else:
                flash(message='Пароли не совпадают')
        else:
            print('Эта почта уже используется')

    return render_template('registrationStilist.html')  # Возвращаем форму регистрации для GET-запроса

@app.route('/anket-gender', methods = ['POST', 'GET']) # выбор пола для анкеты
def anket_gender():
    # if 'email' not in session:
    #     return redirect(url_for('start_page'))
    print(session)
    if 'email' in session:
        email = session['email']
    else:
        pass

    if request.method == 'POST':
        gender = request.form.get('gender')
        print(f'email {email}\ngender {gender}')
        anketa[email]= {'gender': gender}
        return redirect(url_for('anket_purpose'))
    
    return render_template('gender.html') # after that target woman

@app.route('/anket-purpose', methods = ['POST', 'GET']) # первая страниц анкеты(цели)
def anket_purpose():
    email = session['email']
    print(email)
    user_gender = get_gender(email)
    print(f'\n\npurpose {user_gender}\n\n')
    if request.method == 'POST': # запись выбранных ответов
            everyday1 = request.form.get('everyday1')
            everyday2 = request.form.get('everyday2')
            everyday3 = request.form.get('everyday3')
            everyday4 = request.form.get('everyday4')
            everyday5 = request.form.get('everyday5')
            everyday6 = request.form.get('everyday6')

            everyday_section = {'1': everyday1, '2': everyday2, '3': everyday3,
                                '4': everyday4, '5': everyday5, '6': everyday6}

            home1 = request.form.get('home1')
            home2 = request.form.get('home2')
            home3 = request.form.get('home3')
            home4 = request.form.get('home4')
            home5 = request.form.get('home5')
            home6 = request.form.get('home6')
            
            home_section = {'1': home1, '2': home2, '3': home3,
                                '4': home4, '5': home5, '6': home6}

            anketa[email]['purpose'] = {'everyday': everyday_section, 'home': home_section}
            print(f'\n\n{anketa}\n\n')
    
    if user_gender == '0':
        return render_template('targetWoman.html')
    else:
        return render_template('man')

@app.route('/anket-style', methods = ['POST', 'GET']) # выбор стиля 2
def anket_style():
    email = session['email']
    if request.method == 'POST':
        style = request.form.get('') # исправить
        anketa[email]['style'] = style
    return render_template('/chooseStyle.html')

@app.route('/anket-confirmStyle', methods = ['POST', 'GET']) # выбор стиля 4
def confirmStyle():
    email = session['email']
    if request.method == 'POST':
        answer = request.form.get('') # исправить
        anketa[email]['answer'] = answer
    return render_template('confirmStyle.html')

@app.route('/season', methods = ['POST', 'GET']) # сезон 5
def season(): # исправить под два пола
    email = session['email']
    if request.method == 'POST':
        season = request.form.get('') # исправить
        anketa[email]['season'] = season
    return render_template('season.html')

@app.route('/skin1', methods = ['POST', 'GET']) # 6
def skin1():
    email = session['email']
    user_gender = get_gender(email)

    if request.method == 'POST':
        liked = request.form.get('') # исправить

    if user_gender == 0:
        return render_template('skin1.html')
    else:
        return render_template('skin1man.html')

@app.route('/skin2', methods = ['POST', 'GET']) # 7
def skin2():
    email = session['email']
    user_gender = get_gender(email)
    if request.method == 'POST':
        liked = request.form.get('') # исправить

    if user_gender == 0:
        return render_template('skin2.html')
    else:
        return render_template('skin2man.html')

@app.route('/skin3', methods = ['POST', 'GET']) # 8
def skin3():
    email = session['email']
    user_gender = get_gender(email)

    if request.method == 'POST':
        liked = request.form.get('') # исправить

    if user_gender == 0:
        return render_template('skin3.html')
    else:
        return render_template('skin3man.html')
    
@app.route('/skin4', methods = ['POST', 'GET']) # 9
def skin4():
    email = session['email']
    user_gender = get_gender(email)

    if request.method == 'POST':
        liked = request.form.get('') # исправить

    if user_gender == 0:
        return render_template('skin4.html')
    else:
        return render_template('skin4man.html')

@app.route('/skin5', methods = ['POST', 'GET']) # 10
def skin5():
    email = session['email']
    user_gender = get_gender(email)

    if request.method == 'POST':
        liked = request.form.get('') # исправить

    if user_gender == 0:
        return render_template('skin5.html')
    else:
        return render_template('skin5man.html')

@app.route('/skin6', methods = ['POST', 'GET']) #11
def skin6():
    email = session['email']
    user_gender = get_gender(email)

    if request.method == 'POST':
        liked = request.form.get('') # исправить

    if user_gender == 0:
        return render_template('skin6.html')
    else:
        return render_template('skin6man.html')
    
@app.route('/skin7', methods = ['POST', 'GET']) #12
def skin7():
    email = session['email']
    user_gender = get_gender(email)

    if request.method == 'POST':
        liked = request.form.get('') # исправить

    if user_gender == 0:
        return render_template('skin.7.html')
    else:
        return render_template('skin7man.html')
    
@app.route('/skin8', methods = ['POST', 'GET']) #13
def skin8():
    email = session['email']
    user_gender = get_gender(email)

    if request.method == 'POST':
        liked = request.form.get('') # исправить

    if user_gender == 0:
        return render_template('skin.8.html')
    else:
        return render_template('skin8man.html')
    
@app.route('/skin9', methods = ['POST', 'GET']) #14
def skin9():
    email = session['email']
    user_gender = get_gender(email)

    if request.method == 'POST':
        liked = request.form.get('') # исправить

    if user_gender == 0:
        return render_template('skin9.html')
    else:
        return render_template('skin9man.html')
    
@app.route('/skin10', methods = ['POST', 'GET']) #15
def skin10():
    email = session['email']
    user_gender = get_gender(email)

    if request.method == 'POST':
        liked = request.form.get('') # исправить

    if user_gender == 0:
        return render_template('skin10.html')
    else:
        return render_template('skin10man.html')

@app.route('/wrkEDC') # выбор стиля 3
def wrkEDC():
    return render_template('workOrEducation.html')

@app.route('/stylistam')
def stylistam():
    return render_template('stilistam.html')

@app.route('/capsula')
def capsula():
    return render_template('capsula.html')

@app.route('/lkCL')
def lkCL():
    email = session['email']
    user_info = db.get_user_info_by_email(email)

    return render_template('lkClient.html', user_info=user_info)

@app.route('/chatsCL')
def chatsCL():
    email = session['email']
    user_info = db.get_user_info_by_email(email)
    if user_info['stylist'] == 0:
        users = db.get_ST_list()
    else:
        users = db.get_CL_list()

    return render_template('lkClientChat.html', users = users)

####### ДОДЕЛАТЬ СОЗДАНИЕ ЧАТОВ, ОТОБРАЖЕНИЕ СУЩЕСТВУЮЩИХ ЧАТОВ, СОХРАНЕНИЕ И ОТПРАВКА СООБЩЕНИЙ

@app.route('/create_chat_with_user/<int:user_id>', methods = ['GET', 'POST']) # Создание чата
def create_chat_with_user(user_id):
    if 'email' not in session:
        return redirect(url_for('home'))  # Если нет, отправляем на логин
    
    current_user = session['email']
    user_info = db.get_user_info(current_user) # Получение инфомарци о пользователе

    if not user_info:
        flash('Ошибка авторизации')
        return redirect(url_for('home'))
    
    current_user_id = user_info['user_id']

    chat_between_users = db.get_chat_between_users(current_user_id, user_id) # Получении информации о чатах между пользов.
    print(f'Chat between users: {chat_between_users}')

    if not chat_between_users: # Проверка на существование чата между пользователями
        db.create_chat(user_ids=[current_user_id, user_id]) # Создание чата

    return redirect(url_for('chat')) # Обновление страницы по завершении

@app.route('/chatRoom')
def chat_room():
   return render_template('lkClientChatRoom.html') 

@app.route('/lkST')
def lkST():
   email = session['email']
   user_info = db.get_user_info_by_email(email)
   return render_template('lkStilist.html', user_info = user_info) 

@app.route('/users')
def users():
    return db.get_users()

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('email', None)
    return redirect(url_for('start_page'))

def get_gender(email):
    user_gender = anketa.get(email)
    print(f'full {user_gender}')
    print(user_gender['gender'])
    return user_gender['gender']


if __name__ == '__main__':
    socketio.run(app, debug=True)
