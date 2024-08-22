
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import kaavat 
import kehonkoostumus_codes as keho

st.set_page_config(
    page_title="CEMIS-HYVIS-testing",
    page_icon="muscle",
    layout="wide",
    initial_sidebar_state="auto"
)

# Lisää mukautettu CSS taustavärin muuttamiseksi, lista värikoodeista https://htmlcolorcodes.com/
def add_background_color():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #aed6f1;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Kutsu funktio muuttaaksesi taustavärin
add_background_color()

st.title("Rivin valinta taulukosta")
st.write("Valitse haluttu rivi klikkaamalla rivin vasenta laitaa.")
st.write("Voit järjestää taulukkoa uudelleen valitsemalla halutun ominaisuuden.")
@st.cache_data   #decorator to cache the the dataset loading for better performance
def get_dataset():
    #data = pd.read_csv('data/07-24-data.csv')
    data = pd.read_csv('data/08-19-streamlit-data.csv')
    return data

data=get_dataset()

event = st.dataframe(
    data, 
    use_container_width=True, 
    hide_index=True,  
    on_select='rerun', 
    selection_mode="single-row"
)

st.divider()  ###########################################################################

st.header("Valitun rivin tiedot", divider='grey')

person = event.selection.rows  #on muotoa [numero : numero] eli dictionary like objectin osanen
#filtered_df = data.iloc[people]

#st.write("person[0] = " ,person[0])  #tarkistusprintti
selected_row = None
# Check if a row is selected
if person:
    selected_row_index = person[0]
    selected_row = data.iloc[selected_row_index]

    # Layout: two columns
    col1, col2 , col3 = st.columns([0.2,0.4,0.4])

    # Column 1: Display the row's details
    with col1:
        st.write(selected_row)


    with col2:
        width= 0.1
        fig, axs = plt.subplots(figsize=(8,4))

        non_muscle_ffm = selected_row['Rasvaton massa (kg)'] - selected_row['Lihasmassa (kg)']
        axs.bar(0, selected_row['Rasvamassa (kg)'], color='lightpink', width=width, label=f'Rasvamassa {selected_row["Rasvamassa (kg)"]} kg')
        axs.bar(0, non_muscle_ffm, bottom=selected_row['Rasvamassa (kg)'], color='maroon', width=width, label=f'Rasvaton massa {selected_row["Rasvaton massa (kg)"]} kg (pl. lihasmassa)')
        axs.bar(0, selected_row['Lihasmassa (kg)'], bottom=selected_row['Rasvamassa (kg)'] + non_muscle_ffm, color='royalblue', width=width, label=f'Lihasmassa {selected_row["Lihasmassa (kg)"]} kg')
        axs.bar(1, selected_row['Paino (kg)'], color='tan', width=width, label=f'Kokonaispaino {selected_row["Paino (kg)"]} kg')
        axs.set_xticks([])
        axs.set_ylabel('Massa (kg)')
        axs.legend()


        st.pyplot(fig)


    with col3:
        #st.write("*Tähän jokin muu visuaalinen esitys, mikä tärkeää vielä nostaa esiin valitusta henkilöstä?*")
        #st.bar_chart(selected_row[['Lihasmassa (kg)', 'Rasvaton massa (kg)', 'Rasvamassa (kg)']], y_label='Kilot',
        #             horizontal=True, color="#ffaa00")
        fig, axs = plt.subplots(figsize=(8,4))
        axs.set_ylim(bottom=6, top=41)
        axs.axhline(y=selected_row['BMI'], color='g', linestyle='--', label='BMI')
        axs.axhline(y=selected_row['Rasvaprosentti'], color='r', linestyle='--', label='Rasvaprosentti')
        axs.legend()  # Jos haluat näyttää legendan
        st.pyplot(fig)

        


st.divider() ################################################################################

st.write("# Valitse energiatasapainon määrä sekä harjoitusmuodot")

