'use client'

import L from 'leaflet'
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet"
import MarkerIcon from '../node_modules/leaflet/dist/images/marker-icon.png'
import MarkerShadow from '../node_modules/leaflet/dist/images/marker-shadow.png'
import 'leaflet/dist/leaflet.css'



const Map = () => {
    return (
        <div>
            <MapContainer style={{height:"600px"}} center={[63.415368, 10.398524]} zoom={13}>
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />

                <Marker icon={
                    new L.Icon({
                        iconUrl: MarkerIcon.src,
                        iconRetinaUrl: MarkerIcon.src,
                        iconSize: [25, 41],
                        iconAnchor: [12.5, 41],
                        popupAnchor: [0, -41],
                        shadowUrl: MarkerShadow.src,
                        shadowSize: [41, 41],
                    })
                } position={[63.416168, 10.401749]}>
                    <Popup>
                        Position: (63.416168, 10.401749) <br /> Humidity: Moren din er mann
                    </Popup>
                </Marker>
            </MapContainer>
        </div>
    )
}

export default Map