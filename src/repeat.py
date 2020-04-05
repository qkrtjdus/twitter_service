now = datetime.datetime.now()
temp_date=now.strftime('%Y-%m-%d')


res = urllib.request.urlopen("http://ncov.mohw.go.kr/index_main.jsp")
res_source = res.read()

soup = BeautifulSoup(res_source,"html.parser")
datas=soup.find_all("span","num")[1]
datas_1=soup.find_all("span","num_rnum")[1]

temp_count=str(datas_1).split()[1].split('>')[1].split('<')[0]

temp_check=str(datas).split()[1].split('>')[1].split('<')[0]

cur.execute("INSERT INTO board Values('{}','{}','{}')".format(temp_date,temp_count,temp_check))
con.commit()

twitter_text_1 = """
---- 오늘의 코로나19 소식 ----

확진자 수:{}명(전날 대비 {}명 증가)
완치자 수:{}명(전날 대비 {}명 증가)



"""
twitter_text_2="""
--- 오늘의 코로나19 관련 인기 이슈입니다 ---


"""
now = datetime.datetime.now()
today=now.strftime('%Y-%m-%d')
cur.execute(("SELECT * FROM board WHERE Date='{}';").format(today))
a=0


for row in cur:
    a+=1

count=int(row[1].split(',')[0]+row[1].split(',')[1])
check=int(row[2].split(',')[0]+row[2].split(',')[1])


date=(int(today.split('-')[2])-1)
if date<10:
    date='0'+str(date)
yesterday=str(today.split('-')[0])+'-'+str(today.split('-')[1])+'-'+str(date)


cur.execute(("SELECT * FROM board WHERE Date='{}';").format(yesterday))

for row in cur:
    a+=1

yesterday_count=int(row[1].split(',')[0]+row[1].split(',')[1])
yesterday_check=int(row[2].split(',')[0]+row[2].split(',')[1])

count_gap=count-yesterday_count
check_gap=check-yesterday_check

datas = api.GetSearch("코로나",count=5,since=yesterday,result_type="popular")

status=api.PostUpdate(twitter_text_1.format(count,count_gap,check,check_gap))
api.PostUpdate(twitter_text_2,in_reply_to_status_id=status.id)
for data in datas:
    api.PostUpdate(data.text,in_reply_to_status_id=status.id)
