'''
Geração de fases de forma aleatória, (pensar em uma forma de criar estruturas "padrões")
'''
import random
class cell():
    def __init__(self, pos):
        self.pos = pos
        self.hasNear = {'n':False,'s':False,'w':False,'e':False}
        self.n = None
        self.s = None
        self.e = None
        self.w = None
        self.type = '9000'
    def hasNearCells(self,*direction):
        for d in direction:
            self.findCellOn(d)
    def findCellOn(self, direction):
        if direction == 'n':
            if self.pos[1] - 1 >= 0:
                self.hasNear['n'] = True
                return (self.pos[0],self.pos[1]-1)
            else:
                self.hasNear['n'] = False
                return None
        elif direction == 's':
            if self.pos[1] + 1 < 26:
                self.hasNear['s'] = True
                return (self.pos[0],self.pos[1]+1)
            else:
                self.hasNear['s'] = False
                return None
        elif direction == 'w':
            if self.pos[0] - 1 >= 0:
                self.hasNear['w'] = True
                return (self.pos[0]-1,self.pos[1])
            else:
                self.hasNear['w'] = False
                return None
        elif direction == 'e':
            if self.pos[0] + 1 < 64:
                self.hasNear['e'] = True
                return (self.pos[0]+1,self.pos[1])
            else:
                self.hasNear['e'] = False
                return None


        
class phase():
    def __init__(self):
        self.height = 26
        self.width = 64
        self.write = False
        self.matriz = [[cell((x,y)) for x in range(self.width)] for y in range(self.height)]
        self.matrizvisual =  [[0 for x in range(self.width)] for y in range(self.height)]
        self.exit = ((random.randrange(1,self.width-2),random.randrange(self.height-5,self.height-2)))
        self.spawn = ((random.randrange(2,self.width-2),random.randrange(1,4)))
        self.lastDirection = None
        self.path = []
        self.firstDirection = None
    def set_write(self, is_writing):
        self.write = is_writing
    def findCellByPosition(self,position):
        if position is not None:
            return self.matriz[position[1]][position[0]]
        else:
            return None
  
    def setNearCells(self):
        for lista in self.matriz:
            for cell in lista:
                cell.n = self.findCellByPosition(cell.findCellOn('n'))
                cell.w = self.findCellByPosition(cell.findCellOn('w'))
                cell.s = self.findCellByPosition(cell.findCellOn('s'))
                cell.e = self.findCellByPosition(cell.findCellOn('e'))
                self.updateCell(cell)
    def setCellType(self,cell,tipe):
        cell.type = tipe
        self.updateCell(cell)
    def updateCell(self,cell):
        self.matriz[cell.pos[1]][cell.pos[0]] = cell
        #print(cell.type)
    def doIt(self):
        self.path = []
        self.firstDirection = None
        start = self.findCellByPosition(self.spawn)
        end = self.findCellByPosition(self.exit)
        self.random_path(start,end,True)
        self.random_path(start,end,True)
        for i in range(1,15):
           # print('{}|{}'.format(1+i,self.height-2))
            start = (random.randrange(1,self.width-2), random.randrange(1+i,self.height-2))
            end = (random.randrange(1,self.width-2),random.randrange(start[1],self.height-1))
            self.random_path(self.findCellByPosition(start),self.findCellByPosition(end),False)
        #print()
        self.post_processing() 
        return self.write_phase()
    def random_path(self,start,end,is_initial):
        aux = start
        path = []
        randchoice = None
        self.lastDirection = None
        done = False
        possibleNear = []
        cont = 0
        aux1 = None
        while not done:
            aux1 = aux
            if aux is not start:
                possibleNear = []
                if aux.hasNear['w'] is True and self.lastDirection != 'e':
                    if aux.w.hasNear['w']:
                        if aux.pos[1] < end.pos[1]:
                            possibleNear.append(aux.w)
                            possibleNear.append(aux.w)
                            possibleNear.append(aux.w)
                            possibleNear.append(aux.w)
                            possibleNear.append(aux.w)
                            possibleNear.append(aux.w)
                        elif aux.pos[1] == end.pos[1] and aux.pos[0] > end.pos[0]:
                            possibleNear.append(aux.w)
                            possibleNear.append(aux.w)
                            possibleNear.append(aux.w)
                            possibleNear.append(aux.w)
                            possibleNear.append(aux.w)
                            possibleNear.append(aux.w)
                if aux.hasNear['e'] is True and self.lastDirection != 'w':
                    if aux.e.hasNear['e']:
                        if aux.pos[1] < end.pos[1]:
                            possibleNear.append(aux.e)
                            possibleNear.append(aux.e)
                            possibleNear.append(aux.e)
                            possibleNear.append(aux.e)
                            possibleNear.append(aux.e)
                            possibleNear.append(aux.e)
                        elif aux.pos[1] == end.pos[1] and aux.pos[0] < end.pos[0]:
                            possibleNear.append(aux.e)
                            possibleNear.append(aux.e)
                            possibleNear.append(aux.e)
                            possibleNear.append(aux.e)
                            possibleNear.append(aux.e)
                            possibleNear.append(aux.e)
                if aux.hasNear['s'] is True and self.lastDirection !='s':
                    if aux.pos[1] < end.pos[1]:
                        possibleNear.append(aux.s)
