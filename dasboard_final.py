import pandas as pd
import streamlit as st
import plotly.graph_objects as go



# Set page config
st.set_page_config(page_title = "DPMPTSP Dashboard", layout="wide")


# Header
t1, t2 = st.columns((0.07,1))

t1.image('images/dpmptsp_logo2.jpeg', width = 100)
t2.title('Dashboard Tipologi DPMPTSP Jakarta')
t2.markdown("**tel :** 1500164 / (021)1500164 **| website :** https://pelayanan.jakarta.go.id/ **")


with st.spinner('Updating Report .... ') : 

    # Metrics setting and rendering

    sp_izin_df = pd.read_excel('sp_izin.xlsx',sheet_name = 'service_point')
    sp = st.selectbox('Choose Service Point', sp_izin_df, help = 'Filter report to show only one service point of penanaman modal')

    # label logic : determine if kecamatan, kelurahan or kota
    if sp.startswith('Kantor Camat') : 
        level = 'kecamatan' 
    elif sp.startswith('Kantor Lurah') : 
        level = 'kelurahan'
    else :
        level = 'kota / kabupaten'

    # Data total izin berdasarkan status
    tot_status_df = pd.read_excel('sp_izin.xlsx', sheet_name = 'tot_status')
    total_izin = tot_status_df[tot_status_df['service_point']==sp]['total_diajukan']
    average_izin = tot_status_df[tot_status_df['service_point']==sp]['average_status']
    selesai_diproses = tot_status_df[tot_status_df['service_point']==sp]['total_selesai']
    ditolak_dibatalkan = tot_status_df[tot_status_df['service_point']==sp]['total_ditolak_dibatalkan']
    masih_diproses = tot_status_df[tot_status_df['service_point']==sp]['total_proses']

    # percentage
    selesai_perc = selesai_diproses / total_izin * 100
    ditolak_perc = ditolak_dibatalkan / total_izin * 100
    masih_perc = masih_diproses / total_izin * 100

    # total_izin = 597
    # average_izin = 712.1
    # selesai_diproses = 433
    # ditolak_dibatalkan = 163
    # masih_diproses = 1


    # Define layout using column in streamlit
    m1, m2, m3  = st.columns((1,1,1))
    m1.write('')
    m2.metric(label = "Total Izin yang diajukan", value = total_izin)
    m3.write(f"**In Average**")
    m3.write(f"{average_izin.iloc[0]} jumlah izin per {level.capitalize()}")
    m1.write('')
    m1.write('')

    # Layouting status lainnya yang belum masuk
    c3, c4, c5 = st.columns(3)
    c3.metric(label = "Selesai diproses", value = selesai_diproses, delta=f"{round(selesai_perc.iloc[0], 1)}%")
    c4.metric(label = "Masih diproses", value = masih_diproses, delta=f"{round(masih_perc.iloc[0], 1)}%")
    c5.metric(label = "Ditolak & dibatalkan", value = ditolak_dibatalkan, delta=f"{round(ditolak_perc.iloc[0], 1)}%")

    st.markdown("---")

    # Layout untuk grafik piechart dan klasifikasi izin
    g1,g2 = st.columns((1,1))

    pcdf = pd.read_excel('sp_izin.xlsx', sheet_name = 'tot_bidang2')
    pcdf = pcdf[pcdf['service_point']==sp]

    # Define base colors for pie chart that will be used for bar chart too
    base_colors = {
        'Pelayanan Administrasi': '#FF0000',  # Red
        'Kesehatan': '#0000FF',  # Blue  
        'Pekerjaan Umum Dan Penataan Ruang': '#008000', # Green
        'Kesatuan Bangsa Dan Politik Dalam Negeri': '#FFD700', # Gold
        'Lingkungan Hidup': '#800080', # Purple
        'Perdagangan': '#FFA500', # Orange
        'Pendidikan': '#00FFFF', # Cyan
        'Perhubungan': '#FF00FF', # Magenta
        'Sosial': '#008080', # Teal
        'Tenaga Kerja': '#800000', # Maroon
        'Pariwisata': '#000080', # Navy
        'Pertanian': '#808000', # Olive
        'Kelautan Dan Perikanan': '#FF69B4', # Hot Pink
        'Kehutanan': '#4B0082', # Indigo
        'Esdm': '#DC143C', # Crimson
        'Kepemudaan dan Keolahragaan': '#9400D3', # Dark Violet
        'Ketenteraman, ketertiban Umum dan Pelindungan Masyarakat': '#2F4F4F', # Dark Slate Gray
        'Pertanahan Yang Menjadi Kewenangan Daerah': '#8B4513', # Saddle Brown
        'Perumahan Rakyat Dan Kawasan Permukiman': '#4682B4' # Steel Blue
    }

    # Create color list based on pcdf bidang order
    pie_colors = [base_colors[bidang] for bidang in pcdf['bidang_recode']]

    fig1 = go.Figure(data = [go.Pie(labels=pcdf['bidang_recode'], 
                                   values=pcdf['total_diajukan'], 
                                   hole=.3,
                                   marker=dict(colors=pie_colors))])
    
    fig1.update_layout(title_text = "Kategori Bidang yang Dominan", title_x = 0, margin = dict(l=0, r=10, b=10))

    cidf = pd.read_excel('sp_izin.xlsx', sheet_name = 'cluster')
    cidf = cidf[cidf['service_point']==sp]

    if not cidf.empty : 
        cluster_value = cidf['Cluster'].iloc[0]

        if cluster_value == 0 : 
            lvl_cluster = 'didominasi di Bidang **Pelayanan umum dan penataan ruang**, Bidang **Kesehatan** dan Bidang **Pelayanan Administrasi**'
        elif cluster_value == 1 :  
            lvl_cluster = 'didominasi hanya di Bidang **Pelayanan Administrasi**'
        elif cluster_value == 3 :  
            lvl_cluster = 'didominasi utama di Bidang **Kesehatan**'
        elif cluster_value == 4 :  
            lvl_cluster = 'menonjol pada bidang kesehatan yang lebih mendominasi dibandingkan cluster3'
        elif cluster_value == 6 :  
            lvl_cluster = 'didominasi utama di Bidang **Pelayanan Administrasi** dan bidang Kesbangpol'
        elif cluster_value == 7 :  
            lvl_cluster = 'cukup menyebar rata seperti Kesbangpol, Kesehatan, Lingkungan Hidup'
        else :
            lvl_cluster = 'tidak ditemukan cluster ini'

        g1.markdown(f"## <h2 style='color: blue;'> Cluster {cluster_value}</h2>", unsafe_allow_html = True)
        g1.markdown(f"### Cluster ini {lvl_cluster}")
        g2.plotly_chart(fig1, use_container_width = True)

    st.markdown("---")

    # terkait g3 utk pemohon, g4 utk yang dibawah g5 utk yang terakhir
    # pdf merupakan status pemohon apakah perushaaan atau individu
    g3 = st.columns(1)[0]
    pdf = pd.read_excel('sp_izin.xlsx', sheet_name = 'pemohon')
    pdf = pdf[pdf['service_point']==sp]

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        y = pdf['service_point']
        , x=pdf['perorangan']
        , name = 'Perorangan'
        , orientation = 'h'
        , text = pdf['perorangan']
        , textposition = 'auto'
    ))
    fig2.add_trace(go.Bar(
        y = pdf['service_point']
        , x=pdf['perusahaan']
        , name = 'Perusahaan'
        , orientation = 'h'
        , text = pdf['perusahaan']
        , textposition = 'auto'
    ))

    fig2.update_layout(
        barmode = 'stack'
        , title = {
            'text'      : 'Tipe Pemohon berdasarkan izin : Perorangan vs Perusahaan'
            , 'x'         : 0.5
            , 'xanchor'   : 'center'
            , 'yanchor'   : 'top'
        }
        , height = 300
        , xaxis = {
            'showticklabels' : False
        }
    )

    g3.plotly_chart(fig2, use_container_width = True)

    g4 = st.columns(1)

    g5 = st.columns(1)

    
    st.markdown("---")
    st.markdown("## Distribusi Bidang Perizinan")

    # Metrics setting and rendering
    wdf = pd.read_excel('sp_izin.xlsx', sheet_name = 'wilayah_derivative')
    wdf = wdf[wdf['service_point']==sp]


    # Tentukan kolom `sub_region` berdasarkan level wilayah
    if level == 'kecamatan':
        sub_region_col = 'kelurahan'
    elif level == 'kota':
        sub_region_col = 'kecamatan'
    else:
        sub_region_col = 'kota'
    
