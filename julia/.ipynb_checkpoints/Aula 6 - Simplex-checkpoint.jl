using SparseArrays, LinearAlgebra
# Dados do Problema da Produção
A = sparse([2 1 1 0; 1 2 0 1])
c =sparse([4; 3; 0; 0])
b=sparse([4;4])

# Dados do Problema da Produção - Com restrição de produção minima
A = sparse([2 1 1 0 0 ; 1 2 0 1 0; -1 -1 0 0 1])
c =sparse([4; 3; 0; 0 ; 0])
b=sparse([4;4;-1])


# Dados do Problema da Produção - Forma Canonica de Max
A = sparse([2 1 ; 1 2 ; -1 -1 ])
c =sparse([4; 3])
b=sparse([4;4;-1])




m,n = size(A)
k = n - m # Numero de Variáveis não básicas

maxiter = 1000
#Solução Inical
Nbase = collect(1:k)
Bbase = collect(k+1:n)

function Simplex_2(A,b,c,Bbase,Nbase,maxiter)
    iter = 0
    status = -1 #Problema Não Terminado - Numero máximo de iterações
    #Início do Loop
    while iter <= maxiter
        iter += 1 
        B = view(A,:,Bbase)
        N = view(A,:,Nbase)
        cB = c[Bbase]
        cN = c[Nbase]
        xB = B\b
        if minimum(xB) < 0
            println("Bug:SOlução Inviavel encontrada no Fase 2")
            return [],[],-2,iter,Bbase,Nbase
        end
        y = B'\cB 
        cred = cN - N'y
        z = y'b
        v,j = findmax(cred) #j é a variavel não básica que candidata a entrada na base
        if v <= 0
            println("Ótimo Encontrado")
            status = 1
            x = zeros(n)
            x[Bbase] = xB
            return z,x,status,iter,Bbase,Nbase
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
            status = 2
            return Inf,[],status,iter,Bbase,Nbase
        end
        # Troca de Base
        aux = Nbase[j]
        Nbase[j] = Bbase[i]
        Bbase[i] = aux
        # Final do Loop
    end
    x = zeros(n)
    x[Bbase] = xB
    println("Numero Máximo de Iteração")
    return [],x,status,iter,Bbase,Nbase
end

Simplex_2(A,b,c,Bbase,Nbase,maxiter)

function Simplex_1(A,b,maxiter)
    v,i = findmin(b)
    m = length(b)
    Ae = [A -ones(m)]
    m,n = size(Ae)
    k = n-m
    ce = zeros(n)
    ce[n] = -1
    Nbase = [collect(1:k-1);k-1+i]
    Bbase = collect(k:k+m-1)
    Bbase[i] = n
    z,x,status,iter,Bbase,Nbase = Simplex_2(Ae,b,ce,Bbase,Nbase,maxiter)
    if x[n] > 0
        println("Problema Inviavel")
        status = -2
        return -Inf,[],status,iter,Bbase,Nbase
    else
        println("Fim da Fase 1.")
        status = -1
        return [],[],status,iter,Bbase,Nbase
    end
end

Simplex_1(A,b,maxiter)

#function Simplex(A,b,maxiter)
m,n = size(A)    
Ap = [A I(m)]
cp = [c;zeros(m)]
Simplex_1(Ap,b,maxiter)
#end