from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import hashlib
import sys

application = Flask(__name__)
application.config["SECRET_KEY"] = "helloosp"

DB = DBhandler()

@application.route("/")
def hello():
    return render_template("7_1_log_in.html")
    #return redirect(url_for('view_list'))

@application.route("/list")
def view_list():
    page = request.args.get("page", 0, type=int)
    per_page=6
    per_row=3
    row_count=int(per_page/per_row)
    start_idx=per_page*page
    end_idx=per_page*(page+1)
    
    data = DB.get_items()
    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)
    
    for i in range(row_count):
        if (i == row_count-1) and (tot_count%per_row != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])
            
    
    return render_template(
        "list.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        limit=per_page,
        page=page,
        page_count=int((item_counts/per_page)+1),
        total=item_counts
    )

@application.route("/home")
def home():
    return render_template("2_home.html")

@application.route("/review")
def view_review():
    return render_template("review.html")

@application.route("/product_upload")
def product_upload():
    return render_template("1_product_upload.html")

@application.route("/product_detail")
def product_detail():
    return render_template("3_product_detail.html")

@application.route("/review_upload")
def review_upload():
    return render_template("4_review_upload.html")

@application.route("/review_all")
def review_all():
    return render_template("5_review_all.html")

@application.route("/review_detail")
def review_detail():
    return render_template("6_review_detail.html")

@application.route("/log_in")
def log_in():
    return render_template("7_1_log_in.html")

@application.route("/id_find")
def id_find():
    return render_template("7_2_id_find.html")

@application.route("/id_found")
def id_found():
    return render_template("7_3_id_found.html")

@application.route("/pw_find")
def pw_find():
    return render_template("7_4_pw_find.html")

@application.route("/pw_reset")
def pw_reset():
    return render_template("7_5_pw_reset.html")

@application.route("/sign_up")
def sign_up():
    return render_template("8_sign_up.html")

@application.route("/wishlist")
def wishlist():
    return render_template("9_1_wishlist.html")

@application.route("/shopping_cart")
def shopping_cart():
    return render_template("9_2_shopping_cart.html")

@application.route("/mypage")
def mypage():
    return render_template("9_3_mypage.html")

@application.route("/reg_reviews")
def reg_review():
    return render_template("reg_reviews.html")

@application.route("/seller_info")
def seller_info():
    return render_template("11_seller_information.html")

@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    image_file = request.files["file"]
    image_file.save("static/images/{}".format(image_file.filename))
    data = request.form
    DB.insert_item(data['name'], data, image_file.filename)

    return render_template("submit_item_result.html", data=data, img_path=
                           "static/images/{}".format(image_file.filename))

@application.route("/submit_item")
def reg_item_submit():
    name = request.args.get("name")
    seller = request.args.get("seller")
    addr = request.args.get("addr")
    email = request.args.get("email")
    category = request.args.get("category")
    card = request.args.get("card")
    status = request.args.get("status")
    phone = request.args.get("phone")

@application.route("/login")
def login():
    return render_template("login.html")

@application.route("/login_confirm", methods=['POST'])
def login_user():
    id_=request.form['id']
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.find_user(id_, pw_hash):
        session['id']=id_
        return redirect(url_for('hello'))
    else:
        flash("Wrong ID or PW!")
        return render_template("login.html")

@application.route("/signup")
def signup():
    return render_template("signup.html")

@application.route("/signup_post", methods=['POST'])
def register_user():
    data = request.form
    pw = request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.insert_user(data, pw_hash):
        return render_template("login.html")
    else:
        flash("user id already exist!")
        return render_template("signup.html")

    #print(name,addr,phone,category,status)
    #return render_template("reg_item.html")
    
@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('hello'))

@application.route("/view_detail/<name>/")
def view_item_detail(name):
    print("###name:",name)
    data = DB.get_item_byname(str(name))
    print("####data:",data)
    return render_template("detail.html", name=name, data=data)

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)