# Baca data wilayah
wdf = pd.read_excel('sp_izin.xlsx', sheet_name='wilayah_derivative')
selected_row = wdf[wdf['service_point'] == sp].iloc[0]
level_wilayah = selected_row['Level_wilayah']

# Daftar kolom bidang
bidang_cols = ['Esdm', 'Kehutanan', 'Kelautan Dan Perikanan', 'Kepemudaan dan Keolahragaan',
               'Kesatuan Bangsa Dan Politik Dalam Negeri', 'Kesehatan', 
               'Ketenteraman, ketertiban Umum dan Pelindungan Masyarakat',
               'Lingkungan Hidup', 'Pariwisata', 'Pekerjaan Umum Dan Penataan Ruang',
               'Pelayanan Administrasi', 'Pendidikan', 'Perdagangan', 'Perhubungan',
               'Pertanahan Yang Menjadi Kewenangan Daerah', 'Pertanian',
               'Perumahan Rakyat Dan Kawasan Permukiman', 'Sosial', 'Tenaga Kerja']

# Fungsi helper untuk mengurutkan bidang
def sort_bidang_by_total(data, bidang_cols):
    bidang_totals = {bidang: data[bidang].sum() for bidang in bidang_cols}
    sorted_bidang = sorted(bidang_totals.items(), key=lambda x: x[1], reverse=True)
    return [b[0] for b in sorted_bidang if b[1] > 0]

