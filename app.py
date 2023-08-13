from flask import Flask, redirect, render_template, flash, url_for
from flask import request, session
from flask_session import Session
import mysql.connector as mysql
from datetime import date

app = Flask(__name__)
app.secret_key = "super secret key"

def setCust_id_glb(id):
    global cust_id_glob
    cust_id_glob =id
@app.route('/')
def MyhomeRoot():
    return render_template('login.html')

@app.route("/Login_Process", methods=['POST'])
def Login_Process():
    uid = request.form["username"]
    pwd = request.form["password"]
    print(uid)
    print(pwd)
    #print("bad request error")
    try:
        db_connect = mysql.connect(
            host="localhost", database="onlinesportshop", user="root", passwd="KGFbangalore",auth_plugin='mysql_native_password', use_pure=True)
        sql = "Select userid, password,cust_id From loginTable where userid = " + "'" + uid + "'"
        mycursor = db_connect.cursor()
        mycursor.execute(sql)
        cno = mycursor.fetchall()
        res = [tuple(str(item) for item in t) for t in cno]
        print(res)
    except Exception as err:
        print(err)
        print('error1')
        return render_template('Error.html')
    if len(res) == 0:
        status = 0
        print('error2')
        return render_template('Error.html')
    else:
        usrid  = res[0][0]
        passwd = res[0][1]
        cust_id= res[0][2]
        id=cust_id
        setCust_id_glb(id)
        print(usrid)
        print(passwd)
        if (usrid==uid and passwd == pwd and uid=='admin'):
            return render_template('CartReport.html',usrid=usrid)

        elif (usrid == uid and pwd == passwd):
            print("loggedin as user")
            cartstmt="select productid,"
            return render_template('HomeVer2.html', usrid=usrid,cust_id=cust_id)
        else:
            print('error3')
            """status = 0"""
            return render_template('Error.html')

@app.route("/AddProduct", methods=['POST'])
def AddProduct():
    try:
        prod_id=request.form["prod_id"]
        pname=request.form["pname"]
        ptype=request.form["ptype"]
        pQuantity=request.form["Quantity"]
        pprice=request.form["price"]
        db_connect = mysql.connect(
            host="localhost", database="onlinesportshop", user="root", passwd="KGFbangalore",auth_plugin='mysql_native_password', use_pure=True)
        sql = "INSERT INTO product VALUES (" +  prod_id  + "," + "'" + pname +"'" + "," + "'"+ptype+"'" + "," +    pprice  + ","  +   pQuantity + ")" 
        print(pname)
        print(prod_id)
        print(ptype)
        print(pQuantity)
        print(pprice)
        print("INSERT INTO product VALUES (" +  prod_id  + "," + "'" + pname +"'" + "," + "'"+ptype+"'" + "," +    pprice  + "," + "," +   pQuantity + ")")
        mycursor = db_connect.cursor()
        mycursor.execute(sql)
        db_connect.commit()
        return render_template("addProduct.html")
    except Exception as err:
        print(err)
        return render_template('MyError.html')

@app.route("/deleteProduct", methods=['POST'])
def deleteProduct():
    try:
        prod_id=request.form["prod_id"]
        db_connect = mysql.connect(
            host="localhost", database="onlinesportshop", user="root", passwd="KGFbangalore",auth_plugin='mysql_native_password', use_pure=True)
        sql = "DELETE FROM product where productid =" +  prod_id +";" 
        print(sql)
        mycursor = db_connect.cursor()
        mycursor.execute(sql)
        print(sql)
        db_connect.commit()
        return render_template("deleteProduct.html")
    except Exception as err:
        print(err)
        return render_template('MyError.html')

