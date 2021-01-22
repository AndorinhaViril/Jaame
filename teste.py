'''import time

t = time.time()
a = 0
while a < 1000000:
	a+=1

t= time.time()-t
print(t)
'''
import os
archieves = []
caminhos = [os.path.join('maps', nome) for nome in os.listdir('maps')]
arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
for arq in arquivos: 
	if arq.lower().endswith(".phg"):
		aux = arq.replace('.phg','')
		aux = aux.replace('maps\\','')

		archieves.append(aux)
for p in archieves:
	print(f'{p.lower()} ASDASD {type(p)}')
'''

if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        print(text)
                        text = ''
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

'''