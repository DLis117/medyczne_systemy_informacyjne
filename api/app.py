from flask import Flask, render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager,login_user, current_user,logout_user,login_required
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)
db=SQLAlchemy()
login_manager=LoginManager()

class User(UserMixin,db.Model):
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(100),unique=True)
    name=db.Column(db.String(25))
    password=db.Column(db.String(100))

    def __init__(self, email, name, password):
        self.name = name
        self.email = email
        self.password = password

class Grupy(db.Model):
    idGrupy=db.Column(db.Integer, primary_key=True)
    userGrupy=db.Column(db.Integer,db.ForeignKey(User.id))###########3do zanotowania
    nazwaGrupy=db.Column(db.String(100))

    def __init__(self, userGrupy, nazwaGrupy):
        self.userGrupy = userGrupy
        self.nazwaGrupy=nazwaGrupy

class Notatka(db.Model):
    idNotatki=db.Column(db.Integer, primary_key=True)
    userNotatki=db.Column(db.Integer,db.ForeignKey(User.id))###########3do zanotowania
    grupaNotatki=db.Column(db.Integer,db.ForeignKey(Grupy.idGrupy))
    trescNotatki=db.Column(db.String(1000))#notatki do 1000znakow
    nazwaNotatki=db.Column(db.String(25))#nazwy do 25znakow bo wychodza poza pole xd

    def __init__(self, userNotatki, grupaNotatki, trescNotatki,nazwaNotatki):
        self.userNotatki = userNotatki
        self.grupaNotatki = grupaNotatki
        self.trescNotatki = trescNotatki
        self.nazwaNotatki = nazwaNotatki


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def main():
    return render_template("index.html")


@app.route('/login',methods=['POST','GET'])
def login():
        return render_template(('logowanie.html'))

@app.route('/logging',methods=['POST','GET'])
def logging():
    if(request.method=='POST'):
        login=request.form.get('login')
        haslo = request.form.get('haslo')
        if (login == "") or (haslo == ""):
            flash("wypelnij wszystkie pola!")
            return render_template(('logowanie.html'))
        x=User.query.filter_by(name=login).first()
        if x and check_password_hash(x.password,haslo):
            login_user(x)
            return redirect(url_for('logged'))
        flash("nieprawidlowy login lub haslo!")
        return render_template(('logowanie.html'))

@app.route('/logged')
@login_required
def logged():
    baza=[]
    x=Grupy.query.filter(Grupy.userGrupy==current_user.id)
    y=Notatka.query.filter(Notatka.userNotatki==current_user.id)#na start wyswietl wszystkie notatki danego usera
    baza.append(current_user.name)
    baza.append(x)
    baza.append(y)
    baza.append(current_user.id)

    return render_template('profile.html',dana=baza)

@app.route('/trytoeditprofile',methods=['POST','GET'])
@login_required
def editprofinish():
    if (request.method == 'POST'):
        obecnynick=current_user.name
        # id=current_user.id
        haslo=request.form.get('haslo')
        nowynick=request.form.get('login')
        userzy=User.query.all()
        if (len(nowynick) < 1):
            flash("login nie moze byc pusty!")
            baza = []
            baza.append(current_user.name)
            baza.append(current_user.id)
            return render_template('editprofile.html', dana=baza)
        if (len(nowynick)>25):
            flash("login nie moze przekraczac 25 znakow!")
            baza = []
            baza.append(current_user.name)
            baza.append(current_user.id)
            return render_template('editprofile.html', dana=baza)
        for i in userzy:
            if(i.name==nowynick):
                flash("login zajety!")
                baza = []
                baza.append(current_user.name)
                baza.append(current_user.id)
                return render_template('editprofile.html', dana=baza)
        x = User.query.filter_by(name=obecnynick).first()
        if check_password_hash(x.password, haslo):
            x.name=nowynick
            db.session.commit()
            logout_user()
            return render_template(('index.html'))
        else:
            flash("hasla sie nie zgadzaja!")
            baza = []
            baza.append(current_user.name)
            baza.append(current_user.id)
            return render_template('editprofile.html', dana=baza)

