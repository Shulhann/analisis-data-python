import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

main_data_df = pd.read_csv("main_data.csv")

st.title("Analisis Air Quality Dataset - Muhammad Shulhan")
st.write("Dashboard ini merupakan dashboard yang dibentuk untuk merangkum hasil analisis yang telah dilakukan terhadap Air Quality Dataset. Dataset ini yang digunakan pada analisis ini merupakan dataset yang diperoleh dari https://drive.google.com/file/d/1RhU3gJlkteaAQfyn9XOVAz7a5o1-etgr/view yang telah dilalui proses data wrangling oleh penulis.")

st.write("Ada 2 pertanyaan bisnis sederhana yang dianalis yaitu")
st.write("- Bagaimana hubungan antara tingkat polusi udara dan kondisi cuaca?")
st.write("Dataset mengandung sejumlah atribut yang merepresentasikan kondisi cuaca (TEMP, PRES, dsb) dan tingkat polusi (PM2.5 dan PM10). Atribut-atribut ini akan dianalisis lebih lanjut apakah mereka saling berhubungan atau tidak.")
st.write("- Apakah ada tren peningkatan atau penurunan kualitas udara yang signifikan selama musim tertentu?")
st.write("Dataset tersebut merupakan data kualitas udara yang diambil dari beberapa kota di negara cina. Mengingat cina merupakan negara dengan 4 musim, akan dicoba analisis bagaimana nilai kualitas udara (PM2.5 dan PM10) dalam setiap musim tersebut.")


# Correlation Matrix
st.title("Korelasi Polusi dan Kondisi Cuaca")
correlation_matrix = main_data_df[['PM2.5', 'PM10', 'TEMP', 'PRES', 'DEWP', 'WSPM']].corr()
subset_correlation_matrix = correlation_matrix.loc[['PM2.5', 'PM10'], ['TEMP', 'PRES', 'DEWP', 'WSPM']]

plt.figure(figsize=(10, 4))
sns.heatmap(subset_correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, linewidths=0.5)
plt.title('Heatmap of Correlation Matrix (Subset)', fontsize=16)
st.pyplot(plt)
st.write("Hubungan antara tingkat polusi dan kondisi cuaca tertanya paling besar dipengaruhi oleh titik embun, yaitu sekitar 0,37 untuk PM2.5 dan 0,29 untuk PM10. Angka tersebut bukan nilai korelasi yang cukup tinggi namun tidak bisa diabaikan pula untuk dicarikan korelasinya. Selanjutnya, pengaruh polusi dipengaruhi oleh kecepatan angin, tekanan dan suhu.")



# Box Plot untuk visualisasi PM2.5 dan PM10 berdasarkan musim
st.title("Box Plot dan Bar Plot PM2.5 dan PM10 Berdasarkan Musim")
def assign_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    elif month in [9, 10, 11]:
        return 'Autumn'
main_data_df['Season'] = main_data_df['month'].apply(assign_season)

def create_box_plots(df):
    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    sns.boxplot(x='Season', y='PM2.5', data=df)
    plt.title('Box Plot of PM2.5 berdasarkan musim')
    plt.ylabel('PM2.5')
    plt.xlabel('Musim')
    plt.subplot(1, 2, 2)
    sns.boxplot(x='Season', y='PM10', data=df)
    plt.title('Box Plot of PM10 berdasarkan musim')
    plt.ylabel('PM10')
    plt.xlabel('Musim')

    plt.tight_layout()
    st.pyplot(plt)

create_box_plots(main_data_df)


# Bar Plot untuk visualisasi PM2.5 dan PM10 berdasarkan musim
seasonal_means = main_data_df.groupby('Season')[['PM2.5', 'PM10']].mean().reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(x='Season', y='PM2.5', data=seasonal_means, color='blue', label='PM2.5')
sns.barplot(x='Season', y='PM10', data=seasonal_means, color='orange', label='PM10', alpha=0.6)

plt.title('Nilai Rata-rata PM2.5 dan PM10 per Musim')
plt.ylabel('Nilai Rata-rata')
plt.xlabel('Musim')
plt.legend()
plt.tight_layout()
st.pyplot(plt)

st.write("Perubahan kualitas udara pada tiap musimnya ternyata paling terlihat di musim winter. Winter memiliki perbedaan nilai yang signifikan dibanding dengan 3 musim lainnya. Selain itu, ANOVA test yang telah dilakukan juga menyatakan bahwa perbedaan PM2.5 dan PM10 yang terdapat antar musim cukup signifikan dan bukan karena kebetulan.")