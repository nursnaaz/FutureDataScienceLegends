


"""
Dubai Infrastructure Monitoring - Synthetic Data Generator
Complete Python implementation for generating realistic Dubai infrastructure data
"""


import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import json
import sqlite3
from dataclasses import dataclass
from typing import List, Dict, Tuple
import uuid


# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)


@dataclass
class DubaiZone:
   """Dubai zone configuration"""
   zone_id: str
   zone_name: str
   center_lat: float
   center_lng: float
   area_km2: float
   population: int
   infrastructure_density: str


# Real Dubai zones with actual coordinates
DUBAI_ZONES = [
   DubaiZone("DT", "Downtown Dubai", 25.1972, 55.2744, 4.567, 85000, "very_high"),
   DubaiZone("MR", "Dubai Marina", 25.0781, 55.1370, 2.345, 65000, "high"),
   DubaiZone("DR", "Deira", 25.2697, 55.3095, 8.921, 120000, "high"),
   DubaiZone("BB", "Business Bay", 25.1877, 55.2439, 1.234, 45000, "very_high"),
   DubaiZone("JM", "Jumeirah", 25.2285, 55.2593, 6.789, 78000, "medium"),
   DubaiZone("JBR", "JBR", 25.0867, 55.1324, 1.567, 35000, "high"),
   DubaiZone("SZR", "Sheikh Zayed Road Corridor", 25.2048, 55.2708, 12.345, 25000, "medium"),
   DubaiZone("DIFC", "Dubai International Financial Centre", 25.2138, 55.2824, 1.100, 15000, "very_high"),
   DubaiZone("JVC", "Jumeirah Village Circle", 25.0647, 55.2066, 2.890, 42000, "medium"),
   DubaiZone("DSO", "Dubai Silicon Oasis", 25.1207, 55.3825, 7.200, 28000, "low")
]


