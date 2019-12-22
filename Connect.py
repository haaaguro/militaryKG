
from CrawlerS import settings
import pymysql
from pymysql import connections
class Connect:
    def __init__(self):
        self.conn = pymysql.connect(
            host=settings.HOST_IP,
            user=settings.USER,
            passwd=settings.PASSWD,
            db=settings.DB_NAME,
            charset='utf8mb4',
            use_unicode=True
            )
        self.cursor = self.conn.cursor()
    def saveInIorg(self,item):
        item_name = item.item_name
        org_name = item.org_name
        self.cursor.execute("SELECT MAX(use_id) from item.use;")
        result = self.cursor.fetchall()[0]
        if None in result:
                use_id = 1
        else:
                use_id = result[0] + 1
        sql = "INSERT INTO item.use(use_id, org_name,item_name) VALUES (%s, %s, %s)"
        self.cursor.execute(sql,(use_id,org_name,item_name))
        self.conn.commit()
    def saveInIwar(self,item):
        item_name = item.item_name
        war_name = item.war_name
        self.cursor.execute("SELECT MAX(id) from item.warI;")
        result = self.cursor.fetchall()[0]
        if None in result:
                use_id = 1
        else:
                use_id = result[0] + 1
        sql = """INSERT INTO item.warI(id,item_name,war_name) VALUES (%s, %s, %s)"""
        self.cursor.execute(sql,(use_id,item_name,war_name))
        self.conn.commit()
        self.cursor.execute("SELECT war_name FROM item.war;")
        bankList = self.cursor.fetchall()
        if(war_name not in bankList):
            self.cursor.execute("SELECT MAX(war_id) from item.war;")
            result = self.cursor.fetchall()[0]
            if None in result:
                    use_id = 1
            else:
                    use_id = result[0] + 1
        sql = """INSERT INTO item.war(war_id,war_name) VALUES (%s, %s)"""
        self.cursor.execute(sql,(use_id,war_name))
        self.conn.commit()
    def fullDb(self):
        self.cursor.execute("SELECT name FROM item.new_table;")
        itemList = self.cursor.fetchall()
        return itemList
    def getCountry(self):
        self.cursor.execute("SELECT country_name FROM item.country where ISOCODE is not null;")
        itemList = self.cursor.fetchall()
        return itemList
    def saveInOrg(self,item):
        org_name = item.org_name
        self.cursor.execute("SELECT organization_name FROM item.organization;")
        bankList = self.cursor.fetchall()
        if(org_name not in bankList):
            self.cursor.execute("SELECT MAX(organization_id) from item.organization;")
            result = self.cursor.fetchall()[0]
            if None in result:
                    org_id = 1
            else:
                    org_id = result[0] + 1
        sql = """INSERT INTO item.organization(organization_id,organization_name) VALUES (%s, %s)"""
        self.cursor.execute(sql,(org_id,org_name))
        self.conn.commit()
    def insertWarC(self,warname,countryL):
        war_name = warname
        print(war_name)
        if len(countryL)>0:
            for i in range(0,len(countryL)):
                country=countryL[i]
                self.cursor.execute("SELECT MAX(id) from item.warC;")
                result = self.cursor.fetchall()[0]
                if None in result:
                        use_id = 1
                else:
                        use_id = result[0] + 1
                sql = """INSERT INTO item.warC(id,country_name,war_name) VALUES (%s, %s, %s)"""
                self.cursor.execute(sql,(use_id,country,warname))
                self.conn.commit()
        self.cursor.execute("SELECT war_name FROM item.war;")
        bankList = self.cursor.fetchall()
        if(war_name not in bankList):
            self.cursor.execute("SELECT MAX(war_id) from item.war;")
            result = self.cursor.fetchall()[0]
            if None in result:
                    war_id = 1
            else:
                    war_id = result[0] + 1
        sql = """INSERT INTO item.war(war_id,war_name) VALUES (%s, %s)"""
        self.cursor.execute(sql,(war_id,war_name))
        self.conn.commit()
    def insertCountry(self,country_name,ISO_code):
        print(country_name)
        self.cursor.execute("SELECT MAX(country_id) from item.country;")
        result = self.cursor.fetchall()[0]
        if None in result:
                use_id = 1
        else:
                use_id = result[0] + 1
        sql = """INSERT INTO item.country(country_id,country_name,ISOCODE) VALUES (%s, %s, %s)"""
        self.cursor.execute(sql,(use_id,country_name,ISO_code))
        self.conn.commit()
    def updateItem(self,item):
        desinger = item.desinger
        name = item.item_name
        sql = """UPDATE item.new_table SET desinger = %s WHERE name = %s"""
        self.cursor.execute(sql,(desinger,name))
        self.conn.commit()
    def updateCountry(self,name,searchItem):
        sql = """UPDATE item.country SET country_boss = %s WHERE country_name = %s"""
        self.cursor.execute(sql,(name,searchItem))
        self.conn.commit()
    def query(self,label,war,country,item,sql,people):
        if label == 'cw':
            war='%'+war+'%'
            self.cursor.execute(sql,(country,war))
            result = self.cursor.fetchall()
            if len(result)>0:
                return'当然咯'
            else:
                return'没有'
        if label == 'ci':
            self.cursor.execute(sql,(country,item))
            result = self.cursor.fetchall()
            if len(result)>0:
                return'没毛病'
            else:
                return'不是的呢亲'
        if label == 'cni':
            self.cursor.execute(sql,(country))
            result = self.cursor.fetchall()
            if len(result)>0:
               return result
            else:
                return'这个国家很蠢，什么都没做出来'
        if label=='cnw':
            self.cursor.execute(sql,(country))
            result = self.cursor.fetchall()
            if len(result)>0:
               return result
            else:
                return'这个国家都是和平主义者'
        if label=='cnp':
            country ='%'+country+'%'
            self.cursor.execute(sql,(country))
            result = self.cursor.fetchall()[0]
        if label =='inc':
            item = '%'+item+'%'
            self.cursor.execute(sql,(item))
            result = self.cursor.fetchall()[0]
            return result
        if label=='inw':
            self.cursor.execute(sql,(item))
            result = self.cursor.fetchall()
            if len(result)>0:
                return result
        if label=='wnc':
            war='%'+war+'%'
            self.cursor.execute(sql,(war))
            result = self.cursor.fetchall()
            if len(result)>0:
               return result
        if label == 'people':
            people = '%'+people+'%'
            self.cursor.execute(sql,(people))
            result = self.cursor.fetchall()[0]
            return result[0]
    def close(self):
        self.conn.close();