import regex as re
'''
将正文直接复制粘贴到txt，分成两部分，一部分只有正文，另一部分只有参考文献
年份前只能有一个单词或者中文，如出现诸如(John,M,2020)的错误格式则会无视，但会被警告
搜索到的正文引用再变量citations中，其中citations1和2分别为两种类型的引用
'''
def alpha_exist(text):#text内有[\p{L}]集合中的元素,理论也可以直接用re.findall('\p{L}')
    for s in text:
        if s.isalpha():
            return True
    return False

with open("正文.txt",'r',encoding='utf-8') as f:
    zhengwen=f.read()
with open("参考文献.txt",'r',encoding='utf-8') as f:
    ckparas=f.readlines()
    cankao_num=0
    cankao=[]
    cankao_author_year=[]
    for para in ckparas:
        if para=='':
            continue
        cankao_num+=1
        cankao.append(para)
        name=re.findall(r'^[\p{L}\p{M}]+',para)[0]
        year=re.findall(r'(?<=\D)(?:18|19|20)\d{2}[ab]?(?=\D|$)',para)[0]
        cankao_author_year.append([name,year])

#%% 调参cite_pattern
# cite_pattern=r'(?<=\D)(?:19|20)\d{2}[ab]?(?=\D)'#纯年份
#有括号为首要前提
front='(?<=[(（]) ?'
end=' ?(?=[)）])'
#cite_pattern1匹配"(作者,年份;作者,年份)"

author_year='(?:[一-龥]{1,6}? ?|[A-Za-z\p{M} -]{1,25} ?)(?: et al\.|等)?[,，] ?(?:(?:18|19|20)\d{2}[ab]?[,，;；] ?)*?(?:18|19|20)\d{2}[ab]?'
repeat_pattern='(?:'+author_year+'[;；])*? ?'

cite_pattern1=front+repeat_pattern+author_year+end

#cite_pattern2匹配"作者(年份)"
front2='(?<=\n|^|[.。)）;；，,])[\p{L}\p{M} ]+?(?:al\.)? ?[(（] ?'
year='(?:(?:19|20)\d{2}[ab]?[，,；;] ?)*?(?:18|19|20)\d{2}[ab]?'
cite_pattern2=front2+year+end


#其中[一-龥]+|[A-Za-z]+)表示名字，[^\d]+表示名字和年份中间的若干个非数字字符

#%% 检查cite_pattern1
cite_pat1c='(?<=[(（])[^(（））\n]+?\D(?:18|19|20)\d{2}[ab]? ?(?=[)）])'
citations1=re.findall(cite_pattern1,zhengwen)
cite1_greed=re.findall(cite_pat1c,zhengwen)
if not cite1_greed==citations1:
    print('保险起见，请检查如下文本：')
    assert len(cite1_greed)>len(citations1),'离谱呀，宽松条件下正则表达式的匹配结果比严格条件下的结果还少？'
    diffs=set(cite1_greed)-set(citations1)
    for diff in diffs:
        print(diff)

citations2=re.findall(cite_pattern2,zhengwen)
    
for citation in citations1:
    if ';' in citation:
        citations1=citations1+citation.split(';')
    elif '；' in citation:
        citations1=citations1+citation.split('；')
        
for citation in citations1[:]:
    if (';' in citation) or ('；' in citation):
        citations1.remove(citation)

#防止(作者，年份;年份)
for i,citation in enumerate(citations1):
    if citation.isdigit():
        citations1[i]=re.findall('\p{L}\D+?(?=\d)',citations1[i-1])[0]+citations1[i]
        
#类型1 (作者,年份;作者,年份)
for citation in citations1:
    name_w=re.findall('\p{L}\D+?(?=\d)',citation)[0]
    years=re.findall('\d{4}[ab]?',citation)
    if len(years)>1:
        for year in years:
            citations1.append(name_w+year)#1
    
for citation in citations1[:]:#删除
    if len(re.findall('\d{4}[ab]?',citation))!=1:
        citations1.remove(citation)#或citations1=[x for x in citations1 if len(re.findall('\d{4}[ab]?',x))==1]

#类型2 作者(年份)
for citation in citations2:
    name_w=re.findall('\p{L}\D+?(?=\d)',citation)[0]
    years=re.findall('\d{4}[ab]?',citation)
    if citation==' et al.（2020':
        print('123')
    if len(years)>1:
        for year in years:
            citations2.append(name_w+year)#2
for citation in citations2[:]:#删除
    if len(re.findall('\d{4}[ab]?',citation))!=1:
        citations2.remove(citation)

citations=citations1+citations2
print("\n引用了但参考文献中不存在的文献：")
missing_references=[]
for citation in citations:
    found=False
    for reference in cankao_author_year:
        if reference[0] in citation and reference[1] in citation:
            found=True
            break
    if not found:
        missing_references.append(citation)
        print(citation)
print("\n在参考文献中出现但在正文中未引用的文献：（也可能引用了但正文有格式问题）")
unused_references=[]
for reference,reference_all in zip(cankao_author_year,cankao):
    found=False
    for citation in citations:
        if reference[0] in citation and reference[1] in citation:
            found=True
            break
    if not found:
        unused_references.append(reference_all)
        print(reference_all)
print('\n相同作者和年份的引用文献:')
repeated = []
for citation in citations:
    if citations.count(citation)>1:
        repeated.append(citation)
print(repeated)

del zhengwen,year,years,reference,para,name_w
del name,i,front,front2,end,found,citation,cankao_num,f,diff