if level_wilayah == 'Kel':
    st.info("Data sama dengan Pie Chart diatas")

elif level_wilayah == 'Dinas':
    # Data untuk level dinas
    dinas = selected_row['dinas']
    dinas_data = wdf[wdf['dinas'] == dinas]
    
    # Agregasi data per kota
    agg_data = dinas_data.groupby('kota')[bidang_cols].sum().reset_index()
    agg_data['total'] = agg_data[bidang_cols].sum(axis=1)
    
    # Hitung total untuk setiap bidang
    bidang_totals = {bidang: agg_data[bidang].sum() for bidang in bidang_cols}
    sorted_bidang = sorted(bidang_totals.items(), key=lambda x: x[1], reverse=True)
    active_bidang = [b[0] for b in sorted_bidang if b[1] > 0]
    
    fig = go.Figure()
    for idx, bidang in enumerate(active_bidang):
        fig.add_trace(go.Bar(
            y=agg_data['kota'],
            x=agg_data[bidang] / agg_data['total'] * 100,
            name=bidang,
            orientation='h',
            text=[f'{x:.1f}% ({int(y)})' for x, y in zip(agg_data[bidang] / agg_data['total'] * 100, agg_data[bidang])],
            textposition='inside',
            marker_color=base_colors[bidang],
            legendgroup=bidang,
            showlegend=True
        ))
    title_text = f'Distribusi Bidang Perizinan untuk Dinas {dinas}'

