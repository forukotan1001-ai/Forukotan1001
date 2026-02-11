import React, { useState, useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { View, Text, StyleSheet, Alert } from 'react-native';
import * as Location from 'expo-location';
import LocationScreen from './screens/LocationScreen';
import WorkScreen from './screens/WorkScreen';
import MapScreen from './screens/MapScreen';

const Tab = createBottomTabNavigator();

export default function App() {
  const [location, setLocation] = useState(null);

  useEffect(() => {
    getLocationPermission();
  }, []);

  const getLocationPermission = async () => {
    try {
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        Alert.alert('Permission Denied', 'Location permission is required for this app.');
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to request location permission');
    }
  };

  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={{
          headerShown: true,
          tabBarActiveTintColor: '#007AFF',
          tabBarInactiveTintColor: '#8E8E93',
        }}
      >
        <Tab.Screen
          name="Location"
          component={LocationScreen}
          options={{
            title: 'Track Location',
            tabBarLabel: 'Location',
          }}
        />
        <Tab.Screen
          name="Map"
          component={MapScreen}
          options={{
            title: 'Location Map',
            tabBarLabel: 'Map',
          }}
        />
        <Tab.Screen
          name="Work"
          component={WorkScreen}
          options={{
            title: 'Import Work',
            tabBarLabel: 'Work',
          }}
        />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
