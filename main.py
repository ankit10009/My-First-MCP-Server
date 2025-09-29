
import os,sqlite3
from fastmcp import FastMCP

DB_PATH =os.path.join(os.path.dirname(__file__),"expenses.db")

#Create a FastMCP Server instance
mcp = FastMCP(name = "ExpenseTracker")

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""
                    CREATE TABLE IF NOT EXISTS expenses(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    subcategory TEXT DEFAULT '',
                    note TEXT DEFAULT ''
                  )
                  """)
        
init_db()

@mcp.tool
def add_expense(date,amount,category,subcategory="",note=""):
    """Add a New expense Entry into the database."""
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
                    "INSERT INTO expenses(date,amount,category,subcategory,note) VALUES (?,?,?,?,?)",
                        (date,amount,category,subcategory,note)
                  )
        return {"status": "ok", "id": cur.lastrowid}
    
@mcp.tool
def list_expenses(start_date,end_date):
    """List Expense Entries within an inclusive date range."""
    with sqlite3.connect(DB_PATH) as c: 
        cur = c.execute("""SELECT id,date,amount,category,subcategory,note 
                        from expenses
                        where date between ? and ?
                        ORDER BY ID ASC""",(start_date,end_date))
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols,r)) for r in cur.fetchall()]
           
if __name__ == "__main__":
    mcp.run()    