@app.route('/trytoeditpassword',methods=['POST','GET'])
@login_required
def editpass():
    if (request.method == 'POST'):
        haslo1=request.form.get('haslo1')
        haslo2 = request.form.get('haslo2')
        x = User.query.filter(User.id==current_user.id).first()
        if check_password_hash(x.password, haslo1):
            if(len(haslo2)<8):
                flash("haslo musi miec przynajmniej 8 znakow!")
                baza = []
                baza.append(current_user.name)
                baza.append(current_user.id)
                return render_template('editprofile.html', dana=baza)
            else:
                x.password=generate_password_hash(haslo2)
                db.session.commit()
                logout_user()
                return render_template(('index.html'))
        else:
            flash("obecne haslo niepoprawne!")
            baza = []
            baza.append(current_user.name)
            baza.append(current_user.id)
            return render_template('editprofile.html', dana=baza)


@app.route('/editprofile',methods=['POST','GET'])
@login_required
def editpro():
    if (request.method == 'POST'):
        baza=[]
        baza.append(current_user.name)
        baza.append(current_user.id)
        return render_template('editprofile.html',dana=baza)

@app.route('/usunkonto',methods=['POST','GET'])
@login_required
def delacc():
    if (request.method == 'POST'):
        cri=current_user.id
        gr=Grupy.query.filter(Grupy.userGrupy==cri)
        for i in gr:
            v=Notatka.query.filter(Notatka.grupaNotatki==i.idGrupy)
            for j in v:
                db.session.delete(j)
            db.session.commit()
            db.session.delete(i)
        db.session.commit()
        q=User.query.filter(User.id==cri).first()
        db.session.delete(q)
        db.session.commit()
        logout_user()
        return render_template(('index.html'))


@app.route('/displayfromgroup',methods=['POST','GET'])
@login_required
def disp():
    if (request.method == 'POST'):
        idgrupyy = request.form.get('idgrupyy')
        # print(idgrupyy)
    baza=[]
    x=Grupy.query.filter(Grupy.userGrupy==current_user.id)
    z=Notatka.query.filter(Notatka.userNotatki==current_user.id)#na start wyswietl wszystkie notatki danego usera
    y=[]

    for i in z:
        if int(i.grupaNotatki)==int(idgrupyy):
            y.append(i)
    b=Grupy.query.filter(Grupy.idGrupy==idgrupyy).first()
    baza.append(current_user.name)
    baza.append(x)
    baza.append(y)
    baza.append(idgrupyy)
    baza.append(b.nazwaGrupy)
    return render_template('profile.html',dana=baza)


@app.route('/usunNotatke',methods=['POST','GET'])
@login_required
def delnot():
    if (request.method == 'POST'):
        idnotki = request.form.get('idnotki')
        # print(idnotki)
        q=Notatka.query.filter(idnotki==Notatka.idNotatki).first()
        db.session.delete(q)
        db.session.commit()

    baza=[]
    x=Grupy.query.filter(Grupy.userGrupy==current_user.id)
    y=Notatka.query.filter(Notatka.userNotatki==current_user.id)#na start wyswietl wszystkie notatki danego usera

    baza.append(current_user.name)
    baza.append(x)
    baza.append(y)
    return render_template('profile.html',dana=baza)




@app.route('/usunGrupe',methods=['POST','GET'])
@login_required
def delgr():
    if (request.method == 'POST'):
        idgrupyy = request.form.get('idgruppy')
        idgrupyy=int(idgrupyy)
        #najpierw usun z niej wszystkie notatki
        q=Notatka.query.filter(Notatka.userNotatki==current_user.id)
        for i in q:
            if int(i.grupaNotatki) == int(idgrupyy):
                db.session.delete(i)
        db.session.commit()
        b = Grupy.query.filter(Grupy.idGrupy == idgrupyy).first()
        db.session.delete(b)
        db.session.commit()

    baza=[]
    x=Grupy.query.filter(Grupy.userGrupy==current_user.id)
    y=Notatka.query.filter(Notatka.userNotatki==current_user.id)#na start wyswietl wszystkie notatki danego usera

    baza.append(current_user.name)
    baza.append(x)
    baza.append(y)
    return render_template('profile.html',dana=baza)




@app.route('/edytujGrupe',methods=['POST','GET'])
@login_required
def editGr():
    if (request.method == 'POST'):
        idgruppy = request.form.get('idgruppy')
        b = Grupy.query.filter(Grupy.idGrupy==idgruppy).first()
        grupa=[]
        grupa.append(b.nazwaGrupy)
        grupa.append(idgruppy)
        return render_template('editgroup.html',grupa=grupa)