@app.route("/UpdateQuantity", methods=['POST'])
def UpdateQuantity():
    try:
        prod_id=request.form["prod_id"]
        pQuantity=request.form["Quantity"]
        print(prod_id)
        print(pQuantity)
        
        db_connect = mysql.connect(
            host="localhost", database="onlinesportshop", user="root", passwd="KGFbangalore",auth_plugin='mysql_native_password', use_pure=True)
        #sql_std = "UPDATE product SET Marks = " + user_mks +" WHERE USN = " + "'" + prod_id + "'"
        sql_std="select quantity from product where productid = "+prod_id
        print(sql_std)
        mycursor = db_connect.cursor()
        mycursor.execute(sql_std)
        qData=mycursor.fetchall()
        print(qData[0][0])
        db_connect.commit()
        pQuantity=int(pQuantity)+int(qData[0][0])
        print(pQuantity)
        sql="update product Set quantity = "+ str(pQuantity) +" where productid = " + "'"+prod_id + "'"
        print(sql)
        mycursor=db_connect.cursor()
        mycursor.execute(sql)
        db_connect.commit()
        return render_template("UpdateProduct.html")

      
    except Exception as err:
        print(err)
        return render_template('MyError.html')


@app.route('/salesReport',methods=['POST'])
def salesReport():
    try:
        cartid=request.form["cartid"]
        db_connect = mysql.connect(
            host="localhost", database="onlinesportshop", user="root", passwd="KGFbangalore",auth_plugin='mysql_native_password', use_pure=True)
        mycursor=db_connect.cursor()   
        sql="select productid,product_name,quantity,cost,date from cart_items where cartid = "+"'"+str(cartid)+"'"
        mycursor.execute(sql)
        cartitems=mycursor.fetchall()
        return render_template("reportver2.html",cartitems=cartitems)

    except Exception as err:
        print(err)
        return render_template("Error.html")

@app.route('/AddTocart',methods=['POST'])
def AddTocart():
    try:
        addvalue=request.form["quantity"]
        Pid_1name=request.form["pid"]
        print(addvalue)
        print(Pid_1name)
        cur_date= date.today()
        db_connect = mysql.connect(
            host="localhost", database="onlinesportshop", user="root", passwd="KGFbangalore",auth_plugin='mysql_native_password', use_pure=True)
        mycursor=db_connect.cursor()     
        #=====================fetch product type ========================
        fetchTypeSql="select ptype from product where productid ="+"'"+Pid_1name+"'"
        mycursor.execute(fetchTypeSql)
        Prodtype=mycursor.fetchone()
        Prodtype=Prodtype[0]
        print(Prodtype)
        #====================fetch product name ========================
        fetchpnameSql="select pname from product where productid ="+"'"+Pid_1name+"'"
        mycursor.execute(fetchpnameSql)
        Prodname=mycursor.fetchone()
        print(Prodname)
        Prodname=Prodname[0]
        print(Prodname)
        #==================fetch user cart id ===========================
        sql="select cartid from cart where customerid = " +"'"+cust_id_glob+"'"
       
        mycursor.execute(sql)
        cartid=mycursor.fetchone()
        cartid=int(cartid[0])
        print(cartid)
        #===================fetch price================= 
        sqlPprice="select prodprice from product where productid= "+"'"+Pid_1name+"'"
        mycursor.execute(sqlPprice)
        ProdPrice=mycursor.fetchone()
        ProdPrice=int(ProdPrice[0])
        print(ProdPrice)
        #==================Quantity * price================
        cost = int(addvalue)*ProdPrice
        print(cost)
        #==================update product table=============
        sqlRetQuaty="select quantity from product where productid= "+"'"+Pid_1name+"'"
        mycursor.execute(sqlRetQuaty)
        productQuantity=mycursor.fetchone()
        productQuantity=int(productQuantity[0])
        newQuantity=productQuantity-int(addvalue)
        sqlSetnewqua="update product set quantity ="+"'"+str(newQuantity)+"' where productid="+"'"+Pid_1name+"'"
        print(sqlSetnewqua)
        mycursor.execute(sqlSetnewqua)
        db_connect.commit()
        #================== insert into cart_items===============
        sqlinsert="insert into cart_items (cartid,productid,product_name,quantity,cost,date)values("+"'"+str(cartid)+"',"+"'"+Pid_1name+"',"+"'"+str(Prodname)+"',"+"'"+addvalue+"',"+"'"+str(cost)+"',"+"'"+str(cur_date)+"')"
        print(sqlinsert)
        mycursor.execute(sqlinsert)
        db_connect.commit()
        cost =0
        #================== return the page =========================
        if(Prodtype=="Football"):
            return render_template('footballPagever2.html',Pid_name=Pid_name,cust_id=cust_id_glob) 
        if Prodtype=="cricket":
            return render_template('cricketPagever2.html',Pid_name=Pid_name,cust_id=cust_id_glob) 
        if Prodtype=="Badminton":
            return render_template('badmintonPagever2.html',Pid_name=Pid_name,cust_id=cust_id_glob)      
       
    except Exception as err:
        print(err)
        return render_template('Error.html')  

