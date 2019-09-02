import mysql.connector

class Database:
    def __init__(self,database):
        self.__database = database
        try:
            self.__mydb = mysql.connector.connect(
                host='localhost',
                user='root',
                passwd='Ab123456',
                database=self.__database
            )
            self.__mycursor = self.__mydb.cursor()
            print("Conectado com sucesso.")
        except:
            self.__mydb = mysql.connector.connect(
                host='localhost',
                user='root',
                passwd='Ab123456',
            )
            self.__mycursor = self.__mydb.cursor()
            self.__mycursor.execute('CREATE DATABASE {}'.format(self.__database))
            print("Database foi criado.")
            self.__init__(self.__database)

    def CreateTable(self,table,args):
        self.__mycursor.execute('SHOW TABLES')
        tablesList = []
        for element in self.__mycursor.fetchall():
            tablesList.append(element[0])
        if(table not in tablesList):
            tableColumns = '(id int NOT NULL AUTO_INCREMENT,'
            for element in args:
                tableColumns += element[0]
                if(element[1] == 'var'):
                    tableColumns += ' VARCHAR(255),'
                else:
                    tableColumns += ' INT(10),'
            tableColumns = tableColumns+'PRIMARY KEY (id))'
            sql = "CREATE TABLE {}{}".format(table,tableColumns)
            self.__mycursor.execute(sql)
            print('Tabela {} criada com sucesso.'.format(table))
        else:
            print('Essa tabela já existe.')


    def ShowData(self,table,column=None,search=''):
        if(column==None):
            sql = "SELECT * FROM {}".format(table)
        else:
            sql = "SELECT * FROM {} WHERE {} LIKE '%{}%'".format(table,column,search)
        self.__mycursor.execute(sql)
        myresult = self.__mycursor.fetchall()
        print(myresult)


    def InsertData(self,table,args):
        columns = self.__GetColumns(table)
        columnsStr = '('
        for element in columns[1:]:
            columnsStr +=element+','
        columnsStr = columnsStr[:-1]+')'
        args = tuple(args)

        if(len(columns) == len(args)+1):
            sql = 'INSERT INTO {} {} VALUES {}'.format(table,columnsStr,args)
            self.__mycursor.execute(sql)
            self.__mydb.commit()
        else:
            print("Numero de dados não confere com o numero de colunas.")


    def UpdateData(self,table,id,column,arg):
        columns = self.__GetColumns(table)
        if(column in columns):
            sql = "UPDATE {} SET {}='{}' WHERE id={}".format(table,column,arg,id)
            self.__mycursor.execute(sql)
            self.__mydb.commit()
        else:
            print('Coluna indicada não existe.')


    def RemoveData(self,table,column,arg):
        columns = self.__GetColumns(table)
        if(column in columns):
            sql = "DELETE FROM {} WHERE {} = '{}'".format(table,column,arg)
            self.__mycursor.execute(sql)
            self.__mydb.commit()
        else:
            print('A coluna especifica não existe.')


    def __GetColumns(self,table):
        sql = 'SHOW COLUMNS FROM {}'.format(table)
        self.__mycursor.execute(sql)
        myresult = self.__mycursor.fetchall()
        columns = []
        for element in myresult:
            columns.append(element[0])
        return columns


cols = (('Name','var'),('Age','int'),('BloodType','var'))

data = Database('bloodbank')
data.CreateTable('donors',cols)
data.InsertData('donors',('Juliana',38,'O+'))
data.UpdateData('donors',1,'Name','Jorge')
data.UpdateData('donors',1,'BloodType','O-')
data.InsertData('donors',('Lucas',26,'O-'))
data.InsertData('donors',('Julia',22,'B+'))
data.InsertData('donors',('Alessandro',21,'O-'))
data.InsertData('donors',('Luisa',25,'A+'))
data.InsertData('donors',('Larissa',18,'O-'))
data.ShowData('donors')
data.RemoveData('donors','Name','Lucas')
data.ShowData('donors','BloodType','O-')