elif level_wilayah == 'Kota':
    # Data untuk level kota
    kota = selected_row['kota']
    kota_data = wdf[wdf['kota'] == kota]
    agg_data = kota_data.groupby('kecamatan')[bidang_cols].sum().reset_index()
    agg_data['total'] = agg_data[bidang_cols].sum(axis=1)
    
    bidang_totals = {bidang: agg_data[bidang].sum() for bidang in bidang_cols}
    sorted_bidang = sorted(bidang_totals.items(), key=lambda x: x[1], reverse=True)
    active_bidang = [b[0] for b in sorted_bidang if b[1] > 0]
    
    fig = go.Figure()
    for idx, bidang in enumerate(active_bidang):
        fig.add_trace(go.Bar(
            y=agg_data['kecamatan'],
            x=agg_data[bidang] / agg_data['total'] * 100,
            name=bidang,
            orientation='h',
            text=[f'{x:.1f}% ({int(y)})' for x, y in zip(agg_data[bidang] / agg_data['total'] * 100, agg_data[bidang])],
            textposition='inside',
            marker_color=base_colors[bidang],
            legendgroup=bidang,
            showlegend=True
        ))
    title_text = f'Distribusi Bidang Perizinan di Kota {kota}'

elif level_wilayah == 'Kec':
    # Data untuk level kecamatan
    kecamatan = selected_row['kecamatan']
    kec_data = wdf[wdf['kecamatan'] == kecamatan]
    kec_data['total'] = kec_data[bidang_cols].sum(axis=1)
    
    # Tambahkan informasi cluster
    cidf = pd.read_excel('sp_izin.xlsx', sheet_name='cluster')
    kec_data = kec_data.merge(cidf[['service_point', 'Cluster']], on='service_point', how='left')
    
    bidang_totals = {bidang: kec_data[bidang].sum() for bidang in bidang_cols}
    sorted_bidang = sorted(bidang_totals.items(), key=lambda x: x[1], reverse=True)
    active_bidang = [b[0] for b in sorted_bidang if b[1] > 0]
    
    fig = go.Figure()
    for idx, bidang in enumerate(active_bidang):
        values = kec_data[bidang].fillna(0)
        percentages = (values / kec_data['total'] * 100).fillna(0)
        
        text_labels = [f'{x:.1f}% ({int(y)})' if not pd.isna(y) else '0% (0)' 
                      for x, y in zip(percentages, values)]
        
        fig.add_trace(go.Bar(
            y=kec_data['service_point'],
            x=percentages,
            name=bidang,
            orientation='h',
            text=text_labels,
            textposition='inside',
            marker_color=base_colors[bidang],
            legendgroup=bidang,
            showlegend=True
        ))

    # Tambahkan anotasi cluster
    for idx, row in kec_data.iterrows():
        fig.add_annotation(
            x=100,
            y=row['service_point'],
            text=f"Cluster {int(row['Cluster'])}",
            xanchor='left',
            yanchor='middle',
            showarrow=False,
            xshift=10,
            font=dict(size=12)
        )
    
    title_text = f'Distribusi Bidang Perizinan di Kecamatan {kecamatan}'

if level_wilayah != 'Kel':
    # Pengaturan layout yang sama untuk semua level
    fig.update_layout(
        barmode='stack',
        title=title_text,
        xaxis_title='Persentase (%)',
        height=800,
        bargap=0.2,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='rgba(0, 0, 0, 0.3)',
            borderwidth=1,
            itemsizing='constant',
            itemwidth=40
        ),
        margin=dict(b=150),
        uniformtext=dict(mode='hide', minsize=8)
    )
    
    # Tambahkan button untuk toggle legend
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=list([
                    dict(
                        args=[{"visible": [True] * len(fig.data)}],
                        label="Show All",
                        method="restyle"
                    ),
                    dict(
                        args=[{"visible": [False] * len(fig.data)}],
                        label="Hide All",
                        method="restyle"
                    )
                ]),
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.11,
                xanchor="left",
                y=1.1,
                yanchor="top"
            ),
        ]
    )

    st.plotly_chart(fig, use_container_width=True)


