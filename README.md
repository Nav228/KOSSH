# KOSSH - Inventory Management System

**Version 2.1.0**

KOSSH is a full-featured warehouse and PCB inventory management system. It handles the complete lifecycle of electronic components — from BOM loading and job tracking to stock operations, shortage reporting, and barcode-based PCN management.

## Features

### Inventory Operations
- **Stock Parts** - Add inventory to warehouse with location, date code, and MSD tracking
- **Pick Parts** - Remove inventory with PCN scanning and transaction logging
- **Restock Parts** - Move parts from Count Area back to warehouse
- **Part Number Change** - Track and manage part number changes across inventory

### Job & BOM Management
- **BOM Loader** - Upload Excel BOMs with automatic column mapping and validation
- **Job Management** - Create, view, and manage jobs with BOM detail, revisions, and build quantities
- **Shortage Reports** - Generate, view, and export shortage reports comparing BOM requirements vs. on-hand inventory

### PCN & Part Numbers
- **Generate PCN** - Create unique PCN barcodes for inventory items with assignment tracking
- **Part Number Creator** - Create consecutive part numbers for non-BOM parts to place in stock
- **PCN History** - Full history of PCN generation and assignments
- **PO History** - Purchase order history tracking

### Inventory Browsers
- **PCB Inventory** - Browse and search PCB inventory with filtering
- **Warehouse Inventory** - View warehouse stock with item details, locations, and expiration status

### Reporting & Admin
- **Reports** - Statistics dashboard with inventory valuation and trends
- **Admin Notifications** - Activity log for all user actions (stock, pick, restock, PCN, login/logout)
- **User Management** - Role-based access control (Super User, Manager, User, Operator, ITAR)
- **Location Management** - Manage warehouse location codes
- **Print Labels** - Generate and print labels with ZPL barcode support

### Platform
- **SSO** - Optional single sign-on integration via JWT
- **Dark Mode** - Toggle between light and dark themes
- **Responsive Design** - Optimized for desktop, tablet, and mobile devices
- **Barcode Scanning** - Scan PCN barcodes from any page to view item details

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.11, Flask 2.3 |
| Database | PostgreSQL 15 |
| Frontend | Jinja2, Bootstrap 5, JavaScript |
| Excel Parsing | SheetJS (client-side), openpyxl (server-side) |
| Auth | Session-based + optional SSO (JWT) with bcrypt |
| Deployment | Docker Compose, Nginx, Gunicorn |

## Getting Started

### Requirements
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Run with Docker

```bash
# Clone the repo
git clone https://github.com/Nav228/KOSSH.git
cd KOSSH

# Set up environment
cp .env.example .env
# Edit .env and set a strong SECRET_KEY

# Start all services
docker compose up --build

# App available at:
#   http://localhost:5002
```

### Environment Variables

Copy `.env.example` to `.env` and configure:

| Variable | Description | Default |
|---|---|---|
| `POSTGRES_HOST` | Database host | `kosh-database` |
| `POSTGRES_DB` | Database name | `kosh` |
| `POSTGRES_USER` | Database user | `stockpick_user` |
| `POSTGRES_PASSWORD` | Database password | *(set this)* |
| `SECRET_KEY` | Flask session secret | *(set this)* |
| `SSO_SECRET_KEY` | JWT secret for SSO (optional) | — |

### Database Schema

KOSSH uses a `pcb_inventory` schema in PostgreSQL with tables including:

- `tblWhse_Inventory` - Warehouse inventory
- `tblBOM` / `tblJob` - Bills of Materials and Jobs
- `tblTransaction` - Audit trail
- `tblPCB_Inventory` - PCB inventory
- `tblShortageReport` - Shortage reports
- `tblUser` - User accounts and roles
- `tblActivityLog` - Admin notification feed

## Project Structure

```
KOSSH/
├── app.py                  # Main Flask application
├── expiration_manager.py   # DC/MSD expiration logic
├── templates/              # Jinja2 HTML templates
├── static/                 # CSS, SVG assets
├── Dockerfile              # Docker image
├── docker-compose.yml      # All services (app + postgres + nginx)
├── nginx.conf              # Nginx reverse proxy config
├── requirements.txt        # Python dependencies
└── .env.example            # Environment variable template
```

## Author

Developed by **Kanav Sharma**

## License

MIT License
