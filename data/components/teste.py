a = '1234'
def coloca(lugar,oq,onde):
    aux = list(onde)
    aux[lugar] = oq
    ret = ''.join(aux)
    return ret

a = coloca(1,'6',a)
print(a)
