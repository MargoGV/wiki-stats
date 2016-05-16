
import os
import sys
import math

import array

import statistics as st

#Cantarell
import matplotlib.pyplot as plt
plt.rc('font', family='Carlito')


class WikiGraph:

    def load_from_file(self, filename):
        print('Загружаю граф из файла: ' + filename)

        with open(filename) as f:
            (n, _nlinks) = (0, 0) 
            
            self._titles = []
            self._sizes = array.array('L', [0]*n)
            self._links = array.array('L', [0]*_nlinks)
            self._redirect = array.array('B', [0]*n)
            self._offset = array.array('L', [0]*(n+1))
            data=f.readline().split()
            n,_nlinks=int(data[0]),int(data[1])                     
            for i in range(n):                                       
                self._titles.append(f.readline().rstrip())          
                data=f.readline().split()                           
                self._sizes.append(int(data[0]))                    
                self._redirect.append(int(data[1]))                 
                self._offset.append(self._offset[i]+int(data[2]))   
                for j in range(int(data[2])):                       
                    self._links.append(int(f.readline().rstrip()))  
        print('Граф загружен')
    def get_number_of_links_from(self, _id):
        return(self._offset[_id+1]-self._offset[_id])

    def get_links_from(self, _id):
        links=[]
        for i in range(self._offset[_id],self._offset[_id+1]):
            links.append(self._links[i])
        return links

    def get_id(self, title):
        for i in range(len(self._titles)):
            if title==self._titles[i]:
                return i

    def get_number_of_pages(self):
        return len(self._titles)

    def is_redirect(self, _id):
        if self._redirect[_id]:
            return True
        return False            

    def get_title(self, _id):
        return self._titles[_id]

    def get_page_size(self, _id):
        return self._sizes[_id]
    
    
    
                
        
        
    
    def analyse(self): 
    
        print('Количество статей с перенаправлением: ',sum(self._redirect),' (',round(100*sum(self._redirect)/self.get_number_of_pages(),2),'%)',sep='')
        
        minimum=None
        count=1
        
        for i in range(self.get_number_of_pages()):
            if minimum==None or minimum>self.get_number_of_links_from(i):
                count=1
            elif minimum==self.get_number_of_links_from(i):
                count+=1
            if minimum==None:
                minimum=self.get_number_of_links_from(i) 
            else:
                minimum=min(minimum,self.get_number_of_links_from(i))
                
        print('Минимальное количество ссылок из статьи: ',minimum)
        
        print('Количество статей с минимальным количеством ссылок: ',count)
        
        maximum=None
        count=1
        
        for i in range(self.get_number_of_pages()):
            if maximum==None or maximum<self.get_number_of_links_from(i):
                count=1
                number=i
            elif maximum==self.get_number_of_links_from(i):
                count+=1
            if maximum==None:
                maximum=self.get_number_of_links_from(i) 
            else:
                maximum=max(maximum,self.get_number_of_links_from(i))
        print('Максимальное количество ссылок из статьи: ',maximum)
        
        print('Количество статей с максимальным количеством ссылок: ',count)
        
        print('Статья с наибольшим количеством ссылок: ',self.get_title(number))
        
        articles=[]           
        
        for i in range(self.get_number_of_pages()):
            if  not self._redirect[i]:
                articles.append(self.get_number_of_links_from(i))
        print('Среднее количество ссылок в статье: ',round(st.mean(articles),2),'(ср. откл. ',round(st.stdev(articles),2),')')
        articles2=[0]*self.get_number_of_pages()                
        for i in range(self.get_number_of_pages()):
            if not self._redirect[i]:
                for j in range(self._offset[i],self._offset[i+1]):
                    articles2[self._links[j]]+=1
        print('Минимальное количество ссылок на статью:  ',min(articles2))
        print('Количествое статей с минимальным количеством внешних ссылок: ',articles2.count(min(articles2)))
        print('Максимально количество ссылок на статью:  ',max(articles2))
        g=max(articles2)
        g1=articles2.count(max(articles2))
        print('Количество статей с максимальным количеством внешних ссылок: ',g1)
        for i in range(len(articles2)):
            if articles2[i]==g:
                number=i
                break
        print('Статья с наибольшим количеством внешних ссылок: ',self.get_title(number))
        print('Среднее количество ссылок в статье: ',round(st.mean(articles2),2),'(ср. откл. ',round(st.stdev(articles2),2),')')
        articles3=[0]*self.get_number_of_pages()                #Количество перенаправлений на статью
        for i in range(self.get_number_of_pages()):
            if self._redirect[i]:
                for j in range(self._offset[i],self._offset[i+1]):
                    articles3[self._links[j]]+=1
        print('Минимальное количество перенаправлений на статью:  ',min(articles3))
        print('Количество статей с минимальным количеством внешних перенаправлений: ',articles3.count(min(articles3)))
        print('Максимальное количество перенаправлений на статью:  ',max(articles3))
        g=max(articles3)
        g1=articles3.count(max(articles3))
        print('Количество статей с максимальным количеством внешних перенаправлений: ',g1)
        for i in range(len(articles3)):
            if articles3[i]==g:
                number=i
                break
        print('Статья с наибольшим количеством внешних перенаправлений: ',self.get_title(number))
        print('Среднее количество внешних перенаправлений на статью: ',round(st.mean(articles3),2),'(ср. откл. ',round(st.stdev(articles3),2),')')
        return (articles,articles2,articles3)
        
            
        
        
      
        
                  
        
