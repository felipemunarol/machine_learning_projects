#dados do problema da produção 
using SparseArrays

#problema da produção original
A = 1.0*[2 1 1 0 ; 1 2 0 1]
c = 1.0*[4; 3 ;0;0]
b= 1.0*[4;4]
#problema da produção com restrição de produção mínima
A = 1.0*[2 1 1 0 0; 1 2 0 1 0; -1 -1 0 0 1]
c = 1.0*[4; 3 ;0;0; 0]
b= 1.0*[4;4; -1]

m,n = size(A)
k = n-m#número de variáveis não básicas


Nbase = collect(1:k)
Bbase = collect(k+1:n)
max_iter =1000

function simplex_fase1(A,b,c,Max_iter)
    m,n = size(A)
    Anova = [A -ones(m)]
    m,n = size(Anova)
    k = n-m
    v,i = findmin(b)
    Nbase = [collect(1:k-1);k-1+i]
    Bbase = collect(k:k+m-1)
    Bbase[i] = n
    

end

function simplex_fase2(A,b,c,Nbase,Bbase,max_iter)
    m,n = size(A)
    k = n-m
    
    
    iter=0
    status = -1# não iniciado
    #começo do loop
    while(iter<=max_iter)
        iter+=1
        #B = view(A,:,Bbase)

        #N = view(A,:,Nbase)
        B = 1.0*A[:,Bbase]
        N = 1.0*A[:,Nbase]
        #colocar os views, view evita a criação de uma nova matriz em outro bloco de memoria
        #apenas faz referencia aos endereco de memoria da matriz original
        cB = 1.0*c[Bbase]
        cN = 1.0*c[Nbase]
    
        println("B",B)
        println("b",b)
        println("iter",iter)

        x = zeros(n)
        
        xB = B\b
        x[Bbase] = xB
        if minimum(xB) < 0
            println("solução inicial inviável encontrada")
            return NaN,[],status,iter
        end
        #calcular o custo reduzido
        y = B'\cB
        cred = cN - N'y #4 ;3
        z = y'b
        v,j = findmax(cred)
        if v<=0
            status = 1#ótimo encontrado
            println("otimo")
            return z,x, status,iter
        end
        #troca de base
        dB = B\N[:,j]
        r = Inf
        i =0 

        for ii in 1:m
            if dB[ii] > 0 && xB[ii]/dB[ii] < r
                r = xB[ii]/dB[ii]
                i = ii
            end
        end

        #verificar se o problema é ilimitado
        if i ==0
            status = 0 # problema ilimitado
            println("ilimitado")
            return Inf,[], status,iter
        end

        #atualizar a base

        aux = Bbase[i]
        Bbase[i] = Nbase[j]
        Nbase[j] = aux

        #fim do loop
    end
    return NaN,[],status,iter
end

simplex_fase2(A,b,c,Nbase,Bbase,max_iter)