@app.route('/edytujNotatke',methods=['POST','GET'])
@login_required
def editNot():
    if (request.method == 'POST'):
        idnotatkii = request.form.get('idnotatkii')
        b = Notatka.query.filter(Notatka.idNotatki==idnotatkii).first()
        grupa=[]
        grupa.append(b.idNotatki)
        grupa.append(b.nazwaNotatki)
        grupa.append(b.trescNotatki)

        c = Grupy.query.filter(Grupy.userGrupy==current_user.id)
        grupa.append(c)
        return render_template('editnote.html',grupa=grupa)


@app.route('/editnotefinish',methods=['POST','GET'])
@login_required
def editnotefinish():
    if (request.method == 'POST'):
        idnotatki = request.form.get('idnotatkii')
        nazwanotatkii = request.form.get('nazwanotatkii')
        git=True
        if(len(nazwanotatkii)>25):
            git=False
            flash("nazwa notatki nie moze przekraczac 25 znakow!")
        if(len(nazwanotatkii)<1):
            flash("nazwa notatki nie moze byc pusta!")
            git=False

        trescnotatkii = request.form.get('trescnotatkii')
        if (len(trescnotatkii) > 1000):
            git = False
            flash("nazwa notatki nie moze przekraczac 1000 znakow!")
        if(git==False):
            idnotatkii = request.form.get('idnotatkii')
            b = Notatka.query.filter(Notatka.idNotatki == idnotatkii).first()
            grupa = []
            grupa.append(b.idNotatki)
            grupa.append(b.nazwaNotatki)
            grupa.append(b.trescNotatki)

            c = Grupy.query.filter(Grupy.userGrupy == current_user.id)
            grupa.append(c)
            return render_template('editnote.html', grupa=grupa)

        nazwagruppy = request.form.get('nazwagrupyy')

        q=Notatka.query.filter(idnotatki==Notatka.idNotatki).first()
        db.session.delete(q)
        db.session.commit()

        v=Grupy.query.filter(Grupy.userGrupy==current_user.id)

        for i in v:
            if(i.nazwaGrupy==nazwagruppy):
                no=Notatka(current_user.id,i.idGrupy,trescnotatkii,nazwanotatkii)
                db.session.add(no)
                db.session.commit()
                break

        baza = []
        x = Grupy.query.filter(Grupy.userGrupy == current_user.id)
        y = Notatka.query.filter(
            Notatka.userNotatki == current_user.id)  # na start wyswietl wszystkie notatki danego usera

        baza.append(current_user.name)
        baza.append(x)
        baza.append(y)
        return render_template('profile.html', dana=baza)


@app.route('/editGr',methods=['POST','GET'])
@login_required
def editGrfinish():
    if (request.method == 'POST'):
        idgruppy = request.form.get('idgruppy')
        nazwagruppy = request.form.get('nazwagruppy')

        if(len(nazwagruppy)>25):
            flash("nazwa grupy nie moze przekraczac 25 znakow!")
            idgruppy = request.form.get('idgruppy')

            b = Grupy.query.filter(Grupy.idGrupy == idgruppy).first()
            grupa = []
            grupa.append(b.nazwaGrupy)
            grupa.append(idgruppy)
            return render_template('editgroup.html', grupa=grupa)
        if(len(nazwagruppy)<1):
            flash("nazwa grupy nie moze byc pusta!")
            idgruppy = request.form.get('idgruppy')

            b = Grupy.query.filter(Grupy.idGrupy == idgruppy).first()
            grupa = []
            grupa.append(b.nazwaGrupy)
            grupa.append(idgruppy)
            return render_template('editgroup.html', grupa=grupa)

        b = Grupy.query.filter(Grupy.idGrupy == idgruppy).first()
        b.nazwaGrupy = nazwagruppy
        db.session.commit()
        # print(b.nazwaGrupy)

        baza = []
        x = Grupy.query.filter(Grupy.userGrupy == current_user.id)
        y = Notatka.query.filter(
            Notatka.userNotatki == current_user.id)  # na start wyswietl wszystkie notatki danego usera

        baza.append(current_user.name)
        baza.append(x)
        baza.append(y)
        return render_template('profile.html', dana=baza)

@app.route('/dodaj',methods=['POST','GET'])
@login_required
def addne():
    if (request.method == 'POST'):
        x = Grupy.query.filter(Grupy.userGrupy == current_user.id)
        return render_template('addnew.html',x=x)