def find_a_way(wg,start,end):
    stack=array.array('L',[0]*wg.get_number_of_pages())
    way=[]
    stack[0]=start
    ways=array.array('l',[-1]*wg.get_number_of_pages())
    flag_list=array.array('B',[0]*wg.get_number_of_pages())
    first=0
    last=1
    while first<last:
        node=stack[first]
        first+=1
        flag_list[node]=1
        if node==end:
            break
        else:
            for l in wg.get_links_from(node):
                if not flag_list[l]:
                    flag_list[l]=1
                    ways[l]=node
                    stack[last]=l
                    last+=1
                        
    
    node=end
    while node!=-1:
        way.append(node)
        node=ways[node]         
    return way[-1::-1]

        
        


def hist(fname, data, bins, xlabel, ylabel, title, facecolor='green', alpha=0.5, transparent=True,ranger=None, **kwargs):
    plt.clf()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.hist(data,bins,range=ranger)
    plt.show()
    plt.savefig(fname,format='png')
    


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Использование: wiki_stats.py <файл с графом статей>')
        sys.exit(-1)

    if os.path.isfile(sys.argv[1]):
        wg = WikiGraph()
        wg.load_from_file(sys.argv[1])
        data,data2,data3=wg.analyse()
        way=[0]* wg.get_number_of_pages()
        print('Запускаем поиск в ширину')
        way=find_a_way(wg,wg.get_id('Python'),wg.get_id('Боль'))
        print('Поиск закончен. Найден путь:')
        for i in way:
            print(wg.get_title(i))
        
        
        hist('Распределение количества ссылок из статьи',data,100,'Количество статей','Количество ссылок','Распределение количества ссылок из статьи',ranger=(0,200))
        hist('Распределение количества ссылок на статью',data2,100,'Количество статей','Количество ссылок','Распределение количества ссылок на статью',ranger=(0,200))
        hist('Распределение количества перенаправлений на статью',data3,30,'Количество статей','Количество ссылок','Распределение количества перенаправлений на статью',ranger=(0,20))
        hist('Распределение размеров статей',wg._sizes,100,'Размер статьи','Количество статей','Распределение размеров статей',ranger=(300,100000))
        log=[]
        for i in range(len(wg._sizes)):
            log.append(math.log10(wg._sizes[i]))
        hist('Распределение размеров статей(в логарифмическом масштабе)',log,20,'Размер статьи','Количество статей','Распределение размеров статей(в логарифмическом масштабе)',ranger=(0,6))
            
        
        
                
        
    else:
        print('Файл с графом не найден')
        sys.exit(-1)

