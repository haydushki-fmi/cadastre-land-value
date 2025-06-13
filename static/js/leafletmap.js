// Initialize the map
// Set view to a default location (e.g., Sofia) and zoom level
const map = L.map('map').setView([42.6977, 23.3219], 15);

// Add a Tile Layer (OpenStreetMap is a good default choice)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Layer group for land properties
const landPropertiesLayer = L.layerGroup().addTo(map);

// Layer group for isolines
const isolays = L.layerGroup().addTo(map);

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
