# KOSSH — Inventory at Speed ⚡

**Version 2.1.0** | Production-Ready | Full-Stack Open Source

> Enterprise-grade PCB and warehouse inventory management system built with modern web technologies. Designed for electronics manufacturers who need **real-time inventory visibility, intelligent job tracking, and automated shortage detection**.

🎨 **Beautiful Modern UI** — Premium glassmorphic design, particle animations, professional landing page, and smooth login experience.

## ✨ What Makes KOSSH Different

- **Purpose-Built for Electronics** — Handles MSD tracking, date codes, and PCN barcode management out of the box
- **Real-Time Inventory** — Instant stock updates with transaction logging for complete auditability
- **Shortage Intelligence** — Automatically compare BOM requirements against on-hand inventory and generate reports
- **Barcode-Driven Workflow** — PCN scanning from any page for seamless pick/stock operations
- **Role-Based Access** — 5 permission levels (Super User, Manager, User, Operator, ITAR) for enterprise deployments
- **Modern Premium UI** — Beautiful, responsive glassmorphic design with particle animations, professional landing page, and smooth login flow
- **Devanagari Branding** — Sanskrit character (क) logo with multi-color gradient aesthetic (red → purple → cyan)

## 🚀 Core Features

### Inventory Operations
- **Stock Parts** — Add components with location, date code, and MSD level tracking
- **Pick Parts** — Remove inventory via PCN scanning with automatic transaction logging
- **Restock Flow** — Move parts from Count Area back to warehouse with audit trail
- **Part Number Management** — Create and track part number changes across inventory

### Job & BOM Management
- **Smart BOM Loader** — Upload Excel files with automatic column detection and validation
- **Job Tracking** — Create jobs, manage revisions, and track build quantities in real-time
- **Shortage Reports** — Instant BOM-to-inventory analysis with export capabilities
- **Detailed Job Views** — See complete BOM details, component requirements, and shortages at a glance

### Intelligence & Reporting
- **Dashboard Analytics** — Inventory valuation, stock trends, and real-time statistics
- **PCN Generation** — Automated barcode creation with assignment tracking
- **Activity Logging** — Complete audit trail for stock, picks, restocks, and user actions
- **Warehouse Browser** — Filter and search inventory with expiration status visibility

### Enterprise Features
- **SSO Integration** — Optional JWT-based single sign-on for enterprise environments
- **User Management** — Role-based access control with permission inheritance
- **Location Management** — Configurable warehouse location codes
- **Label Generation** — ZPL barcode labels with print-ready formatting
- **Public Signup** — Open user registration with admin activity tracking
- **Login Notifications** — Real-time admin notifications with IP address tracking for security monitoring
- **Activity Logging** — Complete audit trail of all user logins, signups, and actions

## 🛠️ Tech Stack

| Layer | Technologies |
|-------|---------------|
| **Backend** | Python 3.11 • Flask 2.3 • Gunicorn |
| **Database** | PostgreSQL 15 • SQLAlchemy ORM |
| **Frontend** | Jinja2 • JavaScript • CSS3 (Glassmorphism) |
| **File Handling** | SheetJS (client) • openpyxl (server) |
| **Security** | Session-based auth • JWT SSO • bcrypt hashing |
| **Deployment** | Docker • Docker Compose • Nginx reverse proxy |
| **Barcode Support** | ZPL label generation • PCN scanning |

## 🚀 Quick Start

### Local Development (Docker)

```bash
git clone https://github.com/Nav228/KOSSH.git
cd KOSSH

# Copy and configure environment
cp .env.example .env
# Edit .env to set POSTGRES_PASSWORD and SECRET_KEY

# Start all services (postgres, flask, nginx)
docker compose up --build

# In another terminal, run database migrations
docker exec kosh-database psql -U stockpick_user -d kosh -f /tmp/migrations.sql

# Open browser to http://localhost:5002
# Sign up or log in at http://localhost:5002/login
```

**Requirements:** [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Database Migrations

After first startup, run migrations to set up IP tracking and notification features:

```bash
# Copy migrations into the container
docker cp migrations/. kosh-database:/tmp/

# Run migrations
docker exec kosh-database psql -U stockpick_user -d kosh -c "
CREATE TABLE IF NOT EXISTS pcb_inventory.\"tblLoginNotifications\" (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    username VARCHAR(255),
    full_name VARCHAR(255),
    login_time TIMESTAMP WITH TIME ZONE,
    ip_address VARCHAR(45),
    event_type VARCHAR(50) DEFAULT 'LOGIN',
    seen BOOLEAN DEFAULT FALSE
);

ALTER TABLE pcb_inventory.\"tblLoginNotifications\"
ADD COLUMN IF NOT EXISTS ip_address VARCHAR(45);

ALTER TABLE pcb_inventory.\"tblLoginNotifications\"
ADD COLUMN IF NOT EXISTS event_type VARCHAR(50) DEFAULT 'LOGIN';
"
```

### Environment Configuration

Copy `.env.example` to `.env`:

| Variable | Purpose | Example |
|----------|---------|---------|
| `POSTGRES_PASSWORD` | Database password | `your-secure-password` |
| `SECRET_KEY` | Flask session secret | `openssl rand -hex 32` |
| `FLASK_ENV` | Environment mode | `production` or `development` |
| `SSO_SECRET_KEY` | JWT secret (optional) | — |

### Cloud Deployment

**Ready for production on:**
- Docker Container Services (Koyeb, Railway, Render)
- Serverless (Vercel with Neon PostgreSQL)
- Kubernetes (via Docker image)

See [Deployment Guide](./DEPLOYMENT.md) for detailed instructions.

## 📊 Database Schema

KOSSH uses PostgreSQL with a `pcb_inventory` schema:

```
tblWhse_Inventory    → Warehouse stock ledger
tblBOM / tblJob      → Bill of Materials and job definitions
tblTransaction       → Complete audit trail for all operations
tblPCB_Inventory     → PCB component catalog
tblShortageReport    → Generated shortage analysis
tblUser              → User accounts with role-based permissions
tblActivityLog       → Admin activity stream
```

## 📁 Project Structure

```
KOSSH/
├── app.py                    # Flask app entry point
├── expiration_manager.py     # MSD/date code tracking
├── api/
│   └── index.py             # Vercel serverless entry
├── templates/               # Jinja2 HTML (landing, login, dashboard)
├── static/                  # CSS, JS, SVG assets
├── Dockerfile               # Container image
├── docker-compose.yml       # Local dev stack
├── nginx.conf               # Reverse proxy config
├── requirements.txt         # Python dependencies
└── .env.example             # Configuration template
```

## 💡 Use Cases

- **Electronics Manufacturers** — Track PCBs, components, and job inventory
- **Warehouse Operations** — Real-time stock visibility with MSD/date code compliance
- **Supply Chain Teams** — Automated shortage detection and BOM-to-inventory comparison
- **Quality Assurance** — Complete audit trail for regulatory compliance

## 🔗 Links & Demo

- **GitHub:** [Nav228/KOSSH](https://github.com/Nav228/KOSSH)
- **Live Demo:** [kossh.vercel.app](https://kossh.vercel.app) — See the landing page and modern UI in action
- **Login Page:** [kossh.vercel.app/login](https://kossh.vercel.app/login)
- **Author:** [Kanav Sharma](https://linkedin.com/in/kanav-sharma) | [GitHub](https://github.com/Nav228)

## 📄 License

MIT License — Free for commercial and personal use

---

**Building inventory management software? Star this repo and join the community of users managing thousands of parts in real-time! 🎯**
