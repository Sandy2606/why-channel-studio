import sys, json; sys.path.insert(0,'/home/claude/g4'); import clipkit as C
C.Z='/home/claude/g5/z/'
out={}
P={'bs':[('icmai-digest-2025-03-29.pdf',2,(28,592,580,724),['25,000 tonnes.','top 10 central banks'])],
   'mint':[('mint-gold-loans.pdf',1,(30,222,580,285),[]),('mint-gold-loans.pdf',1,(30,636,580,714),['second-largest retail credit category'])],
   'mint16':[('mint-gold-loans.pdf',1,(40,507,580,531),['record ₹ 16 trillion,'])],
   'abc':[('aditya-birla-gold-price-history.pdf',3,(30,0,580,0),['8,400'])]}
# abc: find the 20 Years row on page 3
r=C.box(C.find('aditya-birla-gold-price-history.pdf',3,'20 Years'),(0,0)); print('abc row',r)
P['abc']=[('aditya-birla-gold-price-history.pdf',2,(30,741,414,758),[]),('aditya-birla-gold-price-history.pdf',3,(30,r[1]-3,414,r[3]+2.5),['20 Years','2006','8,400'])]
for k,parts in P.items():
    im,h=C.build(parts); im.save(f'clip_{k}.png'); out[k]={'hl':h}; print(k,im.size)
json.dump(out,open('clips.json','w'))
