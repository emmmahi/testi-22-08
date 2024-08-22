
def hiit_training(x: int):
    """
    Syötteenä viikkojen määrä, tuloksena kasvun määrä prosentteina. 
    Harjoittelumuoto: kovatehoinen intrevalli- eli HIIT-harjoittelu 2-3 kertaa viikossa.
    Palauttaa kertoimen, jolla aina alkuperäinen arvo kerrotaan.
    """
    result = -0.021*x**2 + 1.102*x + 0.624
    result = result/100 +1
    return round(result,2)


# kestävyyden kaavat (3 eri tilannetta harjoitustyypin ja kertojen mukaan)
def low_impact_three_per_week(x: int):
    """
    Syötteenä viikkojen määrä, tuloksena kasvun määrä prosentteina. 
    Harjoittelumuoto: matalatehoinen ja pitkäkestoinen, 3 kertaa viikossa
    """
    result = - 0.0147813250060644* x**2 + 0.818631716067065*x + 0.644582934669111
    result = result/100 +1
    return round(result,2) 
    
def low_impact_two_per_week(x: int):
    """
    Syötteenä viikkojen määrä, tuloksena kasvun määrä prosentteina. 
    Harjoittelumuoto: matalatehoinen ja pitkäkestoinen, 2 kertaa viikossa
    """
    result = -0.00979537922395396*x**2 + 0.495346288599892*x - 0.111228306541958
    result = result/100 +1
    return round(result,2)


#  lihasmassan kaavat (2 eri tilannetta harjoitustyypin mukaan
def muscle_mass_blue_orig(x: int):
    """
    Hypertrofinen/lihasmassaa kasvattava
    x: viikkojen määrä
    return: kasvun määrä prosentteina
    Harjoittelumuoto: hypertrofinen??? kaksi kertaa viikossa
    """
    result =  4.61164958273993E-05 * x**4 - 0.00269325967488724 * x**3 + 0.0452109020879873 * x**2 - 0.0731953018389452 * x + 0.0268766716789236
    result = result/100 +1
    #result = result/10 +1  # pitääkö saatu prosenttilukema kertoa kymmenellä? vrt. lihasvoiman kaavion y-akseliin
    return round(result,2)
    
def muscle_mass_orange_orig(x: int):
    """
    Kestovoimaa kasvattava
    x: viikkojen määrä
    return: kasvun määrä prosentteina
    Harjoittelumuoto: kestovoima??? kaksi kertaa viikossa
    """
    result = -5.64590881412909E-05 * x**3 - 0.000483816707150222 * x**2 + 0.104065871416303 * x - 0.234270795159786
    result = result/100 +1
    return round(result,2)


# maksimivoiman kaavat (3 eri tilannetta harjoitustyypin mukaan
def muscle_strength_high_load_orig(x):
    result =  -7.37096740461747e-6 * x**3 - 0.000696853923096596 * x**2 + 0.0406473456690426*x - 0.00324872224317297 
    result = result +1
    return round(result,2)
    
def muscle_strength_medium_load_orig(x):
    """
    
    """
    result = -0.000589138923545647* x**2 + 0.027224973648555 * x + 0.000527739726876137
    result = result +1
    return round(result,2)

def muscle_strength_low_load_orig(x):
    result = -8.11769179414301e-6 * x**3 + 0.000113171645835558 * x**2 + 0.00958601333971586 * x + 0.000254386496098311
    result = result +1
    return round(result,2)
