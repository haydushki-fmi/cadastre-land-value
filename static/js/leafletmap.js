// Initialize the map
// Set view to a default location (e.g., Sofia) and zoom level
const map = L.map('map').setView([42.6977, 23.3219], 15);

// Layer group for land properties
const landPropertiesLayer = L.layerGroup().addTo(map);

// Layer group for isolines
const isolays = L.layerGroup().addTo(map);

// ----------------------------------------------
// Tile layers
// ----------------------------------------------

// Define Base Tile Layers
const osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
});

const esriStreet = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community'
});

const esriTopo = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community'
});

const cartoPositron = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CartoDB</a>'
});

const cartoDarkMatter = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CartoDB</a>'
});

const stamen_terrain = L.tileLayer('https://tiles.stadiamaps.com/tiles/stamen_terrain/{z}/{x}/{y}{r}.png', {
    attribution: 'Map tiles by <a href="https://stamen.com">Stamen Design</a>, under <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>, data by <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
});

const openTopoMap = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
});

// Add default base layer
cartoPositron.addTo(map);

// Create an object for base layers
const baseLayers = {
    "OpenStreetMap": osmLayer,
    "ESRI Street": esriStreet,
    "ESRI Topo": esriTopo,
    "CartoDB Positron": cartoPositron,
    "CartoDB Dark Matter": cartoDarkMatter,
    "Stamen Terrain": stamen_terrain,
    "OpenTopoMap": openTopoMap,
};

// Add the layer control to the map
L.control.layers(baseLayers).addTo(map);

// ----------------------------------------------
// Helpers
// ----------------------------------------------
async function fetchLandPropertyValue(lat, lng) {
    try {
        const travelRange = parseInt(document.getElementById('travelRange').value, 10) * 60;
        const travelMode = document.getElementById('travelMode').value;
        const amenityType = document.getElementById('amenityType').value;

        const url = `/api/isoline-amenities?` +
            `lat=${lat}&` +
            `lon=${lng}&` +
            `travel_range=${travelRange}&` +
            `travel_mode=${travelMode}&` +
            `amenity_type=${amenityType}`;

        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching land property value:', error);
        throw error;
    }
}

async function displayIsoline(latitude, longitude, color) {
    try {
        const propertyValueData = await fetchLandPropertyValue(latitude, longitude);
        isolays.clearLayers();
        L.geoJSON(propertyValueData, {
            style: {
                fillColor: color,
                color: color,
                weight: 2,
                opacity: 0.5,
                fillOpacity: 0.2
            }
        }).addTo(isolays);

    } catch (error) {
        console.error('Error fetching or displaying clicked property value:', error);
    }
}

function handleClickOnFeature(feature, layer) {
    // Create popup
    if (feature.properties) {
        let cadnum = feature.properties.cadnum;
        let ogc_fid = feature.properties.ogc_fid;
        let proptype = feature.properties.proptype;

        let jsString = `Cadastral Number: ${cadnum}<br/>
                        OGC FID: ${ogc_fid}<br/>
                        Property Type: ${proptype}`;

        layer.bindPopup(jsString);
    }
    // Display centroid
    layer.on('click', async function (e) {
        if (feature.properties && feature.properties.centroid) {
            const centroid = JSON.parse(feature.properties.centroid);

            const longitude = centroid.coordinates[0];
            const latitude = centroid.coordinates[1];
            const color = 'red'

            try {
                displayIsoline(latitude, longitude, color)
            } catch (error) {
                console.error('Error fetching or displaying clicked property value:', error);
            }
        }
    })
}


const fetchData = async (admDiv) => {
    try {
        const response = await fetch('/api/land-properties?adm_div=' + admDiv);
        const geojsonData = await response.json();

        landPropertiesLayer
            .clearLayers();
        isolays.clearLayers();
        const geoJsonLayer = L.geoJSON(geojsonData, {
            onEachFeature: handleClickOnFeature
        }).addTo(landPropertiesLayer
        );

        // Focus to content
        map.fitBounds(geoJsonLayer.getBounds());

        map.on('click', async (e) => {
            const {lat, lng} = e.latlng; // Get latitude and longitude from the click event
            const color = 'green'

            try {
                displayIsoline(lat, lng, color)
            } catch (error) {
                console.error('Error fetching or displaying clicked property value:', error);
            }
        });

    } catch (error) {
        console.error('Error loading JSON data', error);
        alert('Error loading JSON data');
    }
};
