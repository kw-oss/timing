import folium

# 위도
lat = 37.6194319

#경도
lon = 127.0572451

m = folium.Map(location=[lat, lon],
               zoom_start=17,
               width= 750,
               height=500
            )

m.save('map.html')