# Real Dubai infrastructure with exact coordinates
REAL_INFRASTRUCTURE = {
   "road": [
       {"name": "Sheikh Zayed Road E11 - Trade Centre", "lat": 25.2326, "lng": 55.2928, "usage": 280000},
       {"name": "Sheikh Zayed Road E11 - Financial Centre", "lat": 25.2138, "lng": 55.2824, "usage": 265000},
       {"name": "Sheikh Zayed Road E11 - Business Bay", "lat": 25.1877, "lng": 55.2439, "usage": 250000},
       {"name": "Sheikh Zayed Road E11 - Downtown", "lat": 25.1972, "lng": 55.2744, "usage": 290000},
       {"name": "Al Khaleej Road D89 - Deira", "lat": 25.2697, "lng": 55.3095, "usage": 120000},
       {"name": "Dubai Marina Boulevard", "lat": 25.0781, "lng": 55.1370, "usage": 85000},
       {"name": "Jumeirah Beach Road - JBR", "lat": 25.0867, "lng": 55.1324, "usage": 65000},
       {"name": "Jumeirah Beach Road - Jumeirah", "lat": 25.2285, "lng": 55.2593, "usage": 45000},
       {"name": "Dubai-Al Ain Road E66", "lat": 25.1207, "lng": 55.3825, "usage": 95000},
       {"name": "Airport Road E44", "lat": 25.2532, "lng": 55.3657, "usage": 135000},
       {"name": "Business Bay Crossing", "lat": 25.1877, "lng": 55.2439, "usage": 110000},
       {"name": "The Walk JBR Promenade", "lat": 25.0825, "lng": 55.1304, "usage": 25000},
       {"name": "Palm Jumeirah Trunk Road", "lat": 25.1124, "lng": 55.1390, "usage": 75000},
       {"name": "JLT Main Boulevard", "lat": 25.0694, "lng": 55.1441, "usage": 55000},
       {"name": "Al Barsha Road", "lat": 25.0958, "lng": 55.1928, "usage": 70000},
       {"name": "Mall of Emirates Access", "lat": 25.1183, "lng": 55.2006, "usage": 85000},
       {"name": "Dubai Mall Boulevard", "lat": 25.1972, "lng": 55.2796, "usage": 120000},
       {"name": "Financial Centre Road DIFC", "lat": 25.2138, "lng": 55.2824, "usage": 95000},
       {"name": "Trade Centre Road", "lat": 25.2326, "lng": 55.2928, "usage": 105000},
       {"name": "Zabeel Road", "lat": 25.2285, "lng": 55.2970, "usage": 65000},
       {"name": "Al Garhoud Road", "lat": 25.2532, "lng": 55.3418, "usage": 80000},
       {"name": "Silicon Oasis Boulevard", "lat": 25.1207, "lng": 55.3825, "usage": 35000},
       {"name": "Academic City Road", "lat": 25.1050, "lng": 55.4086, "usage": 25000},
       {"name": "Dubai Festival City Access", "lat": 25.2217, "lng": 55.3538, "usage": 40000},
       {"name": "Mohammed Bin Rashid Boulevard", "lat": 25.1972, "lng": 55.2744, "usage": 90000}
   ],
   "bridge": [
       {"name": "Business Bay Bridge", "lat": 25.1877, "lng": 55.2439, "usage": 95000},
       {"name": "Al Maktoum Bridge", "lat": 25.2697, "lng": 55.3260, "usage": 75000},
       {"name": "Al Garhoud Bridge", "lat": 25.2532, "lng": 55.3418, "usage": 85000},
       {"name": "Floating Bridge Al Shindagha", "lat": 25.2697, "lng": 55.2995, "usage": 45000},
       {"name": "Dubai Water Canal Bridge Sheikh Zayed", "lat": 25.2138, "lng": 55.2824, "usage": 180000},
       {"name": "Dubai Water Canal Bridge Al Wasl", "lat": 25.2090, "lng": 55.2650, "usage": 65000},
       {"name": "Dubai Water Canal Bridge Jumeirah", "lat": 25.2200, "lng": 55.2580, "usage": 55000},
       {"name": "Creek Crossing Extension", "lat": 25.2600, "lng": 55.3100, "usage": 35000},
       {"name": "Palm Jumeirah Bridge", "lat": 25.1124, "lng": 55.1390, "usage": 60000},
       {"name": "Dubai Hills Bridge Mohammed Bin Rashid City", "lat": 25.0958, "lng": 55.2500, "usage": 45000},
       {"name": "Trade Centre Overpass", "lat": 25.2326, "lng": 55.2928, "usage": 85000}
   ],
   "utility": [
       {"name": "DEWA Substation Downtown Dubai", "lat": 25.1972, "lng": 55.2744, "usage": 85000},
       {"name": "DEWA Substation Dubai Marina", "lat": 25.0781, "lng": 55.1370, "usage": 65000},
       {"name": "DEWA Substation Deira", "lat": 25.2697, "lng": 55.3095, "usage": 120000},
       {"name": "DEWA Substation JLT", "lat": 25.0694, "lng": 55.1441, "usage": 35000},
       {"name": "DEWA Substation Business Bay", "lat": 25.1877, "lng": 55.2439, "usage": 45000},
       {"name": "Dubai Water Pumping Station Jumeirah", "lat": 25.2285, "lng": 55.2593, "usage": 78000},
       {"name": "Dubai Water Treatment Plant Jebel Ali", "lat": 25.0126, "lng": 55.0775, "usage": 2800000},
       {"name": "Empower District Cooling Downtown", "lat": 25.1972, "lng": 55.2744, "usage": 85000},
       {"name": "Empower District Cooling DIFC", "lat": 25.2138, "lng": 55.2824, "usage": 15000},
       {"name": "DU Telecommunications Hub TECOM", "lat": 25.0958, "lng": 55.1700, "usage": 500000},
       {"name": "Etisalat Central Exchange Karama", "lat": 25.2400, "lng": 55.3030, "usage": 800000},
       {"name": "Dubai Gas Distribution Center Al Qusais", "lat": 25.2854, "lng": 55.3924, "usage": 150000},
       {"name": "Dubai Municipality Water Network Control", "lat": 25.2285, "lng": 55.2970, "usage": 2500000},
       {"name": "Smart City Infrastructure Hub DIFC", "lat": 25.2138, "lng": 55.2824, "usage": 15000},
       {"name": "DEWA Solar Park Connection Mohammed Bin Rashid", "lat": 24.8607, "lng": 55.3756, "usage": 1800000}
   ],
   "tunnel": [
       {"name": "Shindagha Tunnel", "lat": 25.2697, "lng": 55.2995, "usage": 85000},
       {"name": "Airport Tunnel DXB", "lat": 25.2532, "lng": 55.3657, "usage": 95000},
       {"name": "Dubai Metro Red Line Tunnel DIFC", "lat": 25.2138, "lng": 55.2824, "usage": 125000},
       {"name": "Dubai Metro Red Line Tunnel BurJuman", "lat": 25.2534, "lng": 55.3040, "usage": 110000},
       {"name": "Business Bay Underpass", "lat": 25.1877, "lng": 55.2439, "usage": 75000},
       {"name": "Trade Centre Underpass", "lat": 25.2326, "lng": 55.2928, "usage": 65000}
   ]
}


