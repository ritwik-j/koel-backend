
// import { useRef, useState } from "react";
// import Link from "next/link";

// import "mapbox-gl/dist/mapbox-gl.css";
import React, { useRef, useState } from "react";
import Link from "next/link";
//import { Image } from "cloudinary-react";
import ReactMapGL, { Marker, Popup, ViewState } from "react-map-gl";
import MapGL from 'react-map-gl';
import Map from 'react-map-gl';
import "mapbox-gl/dist/mapbox-gl.css";
import mapboxgl from "mapbox-gl";

// import { useLocalState } from "src/utils/useLocalState";
// import { HousesQuery_houses } from "src/generated/HousesQuery";
// import { SearchBox } from "./searchBox";

export {};
interface IProps {}

export default function GISMap({}: IProps) {

    React.useEffect(() => {
        mapboxgl.accessToken =
          "pk.eyJ1IjoiZWR3aW5sZW9uZyIsImEiOiJjbHdremVyZ2kxOWxxMmptbXNhbmJiMmQ4In0.azhU6LCbu51RC61fc1teTw";
        const map = new mapboxgl.Map({
          container: "map", // container ID
          style: "mapbox://styles/mapbox/streets-v12",
          center: [103.81784, 1.400953], // starting position [lng, lat]
          zoom: 9.4, // starting zoom
        });
    
        return () => {
          // Clean up resources when component unmounts
          map.remove();
        };
      }, []); 
    
      return (
        <div
          id="map"
          style={{
            position: "relative",
            width: "100%",
            height: "85vh",
            zIndex: 0,
          }}
        />
      );
}