// FILE: subscriber.js
// PROJECT: Warehouse Watcher
// PROGRAMMER: Undefined Chargers - Yujung Park
// FIRST VERSION: 2025-01-23
// DESCRIPTION: 
// https://yeees.tistory.com/475
// cloud works only wss https://community.hivemq.com/t/how-to-connect-to-websocket-with-wss/1681 

import mqtt from 'mqtt';

export const subscribeMQTT = () => {
    const client = mqtt.connect(import.meta.env.VITE_MQTT_HOST, {
        username: import.meta.env.VITE_MQTT_USER,
        password: import.meta.env.VITE_MQTT_PASSWORD,
    });
    
    client.on('connect', function () {
        console.log('Connected');
    });

    client.on('error', function (error) {
        console.log(error);
    });
    
    client.on('message', function (topic, message) {
        console.log('Received message:', topic, message.toString());
        // store the object
    });
    
    client.subscribe('#');
};