with st.expander("## Distribusi Total Perizinan di Sub-wilayah", expanded=False):
    # Initialize sub_data as None
    sub_data = None

    if level_wilayah == 'Kota':
        # For Kota level, show Kelurahan data
        kecamatan = wdf[wdf['kota'] == selected_row['kota']]['kecamatan'].unique()
        sub_data = wdf[wdf['kecamatan'].isin(kecamatan)].copy()
        group_col = 'kelurahan'
        title_text = f'Distribusi Total Perizinan per Kelurahan di {selected_row["kota"]}'
    elif level_wilayah == 'Dinas':
        # For DPMPTSP DKI JAKARTA, show aggregated Kecamatan data
        sub_data = wdf.copy()
        group_col = 'kecamatan'
        title_text = 'Distribusi Total Perizinan per Kecamatan di DKI Jakarta'

    if sub_data is not None:
        # Calculate total for all bidang_cols
        sub_data['total_izin'] = sub_data[bidang_cols].sum(axis=1)
        
        # Aggregate data by sub-region
        agg_sub_data = sub_data.groupby(group_col)['total_izin'].sum().reset_index()
        
        # Sort by total
        agg_sub_data = agg_sub_data.sort_values('total_izin', ascending=False)
        
        # Rename columns for display
        agg_sub_data.columns = ['Wilayah', 'Total Perizinan']
        
        # Format the Total Perizinan column with thousands separator
        agg_sub_data['Total Perizinan'] = agg_sub_data['Total Perizinan'].apply(lambda x: f"{int(x):,}")
        
        # Display title
        st.markdown(f"### {title_text}")
        
        # Display table with styling
        st.dataframe(
            agg_sub_data,
            height=400,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Wilayah": st.column_config.TextColumn(
                    "Wilayah",
                    width="medium",
                ),
                "Total Perizinan": st.column_config.TextColumn(
                    "Total Perizinan",
                    width="medium",
                )
            },
            column_order=["Wilayah", "Total Perizinan"]
        )

        # ... existing code ...

# Add new section for detailed permits
# Add new section for detailed permits
# ... existing code ...

# Add new section for detailed permits
with st.expander("## Detail Izin berdasarkan Bidang", expanded=False):
    try:
        # Read the data
        izin_detail_df = pd.read_excel('sp_izin.xlsx', sheet_name='nama_izin')
        
        # Filter data based on selected service point
        filtered_izin = izin_detail_df[izin_detail_df['service_point'] == sp].copy()
        
        if not filtered_izin.empty:
            # Ensure columns exist and handle missing data
            required_columns = ['service_point', 'bidang_recode', 'nama_izin', 'total_selesai']
            if all(col in filtered_izin.columns for col in required_columns):
                # Group by bidang and nama_izin
                grouped_izin = (filtered_izin
                    .groupby(['bidang_recode', 'nama_izin'])
                    .agg({'total_selesai': 'sum'})
                    .reset_index()
                    .sort_values('total_selesai', ascending=False)
                )
                
                # Display the table
                st.markdown(f"### Detail Izin di {sp}")
                st.dataframe(
                    grouped_izin,
                    height=400,
                    hide_index=True,
                    use_container_width=True,
                    column_config={
                        "bidang_recode": st.column_config.TextColumn(
                            "Bidang",
                            width="medium",
                        ),
                        "nama_izin": st.column_config.TextColumn(
                            "Nama Izin",
                            width="large",
                        ),
                        "total_selesai": st.column_config.NumberColumn(
                            "Total Izin Selesai",
                            width="small",
                            format="%d"
                        )
                    }
                )
                
                # Display summary statistics
                st.markdown("### Ringkasan")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Jenis Izin", len(grouped_izin['nama_izin'].unique()))
                with col2:
                    st.metric("Total Bidang", len(grouped_izin['bidang_recode'].unique()))
                with col3:
                    st.metric("Total Izin Selesai", int(grouped_izin['total_selesai'].sum()))
            else:
                st.error("Format data tidak sesuai. Mohon periksa kolom yang diperlukan.")
        else:
            st.info("Tidak ada data izin untuk service point ini")
            
    except Exception as e:
        st.error(f"Terjadi kesalahan: {str(e)}")