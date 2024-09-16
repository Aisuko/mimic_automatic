import numpy as np
import pickle
import logging
import psycopg2
import concurrent.futures

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

np_data = np.load('data_extraction/get_list_of_hadm_id.npy')

list_adm_id = np_data.tolist()
print(len(list_adm_id))


# SpO2 - 646, 220277
# HR - 211, 220045
# RR - 618, 615, 220210, 224690
# SBP - 51,442,455,6701,220179,220050
# DBP - 8368,8440,8441,8555,220180,220051
# EtCO2 - 1817, 228640
# Temp(F) - 223761,678
# Temp(C) - 223762,676
# TGCS - 198, 226755, 227013
# CRR - 3348
# Urine Output - 43647, 43053, 43171, 43173, 43333, 43347,
# 43348, 43355, 43365, 43373, 43374, 43379, 43380, 43431,
# 43519, 43522, 43537, 43576, 43583, 43589, 43638, 43654,
# 43811, 43812, 43856, 44706, 45304, 227519,
# FiO2 - 2981, 3420, 3422, 223835,
# Glucose - 807,811,1529,3745,3744,225664,220621,226537
# pH - 780, 860, 1126, 1673, 3839, 4202, 4753, 6003, 220274, 220734, 223830, 228243,

def preprocess_vitals(list_adm_id: list, number: int):
    data = []
    for id in range(len(list_adm_id)):
        # print(id, list_adm_id[id][0])
        print(f"Processing admission {id}")
        hadm_id = list_adm_id[id][0]
        vitals = []

        conn = psycopg2.connect(dbname='mimic', user='postgres', host='localhost', port='5432', password='p13240!')
        cur = conn.cursor()
        # Set the search path for this connection
        cur.execute("SET search_path TO mimiciii;")

        cur.execute("select charttime, valuenum from chartevents where hadm_id = "
                    + str(hadm_id) + " and (itemid = " + str(646) +
                    " or itemid = " + str(220277) + ") order by charttime")
        vitals.append(cur.fetchall())

        # Heart Rate
        cur.execute("select charttime, valuenum from chartevents where hadm_id = "
                    + str(hadm_id) + " and (itemid = " + str(211) +
                    " or itemid = " + str(220045) + ") order by charttime")
        vitals.append(cur.fetchall())

        # Respiratory Rate
        cur.execute("select charttime, valuenum from chartevents where hadm_id = "
                    + str(hadm_id) + " and (itemid = " + str(618) +
                    " or itemid = " + str(615) + " or itemid = " + str(220210) +
                    " or itemid = " + str(224690) + ") order by charttime")
        vitals.append(cur.fetchall())

        # Systolic Blood Pressure
        cur.execute("select charttime, valuenum from chartevents where hadm_id = "
                    + str(hadm_id) + " and (itemid = " + str(51) +
                    " or itemid = " + str(442) + " or itemid = " + str(455) +
                    " or itemid = " + str(6701) + " or itemid = " + str(220179) +
                    " or itemid = " + str(220050) + ") order by charttime")
        vitals.append(cur.fetchall())

        # Diastolic Blood Pressure
        cur.execute("select charttime, valuenum from chartevents where hadm_id = "
                    + str(hadm_id) + " and (itemid = " + str(8368) +
                    " or itemid = " + str(8440) + " or itemid = " + str(8441) +
                    " or itemid = " + str(8555) + " or itemid = " + str(220180) +
                    " or itemid = " + str(220051) + ") order by charttime")
        vitals.append(cur.fetchall())

        # End-tidal carbon dioxide
        cur.execute("select charttime, valuenum from chartevents where hadm_id = "
                    + str(hadm_id) + " and (itemid = " + str(1817) +
                    " or itemid = " + str(228640) + ") order by charttime")
        vitals.append(cur.fetchall())

        # Temperature
        cur.execute("select charttime, valuenum from chartevents where hadm_id = "
                    + str(hadm_id) + " and (itemid = " + str(678) +
                    " or itemid = " + str(223761) + ") order by charttime")
        vitals.append(cur.fetchall())
        cur.execute("select charttime, valuenum from chartevents where hadm_id = "
                    + str(hadm_id) + " and (itemid = " + str(676) +
                    " or itemid = " + str(223762) + ") order by charttime")
        vitals.append(cur.fetchall())

        # Total Glasgow coma score
        cur.execute("select charttime, valuenum from chartevents where hadm_id = "
                    + str(hadm_id) + " and (itemid = " + str(198) +
                    " or itemid = " + str(226755) + " or itemid = " + str(227013)
                    + ") order by charttime")
        vitals.append(cur.fetchall())

        # Peripheral capillary refill rate
        cur.execute("select charttime, value from chartevents where hadm_id = "
                    + str(hadm_id) + " and itemid = " + str(3348) +
                    " order by charttime")
        vitals.append(cur.fetchall())
        cur.execute("select charttime, value from chartevents where hadm_id = "
                    + str(hadm_id) + " and (itemid = " + str(115) +
                    " or itemid = 223951) order by charttime")
        vitals.append(cur.fetchall())
        cur.execute("select charttime, value from chartevents where hadm_id = "
                    + str(hadm_id) + " and (itemid = " + str(8377) +
                    " or itemid = 224308) order by charttime")
        vitals.append(cur.fetchall())

        # Urine output
        cur.execute("select charttime, VALUE from outputevents where hadm_id = "
                    + str(hadm_id) + " and ( itemid = 40405 or itemid = " +
                    " 40428 or itemid = 41857 or itemid = 42001 or itemid = 42362 or itemid = " +
                    " 42676 or itemid = 43171 or itemid = 43173 or itemid = 42042 or itemid = " +
                    " 42068 or itemid = 42111 or itemid = 42119 or itemid = 40715 or itemid = " +
                    " 40056 or itemid = 40061 or itemid = 40085 or itemid = 40094 or itemid = " +
                    " 40096 or itemid = 43897 or itemid = 43931 or itemid = 43966 or itemid = " +
                    " 44080 or itemid = 44103 or itemid = 44132 or itemid = 44237 or itemid = " +
                    " 43348 or itemid = " +
                    " 43355 or itemid = 43365 or itemid = 43372 or itemid = 43373 or itemid = " +
                    " 43374 or itemid = 43379 or itemid = 43380 or itemid = 43431 or itemid = " +
                    " 43462 or itemid = 43522 or itemid = 44706 or itemid = 44911 or itemid = " +
                    " 44925 or itemid = 42810 or itemid = 42859 or itemid = 43093 or itemid = " +
                    " 44325 or itemid = 44506 or itemid = 43856 or itemid = 45304 or itemid = " +
                    " 46532 or itemid = 46578 or itemid = 46658 or itemid = 46748 or itemid = " +
                    " 40651 or itemid = 40055 or itemid = 40057 or itemid = 40065 or itemid = " +
                    " 40069 or itemid = 44752 or itemid = 44824 or itemid = 44837 or itemid = " +
                    " 43576 or itemid = 43589 or itemid = 43633 or itemid = 43811 or itemid = " +
                    " 43812 or itemid = 46177 or itemid = 46727 or itemid = 46804 or itemid = " +
                    " 43987 or itemid = 44051 or itemid = 44253 or itemid = 44278 or itemid = " +
                    " 46180 or itemid = 45804 or itemid = 45841 or itemid = 45927 or itemid = " +
                    " 42592 or itemid = 42666 or itemid = 42765 or itemid = 42892 or itemid = " +
                    " 43053 or itemid = 43057 or itemid = 42130 or itemid = 41922 or itemid = " +
                    " 40473 or itemid = 43333 or itemid = 43347 or itemid = 44684 or itemid = " +
                    " 44834 or itemid = 43638 or itemid = 43654 or itemid = 43519 or itemid = " +
                    " 43537 or itemid = 42366 or itemid = 45991 or itemid = 43583 or itemid = " +
                    " 43647) order by charttime ")
        vitals.append(cur.fetchall())

        # Fraction inspired oxygen
        cur.execute("select charttime, valuenum from chartevents where hadm_id = "
                    + str(hadm_id) + " and (itemid = " + str(2981) +
                    " or itemid = " + str(3420) + " or itemid = " + str(3422) +
                    " or itemid = " + str(223835) + ") order by charttime")
        vitals.append(cur.fetchall())

        # Glucose
        cur.execute("select charttime, valuenum from chartevents where hadm_id = "
                    + str(hadm_id) + " and (itemid = " + str(807) +
                    " or itemid = " + str(811) + " or itemid = " + str(1529) +
                    " or itemid = " + str(3745) + " or itemid = " + str(3744) +
                    " or itemid = " + str(225664) + " or itemid = " + str(220621) +
                    " or itemid = " + str(226537) + ") order by charttime")
        vitals.append(cur.fetchall())

        # pH
        cur.execute("select charttime, valuenum from chartevents where hadm_id = "
                    + str(hadm_id) + " and (itemid = " + str(780) +
                    " or itemid = " + str(860) + " or itemid = " + str(1126) +
                    " or itemid = " + str(1673) + " or itemid = " + str(3839) +
                    " or itemid = " + str(4202) + " or itemid = " + str(4753) +
                    " or itemid = " + str(6003) + " and itemid = " + str(220274) +
                    " or itemid = " + str(220734) + " or itemid = " + str(223830) +
                    " or itemid = " + str(228243) + ") order by charttime")
        vitals.append(cur.fetchall())

        # Append the vitals for this admission ID to the main data list
        print("Vitals: ", len(vitals))

        data.append(vitals)

    cur.close()
    conn.close()

    pickle.dump(data, open(f'vitals_records_{number}.p', 'wb'))