@app.route('/cart_rem',methods=['POST'])        
def cart_rem():
    try:
        cartitem_id=request.form["carti_id"]

        #check if u have more than product in order to remove
        print(cartitem_id)
        db_connect = mysql.connect(
            host="localhost", database="onlinesportshop", user="root", passwd="KGFbangalore",auth_plugin='mysql_native_password', use_pure=True)
        
        sql="select productid,quantity from cart_items where cart_item_id='"+cartitem_id+"'"
        mycursor=db_connect.cursor()
        mycursor.execute(sql)
        exe=mycursor.fetchone()
        print(exe)
        prodid=exe[0]
        quantity=exe[1]
       
        print(prodid)
        print(quantity)


        sqlp="select quantity from product where productid='"+str(prodid)+"'"
        mycursor.execute(sqlp)
        ProQuan=mycursor.fetchone()
        Pquantity=ProQuan[0]
        print(ProQuan)

        newPquan=Pquantity+quantity
        print(newPquan)

        sqlp="update product set quantity='"+str(newPquan)+"'where productid='"+str(prodid)+"'"
        mycursor.execute(sqlp)

        sqlDelItem_c="delete from cart_items where cart_item_id='"+cartitem_id+"'"
        mycursor.execute(sqlDelItem_c)

        fetchcartid="select cartid from cart where customerid = "+"'"+str(cust_id_glob)+"'"
        mycursor.execute(fetchcartid)
        cartid=mycursor.fetchone()
        cartid=cartid[0]
        print(cartid)
        #===================cart items==============================
        fetchCartsql="select productid,product_name,quantity,cost,cart_item_id from cart_items where cartid = "+"'"+str(cartid)+"'"
        mycursor.execute(fetchCartsql)
        cartitems=mycursor.fetchall()
        print(cartitems)
        #===================sum====================================
        sum="select cost from cart_items where cartid = "+"'"+str(cartid)+"'"
        mycursor.execute(sum)
        Sumtuple=mycursor.fetchall()
        print(Sumtuple)
        total=0
        for i in Sumtuple:
            total+=i[0]
        print(total) 
        db_connect.commit()

        return render_template("cartver2.html",cartitems=cartitems,total=total)

        
    except Exception as err:
        print(err)
        return render_template('Error.html') 


@app.route("/RenderLoginPage")
def RenderLoginPage():
    return render_template("login.html")

@app.route("/RenderAddproduct")
def RenderAddproduct():
    return render_template("addProduct.html")

@app.route("/MyError")
def MyError():
    return render_template("MyError.html")

@app.route("/RenderUpdateQuantity")
def RenderUpdateQuantity():
    return render_template("UpdateProduct.html")

@app.route("/RenderDelProduct")
def RenderDelProduct():
    return render_template("deleteProduct.html")