class DubaiInfrastructureGenerator:
   """Generate realistic Dubai infrastructure data"""
  
   def __init__(self):
       self.zones_df = self._create_zones_data()
      
   def _create_zones_data(self) -> pd.DataFrame:
       """Create Dubai zones dataframe"""
       return pd.DataFrame([{
           'zone_id': zone.zone_id,
           'zone_name': zone.zone_name,
           'center_lat': zone.center_lat,
           'center_lng': zone.center_lng,
           'area_km2': zone.area_km2,
           'population': zone.population,
           'infrastructure_density': zone.infrastructure_density
       } for zone in DUBAI_ZONES])
  
   def _get_zone_for_coordinates(self, lat: float, lng: float) -> DubaiZone:
       """Determine which zone the coordinates belong to based on proximity"""
       min_distance = float('inf')
       closest_zone = DUBAI_ZONES[0]
      
       for zone in DUBAI_ZONES:
           distance = ((lat - zone.center_lat) ** 2 + (lng - zone.center_lng) ** 2) ** 0.5
           if distance < min_distance:
               min_distance = distance
               closest_zone = zone
      
       return closest_zone
  
   def generate_infrastructure_assets(self, count: int = 500) -> pd.DataFrame:
       """Generate infrastructure assets data using real Dubai coordinates"""
       assets = []
       asset_id_counter = 1
      
       # Start with all real infrastructure
       for asset_type, infrastructure_list in REAL_INFRASTRUCTURE.items():
           for infra in infrastructure_list:
               # Determine zone based on coordinates
               zone = self._get_zone_for_coordinates(infra['lat'], infra['lng'])
              
               # Generate realistic condition scores based on infrastructure age and type
               if asset_type == 'tunnel' or 'Metro' in infra['name']:
                   condition_mean, condition_std = 85, 12  # Newer infrastructure
               elif 'Sheikh Zayed' in infra['name'] or 'DIFC' in infra['name']:
                   condition_mean, condition_std = 78, 15  # Well-maintained major infrastructure
               elif asset_type == 'bridge':
                   condition_mean, condition_std = 72, 18  # Bridges need more maintenance
               elif zone.infrastructure_density == 'very_high':
                   condition_mean, condition_std = 75, 16  # Premium areas
               else:
                   condition_mean, condition_std = 68, 20  # Standard maintenance
              
               condition_score = max(25, min(100, int(np.random.normal(condition_mean, condition_std))))
              
               # Risk level based on condition score
               if condition_score >= 80:
                   risk_level = 'low'
               elif condition_score >= 65:
                   risk_level = 'medium'
               elif condition_score >= 45:
                   risk_level = 'high'
               else:
                   risk_level = 'critical'
              
               # Use actual usage data or generate based on infrastructure type
               daily_usage = infra.get('usage', 50000)
              
               # Maintenance cost based on actual infrastructure complexity and usage
               if asset_type == 'utility' and daily_usage > 1000000:
                   maintenance_cost_aed = random.randint(2000000, 8000000)  # Major utilities
               elif asset_type == 'tunnel' or daily_usage > 200000:
                   maintenance_cost_aed = random.randint(800000, 3000000)  # Major infrastructure
               elif asset_type == 'bridge':
                   maintenance_cost_aed = random.randint(500000, 2500000)  # Bridge maintenance
               elif daily_usage > 100000:
                   maintenance_cost_aed = random.randint(300000, 1200000)  # Major roads
               else:
                   maintenance_cost_aed = random.randint(100000, 600000)   # Standard roads
              
               # Adjust cost based on condition (worse condition = higher cost)
               cost_multiplier = 1.0 + (100 - condition_score) / 200
               maintenance_cost_aed = int(maintenance_cost_aed * cost_multiplier)
              
               # Last inspection date based on criticality
               if daily_usage > 200000 or asset_type in ['bridge', 'tunnel']:
                   days_since_inspection = random.randint(15, 90)   # More frequent inspections
               elif daily_usage > 100000:
                   days_since_inspection = random.randint(30, 120)  # Regular inspections
               else:
                   days_since_inspection = random.randint(60, 180)  # Standard inspections
              
               last_inspection = datetime.now().date() - timedelta(days=days_since_inspection)
              
               # Criticality based on usage, asset type, and strategic importance
               if (daily_usage > 200000 or asset_type in ['bridge', 'tunnel'] or
                   'Sheikh Zayed' in infra['name'] or 'DEWA' in infra['name'] or
                   'Downtown' in infra['name'] or 'DIFC' in infra['name']):
                   criticality = random.choices(['high', 'critical'], weights=[0.6, 0.4])[0]
               elif daily_usage > 80000 or zone.infrastructure_density == 'very_high':
                   criticality = random.choices(['medium', 'high'], weights=[0.5, 0.5])[0]
               else:
                   criticality = random.choices(['low', 'medium'], weights=[0.6, 0.4])[0]
              
               # Realistic construction years based on Dubai's development
               if 'Metro' in infra['name']:
                   construction_year = random.randint(2009, 2020)  # Dubai Metro timeline
               elif 'Water Canal' in infra['name']:
                   construction_year = random.randint(2013, 2016)  # Dubai Water Canal project
               elif 'Downtown' in infra['name'] or 'DIFC' in infra['name']:
                   construction_year = random.randint(2000, 2010)  # Dubai boom period
               elif asset_type == 'bridge' and 'Business Bay' in infra['name']:
                   construction_year = 2007  # Actual construction year
               elif 'Sheikh Zayed' in infra['name']:
                   construction_year = random.randint(1998, 2005)  # Major highway development
               else:
                   construction_year = random.randint(1995, 2020)
              
               asset = {
                   'asset_id': f"{asset_type.upper()[:4]}_{asset_id_counter:03d}",
                   'asset_name': infra['name'],
                   'asset_type': asset_type,
                   'latitude': infra['lat'],
                   'longitude': infra['lng'],
                   'district': zone.zone_name,
                   'zone_id': zone.zone_id,
                   'condition_score': condition_score,
                   'risk_level': risk_level,
                   'last_inspection': last_inspection,
                   'daily_usage': daily_usage,
                   'maintenance_cost_aed': maintenance_cost_aed,
                   'criticality': criticality,
                   'construction_year': construction_year,
                   'next_inspection_due': last_inspection + timedelta(days=random.randint(60, 180))
               }
              
               assets.append(asset)
               asset_id_counter += 1
      
       # Add additional synthetic assets to reach target count if needed
       real_asset_count = len(assets)
       remaining_count = count - real_asset_count
      
       if remaining_count > 0:
           print(f"Adding {remaining_count} additional synthetic assets to reach target of {count}")
          
           for i in range(remaining_count):
               # Generate additional assets in various zones
               zone = random.choice(DUBAI_ZONES)
               asset_type = random.choices(['road', 'utility', 'bridge'], weights=[0.7, 0.25, 0.05])[0]
              
               # Generate coordinates near zone center
               radius = random.uniform(0.005, 0.015)
               angle = random.uniform(0, 2 * np.pi)
               lat = zone.center_lat + radius * np.cos(angle)
               lng = zone.center_lng + radius * np.sin(angle)
              
               # Ensure within Dubai bounds
               lat = max(24.7136, min(25.3428, lat))
               lng = max(54.8969, min(55.5731, lng))
              
               condition_score = max(30, min(100, int(np.random.normal(70, 18))))
               risk_level = 'low' if condition_score >= 80 else ('medium' if condition_score >= 65 else 'high')
              
               asset = {
                   'asset_id': f"{asset_type.upper()[:4]}_{asset_id_counter:03d}",
                   'asset_name': f"{zone.zone_name} {asset_type.title()} Section {i+1}",
                   'asset_type': asset_type,
                   'latitude': round(lat, 6),
                   'longitude': round(lng, 6),
                   'district': zone.zone_name,
                   'zone_id': zone.zone_id,
                   'condition_score': condition_score,
                   'risk_level': risk_level,
                   'last_inspection': datetime.now().date() - timedelta(days=random.randint(30, 180)),
                   'daily_usage': random.randint(5000, 80000),
                   'maintenance_cost_aed': random.randint(80000, 500000),
                   'criticality': random.choices(['low', 'medium'], weights=[0.7, 0.3])[0],
                   'construction_year': random.randint(2000, 2022),
                   'next_inspection_due': datetime.now().date() + timedelta(days=random.randint(30, 120))
               }
              
               assets.append(asset)
               asset_id_counter += 1
      
       return pd.DataFrame(assets[:count])  # Ensure exact count
  
   def generate_sensor_data(self, assets_df: pd.DataFrame, sensors_per_asset: int = 2) -> pd.DataFrame:
       """Generate IoT sensor data"""
       sensors = []
       sensor_id_counter = 1
      
       sensor_types = ['vibration', 'temperature', 'traffic_count', 'crack_detection', 'water_level', 'air_quality']
      
       for _, asset in assets_df.iterrows():
           # Number of sensors based on asset type and criticality
           if asset['asset_type'] == 'bridge':
               sensor_count = random.randint(3, 5)
           elif asset['criticality'] in ['high', 'critical']:
               sensor_count = random.randint(2, 4)
           else:
               sensor_count = random.randint(1, 3)
          
           for _ in range(sensor_count):
               sensor_type = random.choice(sensor_types)
              
               # Generate realistic readings based on sensor type
               if sensor_type == 'vibration':
                   reading_value = round(random.uniform(0.5, 15.0), 4)
                   alert_threshold = 12.0
                   unit = 'mm/s'
               elif sensor_type == 'temperature':
                   reading_value = round(random.uniform(28, 52), 2)  # Dubai temperatures
                   alert_threshold = 50.0
                   unit = 'celsius'
               elif sensor_type == 'traffic_count':
                   reading_value = random.randint(50, 8000)
                   alert_threshold = 6000
                   unit = 'vehicles/hour'
               elif sensor_type == 'crack_detection':
                   reading_value = round(random.uniform(0, 45), 2)
                   alert_threshold = 35.0
                   unit = 'percentage'
               elif sensor_type == 'water_level':
                   reading_value = round(random.uniform(0, 25), 2)
                   alert_threshold = 20.0
                   unit = 'cm'
               else:  # air_quality
                   reading_value = random.randint(15, 150)
                   alert_threshold = 100
                   unit = 'aqi'
              
               # Generate timestamp within last 24 hours
               hours_ago = random.uniform(0, 24)
               reading_timestamp = datetime.now() - timedelta(hours=hours_ago)
              
               # Status based on reading vs threshold
               status_weights = [0.85, 0.10, 0.05]  # online, offline, maintenance
               status = random.choices(['online', 'offline', 'maintenance'], weights=status_weights)[0]
              
               sensor = {
                   'sensor_id': f"SEN_{sensor_id_counter:04d}",
                   'asset_id': asset['asset_id'],
                   'sensor_type': sensor_type,
                   'latitude': asset['latitude'] + random.uniform(-0.001, 0.001),
                   'longitude': asset['longitude'] + random.uniform(-0.001, 0.001),
                   'reading_value': reading_value,
                   'reading_timestamp': reading_timestamp,
                   'alert_threshold': alert_threshold,
                   'unit': unit,
                   'status': status,
                   'installation_date': datetime.now().date() - timedelta(days=random.randint(30, 1095)),
                   'battery_level': random.randint(15, 100) if status == 'online' else random.randint(0, 30)
               }
              
               sensors.append(sensor)
               sensor_id_counter += 1
      
       return pd.DataFrame(sensors)
  
   def generate_alerts(self, assets_df: pd.DataFrame, sensor_df: pd.DataFrame, count: int = 150) -> pd.DataFrame:
       """Generate infrastructure alerts"""
       alerts = []
       alert_types = ['maintenance_due', 'high_usage', 'sensor_fault', 'critical_condition', 'environmental_hazard']
      
       for i in range(count):
           asset = assets_df.sample(1).iloc[0]
           alert_type = random.choices(alert_types, weights=[0.35, 0.25, 0.15, 0.15, 0.10])[0]
          
           # Severity based on asset condition and alert type
           if alert_type == 'critical_condition' or asset['risk_level'] == 'critical':
               severity = random.choices(['high', 'critical'], weights=[0.3, 0.7])[0]
           elif alert_type == 'environmental_hazard':
               severity = random.choices(['medium', 'high'], weights=[0.6, 0.4])[0]
           elif asset['risk_level'] == 'high':
               severity = random.choices(['medium', 'high'], weights=[0.4, 0.6])[0]
           else:
               severity = random.choices(['low', 'medium'], weights=[0.6, 0.4])[0]
          
           # Generate alert description
           descriptions = {
               'maintenance_due': f"Scheduled maintenance required for {asset['asset_name']}",
               'high_usage': f"Usage levels exceeded normal capacity on {asset['asset_name']}",
               'sensor_fault': f"Sensor malfunction detected on {asset['asset_name']}",
               'critical_condition': f"Critical condition detected: {asset['asset_name']} requires immediate attention",
               'environmental_hazard': f"Environmental conditions affecting {asset['asset_name']}"
           }
          
           created_at = datetime.now() - timedelta(hours=random.uniform(0, 720))  # Last 30 days
          
           # Status distribution
           if severity == 'critical':
               status = random.choices(['active', 'investigating'], weights=[0.7, 0.3])[0]
           else:
               status = random.choices(['active', 'investigating', 'resolved'], weights=[0.5, 0.3, 0.2])[0]
          
           alert = {
               'alert_id': f"ALT_{i+1:04d}",
               'asset_id': asset['asset_id'],
               'alert_type': alert_type,
               'severity': severity,
               'description': descriptions[alert_type],
               'created_at': created_at,
               'status': status,
               'zone_id': asset['zone_id'],
               'district': asset['district'],
               'estimated_cost_aed': random.randint(10000, 500000),
               'response_time_required_hours': 1 if severity == 'critical' else (4 if severity == 'high' else 24)
           }
          
           alerts.append(alert)
      
       return pd.DataFrame(alerts)
  
   def create_database(self, filename: str = 'dubai_infrastructure.db'):
       """Create SQLite database with all tables"""
       conn = sqlite3.connect(filename)
      
       # Create tables
       conn.execute('''
       CREATE TABLE IF NOT EXISTS dubai_zones (
           zone_id TEXT PRIMARY KEY,
           zone_name TEXT NOT NULL,
           center_lat REAL NOT NULL,
           center_lng REAL NOT NULL,
           area_km2 REAL,
           population INTEGER,
           infrastructure_density TEXT
       )
       ''')
      
       conn.execute('''
       CREATE TABLE IF NOT EXISTS infrastructure_assets (
           asset_id TEXT PRIMARY KEY,
           asset_name TEXT NOT NULL,
           asset_type TEXT NOT NULL,
           latitude REAL NOT NULL,
           longitude REAL NOT NULL,
           district TEXT NOT NULL,
           zone_id TEXT,
           condition_score INTEGER,
           risk_level TEXT,
           last_inspection DATE,
           daily_usage INTEGER,
           maintenance_cost_aed INTEGER,
           criticality TEXT,
           construction_year INTEGER,
           next_inspection_due DATE,
           FOREIGN KEY (zone_id) REFERENCES dubai_zones (zone_id)
       )
       ''')
      
       conn.execute('''
       CREATE TABLE IF NOT EXISTS sensor_data (
           sensor_id TEXT PRIMARY KEY,
           asset_id TEXT NOT NULL,
           sensor_type TEXT NOT NULL,
           latitude REAL,
           longitude REAL,
           reading_value REAL,
           reading_timestamp TIMESTAMP,
           alert_threshold REAL,
           unit TEXT,
           status TEXT,
           installation_date DATE,
           battery_level INTEGER,
           FOREIGN KEY (asset_id) REFERENCES infrastructure_assets (asset_id)
       )
       ''')
      
       conn.execute('''
       CREATE TABLE IF NOT EXISTS alerts (
           alert_id TEXT PRIMARY KEY,
           asset_id TEXT NOT NULL,
           alert_type TEXT NOT NULL,
           severity TEXT NOT NULL,
           description TEXT,
           created_at TIMESTAMP,
           status TEXT,
           zone_id TEXT,
           district TEXT,
           estimated_cost_aed INTEGER,
           response_time_required_hours INTEGER,
           FOREIGN KEY (asset_id) REFERENCES infrastructure_assets (asset_id)
       )
       ''')
      
       conn.commit()
       return conn