##                if len(possibleNear) == 0:
##                    print('a: {} s: {} e: {}'.format(start.pos,aux.pos,end.pos))
                randchoice = random.choice(possibleNear)              
            elif aux is start:
                if is_initial:
                    self.setCellType(aux,'1000')
                    if aux.hasNear['w'] == True and aux.w is not self.firstDirection:
                        possibleNear.append(aux.w)
                    if aux.hasNear['e'] == True and aux.e is not self.firstDirection:
                        possibleNear.append(aux.e)
                    randchoice = random.choice(possibleNear)
                    self.firstDirection  = randchoice
                else:
                    if aux.type == '9000':
                        self.setCellType(aux,'0000')
                    if start.pos[1] != end.pos[1]:
                        if aux.hasNear['w'] == True and aux.w.type != '0000':
                            possibleNear.append(aux.w)
                        if aux.hasNear['e'] == True and aux.e.type != '0000':
                            possibleNear.append(aux.e)
                        if aux.hasNear['s'] == True and aux.s.type != '0000':
                            possibleNear.append(aux.s)

                    else:
                        if aux.hasNear['w'] == True and end.pos[0] < aux.pos[0]:
                            possibleNear.append(aux.w)
                        if aux.hasNear['e'] == True and end.pos[0] > aux.pos[0]:
                            possibleNear.append(aux.e)
                    if len(possibleNear) > 0:
                        randchoice = random.choice(possibleNear)
                    else:
                        done = True
                        break
            self.setCellType(randchoice,'0000')
            
            if randchoice is aux.s:
                if randchoice.hasNear['s'] is True and randchoice.s.pos[1] < end.pos[1]:
                    self.setCellType(randchoice.s,'0000')
                    randchoice = randchoice.s
                    if randchoice.hasNear['s'] is True and randchoice.s.pos[1] < end.pos[1]:
                        self.setCellType(randchoice.s,'0000')
                        aux = randchoice.s
            self.lastDirection = 'e' if randchoice is aux.e else 'w' if randchoice is aux.w else 's' if randchoice is aux.s else ''
            if aux is aux1 or aux1 == None:
                aux = randchoice
            if is_initial:
                path.append(aux.pos)
            if aux is end or aux.e is end or aux.s is end or aux.w is end:
                if is_initial:
                    self.setCellType(end,'8000')
                else:
                    self.setCellType(end,'0000')
                if is_initial:
                    self.path.append(path)
                done = True   
            
        
    def reDoIt(self):
        self.exit = ((random.randrange(1,self.width-1),random.randrange(self.height-5,self.height-2)))
        self.spawn = ((random.randrange(2,self.width-1),random.randrange(1,4)))
        self.doIt()
    def verify_path(self):
        aux = []
        aux3 = []
        aux.append(self.findCellByPosition(self.spawn))
        while len(aux) != 0:
            aux2 = []
            for cell in aux:
                #print('{} | {}'.format(cell.pos,cell.type))
                if cell.type == '8000':
                    return True
                else:
                    aux3.append(cell)
                    if  cell.hasNear['e']:
                        if cell.e.type != '9000' and cell.e.type != '1000' and not cell.e in aux3:
                            aux2.append(cell.e)
                    if  cell.hasNear['w']:
                        if cell.w.type != '9000' and cell.w.type != '1000' and not cell.w in aux3:
                            aux2.append(cell.w)
                    if  cell.hasNear['s']:
                        if cell.s.type != '9000' and cell.s.type != '1000' and not cell.s in aux3:
                            aux2.append(cell.s)
                    aux.remove(cell)
            for c in aux2:
                aux.append(c)
        return False
    def get_cells_without_traps(self):
        cwt = []
        aux = None
        #print('|--',end = ' ')
        #print(self.spawn)
        #print(self.path)
        for list_ in self.path:
            for pos in list_:
                if aux == None:
                    aux = pos
                elif pos[1] != aux[1]:
                    cwt.append(pos)
                    aux = pos
        return cwt
    def post_processing(self):
        self.vertically_widen()
        self.setCellType(self.findCellByPosition(self.spawn),'1000')
        self.setCellType(self.findCellByPosition(self.exit),'8000')
        self.setCellType(self.findCellByPosition((self.spawn[0],self.spawn[1]+1)),'9000')
        self.setCellType(self.findCellByPosition((self.exit[0],self.exit[1]+1)),'9000')
        if not self.verify_path():
            self.reDoIt()
        self.set_traps()
    def set_traps(self):
        spaces = 0
        cells = []
        cellsUp = []
        cellsDown = []
        cannotcells = self.get_cells_without_traps()
        for list_ in self.matriz:
            for cell in list_:
                if cell.type[0] == '0':
                    if cell.hasNear['w']:
                        if cell.w.type[0] == '9':
                            cells.append(cell.w)
                    if cell.hasNear['e']:
                        if cell.e.type[0] == '9':
                            cells.append(cell.e)
                    if cell.hasNear['n']:
                        if cell.n.type[0] == '9':

                            if cell.pos[1] > self.spawn[1]:
                                cellsUp.append(cell.n)
                    if cell.s.type[0] == '9':
                        if cell.pos[0] < self.spawn[0]-5 and cell.pos[0] >self.spawn[0]+5:
                            cellsDown.append(cell.s)
                        elif cell.pos[1] != self.spawn[1]:
                            cellsDown.append(cell.s)
                    spaces += 1
        traps = spaces//20
        rand = None
        can = True
        if len(cellsDown) > 0:
            for i in range(0,traps):
                rand = random.choice(cellsDown)
                if rand.hasNear['n']:
                    if rand.n.hasNear['n']:                    
                        if rand.n.n.type[0] == '0':
                            for pos in cannotcells:
                                if pos[1]+1 == rand.pos[1] and pos[0] == rand.pos[0]:
                                    can = False
                    else:
                        can = False
                    if can:
                        if rand.hasNear['e']:
                            if rand.e.type[1] == '0':
                                rand.type = self.format_cell_type(rand.type,'1',1)
                            else:
                                if rand.e.hasNear['e']:
                                    if rand.e.e.type[1] != '1':
                                        rand.type = self.format_cell_type(rand.type,'1',1)
                                else:
                                    rand.type = self.format_cell_type(rand.type,'1',1)
                        elif rand.hasNear['w']:
                            if rand.w.type[1] == '1':
                                if rand.w.hasNear['w']:
                                    if rand.w.w.type[1] != '1':
                                        rand.type = self.format_cell_type(rand.type,'1',1)
                                else:
                                    rand.type = self.format_cell_type(rand.type,'1',1)
                            else:
                                rand.type = self.format_cell_type(rand.type,'1',1)
                cellsDown.remove(rand)
                can = True
                if len(cellsDown) == 0:
                    break
        
        if len(cells) > 0:
            for i in range(0,traps):
                rand = random.choice(cells)
                rand.type = self.format_cell_type(rand.type,'2',1)
                if rand.hasNear['n']:
                    if rand.n.type[1] != 2:
                        if rand.hasNear['e']:
                            if rand.e.type[0] =='0':
                                rand.type = self.format_cell_type(rand.type,'3',3)
                        if rand.hasNear['w']:
                            if rand.w.type[0] =='0':
                                rand.type = self.format_cell_type(rand.type,'2',3)
                cells.remove(rand)
                if len(cells) == 0:
                    break

        if len(cellsUp) > 0:
            for i in range(0,traps//2):
                rand = random.choice(cellsUp)
                if rand.type[1] == '0':
                    self.setCellType(rand,self.format_cell_type(rand.type,'6',1))
                #print(self.matriz[rand.pos[1]][rand.pos[0]].type)
                cellsUp.remove(rand)
                if len(cellsUp) == 0:
                    break

    def format_cell_type(self,type_,type_to_add,where):
        aux = list(type_)
        aux[where] = type_to_add
        ret = ''.join(aux)
        return ret
    def vertically_widen(self):
        self.setNearCells()
        for list_ in self.matriz:
            for cell in list_:
                if cell.type == '0000' and cell.hasNear['n'] or cell.type == '8000' and cell.hasNear['n'] or cell.type == '1000' and cell.hasNear['n']:
                    if cell.n.hasNear['n']:
                        if cell.n.type == '9000' and cell.n.n.type != '0000':
                            self.setCellType(cell.n,'0000')

    def write_phase(self):
        text_complete = ''
        contador = 0
        for cont in range(0,self.height):
            for contItem in range(0,self.width):
                self.matrizvisual[cont][contItem] = self.matriz[cont][contItem].type
                #print(self.matrizvisual[cont][contItem])
        if self.write:#praticamente inutil    
            text_file = open("data\components\saida.txt", "w")
            for i in self.matrizvisual:
                text = '{}\n'.format(i)
                text = text.replace('[','')
                text = text.replace(']','')
                text = text.replace(', ','')
                text_complete += text
                
                text_file.write(text)
            text_file.close()
        #print(self.matrizvisual)
        return self.matrizvisual
            
    def read_phase(self):#legancy -NÃO UTILIZAR-
        file = open("saida.txt", "r")
        text = file.read()
        file.close()    
        phase = []
        for row in text:
            phase.append(row)
        return phase
##test--
##c = 0
#p = phase()
#while True:
#p.setNearCells()
#p.doIt()
##    #c+=1
##    #print('|{}|'.format(c))
