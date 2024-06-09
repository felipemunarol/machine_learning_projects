using SparseArrays

# Daods do Problema da Produção
A = sparse([2 1 1 0; 1 2 0 1])
c =[4; 3; 0; 0]
b=[4;4]
m,n = size(A)
k = n - m # Numero de Variáveis não básicas


#Solução Inical

Nbase = collect(1:k)
Bbase = collect(k+1:n)


#Início do Loop
B = view(A,:,Bbase)
N = view(A,:,Nbase)
cB = c[Bbase]
cN = c[Nbase]
xB = B\b
y = B'\cB 
cred = cN - N'y
z = y'b
v,j = findmax(cred) #j é a variavel não básica que candidata a entrada na base
if v <= 0
    println("Ótimo Encontrado")
    x = zeros(n)
    x[Bbase] = xB
    return z,x
end
# Encontrando Variavel Báscia para sair da Base 
dB = B\N[:,j] 
i = 0
r = Inf
for ii = 1:m
    if dB[ii] > 0 && xB[ii]/dB[ii] < r
        i = ii
        r = xB[ii]/dB[ii]
    end
end
if i == 0 # Condição de Parada por Problema Ilimitado
    println("Problema Ilimitado")
    return Inf,[]
end
# Troca de Base
aux = Nbase[j]
Nbase[j] = Bbase[i]
Bbase[i] = aux
# Final do Loop


D = B\N

d = B\N[:,j]
