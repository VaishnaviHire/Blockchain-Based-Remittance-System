var i = 0;
var longitude;
var latitude;

//
//function timedCount() {
//    i = i + 1;
//    postMessage(i);
//    setTimeout("timedCount()",500);
//}
//
//timedCount();


 function getLocation() {
     i = i + 1;
     postMessage(i);
     setTimeout("getLocation()",600);

//       if (navigator.geolocation) {
//          navigator.geolocation.watchPosition(showPosition);
//          postMessage(latitude + " " + longitude + " " + i);
//
//      } else {
//          postMessage("Geolocation is not supported by this browser.");}



 }

//  function showPosition(position) {
//      latitude = position.coords.latitude;
//      longitude= position.coords.longitude;
//UPDATE in DB
//  }




 getLocation();
