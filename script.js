var customMarkerImage = 'C://Users//SHAUNAK//Documents//ASE1//web app//2915103_1.png'; // Custom marker image for the user's location
var customHospitalMarkerImage = 'C://Users//SHAUNAK//Documents//ASE1//web app//welfareroom.png'; // Custom marker image for hospitals
var customPoliceMarkerImage = 'C://Users//SHAUNAK//Documents//ASE1//web app//army (1).png';// Custom marker image for police stations

function initMap() {
    // Default center (Dublin)
    var defaultCenter = { lat: 53.349805, lng: -6.26031 };

    // Initialize map
    var map = new google.maps.Map(document.getElementById('map'), {
        center: defaultCenter,
        zoom: 13
    });

    console.log('Initializing map...');
    getCurrentLocation(map);
}

function getCurrentLocation(map) {
    console.log('Getting current location...');
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            console.log('Current position:', position.coords.latitude, position.coords.longitude);
            var currentLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            // Set map center to current location
            map.setCenter(currentLocation);
            map.setZoom(13); // Set the zoom level to desired value

            // Place marker at current location
            var currentMarker = new google.maps.Marker({
                position: currentLocation,
                map: map,
                title: 'Your Location',
                icon: customMarkerImage
            });

            // Find nearby police stations
            var policeRequest = {
                location: currentLocation,
                radius: 5000,
                type: 'police'
            };
            console.log('Searching for nearby police stations...');
            searchAndDisplayPlaces(policeRequest, map, customPoliceMarkerImage); // Call with custom marker image for police stations

            // Find nearby hospitals
            var hospitalRequest = {
                location: currentLocation,
                radius: 5000,
                type: 'hospital'
            };
            console.log('Searching for nearby hospitals...');
            searchAndDisplayPlaces(hospitalRequest, map, customHospitalMarkerImage); // Call with custom marker image for hospitals
        }, function(error) {
            handleGeolocationError(error);
        });
    } else {
        alert('Error: Your browser doesn\'t support geolocation.');
    }
}

function searchAndDisplayPlaces(request, map, customMarkerImage = null) {
    var service = new google.maps.places.PlacesService(map);
    service.nearbySearch(request, function(results, status) {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
            // Find the nearest hospital
            var nearestHospital = results[0];

            // Create markers for hospitals
            for (var i = 0; i < results.length; i++) {
                var hospital = results[i];
                var markerIcon = (hospital === nearestHospital) ? {
                    url: customHospitalMarkerImage,
                    scaledSize: new google.maps.Size(40, 40) // Adjust size for nearest hospital
                } : customMarkerImage; // Use custom marker image for nearest hospital
                createMarker(hospital, map, markerIcon);
            }
        } else {
            console.log('No places found.');
        }
    });
}

function createMarker(place, map, customMarkerImage = null) {
    var marker = new google.maps.Marker({
        map: map,
        position: place.geometry.location,
        title: place.name,
        icon: customMarkerImage // Use custom marker image if provided (null if not)
    });

    // Create info window content
    var infoWindowContent = '<strong>' + place.name + '</strong><br>' + place.vicinity;

    // Create info window
    var infoWindow = new google.maps.InfoWindow({
        content: infoWindowContent
    });

    // Add click event listener to the marker
    marker.addListener('click', function() {
        // Open info window above the marker
        infoWindow.open(map, marker);

        // Calculate and display route from current location to clicked marker
        calculateAndDisplayRoute(map.center, place.geometry.location, map, '#0000FF'); // You can adjust the color as needed
    });
}

function calculateAndDisplayRoute(origin, destination, map, color) {
    var directionsService = new google.maps.DirectionsService();
    var directionsRenderer = new google.maps.DirectionsRenderer({
        map: map,
        suppressMarkers: true, // Don't display default markers
        preserveViewport: true, // Preserve the viewport
        polylineOptions: {
            strokeColor: color, // Set the polyline color
            strokeWeight: 3, // Set the polyline thickness
            strokeOpacity: 1 // Set the polyline opacity
        }
    });

    // Set up request for directions
    var request = {
        origin: origin,
        destination: destination,
        travelMode: google.maps.TravelMode.DRIVING // Change this as needed
    };

    // Get directions
    directionsService.route(request, function(response, status) {
        if (status === google.maps.DirectionsStatus.OK) {
            // Display the directions on the map
            directionsRenderer.setDirections(response);
        } else {
            console.log('Directions request failed:', status);
        }
    });
}

function handleGeolocationError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            alert("User denied the request for Geolocation.");
            break;
        case error.POSITION_UNAVAILABLE:
            alert("Location information is unavailable.");
            break;
            case error.TIMEOUT:
                alert("The request to get user location timed out.");
                break;
            case error.UNKNOWN_ERROR:
                alert("An unknown error occurred.");
                break;
        }
    }