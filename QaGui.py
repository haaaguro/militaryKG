from CrawlerS import Connect
import tkinter as tk
import jieba
import jieba.posseg as pseg
import networkx as nx
import matplotlib.pyplot as plt
def rules(seg_list):
    sql=''
    structure=''
    war = ''
    country = ''
    item = ''
    people=''
    for x in seg_list:
        if x.flag == 'wn':
            structure=structure+' '+x.flag
            war = x.word
        if x.flag == 'in':
            structure=structure+' '+x.flag
            item = x.word
        if x.flag == 'cn':
            structure=structure+' '+x.flag
            country = x.word
        if x.flag == 'n':
            question = x.word
        if x.flag == 'nr' or x.flag =='nrfg' or x.flag =='nrt':
            people =x.word
            structure=structure+' '+x.flag
    if structure == ' cn wn' or structure == ' wn cn':
        label = 'cw'
        sql = "select * from item.warc where country_name= %s and war_name like %s"
    if structure == ' in cn' or structure == ' cn in':
        label = 'ci'
        sql = "select * from item.new_table where country= %s and name = %s"
    if structure == ' cn':
        if question == '武器':
            label = 'cni'
            sql = "select name from item.new_table where country= %s limit 50 "
        if question == '战争':
            label='cnw'
            sql = "select war_name from item.warc where country_name= %s "
        if question =='领袖':
            label = 'cnp'
            sql = "select country_boss from item.country where country_name like %s"
    if structure == ' in':
        if question == '国家':
            label = 'inc'
            sql = "select country from item.new_table where name like %s "
        if question == '战争':
            label='inw'
            sql = "select war_name from item.wari where item_name= %s "
    if structure == ' wn':
        if question == '国家':
            label='wnc'
            sql = "select country_name from item.warc where war_name like %s "
    if structure ==' nr' or structure ==' nrfg' or structure ==' nrt':
        label = 'people'
        sql = "select country_name from item.country where country_boss like %s"
    return label,war,country,item,sql,people
dict_paths=['warName.txt','itemName.txt','countryName.txt']
for p in dict_paths:
        jieba.load_userdict(p)
window = tk.Tk()
window.title('问答窗口')
window.geometry('600x300')
enter=tk.Entry(window,show=None, font=('Arial', 14))
enter.pack()
def query2():
    question = enter.get()
    seg_list =  pseg.cut(question.strip())
    labels,war,country,item,sql,people = rules(seg_list)
    c=Connect.Connect()
    result=c.query(labels,war,country,item,sql,people)
    g = nx.DiGraph()
    g.add_node(war)
    g.add_node(country)
    g.add_node(item)
    g.add_node(people)
    edge_labels={}
    if isinstance(result, str):
        tc3=tk.messagebox.showinfo(title='！',message=result)  # return no
        print (tc3)
    elif len(result)>0:
            for i in range(0,len(result)):
                g.add_node(result[i][0])
                if len(labels)>2:
                    if labels == 'cni' :
                        g.add_edge(country,result[i][0])
                    if labels =='cnw':
                        g.add_edge(country,result[i][0])
                    if labels =='cnp':
                        g.add_edge(country,result[i][0])
                    if labels == 'inw' :
                        g.add_edge(item,result[i][0])
                    if labels == 'wnc':
                        g.add_edge(result[i][0],war)
            pos=nx.kamada_kawai_layout(g)
            nx.draw(g,pos,with_labels=True,node_size=600,font_size=10)
            plt.show()

    c.close()
   
b = tk.Button(window, text='查询', font=('Arial', 12), width=10, height=1, command=query2)
b.pack()
window.mainloop()