colu1, colu2, colu3 = st.columns(3)
with colu1:
    apuviesti_etp='''Kalorimäärää käytetään rasvamassan ja painon muutoksen laskuun 
    (9kcal = 1g rasvaa). Energiataspaino päivitetään neljän viikon välien painon muutoksen takia
     (vaikuttaa henkilön vuorokautiseen aineenvaihduntaan).'''

    st.write("**Kirjoita haluttu energiatasapainon määrä viikossa kaloreina**")

    etp = st.number_input("Energiatp/vko", 
                          min_value=-7000, 
                          max_value=7000, 
                          value=0, 
                          help=apuviesti_etp)


    st.write("Valitsit energiatasapainoksi viikossa", etp)

with colu2:
    st.write("**Valitse kestävyysharjoitusmuoto**")
    apuviesti_kestavyys = '''
    Sovitekäyrien kaavat on otettu excel-taulukoista. Kaavan antama PROSENTTILUKEMA jaetaan 100:lla ja siihen lisätään yksi, 
    jotta saadaan prosenttimäärä desimaalikertoimeksi alkuperäiselle arvolle.'''
    #option1 = st.selectbox("Kestävyysharjoittelu" ("matalatehoinen", "hiit"))
    option_kestavyys  = st.selectbox(
        "Kestävyysharjoittelun muoto",
        ("Hiit", "Matala 2x", "Matala 3x"),
        index=None,
        placeholder="Valitse tästä",
        help=apuviesti_kestavyys
    )
    st.write("Valintasi:", option_kestavyys)


with colu3:
    st.write("**Valitse lihasvoimaharjoittelumuoto**")
    apuviesti_voima = '''
    Sovitekäyrien kaavat on otettu excel-taulukoista.
    '''
    option_lihasvoima = st.selectbox(
        "Lihasvoimaharjoittelumuoto",
        ("Low load", "Medium load", "High load"),
        index=None,
        placeholder="Valitse tästä",
        help=apuviesti_voima
    )
    st.write("Valintasi:", option_lihasvoima)
st.divider()

###### pitäisikö nämä laittaa omaksi koodikseen johonkin moduuliin??? ########
###### luodaan listat toimintakykyarvoista plottauksia varten ##########
viikot = [*range(1, 27, 1)]
if selected_row is not None:
    list_kestavyys = [selected_row['vo2max']]

    if option_kestavyys is not None:
        if option_kestavyys=="Hiit":
            for i in viikot:
                uusi_vo2max = kaavat.hiit_training(i) * selected_row['vo2max']
                list_kestavyys.append(round(uusi_vo2max,1))
            st.write(option_kestavyys)
        if option_kestavyys=="Matala 2x":
            st.write(option_kestavyys)
            for i in viikot:
                uusi_vo2max = kaavat.low_impact_two_per_week(i) * selected_row['vo2max']
                list_kestavyys.append(round(uusi_vo2max,1))
        if option_kestavyys=="Matala 3x":
            st.write(option_kestavyys)
            for i in viikot:
                uusi_vo2max = kaavat.low_impact_three_per_week(i) * selected_row['vo2max']
                list_kestavyys.append(round(uusi_vo2max))
    else:
        list_kestavyys = list_kestavyys* (len(viikot) +1) #plottausta varten arvot viikota 0 viikolla 26


###### EI TOIMI ##########
    list_lihasvoima = [selected_row['Maksimivoima (kg)']]
    if option_lihasvoima is not None:
        if option_lihasvoima == "Low load":
            for i in viikot:
                uusi_toistomaara = kaavat.muscle_strength_low_load_orig(i)* selected_row['Maksimivoima (kg)']
                list_lihasvoima.append(round(uusi_toistomaara))
        elif option_lihasvoima == "Medium load":
            for i in viikot:
                uusi_toistomaara = kaavat.muscle_strength_medium_load_orig(i) * selected_row['Maksimivoima (kg)']
                list_lihasvoima.append(round(uusi_toistomaara))
                #st.write("toistot medium", uusi_toistomaara)           
        elif option_lihasvoima == "High load":
            for i in viikot:
                uusi_toistomaara = kaavat.muscle_strength_high_load_orig(i) * selected_row['Maksimivoima (kg)']
                list_lihasvoima.append(round(uusi_toistomaara))

    else:
        list_lihasvoima = list_lihasvoima* (len(viikot)+1)
    #st.write(list(list_lihasvoima))

