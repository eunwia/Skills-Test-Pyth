from sqlite3 import connect,Row
database = 'db/registration.db'
def getprocess(sql,vals)->list:
    print(sql)
    conn=connect(database)
    conn.row_factory=Row
    cursor=conn.cursor()
    cursor.execute(sql,vals)
    data=cursor.fetchall()
    cursor.close()
    conn.close()
    return data
    
def postprocess(sql,vals)->bool:
    print(sql)
    try:
        conn=connect(database)
        cursor=conn.cursor()
        cursor.execute(sql,vals)
        conn.commit()
    except Exception as e:
        print(f"Error : {e}")
    finally:
        cursor.close()
        conn.close()
        return True if cursor.rowcount>0 else False
    
def getall(table)->list:
    sql = f"SELECT * FROM `{table}`"
    return getprocess(sql,[])
    
def getrecord(table,**kwargs)->list:
    keys = list(kwargs.keys())
    vals = list(kwargs.values())
    fields = []
    for key in keys:
        fields.append(f"`{key}`=?")
    flds = " AND ".join(fields)
    sql = f"SELECT * FROM `{table}` WHERE {flds}"
    return getprocess(sql,vals)
    
def addrecord(table,**kwargs)->bool:
    keys = list(kwargs.keys())
    vals = list(kwargs.values())
    fields = "`,`".join(keys)
    qmark=['?']*len(vals)
    dta = ",".join(qmark)
    sql = f"INSERT INTO `{table}`(`{fields}`) VALUES({dta})"
    return postprocess(sql,vals)
    
def deleterecord(table,**kwargs)->bool:
    keys = list(kwargs.keys())
    vals = list(kwargs.values())
    fields = []
    for key in keys:
        fields.append(f"`{key}`=?")
    flds = " AND ".join(fields)
    sql = f"DELETE FROM `{table}` WHERE {flds}"
    return postprocess(sql,vals)
    
def updaterecord(table,**kwargs)->bool:
    keys = list(kwargs.keys())
    vals = list(kwargs.values())
    newvals = []
    fields = []
    for index in range(1,len(keys)):
        fields.append(f"`{keys[index]}`=?")
        newvals.append(f"{vals[index]}")
    flds = ",".join(fields)
    sql = f"UPDATE `{table}` SET {flds} WHERE `{keys[0]}`='{vals[0]}'"
    return postprocess(sql,newvals)
