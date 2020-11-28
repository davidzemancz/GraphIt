def insertSort(arr):
    for i in range(1, len(arr)): # Prochazim pole od 1 do konce
        j = i
        while j > 0: # Prochazim setridenou cast pole od i do 0
            if arr[j].weight < arr[j - 1].weight: # Pokud je prvek vetsi nez predchozi, prohodim je
                arr[j], arr[j - 1] = arr[j - 1], arr[j]
                j -= 1
            else:
               break

def sort(arr): # Mergesort, co pri poli kratsim 11 vola insertsort
    if len(arr) <= 1:
        return arr
    elif len(arr) <= 10: # Pokud je pole kratsi 11, insertsortim
        return insertSort(arr) 

    # Pulim pole
    mid = len(arr) // 2
    arr_l = arr[:mid]
    arr_r = arr[mid:]
 
    # Rekurzivne volam znovu sort pulky pole ... nez dojdu k len(arr) <= 1
    sort(arr_l)
    sort(arr_r)
 
    # Slevam a slevam ...
    i,j,k = 0,0,0
    while i < len(arr_l) and j < len(arr_r):
        if arr_l[i].weight < arr_r[j].weight:
            arr[k] = arr_l[i]
            i += 1
        else:
            arr[k] = arr_r[j]
            j += 1
        k += 1
 
    # Co zbylo v levem poli ... to jde na radu prvni
    while i < len(arr_l):
        arr[k] = arr_l[i]
        i += 1
        k += 1
 
    # Co zbylo v pravem poli
    while j < len(arr_r):
        arr[k] = arr_r[j]
        j += 1
        k += 1

    return arr