@app.route("/RenderfootBallPage")    
def RenderfootBallPage():
    try:
        db_connect = mysql.connect( host="localhost", database="onlinesportshop", user="root", passwd="KGFbangalore",auth_plugin='mysql_native_password', use_pure=True)
        sql="select productid,pname,prodprice from product where ptype = 'football'"
        mycursor=db_connect.cursor()
        mycursor.execute(sql)
        global Pid_name
        Pid_name=mycursor.fetchall()
        print(Pid_name)
        print(Pid_name[0][0])
        print(Pid_name[0][1])
        print(Pid_name[0][2])
        print('render football section')
        return render_template("footballPagever2.html",Pid_name=Pid_name,cust_id=cust_id_glob)
    except Exception as err:
        print(err)
        return render_template("Error.html") 


@app.route("/RendercricketPage")
def RendercricketPage():
    try:
        db_connect = mysql.connect( host="localhost", database="onlinesportshop", user="root", passwd="KGFbangalore",auth_plugin='mysql_native_password', use_pure=True)
        sql="select productid,pname,prodprice from product where ptype = 'cricket'"
        mycursor=db_connect.cursor()
        mycursor.execute(sql)
        global Pid_name
        Pid_name=mycursor.fetchall()
        print(Pid_name)
        print(Pid_name[0][0])
        print(Pid_name[0][1])
        print(Pid_name[0][2])
        print('render cricket section')
        return render_template("cricketPagever2.html",Pid_name=Pid_name,cust_id=cust_id_glob)
    except Exception as err:
        print(err)
        return render_template("Error.html") 


@app.route("/RenderbadmintonPage")    
def RenderbadmintonPage():
    try:
        db_connect = mysql.connect( host="localhost", database="onlinesportshop", user="root", passwd="KGFbangalore",auth_plugin='mysql_native_password', use_pure=True)
        sql="select productid,pname,prodprice from product where ptype = 'badminton'"
        mycursor=db_connect.cursor()
        mycursor.execute(sql)
        global Pid_name
        Pid_name=mycursor.fetchall()
        print(Pid_name)
        print(Pid_name[0][0])
        print(Pid_name[0][1])
        print(Pid_name[0][2])
        print('render badminton section')
        return render_template("badmintonPagever2.html",Pid_name=Pid_name,cust_id=cust_id_glob)
    except Exception as err:
        print(err)
        return render_template("Error.html") 

@app.route("/cartItems")
def cartItems():
    try:
        db_connect = mysql.connect( host="localhost", database="onlinesportshop", user="root", passwd="KGFbangalore",auth_plugin='mysql_native_password', use_pure=True)
        mycursor=db_connect.cursor()
        #======================CART Id=============================
        fetchcartid="select cartid from cart where customerid = "+"'"+str(cust_id_glob)+"'"
        mycursor.execute(fetchcartid)
        cartid=mycursor.fetchone()
        cartid=cartid[0]
        print(cartid)
        #===================cart items==============================
        fetchCartsql="select productid,product_name,quantity,cost,cart_item_id from cart_items where cartid = "+"'"+str(cartid)+"'"
        mycursor.execute(fetchCartsql)
        cartitems=mycursor.fetchall()
        print(cartitems)
        #====================SUM====================================
        sum="select cost from cart_items where cartid = "+"'"+str(cartid)+"'"
        mycursor.execute(sum)
        Sumtuple=mycursor.fetchall()
        print(Sumtuple)
        total=0
        for i in Sumtuple:
            total+=i[0]
        print(total)    



        return render_template("cartver2.html",cartitems=cartitems,total=total)
    except Exception as err:
        print(err)
        return render_template("Error.html")
@app.route('/R_cartItems')
def R_cartItems():
    return render_template("cartver2.html")
@app.route("/RenderHome")    
def RenderHome():
    return render_template("HomeVer2.html")
@app.route("/rendersales")
def rendersales():
    return render_template("reportver2.html")
@app.route("/renderAdminLogin")
def renderAdminLogin():
    return render_template("CartReport.html")
    
if __name__ == '__main__':
  app.run(port="8000")