import os
import subprocess
import sys
import shutil

# ========= CONFIGURATION =========
CODEQL_ZIP_URL = "https://github.com/github/codeql-cli-binaries/releases/latest/download/codeql.zip"
INSTALL_DIR = "./tools"
CODEQL_DB_PATH = "./codeql-db"

# ========= BANNIÈRE =========
def print_banner():
    print(r"""
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🟦🟦🟦⬛⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🟦🟦🟦⬛⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬛🟦🟦⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🟦🟦🟦⬛⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬛🟦🟦🟦🟦⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛🟦🟦🟦⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬛🟦🟦🟦🟦🟦⬛⬛⬛⬜⬜⬜⬜⬜⬜⬛⬛🟦🟦🟦🟦🟦🟦⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬛🟦🟦🟦🟦🟦🟦🟦🟦⬛⬜⬜⬜⬜⬜⬛🟦🟦🟦🟦🟦🟦🟦⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬛🟦🟦⬛⬛🟦⬛🟦⬛🟦⬛⬛⬛⬛🟦🟦⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🟦⬛🟦⬛🟦🟦⬛🟦🟦🟦🟦🟦⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛🟦⬛🟦🟦⬛⬛⬛🟦🟦🟦🟦🟦⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛🟦🟦⬛🟦🟦⬛🟦🟦🟦🟦⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛🟦⬛🟦🟦⬛🟦🟦🟦🟦⬛🟦🟦⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛🟦🟦⬛🟦🟦🟦🟦🟦🟦🟦⬛⬛⬜⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛🌫️🟦🟦⬛🟦🟦🟦🟦🟦🟦🟦🟦⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🌫️🌫️🟦🟥🌫️🟦🟦⬛⬛🟦🟦🟦🟦🟦⬛⬛🟦🟦⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🌫️🌫️🟦🌫️🟦🟦⬛⬜⬜⬛🟦🟦🟦🟦🟦🟦🟦🟦⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🌫️⬛⬛⬛⬛⬛⬜⬜⬜⬜⬛⬛🟦🟦🟦🟦⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛🟦🟦🟦🟦🟦🟦⬛⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜

                      SArSTicuno - SAST Scanner
""")

# ========= OUTILS =========
def is_command_available(cmd):
    return shutil.which(cmd) is not None

def install_semgrep():
    if is_command_available("semgrep"):
        print("[✓] Semgrep est déjà installé.")
    else:
        print("[*] Installation de Semgrep via pip...")
        subprocess.run([sys.executable, "-m", "pip", "install", "semgrep"], check=True)

def download_codeql():
    if get_codeql_cmd():
        print("[✓] CodeQL est déjà installé.")
        return
    print("[*] Téléchargement de CodeQL...")
    os.makedirs(INSTALL_DIR, exist_ok=True)
    zip_path = os.path.join(INSTALL_DIR, "codeql.zip")
    subprocess.run(["curl", "-L", "-o", zip_path, CODEQL_ZIP_URL], check=True)
    subprocess.run(["unzip", "-o", zip_path, "-d", INSTALL_DIR], check=True)
    os.remove(zip_path)

def get_codeql_cmd():
    for root, _, files in os.walk(INSTALL_DIR):
        if "codeql" in files:
            return os.path.join(root, "codeql")
    return None

# ========= AIDE & LOGIN =========
def show_help(tool):
    print_banner()
    print(f"\n--- Aide pour {tool} ---\n")
    if tool == "semgrep":
        subprocess.run(["semgrep", "--help"])
    elif tool == "codeql":
        codeql_path = get_codeql_cmd()
        if codeql_path:
            subprocess.run([codeql_path, "help"])
        else:
            print("❌ CodeQL non trouvé.")

def semgrep_login():
    print("[*] Connexion à semgrep.dev via navigateur...")
    subprocess.run(["semgrep", "login"])

# ========= SCANS =========
def run_semgrep(target_dir, output_dir):
    print("[*] Lancement de Semgrep...")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "semgrep_results.json")
    cmd = ["semgrep", "scan", "--config=auto", target_dir, "--output", output_file]
    subprocess.run(cmd)
    print(f"[✓] Résultats Semgrep exportés dans {output_file}")

def run_codeql(target_dir, output_dir, export_format):
    print("[*] Lancement de CodeQL...")
    codeql_path = get_codeql_cmd()
    if not codeql_path:
        print("❌ CodeQL introuvable.")
        return

    language = "python"  # TODO: détecter dynamiquement si nécessaire



    if os.path.exists(CODEQL_DB_PATH):
        shutil.rmtree(CODEQL_DB_PATH)

    subprocess.run([
        codeql_path, "database", "create", CODEQL_DB_PATH,
        f"--language={language}", "--source-root", target_dir
    ])

    subprocess.run([codeql_path, "database", "finalize", CODEQL_DB_PATH])

    os.makedirs(output_dir, exist_ok=True)

    valid_formats = {
        "sarif": "sarif-latest",
        "json": "sarif-latest",
        "csv": "csv",
        "sarifv2": "sarifv2",
    }
    if export_format not in valid_formats:
        print("❌ Format non supporté par CodeQL.")
        return
    codeql_format = valid_formats[export_format]

    output_file = os.path.join(output_dir, f"codeql_results.{export_format}")
    subprocess.run([
        codeql_path, "database", "analyze", CODEQL_DB_PATH,
        "--format", codeql_format,
        "--output", output_file
    ])
    print(f"[✓] Résultats CodeQL exportés dans {output_file}")

def run_both_scans(target_dir, output_dir, export_format):
    run_semgrep(target_dir, output_dir)
    run_codeql(target_dir, output_dir, export_format)

# ========= MENU =========
def main():
    print_banner()
    install_semgrep()
    download_codeql()

    while True:
        print("\n--- MENU ---")
        print("0. Se connecter à Semgrep.dev")
        print("1. Aide Semgrep")
        print("2. Aide CodeQL")
        print("3. Scanner avec Semgrep")
        print("4. Scanner avec CodeQL")
        print("5. Scanner avec les deux")
        print("6. Quitter")
        choice = input(">> ")

        if choice == "0":
            semgrep_login()
        elif choice == "1":
            show_help("semgrep")
        elif choice == "2":
            show_help("codeql")
        elif choice in ["3", "4", "5"]:
            target_dir = input("Chemin du dossier à analyser : ").strip()
            output_dir = input("Dossier pour les résultats : ").strip()
            scan_path = os.path.join("scan_result", output_dir)

            if not os.path.isdir(target_dir):
                print("❌ Dossier invalide.")
                continue

            export_format = None
            if choice in ["4", "5"]:
                print("Formats disponibles pour CodeQL : sarif, sarifv2, json, csv")
                export_format = input("Choisir le format d'export : ").strip().lower()

            if choice == "3":
                run_semgrep(target_dir, scan_path)
            elif choice == "4":
                run_codeql(target_dir, scan_path, export_format)
            else:
                run_both_scans(target_dir, scan_path, export_format)
        elif choice == "6":
            print("👋 Fin de SArSTicuno. À bientôt !")
            break
        else:
            print("❌ Choix invalide.")

if __name__ == "__main__":
    main()