if __name__ == "__main__":
    # len(list_adm_id)=58976
    # 58976/1000=58.976
    # 59 chunks

    chunk1 = list_adm_id[:5000]
    chunk2 = list_adm_id[5000:10000]
    chunk3 = list_adm_id[10000:15000]
    chunk4 = list_adm_id[15000:20000]
    chunk5 = list_adm_id[20000:25000]
    chunk6 = list_adm_id[25000:30000]
    chunk7 = list_adm_id[30000:35000]
    chunk8 = list_adm_id[35000:40000]
    chunk9 = list_adm_id[40000:45000]
    chunk10 = list_adm_id[45000:50000]
    chunk11 = list_adm_id[50000:55000]
    chunk12 = list_adm_id[55000:58976]

    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        futures = [
            executor.submit(preprocess_vitals, chunk1, 5000),
            executor.submit(preprocess_vitals, chunk2, 10000),
            executor.submit(preprocess_vitals, chunk3, 15000),
            executor.submit(preprocess_vitals, chunk4, 20000),
            executor.submit(preprocess_vitals, chunk5, 25000),
            executor.submit(preprocess_vitals, chunk6, 30000),
            executor.submit(preprocess_vitals, chunk7, 35000),
            executor.submit(preprocess_vitals, chunk8, 40000),
            executor.submit(preprocess_vitals, chunk9, 45000),
            executor.submit(preprocess_vitals, chunk10, 50000),
            executor.submit(preprocess_vitals, chunk11, 55000),
            executor.submit(preprocess_vitals, chunk12, 58976)
        ]

    # Wait for all futures to complete
    concurrent.futures.wait(futures)