def main():
   """Generate all data and create database"""
   print("🏗️  Generating Dubai Infrastructure Data...")
  
   generator = DubaiInfrastructureGenerator()
  
   # Generate data
   print("📍 Creating zones data...")
   zones_df = generator.zones_df
  
   print("🏗️  Generating infrastructure assets...")
   assets_df = generator.generate_infrastructure_assets(500)
  
   print("📡 Generating sensor data...")
   sensors_df = generator.generate_sensor_data(assets_df)
  
   print("🚨 Generating alerts...")
   alerts_df = generator.generate_alerts(assets_df, sensors_df, 150)
  
   # Create database
   print("💾 Creating database...")
   conn = generator.create_database()
  
   # Insert data
   print("📝 Inserting data into database...")
   zones_df.to_sql('dubai_zones', conn, if_exists='replace', index=False)
   assets_df.to_sql('infrastructure_assets', conn, if_exists='replace', index=False)
   sensors_df.to_sql('sensor_data', conn, if_exists='replace', index=False)
   alerts_df.to_sql('alerts', conn, if_exists='replace', index=False)
  
   # Export to CSV for backup
   print("💾 Exporting to CSV files...")
   zones_df.to_csv('dubai_zones.csv', index=False)
   assets_df.to_csv('infrastructure_assets.csv', index=False)
   sensors_df.to_csv('sensor_data.csv', index=False)
   alerts_df.to_csv('alerts.csv', index=False)
  
   conn.close()
  
   # Print summary
   print(f"\n✅ Data Generation Complete!")
   print(f"📊 Generated:")
   print(f"   • {len(zones_df)} Dubai zones")
   print(f"   • {len(assets_df)} infrastructure assets")
   print(f"   • {len(sensors_df)} IoT sensors")
   print(f"   • {len(alerts_df)} active alerts")
   print(f"\n💾 Database: dubai_infrastructure.db")
   print(f"📁 CSV files exported for backup")
  
   # Print detailed sample data with real coordinates
   print("\n📋 Sample Infrastructure Assets (Real Dubai Coordinates):")
   sample_assets = assets_df[['asset_name', 'district', 'asset_type', 'latitude', 'longitude', 'condition_score', 'risk_level', 'daily_usage']].head(10)
   for _, asset in sample_assets.iterrows():
       print(f"   • {asset['asset_name'][:45]:<45} | {asset['district']:<20} | {asset['latitude']:.6f}, {asset['longitude']:.6f} | Score: {asset['condition_score']:>2} | Usage: {asset['daily_usage']:>7,}")
  
   print(f"\n🗺️  Geographic Coverage:")
   print(f"   • Real Dubai coordinates: {assets_df['latitude'].min():.4f} to {assets_df['latitude'].max():.4f} (lat)")
   print(f"   • Real Dubai coordinates: {assets_df['longitude'].min():.4f} to {assets_df['longitude'].max():.4f} (lng)")
   print(f"   • Major Infrastructure: Sheikh Zayed Road, Business Bay Bridge, DEWA Substations")
   print(f"   • Coverage: Downtown, Marina, Deira, JLT, Business Bay, DIFC")


   # Show some key real infrastructure
   key_infrastructure = assets_df[assets_df['asset_name'].str.contains('Sheikh Zayed|Business Bay Bridge|DEWA|Metro', case=False)][['asset_name', 'latitude', 'longitude', 'daily_usage', 'criticality']].head(5)
   if not key_infrastructure.empty:
       print(f"\n🏗️  Key Real Dubai Infrastructure:")
       for _, infra in key_infrastructure.iterrows():
           print(f"   • {infra['asset_name'][:50]:<50} | {infra['latitude']:.6f}, {infra['longitude']:.6f} | {infra['criticality']}")
  
   return assets_df, sensors_df, alerts_df


if __name__ == "__main__":
   main()

