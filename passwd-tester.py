#!/usr/bin/env python3
# psswd-tester.py
# Uso: python3 psswd-tester.py
#Made By Jacsaw

import os
import re
import time

WORDLIST_FILE = "rockyou.txt"
# Velocidad estimada de pruebas por segundo (depende de hardware, esto es aproximado)
# Por ejemplo, 1 millón de contraseñas por segundo
TRIES_PER_SECOND = 1_000_000  

def load_wordlist():
    if not os.path.isfile(WORDLIST_FILE):
        print(f"Error: no se encontró la wordlist {WORDLIST_FILE}")
        return set()
    print("[i] Cargando wordlist, esto puede tardar unos segundos...")
    with open(WORDLIST_FILE, "r", encoding="latin-1", errors="ignore") as f:
        passwords = set(line.strip() for line in f if line.strip())
    print(f"[i] Wordlist cargada: {len(passwords)} contraseñas únicas")
    return passwords

def password_in_wordlist(password, wordlist):
    return password in wordlist

def complexity_score(password):
    score = 0
    reasons = []

    # Longitud
    l = len(password)
    if l >= 12:
        score += 3
    elif l >= 8:
        score += 2
    elif l >= 6:
        score += 1
    else:
        reasons.append("Muy corta (<6)")

    # Letras minúsculas
    if re.search(r"[a-z]", password):
        score += 1
    else:
        reasons.append("Sin minúsculas")

    # Letras mayúsculas
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        reasons.append("Sin mayúsculas")

    # Números
    if re.search(r"[0-9]", password):
        score += 1
    else:
        reasons.append("Sin números")

    # Símbolos
    if re.search(r"[^\w\s]", password):
        score += 1
    else:
        reasons.append("Sin símbolos")

    # Entropía básica (caracteres únicos)
    unique_chars = len(set(password))
    if unique_chars < 4:
        reasons.append("Pocos caracteres únicos")

    return score, reasons

def classify_score(score, in_wordlist):
    if in_wordlist:
        return "MALÍSIMA"
    elif score <= 3:
        return "MALA"
    elif score <= 5:
        return "MEDIO BUENA"
    elif score <= 7:
        return "BUENA"
    else:
        return "EXCELENTE"

def estimated_crack_time(password):
    # Aproximación: tries per second * número total de combinaciones
    charset = 0
    if re.search(r"[a-z]", password): charset += 26
    if re.search(r"[A-Z]", password): charset += 26
    if re.search(r"[0-9]", password): charset += 10
    if re.search(r"[^\w\s]", password): charset += 32  # símbolos comunes
    if charset == 0:
        charset = 26  # fallback
    combinations = charset ** len(password)
    seconds = combinations / TRIES_PER_SECOND
    # convertir a unidades legibles
    if seconds < 60:
        return f"{seconds:.2f} segundos"
    minutes = seconds / 60
    if minutes < 60:
        return f"{minutes:.2f} minutos"
    hours = minutes / 60
    if hours < 24:
        return f"{hours:.2f} horas"
    days = hours / 24
    if days < 365:
        return f"{days:.2f} días"
    years = days / 365
    return f"{years:.2f} años"

def main():
    wordlist = load_wordlist()
    if not wordlist:
        return

    while True:
        password = input("\nEscribe la contraseña a evaluar (o 'salir' para terminar): ").strip()
        if password.lower() == "salir":
            break
        if not password:
            continue

        in_wordlist = password_in_wordlist(password, wordlist)
        score, reasons = complexity_score(password)
        classification = classify_score(score, in_wordlist)
        time_estimate = estimated_crack_time(password)

        print("\n===== RESULTADO =====")
        print(f"Contraseña: {password}")
        print(f"Clasificación: {classification}")
        print(f"Razones / advertencias: {', '.join(reasons) if reasons else 'Ninguna'}")
        print(f"Tiempo estimado de crackeo (fuerza bruta): {time_estimate}")
        print("=====================\n")

if __name__ == "__main__":
    main()
