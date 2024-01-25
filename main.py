#main.py
import sqlite3
from flask import Flask, redirect, render_template, request, url_for



app = Flask(__name__)




data = []


def veriAl():
    global data
    with sqlite3.connect("book.db") as con:
        cur = con.cursor()
        cur.execute("select * from tblBook")
        data = cur.fetchall()
        for i in data:
            print(i)


def veriekle(title, author, year):
    with sqlite3.connect("book.db") as con:
        cur = con.cursor()
        cur.execute("insert into tblBook (booktitle, bookauthor, bookyear) values (?,?,?)", (title, author, year))
        print("veriler eklendi")




def verisil(id):
    with sqlite3.connect("book.db") as con:
        cur = con.cursor()
        cur.execute("delete from tblBook where id =?", (id,))
        con.commit
        print("veriler silindi")   





def veriguncelle(id, title, author, year):
    with sqlite3.connect("book.db") as con:
        cur = con.cursor()
        cur.execute("update tblBook set booktitle = ? , bookauthor = ? , bookyear = ? where id = ? ", (title, author, year,id))
        print("veriler guncellendi")     



        


@app.route("/index")
def index():

    books = [

    {
        'bookTitle':'Merhabalar'
    },

    {
        'bookTitle':'İyi Günler'
    }

    ]



    return render_template("index.html", books = books)


@app.route("/yemek")
def yemek():
    print("yemek")

    veriAl()


    return render_template("yemek.html", veri = data)


@app.route("/contact")
def contact():
    print("contact")
    return render_template("contact.html")




@app.route("/yemekekle", methods=["GET", "POST"])
def yemekekle():
    print("yemekekle")
    if request.method == "POST":
        bookTitle = request.form.get("bookTitle")
        bookAuthor = request.form.get("bookAuthor")
        bookYear = request.form.get("bookYear")
        veriekle(bookTitle, bookAuthor, bookYear)

    return render_template("yemekekle.html")


@app.route("/yemeksil/<string:id>")
def yemeksil(id):
    print("yemeksil silinecek id", id)
    verisil(id)
    return redirect(url_for("yemek"))



@app.route("/yemekguncelle/<string:id>", methods=["GET", "POST"])
def yemekguncelle(id):
    if request.method == "GET":
        print("guncellenecek id", id)
        guncellenecekveri = []
        for d in data:
            if str(d[0]) == id:
                guncellenecekveri = list(d)

        return render_template("yemekguncelle.html", veri = guncellenecekveri)

    else:
        bookID = request.form.get("bookID")
        bookTitle = request.form.get("bookTitle")
        bookAuthor = request.form.get("bookAuthor")
        bookYear = request.form.get("bookYear")
        veriguncelle(bookID, bookTitle, bookAuthor, bookYear)
        return redirect(url_for("yemek"))
    



@app.route("/yemekdetayi/<string:id>")
def yemekdetayi(id):
    detayVeri=[]
    for d in data:
        if str(d[0]) == id:
             detayVeri = list(d)

    return render_template("yemekdetayi.html", veri = detayVeri)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/projeler")
def projeler():
    
    return render_template("projeler.html")

   

   



if __name__ == "__main__":
    app.run(debug = True)