##### suoritetaan laskennat uusiksi arvoiksi: paino, vuorokausiaineenvaihdunta, bmi
#list_paino, list_bmi, list_rasvaprosentti, list_lihasmassa, list_rasvamassa, list_rasvatonmassa = keho.kehonkoostumus(selected_row, -900)

#
#
    list_paino, list_bmi, list_rasvaprosentti, list_lihasmassa, list_rasvamassa, list_rasvatonmassa, list_etp= keho.kehonkoostumus(selected_row, etp, lihasvoimaharjoitusmuoto=option_lihasvoima)

    data_list = [('Paino (kg)', list_paino, 'Kilogrammat'),
                ('BMI', list_bmi, 'kg/m²'),
                ('Rasvaprosentti', list_rasvaprosentti, '%'),
                ('Lihasmassa (kg)', list_lihasmassa, 'Kilogrammat'),
                ('Hapenottokyky (ml/kg/min)', list_kestavyys, 'ml/kg/min'),
                ('Maksimivoima (kg)', list_lihasvoima, 'Kilogrammat'),
                ('Rasvaton massa', list_rasvatonmassa, 'Kilogrammat'),
                ('Rasvamassa', list_rasvamassa, 'Kilogrammat'),
                ('Energiatasapaino', list_etp, 'kcal')]

    #x_list = ['Kilogrammat', 'kg/m²', '%', 'Kilogrammat', 'ml/kg/min', 'Toistot/min', 'Kilogrammat', 'Kilogrammat']


    if etp is not None:
        fig, axes = plt.subplots(3,3, figsize=(18, 8))

        for ax, (title, data_list, x_list) in zip(axes.flat, data_list):
            ax.plot(data_list, linestyle='--')
            ax.set_title(title)
            if data_list==list_etp:
                ax.set_ylim(min(data_list) -100, max(data_list) +100)
            else:
                ax.set_ylim(min(data_list) -5, max(data_list) +5)
            ax.set_xlim(0, len(data_list)-1)
            if data_list==list_etp:
                ax.set_xlabel('kuukaudet')
            else:
                ax.set_xlabel('viikot')
            ax.set_ylabel(x_list)
            ax.grid(True)
            ax.set_xticks(range(0, len(data_list), 2))
            ax.tick_params(axis='x', rotation=45)

        # Merkitään jokaisen listan ensimmäinen ja viimeinen arvo
            ax.plot(0, data_list[0], 'ro')  # Merkitse ensimmäinen arvo punaisella
            ax.plot(len(data_list)-1, data_list[-1], 'go')  # Merkitse viimeinen arvo vihreällä
        #    data=tulokset[i]
        # Lisää arvon annotaatiot   README.md
            ax.annotate(f'{data_list[0]}', (0, data_list[0]), textcoords="offset points", xytext=(0,10), ha='center', color='red')
            ax.annotate(f'{data_list[-1]}', (len(data_list)-1, data_list[-1]), textcoords="offset points", xytext=(0,10), ha='center', color='green')
        # Lisätään ensimmäinen ja viimeinen arvo tekstiin
            #ax.text(0, list[0], f'{list[0]}', ha='right', va='bottom', fontsize=10)
            #ax.text(len(list) - 1, list[-1], f'{list[-1]}', ha='right', va='bottom', fontsize=10)
        # Lasketaan erotus ja lisätään teksti
            difference = (data_list[-1] - data_list[0]).round(1)
            ax.text(len(data_list) // 2, (min(data_list) + max(data_list)) // 2, f'muutos = {difference}', ha='center', va='center', fontsize=12, color='red')

        plt.tight_layout()
        st.pyplot(fig)

st.divider()
st.title("Generoidun datan piirteiden riippuvuudet")
st.write("**HUOM!** Datan generoinnissa on vielä muutoksia tulossa sykkeeseen testin lopussa sekä lihasvoiman generointiin. Muutokset päivitetään alla olevaan kuvaan.")

st.image(image='./images/data-gen-kaavio2.drawio.png')

