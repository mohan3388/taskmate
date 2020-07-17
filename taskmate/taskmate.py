from tkinter import *
from tkinter import messagebox, Menu
import requests
import json
import sqlite3

pycrypto = Tk()
pycrypto.title("my crypto portfolio")
pycrypto.iconbitmap('favicon.ico')

con = sqlite3.connect('coindb')
cursorObj = con.cursor()
cursorObj.execute("CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY, symbol TEXT, amount INTEGER, price REAL)")
con.commit()

def reset():
  for cell in pycrypto.winfo_children():

    cell.destroy()
  app_nav()
  app_header()
  my_portfolio()

def app_nav():
  def clear_all():
    cursorObj.execute("DELETE FROM coin")
    con.commit()

    messagebox.showinfo("porfolio notification","portfolio cleared - add a new coins")
    reset()
  def close_app():
    pycrypto.destroy()

  menu = Menu(pycrypto)
  file_item = Menu(menu)
  file_item.add_command(label='clear portfolio', command=clear_all)
  file_item.add_command(label='close app', command=close_app)
  menu.add_cascade(label="File", menu=file_item)
  pycrypto.config(menu=menu)

def my_portfolio():
  api_request = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=e1340000-3282-4abe-8f83-58eedbec11a2")
  api = json.loads(api_request.content)

  cursorObj.execute("SELECT * FROM coin")
  coins = cursorObj.fetchall()

  def font_color(amount):

      if amount>= 0:
          return "green"
      else:
          return "red"

  def insert_coin():
    cursorObj.execute("INSERT INTO coin(symbol, price, amount) VALUES(?, ?, ?)", (symbol_txt.get(), price_txt.get(), amount_txt.get()))
    con.commit()
    messagebox.showinfo("portfolio notification","coin added successfully")
    reset()
    
     
  def update_coin():
    cursorObj.execute("UPDATE coin SET=?, price=?, amount=? WHERE id=?", (symbol_update.get(), price_update.get(), amount_update.get(), portid_update.get()))
    con.commit()
    messagebox.showinfo("portfolio notification","coin updated successfully") 
    reset() 

  def delete_coin():
    cursorObj.execute("DELETE FROM coin WHERE id=?", (portid_delete.get(),))
    con.commit() 
    messagebox.showinfo("portfolio notification","coin deleted successfully")
    reset()    
  #  coins = [
  #    {
  #       "symbol":"BTC",
  #       "amount_owned":2,
  #       "price_per_coin":3500
  #     },
  #     { 
  #      "symbol":"EOS",
  #      "amount_owned":100,
  #      "price_per_coin":2.75

  #    },
  #    {
  #      "symbol":"LTC",
  #      "amount_owned":10,
  #      "price_per_coin":40

  #    },
  #    {
  #      "symbol":"XMR",
  #      "amount_owned":10,
  #      "price_per_coin":48.5

  #    }
  #   ]

  total_pl = 0 
  coin_row = 1
  total_current_value = 0
  total_amount_paid = 0


  for i in range(0, 300):
    for coin in coins:

      if api["data"][i]["symbol"] == coin[1]:

        total_paid = coin[2]*coin[3]
        current_value = coin[2]*api["data"][i]["quote"]["USD"]["price"]
      
        pl_percoin = api["data"][i]["quote"]["USD"]["price"]-coin[3]

        total_pl_coin = pl_percoin * coin[2]

        total_pl += total_pl_coin

        total_current_value += current_value

        total_amount_paid += total_paid

            # total_pl = total_pl + total_pl_coin
            # print(api["data"][i]["name"]+ "-" +api["data"][i]["symbol"])
            # print("price-${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]))
            # print("number of coin:", coin[1])
            # print("total amount paid:","${0:.2f}".format(total_paid))
            # print("current_value:","${0:.2f}".format(current_value))
            # print("P/L per coin:","${0:.2f}".format(pl_percoin))
            # print("total pl per coin:","${0:.2f}".format(total_pl_coin))
            # print("----------")
        portfolio_id= Label(pycrypto, text=coin[0], bg="#F3F4F6", fg="black", font="lato 12",padx="5", pady="5", borderwidth=2, relief="groove")
        portfolio_id.grid(row=coin_row, column=0, sticky=N+S+E+W)

        name= Label(pycrypto, text=api["data"][i]["symbol"], bg="#F3F4F6", fg="black", font="lato",padx="5", pady="5", borderwidth=2, relief="groove")
        name.grid(row=coin_row, column=1, sticky=N+S+E+W)

        price= Label(pycrypto, text="${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]), bg="#F3F4F6", fg="black",font="lato 12",padx="5", pady="5", borderwidth=2, relief="groove")
        price.grid(row=coin_row, column=2, sticky=N+S+E+W)

        no_coins= Label(pycrypto, text=coin[0], bg="#F3F4F6", fg="black",font="lato 12",padx="5", pady="5", borderwidth=2, relief="groove")
        no_coins.grid(row=coin_row, column=3, sticky=N+S+E+W)

        amount_paid= Label(pycrypto, text="${0:.2f}".format(total_paid), bg="#F3F4F6", fg="black",font="lato 12",padx="5", pady="5", borderwidth=2, relief="groove")
        amount_paid.grid(row=coin_row, column=4, sticky=N+S+E+W)

        current_value= Label(pycrypto, text="${0:.2f}".format(current_value), bg="#F3F4F6", fg=font_color(float("{0:.2f}".format(current_value))),font="lato 12",padx="5", pady="5", borderwidth=2, relief="groove")
        current_value.grid(row=coin_row, column=5, sticky=N+S+E+W)

        pl_coin= Label(pycrypto, text="${0:.2f}".format(pl_percoin), bg="#F3F4F6", fg=font_color(float("{0:.2f}".format(pl_percoin))),font="lato 12",padx="5", pady="5", borderwidth=2, relief="groove")
        pl_coin.grid(row=coin_row, column=6, sticky=N+S+E+W)

        totalpl= Label(pycrypto, text="${0:.2f}".format(total_pl_coin), bg="#F3F4F6", fg=font_color(float("{0:.2f}".format(total_pl_coin))),font="lato 12",padx="5", pady="5", borderwidth=2, relief="groove")
        totalpl.grid(row=coin_row, column=7, sticky=N+S+E+W)

        coin_row += 1

        #insert coin
  symbol_txt = Entry(pycrypto, borderwidth=2, relief="groove")
  symbol_txt.grid(row=coin_row+1, column=1)

  price_txt = Entry(pycrypto, borderwidth=2, relief="groove")
  price_txt.grid(row=coin_row+1, column=2)

  amount_txt = Entry(pycrypto, borderwidth=2, relief="groove")
  amount_txt.grid(row=coin_row+1, column=3)

  add_coin = Button(pycrypto, text="Add Coin", bg="#142E54", fg="white", command=insert_coin ,font="Lato 12", borderwidth=2, relief="groove", padx="2", pady="2")
  add_coin.grid(row=coin_row + 1, column=4, sticky=N+S+E+W)

        #delete coin

  portid_update = Entry(pycrypto, borderwidth=2, relief="groove")
  portid_update.grid(row=coin_row+2, column=0)

  symbol_update = Entry(pycrypto, borderwidth=2, relief="groove")
  symbol_update.grid(row=coin_row+2, column=1)

  price_update = Entry(pycrypto, borderwidth=2, relief="groove")
  price_update.grid(row=coin_row+2, column=2)

  amount_update = Entry(pycrypto, borderwidth=2, relief="groove")
  amount_update.grid(row=coin_row+2, column=3)

  update_coin_txt = Button(pycrypto, text="update coin", bg="blue", fg="white", command=update_coin, font="lato 12",padx="5", pady="5", borderwidth=2, relief="groove")
  update_coin_txt.grid(row=coin_row+2, column=4, sticky=N+S+E+W)

     #delete coin
  
  portid_delete = Entry(pycrypto, borderwidth=2, relief="groove")
  portid_delete.grid(row=coin_row+3, column=0)
  
  delete_coin_txt = Button(pycrypto, text="delete coin", bg="blue", fg="white", command=delete_coin, font="lato 12",padx="5", pady="5", borderwidth=2, relief="groove")
  delete_coin_txt.grid(row=coin_row+3, column=1, sticky=N+S+E+W)


  totalap = Label(pycrypto, text="${0:.2f}".format(total_amount_paid), bg="green", fg="white", font="lato 12 bold",padx="5", pady="5", borderwidth=2, relief="groove")
  totalap.grid(row=coin_row, column=4, sticky=N+S+E+W)

  totalcv = Label(pycrypto, text="${0:.2f}".format(total_current_value), bg="green", fg="white", font="lato 12 bold",padx="5", pady="5", borderwidth=2, relief="groove")
  totalcv.grid(row=coin_row, column=5, sticky=N+S+E+W)


  totalpl = Label(pycrypto, text="${0:.2f}".format(total_pl), bg="green", fg="white", font="lato 12 bold",padx="5", pady="5", borderwidth=2, relief="groove")
  totalpl.grid(row=coin_row, column=7, sticky=N+S+E+W)

  api = ""

  refresh = Button(pycrypto, text="refresh", bg="blue", fg="white", command=reset, font="lato 12 bold",padx="5", pady="5", borderwidth=2, relief="groove")
  refresh.grid(row=coin_row + 1, column=7, sticky=N+S+E+W)

  
        

def app_header():

  portfolio_id= Label(pycrypto, text="portfolio", bg="#142E54", fg="white", font="lato 12 bold",padx="5", pady="5", borderwidth=2, relief="groove")
  portfolio_id.grid(row=0, column=0, sticky=N+S+E+W)

  name= Label(pycrypto, text="coin name", bg="#142E54", fg="white", font="lato 12 bold",padx="5", pady="5", borderwidth=2, relief="groove")
  name.grid(row=0, column=1, sticky=N+S+E+W)

  price= Label(pycrypto, text="price", bg="#142E54", fg="white", font="lato 12 bold",padx="5", pady="5", borderwidth=2, relief="groove")
  price.grid(row=0, column=2, sticky=N+S+E+W)

  no_coins= Label(pycrypto, text="coin owned", bg="#142E54", fg="white", font="lato 12 bold",padx="5", pady="5", borderwidth=2, relief="groove")
  no_coins.grid(row=0, column=3, sticky=N+S+E+W)

  amount_paid= Label(pycrypto, text="total amount paid", bg="#142E54", fg="white",font="lato 12 bold",padx="5", pady="5", borderwidth=2, relief="groove")
  amount_paid.grid(row=0, column=4, sticky=N+S+E+W)

  current_value= Label(pycrypto, text="current value", bg="#142E54", fg="white", font="lato 12 bold",padx="5", pady="5", borderwidth=2, relief="groove")
  current_value.grid(row=0, column=5, sticky=N+S+E+W)

  pl_coin= Label(pycrypto, text="P/L per coin", bg="#142E54", fg="white", font="lato 12 bold",padx="5", pady="5", borderwidth=2, relief="groove")
  pl_coin.grid(row=0, column=6, sticky=N+S+E+W)

  totalpl= Label(pycrypto, text="total P/L with coin", bg="#142E54", fg="white", font="lato 12 bold",padx="5", pady="5", borderwidth=2, relief="groove")
  totalpl.grid(row=0, column=7, sticky=N+S+E+W)

app_nav()
app_header()
my_portfolio()
pycrypto.mainloop()

cursorObj.close()
con.close()