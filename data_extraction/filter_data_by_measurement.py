import pickle
import psycopg2 as py

conn = py.connect(
    "dbname = 'mimic' user = 'postgres' host = 'localhost' port='5432' password = 'p13240!'")

cur = conn.cursor()
cur.execute("SET search_path TO mimiciii;")

cur.execute("""select hadm_id from admissions""")
list_adm_id = cur.fetchall()

# Dictionary of vitals with itemid sets
vital_itemids = {
    "SpO2": [646, 220277],
    "HR": [211, 220045],
    "RR": [618, 615, 220210, 224690],
    "SBP": [51, 442, 455, 6701, 220179, 220050],
    "DBP": [8368, 8440, 8441, 8555, 220180, 220051],
    "EtCO2": [1817, 228640],
    "Temp_F": [223761, 678],
    "Temp_C": [223762, 676],
    "TGCS": [198, 226755, 227013],
    "CRR": [3348],
    "FiO2": [2981, 3420, 3422, 223835],
    "Glucose": [807, 811, 1529, 3745, 3744, 225664, 220621, 226537],
    "pH": [780, 860, 1126, 1673, 3839, 4202, 4753, 6003, 220274, 220734, 223830, 228243],
}

# Urine output itemids as a separate set since it's fetched from outputevents
urine_output_itemids = [
    43647, 43053, 43171, 43173, 43333, 43347, 43348, 43355, 43365, 
    43373, 43374, 43379, 43380, 43431, 43519, 43522, 43537, 43576, 
    43583, 43589, 43638, 43654, 43811, 43812, 43856, 44706, 45304, 227519
]

data = []
for id in range(len(list_adm_id)):
    hadm_id = list_adm_id[id][0]
    print(id, hadm_id)
    vitals = []

    # Loop through the vital itemids and execute a single query per vital type
    for vital_name, itemids in vital_itemids.items():
        itemid_str = ','.join(map(str, itemids))
        cur.execute(f"SELECT charttime, valuenum FROM chartevents WHERE hadm_id = %s AND itemid IN ({itemid_str}) ORDER BY charttime", [hadm_id])
        vitals.append(cur.fetchall())

    # Fetch urine output from outputevents separately
    urine_itemid_str = ','.join(map(str, urine_output_itemids))
    cur.execute(f"SELECT charttime, VALUE FROM outputevents WHERE hadm_id = %s AND itemid IN ({urine_itemid_str}) ORDER BY charttime", [hadm_id])
    vitals.append(cur.fetchall())

    # Append the vitals for this admission ID to the main data list
    data.append(vitals)


# Use protocol 5 for better performance (if supported)
with open('vitals_records.p', 'wb') as file:
    pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)
