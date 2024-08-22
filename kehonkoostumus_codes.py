import kaavat as k



# uuden vuorokausikulutusarvon laskenta painon muutoksen myötä
def uusi_vrk_pav(sukupuoli, paino, pituus, ikä):
    if sukupuoli.lower() == 'mies':
        pav = 88.362 + (13.397 * paino) + (4.799 * pituus) - (5.677 * ikä)
        vrk_pav = pav + (pav * 0.1) + (pav * 0.15) 
        return vrk_pav
    else:
        pav = 447.593 + (9.247 * paino) + (3.098 * pituus) - (4.330 * ikä)
        vrk_pav = pav + (pav * 0.1) + (pav * 0.15) 
        return vrk_pav



def bmi_laskenta(paino, pituus):
    return round((paino / ((pituus / 100) ** 2)),1)



# energiatasapaino kaloreiksi
def kk_muutos(energiatasapaino):
    grams = energiatasapaino / 9  # materiaaleissa maininta 9 kcal = 1 g rasvaa
    return grams * 4 / 1000




def kehonkoostumus(row, energiatp=0, lihasvoimaharjoitusmuoto = None):
    sukupuoli = row['Sukupuoli']
    ika = row['Ikä']
    pituus = row['Pituus (cm)']
    paino = row['Paino (kg)']
    bmi = row['BMI']
    pav_vrk = row['Vuorokausiaineenvaihdunta']
    rasvaprosentti = row['Rasvaprosentti']
    rasvamassa = row['Rasvamassa (kg)']
    rasvatonmassa = row['Rasvaton massa (kg)']
    lihasmassa = row['Lihasmassa (kg)']
    energiatp=energiatp

    list_paino = [paino]
    list_bmi = [bmi]
    list_rasvaprosentti = [rasvaprosentti]
    list_lihasmassa = [lihasmassa]
    list_rasvatonmassa = [rasvatonmassa]
    list_rasvamassa = [rasvamassa]
    list_vuorokausikulutus = [pav_vrk]
    list_etp = [energiatp]

    viikot = [*range(1, 27, 1)] 
    
    # selvitetään ensin lihasmassan arvot suoraan kaavalla, jos ei harjoittelua, alkuarvo monistetaan
    if lihasvoimaharjoitusmuoto is None:
        list_lihasmassa = list_lihasmassa*(len(viikot)+1)
        #print(len(list_lihasmassa))
        
    for i, num in enumerate(viikot):
        #print(i,num)
        if lihasvoimaharjoitusmuoto=="Medium load":
            uusi_lihasmassa = list_lihasmassa[0]*k.muscle_mass_blue_orig(num)
            list_lihasmassa.append(round(uusi_lihasmassa,1))
            erotus_lihasmassa = (list_lihasmassa[i+1]-list_lihasmassa[i]).round(2)
        elif lihasvoimaharjoitusmuoto=="Low load" or lihasvoimaharjoitusmuoto=="High load":
            uusi_lihasmassa = list_lihasmassa[0]*k.muscle_mass_orange_orig(num)
            list_lihasmassa.append(round(uusi_lihasmassa,1))
            erotus_lihasmassa = (list_lihasmassa[i+1]-list_lihasmassa[i]).round(2)       
        else:
            erotus_lihasmassa = 0
        uusi_rasvatonmassa = list_rasvatonmassa[i] + erotus_lihasmassa
        list_rasvatonmassa.append(round(uusi_rasvatonmassa,1))
        paino_muistiin = list_paino[i] + erotus_lihasmassa
        rasvan_muutos = energiatp /9 /1000
        #print('rasvan muutos', rasvan_muutos)
        paino_muistiin+= rasvan_muutos
        list_paino.append(round(paino_muistiin,1))
        uusi_bmi = bmi_laskenta(paino_muistiin, pituus)
        list_bmi.append(round(uusi_bmi,1))
        uusi_rasvamassa = list_rasvamassa[i]+rasvan_muutos
        list_rasvamassa.append(round(uusi_rasvamassa,1))
        uusi_rasvaprosentti = (uusi_rasvamassa / paino_muistiin *100).round(1)
        list_rasvaprosentti.append(uusi_rasvaprosentti)
       

        if (i+1)%4==0:    ## lasketaan uusi energiatasapaino 4 viikon välein
            #print(f'Paino: {paino_muistiin.round(2)}, BMI: {uusi_bmi}, Rasvamassa: {uusi_rasvamassa.round(2)}, Rasvaprosentti: {uusi_rasvaprosentti.round(1)}, Lihasmassa: {list_lihasmassa[i-1]}, kulutus: {list_vuorokausikulutus}')
            uusi_vrkpav = uusi_vrk_pav(sukupuoli, paino_muistiin, pituus, ika)
            list_vuorokausikulutus.append(round(uusi_vrkpav))
            #print('vanha', pav_vrk.round())
            #print('uusi',uusi_vrkpav.round())
            pav_erotus = pav_vrk - uusi_vrkpav
            #print('pav erotus', pav_erotus.round())
            pav_vrk = uusi_vrkpav
            energiatp= (energiatp + pav_erotus).astype(int)  #meneekö lodiikka oikein!!?!??!!?!!
            list_etp.append(energiatp)
            #print('energiatp', energiatp)

    #print('Painot', list_paino)
    #print('BMI', list_bmi)
    #print('Rasvaprosentit', list_rasvaprosentti)
    #print('Rasvamassa', list_rasvamassa)
    #print('Rasvaton massa', list_rasvatonmassa)
    #print('Lihasmassa:', list_lihasmassa)
    #print(len(list_bmi))
    return list_paino, list_bmi, list_rasvaprosentti, list_lihasmassa, list_rasvamassa, list_rasvatonmassa, list_etp            