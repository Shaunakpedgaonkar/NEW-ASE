var map; // Declare map variable globally
var directionsService;
var directionsRenderer;
var customMarkerImage = '{% static "resources/2915103.png" %}'; // Custom marker image for the user's location
var customHospitalMarkerImage = '{% static "resources/welfareroom.png" %}'; // Custom marker image for hospitals
var customPoliceMarkerImage = '{% static "resources/army.png" %}'; // Custom marker image for police stations
var currentLocation; // Variable to store current location

// Populate incident table on page load
window.onload = function() {
    populateIncidentTable();
    initMap();
};

// Initialize Google Map
function initMap() {
    // Initialize map
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 13,
        styles: [
            {
                elementType: 'labels.text.fill', // Set text fill color
                stylers: [{color: '#000000'}]
            },
            {
                elementType: 'labels.text.stroke', // Set text stroke color
                stylers: [{color: '#ffffff'}]
            }
        ]
    });

    // Initialize DirectionsService and DirectionsRenderer
    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer({
        map: map,
        suppressMarkers: true, // Don't display default markers
        preserveViewport: true, // Preserve the viewport
        polylineOptions: {
            strokeColor: '#0000FF', // Set the polyline color
            strokeWeight: 4, // Set the polyline thickness
            strokeOpacity: 1 // Set the polyline opacity
        }
    });

    console.log('Initializing map...');
    getCurrentLocation();
    initAutocomplete(); // Call initAutocomplete function here
}

// Get current location of user
function getCurrentLocation() {
    console.log('Getting current location...');
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            currentLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            console.log('Current position:', currentLocation);

            // Create marker at current location
            var currentMarker = new google.maps.Marker({
                position: currentLocation,
                map: map,
                title: 'Your Location'
            });

            // Set map center to current location
            map.setCenter(currentLocation);
            map.setZoom(13); // Set the zoom level to desired value

            // Add click event listener to the map to display route when clicking on a place
            map.addListener('click', function(event) {
                calculateAndDisplayRoute(currentLocation, event.latLng);
            });

            // Find nearby police stations
            var policeRequest = {
                location: currentLocation,
                radius: 5000,
                type: 'police'
            };
            console.log('Searching for nearby police stations...');
            searchAndDisplayPlaces(policeRequest, customPoliceMarkerImage); // Call with custom marker image for police stations

            // Find nearby hospitals
            var hospitalRequest = {
                location: currentLocation,
                radius: 5000,
                type: 'hospital'
            };
            console.log('Searching for nearby hospitals...');
            searchAndDisplayPlaces(hospitalRequest, customHospitalMarkerImage); // Call with custom marker image for hospitals
        }, function(error) {
            handleGeolocationError(error);
        }, {
            // Set maximumAge for location data (optional, adjust value as needed)
            maximumAge: 30000 // Update location data every 30 seconds (in milliseconds)
        });
    } else {
        alert('Error: Your browser doesn\'t support geolocation.');
    }
}

// Initialize autocomplete for the destination input
function initAutocomplete() {
    var input = document.getElementById('destination-input');
    var autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.setFields(['geometry']);

    // When a place is selected from the autocomplete dropdown
    autocomplete.addListener('place_changed', function() {
        var place = autocomplete.getPlace();
        if (!place.geometry) {
            window.alert("No details available for input: '" + place.name + "'");
            return;
        }
        var destinationLocation = place.geometry.location;
        console.log("Destination Location:", destinationLocation);
        findNearestHospital(destinationLocation); // Call function to find nearest hospital
    });
}

// Function to find nearest hospital from a given location
function findNearestHospital(destinationLocation) {
    var hospitalRequest = {
        location: destinationLocation,
        radius: 5000,
        type: 'hospital'
    };
    var service = new google.maps.places.PlacesService(map);
    service.nearbySearch(hospitalRequest, function(hospitalResults, hospitalStatus) {
        if (hospitalStatus === google.maps.places.PlacesServiceStatus.OK && hospitalResults.length > 0) {
            var nearestHospital = hospitalResults[0].geometry.location;
            console.log("Nearest Hospital:", nearestHospital);
            calculateAndDisplayRoute(destinationLocation, nearestHospital);
        } else {
            window.alert("No hospitals found nearby.");
        }
    });
}


// Create marker for a place
function createMarker(place, customMarkerImage) {
    var marker = new google.maps.Marker({
        map: map,
        position: place.geometry.location,
        title: place.name,
        icon: customMarkerImage
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
        calculateAndDisplayRoute(currentLocation, place.geometry.location);
    });
}

// Search for nearby places and display them on the map
function searchAndDisplayPlaces(request, customMarkerImage) {
    var service = new google.maps.places.PlacesService(map);
    service.nearbySearch(request, function(results, status) {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
            // Create markers for each place
            for (var i = 0; i < results.length; i++) {
                createMarker(results[i], customMarkerImage);
            }
        } else {
            console.log('No places found.');
        }
    });
}

// Calculate and display route between two locations
function calculateAndDisplayRoute(origin, destination) {
    directionsService.route({
        origin: origin,
        destination: destination,
        travelMode: 'DRIVING',
        provideRouteAlternatives: true // Include alternate routes
    }, function(response, status) {
        if (status === 'OK') {
            // Clear previous routes
            directionsRenderer.setMap(null);
            directionsRenderer = new google.maps.DirectionsRenderer({
                map: map,
                suppressMarkers: true,
                preserveViewport: true,
                polylineOptions: {
                    strokeColor: '#0000FF',
                    strokeWeight: 4,
                    strokeOpacity: 1
                }
            });

            // Display the first (shortest) route on the map
            new google.maps.DirectionsRenderer({
                map: map,
                directions: response,
                routeIndex: 0,
                polylineOptions: {
                    strokeColor: '#0000FF', // Color for the main route
                    strokeWeight: 4,
                    strokeOpacity: 1
                }
            });

            // Display alternate routes when the user clicks the button
            document.getElementById('showAlternateRoutes').addEventListener('click', function() {
                for (let i = 1; i < response.routes.length; i++) {
                    new google.maps.DirectionsRenderer({
                        map: map,
                        directions: response,
                        routeIndex: i,
                        polylineOptions: {
                            strokeColor: '#05f72d', // Color for alternate routes
                            strokeWeight: 4,
                            strokeOpacity: 1
                        }
                    });
                }
            });
        } else {
            window.alert('Directions request failed due to ' + status);
        }
    });
}

// Handle geolocation errors
function handleGeolocationError(error) {
    switch (error.code) {
        case error.PERMISSION_DENIED:
            alert("You denied permission to access your location. The 'A' marker might not be placed accurately.");
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
