nota = 4.5
trabajo_realizado = 'si'

nota_final = 'reprobado'

if (nota >= 4) and (trabajo_realizado == 'si'):
    nota_final = 'aprobado'
else:
    nota_final = 'reprobado'

print(nota_final)