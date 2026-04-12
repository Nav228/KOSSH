#!/usr/bin/env python3
"""
KOSH Demo Data Seeder
Populates the database with realistic demo data for showcasing the application.
Run: python seed_demo_data.py
Or inside Docker: docker exec -it kosh_webapp python seed_demo_data.py
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
import random

DB = {
    'host':     os.getenv('POSTGRES_HOST', 'localhost'),
    'port':     int(os.getenv('POSTGRES_PORT', '5432')),
    'dbname':   os.getenv('POSTGRES_DB', 'kosh'),
    'user':     os.getenv('POSTGRES_USER', 'stockpick_user'),
    'password': os.getenv('POSTGRES_PASSWORD', 'stockpick_pass'),
}

SCHEMA = 'pcb_inventory'

def connect():
    return psycopg2.connect(**DB)

def run(conn, sql, params=None):
    with conn.cursor() as cur:
        cur.execute(sql, params)

def fetch(conn, sql, params=None):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, params)
        return cur.fetchall()

def seed_schema(conn):
    print("  Creating schema and tables if missing…")
    run(conn, f'CREATE SCHEMA IF NOT EXISTS {SCHEMA}')

    run(conn, f"""
        CREATE TABLE IF NOT EXISTS {SCHEMA}."tblLoc" (
            id SERIAL PRIMARY KEY,
            loc_code VARCHAR(20) UNIQUE NOT NULL,
            description VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    run(conn, f"""
        CREATE TABLE IF NOT EXISTS {SCHEMA}."tblPN_List" (
            id SERIAL PRIMARY KEY,
            item VARCHAR(100) UNIQUE,
            "DESC" VARCHAR(500),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    run(conn, f"""
        CREATE TABLE IF NOT EXISTS {SCHEMA}."tblWhse_Inventory" (
            id SERIAL PRIMARY KEY,
            item VARCHAR(100),
            pcn BIGINT,
            mpn VARCHAR(200),
            dc VARCHAR(20),
            onhandqty INTEGER DEFAULT 0,
            mfg_qty TEXT DEFAULT '0',
            qty_old INTEGER DEFAULT 0,
            loc_from VARCHAR(50),
            loc_to VARCHAR(50),
            msd VARCHAR(10),
            po VARCHAR(100),
            cost NUMERIC(12,4) DEFAULT 0,
            vendor VARCHAR(200),
            migrated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_stocked TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    run(conn, f"""
        CREATE TABLE IF NOT EXISTS {SCHEMA}."tblTransaction" (
            id SERIAL PRIMARY KEY,
            trantype VARCHAR(20),
            item VARCHAR(100),
            pcn BIGINT,
            mpn VARCHAR(200),
            dc VARCHAR(20),
            msd VARCHAR(10),
            tranqty INTEGER,
            tran_time VARCHAR(50),
            tran_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            loc_from VARCHAR(50),
            loc_to VARCHAR(50),
            wo VARCHAR(100),
            po VARCHAR(100),
            userid VARCHAR(100),
            reversed BOOLEAN DEFAULT FALSE,
            reversed_by_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    run(conn, f"""
        CREATE TABLE IF NOT EXISTS {SCHEMA}."tblJob" (
            id SERIAL PRIMARY KEY,
            job_number VARCHAR(50) UNIQUE NOT NULL,
            description VARCHAR(500),
            customer VARCHAR(200),
            cust_pn VARCHAR(100),
            build_qty INTEGER DEFAULT 0,
            job_rev VARCHAR(20),
            cust_rev VARCHAR(20),
            last_rev VARCHAR(20),
            wo_number VARCHAR(100),
            notes TEXT,
            status VARCHAR(50) DEFAULT 'New',
            created_by VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    run(conn, f"""
        CREATE TABLE IF NOT EXISTS {SCHEMA}."tblBOM" (
            id SERIAL PRIMARY KEY,
            job VARCHAR(100),
            job_number VARCHAR(50),
            job_rev VARCHAR(20),
            line INTEGER,
            aci_pn VARCHAR(100),
            ref_des VARCHAR(200),
            mpn VARCHAR(200),
            man VARCHAR(200),
            description VARCHAR(500),
            "DESC" VARCHAR(500),
            qty INTEGER DEFAULT 1,
            cost NUMERIC(12,4) DEFAULT 0,
            unit_cost NUMERIC(12,4) DEFAULT 0,
            manufacturer VARCHAR(200),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    run(conn, f"""
        CREATE TABLE IF NOT EXISTS {SCHEMA}."tblActivityLog" (
            id SERIAL PRIMARY KEY,
            user_id INTEGER,
            username VARCHAR(200),
            full_name VARCHAR(200),
            action_type VARCHAR(50),
            description TEXT,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            seen BOOLEAN DEFAULT FALSE,
            seen_at TIMESTAMP
        )
    """)

    run(conn, f"""
        CREATE TABLE IF NOT EXISTS {SCHEMA}."tblPCB_Inventory" (
            id SERIAL PRIMARY KEY,
            pcb_pn VARCHAR(100),
            job VARCHAR(100),
            pcb_type VARCHAR(100),
            description VARCHAR(500),
            pcn BIGINT,
            qty INTEGER DEFAULT 0,
            location VARCHAR(50),
            date_received DATE,
            status VARCHAR(50) DEFAULT 'In Stock',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    run(conn, f"""
        CREATE TABLE IF NOT EXISTS {SCHEMA}."tblShortageReport" (
            id SERIAL PRIMARY KEY,
            job VARCHAR(100),
            report_name VARCHAR(200),
            total_lines INTEGER DEFAULT 0,
            shortage_lines INTEGER DEFAULT 0,
            total_cost NUMERIC(14,4) DEFAULT 0,
            shortage_cost NUMERIC(14,4) DEFAULT 0,
            created_by VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notes TEXT,
            order_qty INTEGER DEFAULT 1,
            job_rev VARCHAR(20)
        )
    """)

    run(conn, f"""
        CREATE TABLE IF NOT EXISTS {SCHEMA}."tblShortageReportItems" (
            id SERIAL PRIMARY KEY,
            report_id INTEGER REFERENCES {SCHEMA}."tblShortageReport"(id) ON DELETE CASCADE,
            line_no INTEGER,
            aci_pn VARCHAR(100),
            pcn BIGINT,
            mpn VARCHAR(200),
            qty_required INTEGER DEFAULT 0,
            qty_on_hand INTEGER DEFAULT 0,
            order_qty INTEGER DEFAULT 1,
            item VARCHAR(100),
            location VARCHAR(50),
            unit_cost NUMERIC(12,4) DEFAULT 0,
            line_cost NUMERIC(12,4) DEFAULT 0,
            manufacturer VARCHAR(200),
            description VARCHAR(500),
            req INTEGER DEFAULT 0
        )
    """)

    run(conn, f"""
        CREATE TABLE IF NOT EXISTS {SCHEMA}."users" (
            id SERIAL PRIMARY KEY,
            userid VARCHAR(100) UNIQUE,
            username VARCHAR(200),
            userlogin VARCHAR(100) UNIQUE,
            password VARCHAR(200),
            usersecurity VARCHAR(50) DEFAULT 'USER',
            session_token VARCHAR(200),
            token_expires_at TIMESTAMP,
            last_login TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Migrate: add any columns that may be missing from pre-existing tables
    migrations = [
        ('tblWhse_Inventory', 'mfg_qty',   "TEXT DEFAULT '0'"),
        ('tblWhse_Inventory', 'qty_old',    'INTEGER DEFAULT 0'),
        ('tblWhse_Inventory', 'cost',       'NUMERIC(12,4) DEFAULT 0'),
        ('tblWhse_Inventory', 'vendor',     'VARCHAR(200)'),
        ('tblTransaction',    'reversed',   'BOOLEAN DEFAULT FALSE'),
        ('tblTransaction',    'reversed_by_id', 'INTEGER'),
        ('tblTransaction',    'tran_date',  'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'),
        ('tblJob',            'description','VARCHAR(500)'),
        ('tblBOM',            'job',        'VARCHAR(100)'),
        ('tblBOM',            'job_rev',    'VARCHAR(20)'),
        ('tblBOM',            'line',       'INTEGER'),
        ('tblBOM',            'aci_pn',     'VARCHAR(100)'),
        ('tblBOM',            'man',        'VARCHAR(200)'),
        ('tblBOM',            '"DESC"',     'VARCHAR(500)'),
        ('tblBOM',            'cost',       'NUMERIC(12,4) DEFAULT 0'),
        ('tblBOM',            'unit_cost',  'NUMERIC(12,4) DEFAULT 0'),
        ('tblBOM',            'manufacturer','VARCHAR(200)'),
        ('tblPCB_Inventory',  'job',        'VARCHAR(100)'),
        ('tblPCB_Inventory',  'pcb_type',   'VARCHAR(100)'),
    ]
    for table, col, coltype in migrations:
        try:
            run(conn, f'ALTER TABLE {SCHEMA}."{table}" ADD COLUMN IF NOT EXISTS {col} {coltype}')
        except Exception:
            conn.rollback()

    conn.commit()

def seed_locations(conn):
    print("  Seeding warehouse locations…")
    locations = [
        ('A1-01', 'Row A, Shelf 1, Bin 1'), ('A1-02', 'Row A, Shelf 1, Bin 2'),
        ('A1-03', 'Row A, Shelf 1, Bin 3'), ('A2-01', 'Row A, Shelf 2, Bin 1'),
        ('A2-02', 'Row A, Shelf 2, Bin 2'), ('B1-01', 'Row B, Shelf 1, Bin 1'),
        ('B1-02', 'Row B, Shelf 1, Bin 2'), ('B2-01', 'Row B, Shelf 2, Bin 1'),
        ('C1-01', 'Row C, Shelf 1, Bin 1'), ('C1-02', 'Row C, Shelf 1, Bin 2'),
        ('D1-01', 'Row D, Shelf 1, Bin 1'), ('RECV',  'Receiving Area'),
        ('COUNT', 'Count Area'),             ('FLOOR', 'Production Floor'),
    ]
    for code, desc in locations:
        run(conn, f"""
            INSERT INTO {SCHEMA}."tblLoc" (loc_code, description)
            VALUES (%s, %s) ON CONFLICT (loc_code) DO NOTHING
        """, (code, desc))
    conn.commit()
    print(f"    → {len(locations)} locations added")

def seed_jobs(conn):
    print("  Seeding jobs…")
    jobs = [
        ('6163L', 'Patient Monitor Control Board',  'MedShift Technologies',   '7394-PCB-A',   250,  'B', 'B', 'WO-23788'),
        ('8481L', 'Secure Comms Slim Module',        'Apex Defense Systems',    '8481-SLIM',    120,  'C', 'C', 'WO-24001'),
        ('5520K', 'Autonomous Drive Controller',     'Vertex Robotics Inc.',    '5520-CTRL-R2', 500,  'B', 'A', 'WO-23500'),
        ('9102M', 'RF Transceiver Board v3',         'Orbit Communications',    '9102-RF-V3',   300,  'A', 'B', 'WO-24200'),
        ('3347P', 'Pressure Sensor Interface',       'Precision Instruments',   '3347-SENS-B',  750,  'D', 'D', 'WO-23100'),
        ('7721Q', 'Power Management Module',         'NovaTech Electronics',    '7721-PWR-2',   180,  'B', 'C', 'WO-24350'),
        ('4490R', 'Flight Avionics Controller',      'Stellar Aerospace',       '4490-CTRL',    80,   'A', 'A', 'WO-24512'),
        ('2281S', 'Portable Diagnostic Main Board',  'BioScan Medical',         '2281-MAIN',    400,  'C', 'B', 'WO-24600'),
        ('1194T', 'Industrial I/O Expansion Card',   'HydroTech Systems',       '1194-IO',      600,  'D', 'C', 'WO-24710'),
        ('8833U', 'Quantum Processing Unit Board',   'Quantum Dynamics LLC',    '8833-CPU',     50,   'B', 'B', 'WO-24820'),
    ]
    for job, desc, customer, cust_pn, qty, job_rev, cust_rev, wo in jobs:
        run(conn, f"""
            INSERT INTO {SCHEMA}."tblJob"
            (job_number, description, customer, cust_pn, build_qty, job_rev, cust_rev,
             last_rev, wo_number, status, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'Active', 'admin')
            ON CONFLICT (job_number) DO UPDATE SET description = EXCLUDED.description
        """, (job, desc, customer, cust_pn, qty, job_rev, cust_rev, job_rev, wo))
    conn.commit()
    print(f"    → {len(jobs)} jobs added")

def seed_inventory(conn):
    print("  Seeding warehouse inventory…")
    parts = [
        # (item, mpn, dc, qty, loc, msd, po, cost)
        ('Resistor, 10K 0402',         'RC0402FR-0710KL',     '2302', 18500, 'A1-01', '1',  'PO-10042', 0.002),
        ('Resistor, 100R 0402',        'RC0402JR-07100RL',    '2304', 12400, 'A1-02', '1',  'PO-10043', 0.002),
        ('Resistor, 1K 0402',          'RC0402FR-071KL',      '2302', 9800,  'A1-02', '1',  'PO-10071', 0.002),
        ('Resistor, 47R 0603',         'RC0603FR-0747RL',     '2303', 6200,  'A1-03', '1',  'PO-10072', 0.003),
        ('Capacitor, 100nF 0402',      'GRM155R71C104KA88D',  '2301', 24000, 'A1-03', '2A', 'PO-10044', 0.008),
        ('Capacitor, 10uF 0805',       'GRM21BR61A106KE19L',  '2303', 7600,  'A2-01', '2A', 'PO-10045', 0.045),
        ('Capacitor, 1uF 0603',        'GRM188R61A105KA61D',  '2309', 14200, 'A2-01', '2A', 'PO-10060', 0.012),
        ('Capacitor, 22pF 0402',       'GRM1555C1H220JA01D',  '2309', 31000, 'A1-01', '1',  'PO-10065', 0.005),
        ('Capacitor, 4.7uF 0402',      'GRM155R60J475ME47D',  '2310', 8900,  'A2-02', '2A', 'PO-10073', 0.018),
        ('IC, STM32F405RGT6',          'STM32F405RGT6',       '2312', 284,   'B1-01', '3',  'PO-10046', 8.50),
        ('IC, STM32G031K8T6',          'STM32G031K8T6',       '2311', 156,   'B1-01', '3',  'PO-10074', 3.20),
        ('IC, LM317T Regulator',       'LM317T',              '2311', 420,   'B1-02', '1',  'PO-10047', 0.45),
        ('IC, TPS63060DSCR',           'TPS63060DSCR',        '2310', 318,   'B2-01', '3',  'PO-10048', 2.80),
        ('IC, ESP32-WROOM-32E',        'ESP32-WROOM-32E',     '2312', 192,   'B2-01', '3',  'PO-10062', 3.50),
        ('IC, LPC11U68JBD48',          'LPC11U68JBD48',       '2308', 88,    'B1-01', '3',  'PO-10066', 4.10),
        ('IC, MAX3232ECPE+',           'MAX3232ECPE+',        '2311', 210,   'B1-02', '3',  'PO-10075', 1.20),
        ('IC, MCP6002-I/SN',           'MCP6002-I/SN',        '2311', 340,   'B1-02', '3',  'PO-10058', 0.65),
        ('IC, 24LC256-I/SN',           '24LC256-I/SN',        '2310', 175,   'C1-01', '3',  'PO-10059', 0.55),
        ('Inductor, 10uH 2520',        'SRR6028-100Y',        '2309', 2800,  'C1-01', '1',  'PO-10049', 0.18),
        ('Inductor, 4.7uH 0603',       'LQM18FN4R7M00D',     '2310', 1900,  'C1-01', '1',  'PO-10076', 0.22),
        ('LED, Red 0402',              'LTST-C190KRKT',       '2308', 42000, 'C1-02', '1',  'PO-10050', 0.04),
        ('LED, Green 0402',            'LTST-C190KGKT',       '2308', 38000, 'C1-02', '1',  'PO-10051', 0.04),
        ('LED, Blue 0402',             'LTST-C190TBKT',       '2309', 15000, 'C1-02', '1',  'PO-10077', 0.05),
        ('Connector, USB-C',           'USB4105-GF-A',        '2307', 1240,  'D1-01', '2B', 'PO-10052', 1.80),
        ('Connector, 2-pin 2.54mm',    'TSW-102-07-G-S',      '2306', 4800,  'D1-01', '1',  'PO-10053', 0.25),
        ('Connector, JST-SH 4-pin',    'SM04B-SRSS-TB',       '2310', 680,   'D1-01', '2B', 'PO-10078', 0.55),
        ('Crystal, 16MHz',             'ABLS-16.000MHZ-B4-T', '2305', 920,   'A2-02', '2B', 'PO-10054', 0.35),
        ('Crystal, 32.768kHz',         'FC-135R 32.768KHZ',   '2306', 550,   'A2-02', '2B', 'PO-10079', 0.28),
        ('Transistor, BSS138',         'BSS138-7-F',          '2304', 3600,  'A1-01', '1',  'PO-10055', 0.06),
        ('Diode, 1N4148W',             '1N4148W-7-F',         '2303', 8200,  'A1-02', '1',  'PO-10056', 0.03),
        ('MOSFET, SI2302',             'SI2302DS-T1-E3',      '2312', 1800,  'B1-01', '1',  'PO-10057', 0.15),
        ('Fuse, 1A 0603',              'F0603FF01000V100',    '2311', 3200,  'C1-02', '1',  'PO-10063', 0.12),
        ('Button, Tactile 4-pin',      'EVQ-Q2B03W',          '2310', 2100,  'D1-01', '1',  'PO-10064', 0.22),
        ('Ferrite Bead, 600R 0402',    'BLM15AX601SN1D',      '2309', 9500,  'A1-03', '1',  'PO-10080', 0.04),
        ('Voltage Ref, LM4040-2.5',    'LM4040AIM3-2.5/NOPB','2310', 145,   'B1-02', '1',  'PO-10081', 0.85),
    ]

    pcn_start = 100001

    for i, (item, mpn, dc, qty, loc, msd, po, cost) in enumerate(parts):
        pcn = pcn_start + i
        run(conn, f"""
            INSERT INTO {SCHEMA}."tblWhse_Inventory"
            (item, pcn, mpn, dc, onhandqty, mfg_qty, loc_from, loc_to, msd, po, cost)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (item, pcn, mpn, dc, qty, str(qty), 'RECV', loc, msd, po, cost))

        # Add to part number lookup table
        run(conn, f"""
            INSERT INTO {SCHEMA}."tblPN_List" (item, "DESC")
            VALUES (%s, %s) ON CONFLICT (item) DO NOTHING
        """, (item, item))

        # Add transaction record
        run(conn, f"""
            INSERT INTO {SCHEMA}."tblTransaction"
            (trantype, item, pcn, mpn, dc, msd, tranqty, tran_time, loc_from, loc_to, wo, po, userid, reversed)
            VALUES ('STOCK', %s, %s, %s, %s, %s, %s,
                    TO_CHAR(CURRENT_TIMESTAMP - INTERVAL '{random.randint(1, 30)} days', 'MM/DD/YY HH24:MI:SS'),
                    'RECV', %s, 'WO-DEMO', %s, 'admin', FALSE)
        """, (item, pcn, mpn, dc, msd, qty, loc, po))

    conn.commit()
    print(f"    → {len(parts)} inventory items added")

def seed_pcb_inventory(conn):
    print("  Seeding PCB inventory…")
    pcbs = [
        ('6163L-PCB', '6163L', 'Patient Monitor Control Board',  105001, 45, 'B1-01', '2024-01-15'),
        ('8481L-PCB', '8481L', 'Defense Slim Module PCB',        105002, 20, 'B1-02', '2024-02-10'),
        ('5520K-PCB', '5520K', 'Robotics Controller PCB',        105003, 88, 'B2-01', '2024-01-28'),
        ('9102M-PCB', '9102M', 'RF Communications Board',        105004, 62, 'C1-01', '2024-03-05'),
        ('3347P-PCB', '3347P', 'Sensor Interface PCB Rev A',     105005, 175,'C1-02', '2024-02-20'),
    ]
    for pn, job, desc, pcn, qty, loc, date_recv in pcbs:
        run(conn, f"""
            INSERT INTO {SCHEMA}."tblPCB_Inventory"
            (pcb_pn, job, pcb_type, description, pcn, qty, location, date_received, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'In Stock')
        """, (pn, job, pn, desc, pcn, qty, loc, date_recv))
    conn.commit()
    print(f"    → {len(pcbs)} PCB inventory records added")

def seed_activity(conn):
    print("  Seeding activity log…")
    now = datetime.now()
    activities = [
        ('STOCK',   'Stocked 2500 units of Resistor, 10K 0402 at A1-01'),
        ('PICK',    'Picked 50 units of IC, STM32F405RGT6 for WO-23788'),
        ('STOCK',   'Stocked 3200 units of Capacitor, 100nF 0402 at A1-03'),
        ('PCN',     'Generated PCN 100001 for Resistor, 10K 0402'),
        ('RESTOCK', 'Restocked 120 units from Count Area to B1-02'),
        ('STOCK',   'Stocked 200 units of Connector, USB-C at D1-01'),
        ('PICK',    'Picked 25 units of IC, LM317T Regulator for WO-24001'),
        ('PCN',     'Generated PCN 100005 for IC, STM32F405RGT6'),
        ('STOCK',   'Stocked 5000 units of LED, Red 0402 at C1-02'),
        ('BOM',     'BOM loaded for job 6163L — 18 line items'),
        ('STOCK',   'Stocked 35 units of IC, ESP32-WROOM-32E at B2-01'),
        ('PICK',    'Picked 10 units of Crystal, 16MHz for WO-24200'),
    ]
    for idx, (atype, desc) in enumerate(activities):
        created = now - timedelta(hours=idx * 2 + random.randint(0, 60))
        run(conn, f"""
            INSERT INTO {SCHEMA}."tblActivityLog"
            (user_id, username, full_name, action_type, description, created_at, seen)
            VALUES (1, 'admin', 'Admin User', %s, %s, %s, %s)
        """, (atype, desc, created, idx > 5))
    conn.commit()
    print(f"    → {len(activities)} activity records added")

def seed_bom(conn):
    print("  Seeding BOM data…")
    bom_items = [
        # (job, line, aci_pn, ref_des, mpn, man, desc, qty, cost)
        ('6163L', 1, 'ACI-C001', 'C1,C2,C3',    'GRM155R71C104KA88D', 'Murata',  'Capacitor 100nF 0402', 3, 0.008),
        ('6163L', 2, 'ACI-R001', 'R1,R2',       'RC0402FR-0710KL',    'Yageo',   'Resistor 10K 0402',    2, 0.002),
        ('6163L', 3, 'ACI-U001', 'U1',          'STM32F405RGT6',      'STMicro', 'MCU STM32F405',        1, 8.50),
        ('6163L', 4, 'ACI-U002', 'U2',          'TPS63060DSCR',       'TI',      'Buck-Boost Converter', 1, 2.80),
        ('6163L', 5, 'ACI-J001', 'J1',          'USB4105-GF-A',       'GCT',     'USB-C Connector',      1, 1.80),
        ('8481L', 1, 'ACI-C002', 'C1-C5',       'GRM21BR61A106KE19L', 'Murata',  'Capacitor 10uF 0805',  5, 0.045),
        ('8481L', 2, 'ACI-R002', 'R1-R8',       'RC0603FR-0747RL',    'Yageo',   'Resistor 47R 0603',    8, 0.003),
        ('8481L', 3, 'ACI-U003', 'U1',          'LPC11U68JBD48',      'NXP',     'ARM Cortex-M0+ MCU',   1, 4.10),
        ('5520K', 1, 'ACI-U004', 'U1',          'ESP32-WROOM-32E',    'Espressif','WiFi/BT Module',      1, 3.50),
        ('5520K', 2, 'ACI-D001', 'D1-D4',       'LTST-C190KRKT',      'Lite-On', 'LED Red 0402',         4, 0.04),
    ]
    for job, line, aci_pn, ref, mpn, man, desc, qty, cost in bom_items:
        run(conn, f"""
            INSERT INTO {SCHEMA}."tblBOM"
            (job, job_number, line, aci_pn, ref_des, mpn, man, description, "DESC", qty, cost, unit_cost, manufacturer)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (job, job, line, aci_pn, ref, mpn, man, desc, desc, qty, cost, cost, man))
    conn.commit()
    print(f"    → {len(bom_items)} BOM line items added")

def main():
    print("\n KOSH Demo Data Seeder")
    print("=" * 40)
    try:
        conn = connect()
        print(f"  Connected to {DB['host']}:{DB['port']}/{DB['dbname']}")
    except Exception as e:
        print(f"  Connection failed: {e}")
        print(f"  Make sure the database is running and env vars are set.")
        return

    try:
        seed_schema(conn)
        seed_locations(conn)
        seed_jobs(conn)
        seed_inventory(conn)
        seed_pcb_inventory(conn)
        seed_bom(conn)
        seed_activity(conn)

        print("\n  All demo data seeded successfully!")
        print("  Restart the app and refresh the dashboard.")
    except Exception as e:
        conn.rollback()
        print(f"\n  Error during seeding: {e}")
        import traceback; traceback.print_exc()
    finally:
        conn.close()

if __name__ == '__main__':
    main()
