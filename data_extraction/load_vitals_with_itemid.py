import numpy as np
import math
from multiprocessing import Process, cpu_count
import logging
import psycopg2 as py



# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

np_data = np.load('list_adm_id.npy')

list_adm_id = np_data.tolist()

# Function to split list into chunks
def split_list(lst, n):
    chunk_size = math.ceil(len(lst) / n)
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

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


# Function to process each chunk and save it as a .npy file
def process_chunk(chunk, chunk_index):

    conn = py.connect("dbname = 'mimic' user = 'postgres' host = 'localhost' port='5432' password = 'p13240!'")
    cur = conn.cursor()
    cur.execute("SET search_path TO mimiciii;")

    logging.info(f"Starting processing chunk {chunk_index} with {len(chunk)} admissions.")
    data = []
    for id in range(len(chunk)):
        hadm_id = chunk[id][0]
        logging.info(f"Processing admission {id} in chunk {chunk_index}, hadm_id: {hadm_id}")
        vitals = []

        # Loop through the vital itemids and execute a single query per vital type
        for vital_name, itemids in vital_itemids.items():
            itemid_str = ','.join(map(str, itemids))
            # Simulating the query execution
            cur.execute(f"SELECT charttime, valuenum FROM chartevents WHERE hadm_id = {hadm_id} AND itemid IN ({itemid_str}) ORDER BY charttime")
            vitals.append(cur.fetchall())

        # Fetch urine output from outputevents separately
        urine_itemid_str = ','.join(map(str, urine_output_itemids))
        cur.execute(f"SELECT charttime, VALUE FROM outputevents WHERE hadm_id = {hadm_id} AND itemid IN ({urine_itemid_str}) ORDER BY charttime")
        vitals.append(cur.fetchall())

        # Append the vitals for this admission ID to the main data list
        data.append(vitals)

    # Save the chunk's data as a .npy file
    np.save(f"chunk_{chunk_index}.npy", np.array(data))
    logging.info(f"Chunk {chunk_index} saved with {len(chunk)} admissions.")

# Split the list_adm_id into as many chunks as available CPU cores
num_cores = cpu_count()  # Get number of CPU cores
chunks = split_list(list_adm_id, num_cores)

# Log the number of cores and chunks
logging.info(f"Using {num_cores} cores. Splitting data into {len(chunks)} chunks.")

# Process each chunk using multiprocessing
processes = []
for i, chunk in enumerate(chunks):
    p = Process(target=process_chunk, args=(chunk, i))
    processes.append(p)
    p.start()
    logging.info(f"Started process {i} for chunk {i}.")

# Wait for all processes to complete
for p in processes:
    p.join()

logging.info("All chunks processed and saved.")