@app.route('/addgroup',methods=['POST','GET'])
@login_required
def addng():
    if (request.method == 'POST'):
        naz=request.form.get('nazwa')

        if (len(naz) > 25):
            flash("nazwa grupy nie moze przekraczac 25 znakow!")
            return render_template('addnew.html')
        if (len(naz) < 1):
            flash("nazwa grupy nie moze byc pusta!")
            return render_template('addnew.html')

        gr=Grupy(current_user.id,naz)
        db.session.add(gr)
        db.session.commit()

        baza = []
        x = Grupy.query.filter(Grupy.userGrupy == current_user.id)
        y = Notatka.query.filter(
            Notatka.userNotatki == current_user.id)  # na start wyswietl wszystkie notatki danego usera

        baza.append(current_user.name)
        baza.append(x)
        baza.append(y)
        return render_template('profile.html', dana=baza)


@app.route('/addnot',methods=['POST','GET'])
@login_required
def addngx():
    if (request.method == 'POST'):
        x = Grupy.query.filter(Grupy.userGrupy == current_user.id)
        naz=request.form.get('nazwa')
        if (len(naz) > 25):
            flash("nazwa notatki nie moze przekraczac 25 znakow!")
            return render_template('addnew.html',x=x)
        if (len(naz) < 1):
            flash("nazwa notatki nie moze byc pusta!")
            return render_template('addnew.html',x=x)
        tresc=request.form.get('tresc')
        if (len(tresc) > 1000):
            flash("tresc notatki nie moze przekraczac 1000 znakow!")
            return render_template('addnew.html',x=x)

        nazwagrupyy=request.form.get('nazwagrupyy')

        v = Grupy.query.filter(Grupy.userGrupy == current_user.id)
        for i in v:
            if (i.nazwaGrupy == nazwagrupyy):
                no = Notatka(current_user.id, i.idGrupy, tresc, naz)
                db.session.add(no)
                db.session.commit()
                break

        baza = []
        x = Grupy.query.filter(Grupy.userGrupy == current_user.id)
        y = Notatka.query.filter(
            Notatka.userNotatki == current_user.id)  # na start wyswietl wszystkie notatki danego usera

        baza.append(current_user.name)
        baza.append(x)
        baza.append(y)
        return render_template('profile.html', dana=baza)


@app.route('/logout',methods=['POST','GET'])
@login_required
def logout():
    logout_user()
    return render_template(('index.html'))


@app.route('/register',methods=['POST','GET'])
def reg():
        return render_template(('rejestracja.html'))

@app.route('/trytoregister',methods=['POST','GET'])
def trytoreg():
    if(request.method=='POST'):
        #czy wszystkie pola zostaly wypelnione?
        login=request.form.get('login')
        haslo = request.form.get('haslo')
        email=request.form.get('email')
        # print(login,email,haslo)
        if(login=="")or(haslo=="")or(email==""):
            flash("wypelnij wszystkie pola!")
            return render_template(('rejestracja.html'))
        else:
            #sprawdz czy sie nie powtarzaja
            x = User.query.filter_by(name=login).first()
            if x != None:
                flash('uzytkownik o takim nicku juz istnieje!')
                # print('uzytkownik o takim nicku juz istnieje!')
                return render_template(('rejestracja.html'))
            x = User.query.filter_by(email=email).first()
            if x != None:
                flash("na ten adres email zostalo juz zalozone konto!")
                return render_template(('rejestracja.html'))
            if (len(haslo) < 8):
                flash("dlugosc hasla powinna wynosic conajmniej 8 zakow!")
                return render_template(('rejestracja.html'))
            if (len(login) > 100):
                flash("dlugosc loginu nie moze przekraczac 100 znakow!")
                return render_template(('rejestracja.html'))
            if (len(haslo) > 100):
                flash("dlugosc hasla nie moze przekraczac 100 znakow!")
                return render_template(('rejestracja.html'))
            if (len(login) >25):
                flash("dlugosc loginu nie moze przekraczac 25 znakow!")
                return render_template(('rejestracja.html'))
        # print("przed dodaniem")
        nowy_user = User(email, login,generate_password_hash(haslo))#????????
        db.session.add(nowy_user)
        db.session.commit()
        return render_template(('index.html'))

if __name__=="__main__":
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite'
    app.config['SECRET_KEY']='XDDDDD'
    db.init_app(app)
    login_manager.login_view='login'
    login_manager.init_app(app)
    db.create_all(app=app)
    app.run()