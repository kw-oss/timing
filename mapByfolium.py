import folium

# 위도
lat = 37.6194319

#경도
lon = 127.0572451

def makeMap():
    m = folium.Map(location=[lat, lon],
                zoom_start=17,
                width= 1024,
                height=1000
                )

    folium.Marker(
                [37.62006077967472, 127.05818653255353],
                popup ="설빙",
                #tooltip= "설빙2층"
                ).add_to(m)

    m.save('map.html')
    
makeMap()