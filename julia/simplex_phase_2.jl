import Pkg

# Pkg.add("Random")

using Random
using SparseArrays

# Simplex fase 2
function simplex_fase2(A,b,c,Nbase,Bbase,max_iter, tolerance)
    m, n = size(A)
    k = n - m # número de variáveis não básicas (igual ao número de variáveis menos o número de restrições, 
    # sendo que cada restrição é uma variável básica)
    
    iter = 0
    status = -1    # não iniciado
    # Começo do loop
    while(iter<=max_iter)
        iter+=1
        println("iter:",iter)
        #B = view(A,:,Bbase)
        #N = view(A,:,Nbase)
        
        B = 1.0*A[:,Bbase]
        N = 1.0*A[:,Nbase]
        # Colocar os views, view evita a criação de uma nova matriz em outro bloco de memoria
        #apenas faz referencia aos endereco de memoria da matriz original
        cB = 1.0*c[Bbase]
        cN = 1.0*c[Nbase]
    
        println("B:",B)
        println("N:",N)
        println("Nbase:",Nbase)
        println("Bbase:",Bbase)

        x = zeros(n)
        
        xB = inv(B)*b
        println("xb", xB)
        x[Bbase] = xB
        println("x", x)
        if minimum(xB) < 0
            println("solução inicial inviável encontrada")
            return NaN,[],status,iter
        end
        # Calcular o custo reduzido
        y = (cB')*inv(B)
        cred = cN' - y*N
        println("Custo Reduzido:", cred)
        z = y*b
        v,j = findmax(cred') #j é a variavel não básica que candidata a entrada na base
        if v <= 0
            println("Ótimo Encontrado")
            status = 1
            x = zeros(n)
            x[Bbase] = xB
            return z,x,status,iter,Bbase,Nbase
        end
        #troca de base
        dB = B\N[:,j]
        r = Inf
        i = 0

        for ii in 1:m
            if dB[ii] > 0 && xB[ii]/dB[ii] < r
                r = xB[ii]/dB[ii]
                i = ii
            end
        end

        #verificar se o problema é ilimitado
        if i == 0
            status = 0 # problema ilimitado
            println("ilimitado")
            return Inf,[], status,iter, Bbase, Nbase
        end

        # Atualizar a base

        aux = Bbase[i]
        Bbase[i] = Nbase[j]
        Nbase[j] = aux

        # fim do loop
    end
    return NaN,[],status,iter
end

# Testes
function tests_main()

    max_iter =1000
    # Problema da produção original
    print("Teste do algoritmo para o: Problema da produção \n")
    A = 1.0*[
        2 1 1 0; 
        1 2 0 1
    ]
    c = 1.0*[
        4; 3 ; 0; 0
    ]
    b= 1.0*[
        4;
        4
    ]
    m, n = size(A)
    k = n - m
    Nbase = collect(1:k)
    Bbase = collect(k+1:n)
    z, x, status, iter, Bbase, Nbase = simplex_fase2(A,b,c,Nbase,Bbase,max_iter, 1)
    print(repeat("-", 200), "\n")
    
    print("Teste do algoritmo para o: Problema ilimitado \n")
    # Problema ilimitado
    A = 1.0*[
        1 -1 1 0; 
        1 -1 0 -1
    ]
    c = 1.0*[
        2; 1 ; 0; 0
    ]
    b= 1.0*[
        1;
        -1
    ]
    m, n = size(A)
    k = n - m
    Nbase = collect(1:k)
    Bbase = collect(k+1:n)
    z, x, status, iter, Bbase, Nbase = simplex_fase2(A,b,c,Nbase,Bbase,max_iter, 1)
    print(repeat("-", 200), "\n")
    
    print("Teste do algoritmo para o: Problema da produção 10 vars \n")
    # Problema producao aumentado - 10 variaveis
    Random.seed!(222)   # set the seed to not generate different results in every execution
    A = rand([1, 2, 3, 4, 5], 2, 10)
    A = 1.0*hcat(A, [1 0 ; 0 1])
    c = rand([1, 2, 3, 4, 5], 10, 1)
    c = 1.0*vcat(c, [0; 0])
    b= 1.0*[
        100;
        20
    ]
    m, n = size(A)
    k = n - m
    Nbase = collect(1:k)
    Bbase = collect(k+1:n)
    z, x, status, iter, Bbase, Nbase = simplex_fase2(A,b,c,Nbase,Bbase,max_iter, 1)
    print(repeat("-", 200), "\n")
    
    print("Teste do algoritmo para o: Problema da produção 100 vars \n")
    # Problema producao aumentado - 100 variaveis
    Random.seed!(222)   # set the seed to not generate different results in every execution
    A = rand([1, 2, 3, 4, 5], 2, 100)
    A = 1.0*hcat(A, [1 0 ; 0 1])
    c = rand([1, 2, 3, 4, 5], 100, 1)
    c = 1.0*vcat(c, [0; 0])
    b= 1.0*[
        100;
        20
    ]
    m, n = size(A)
    k = n - m
    Nbase = collect(1:k)
    Bbase = collect(k+1:n)
    z, x, status, iter, Bbase, Nbase = simplex_fase2(A,b,c,Nbase,Bbase,max_iter, 1)
end

tests_main()