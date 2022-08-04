
// Initialize and add the map
function initMap() {
  // The location and name of the hotel
  const latitude = parseFloat(document.getElementById("latitude"));
  const longtitude = parseFloat(document.getElementById("longtitude"));
  const location = { lat: latitude, lng: longtitude };
  // The map, centered at the hotel
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 4,
    center: location,
  });
  // The marker, positioned at the hotel
  const marker = new google.maps.Marker({
    position: location,
    map: map,
    title:"Click to zoom",
  });
  //set click event
  map.addListener("center_changed", () => {
    // 3 seconds after the center of the map has changed, pan back to the
    // marker.
    window.setTimeout(() => {
      map.panTo(marker.getPosition());
    }, 3000);
  });
  marker.addListener("click", () =>{
    map.setZoom(8);
    map.setCenter(marker.getPosition());
  });
}

window.initMap = initMap;
