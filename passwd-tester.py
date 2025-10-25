#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Password Strength Checker con interfaz en consola usando rich
Coloca rockyou.txt en la misma carpeta que el script
"""

import os
import re
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import track

console = Console()

TRIES_PER_SECOND = 1_000_000

def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))

def load_wordlist(filename="rockyou.txt"):
    script_dir = get_script_dir()
    path = Path(script_dir) / filename
    if not path.is_file():
        console.print(f"[red]Error:[/] no se encontró la wordlist en: {path}")
        return set()

    console.print(f"[cyan][i]Cargando wordlist desde: {path}[/i][/cyan]")
    passwords = set()
    with open(path, "r", encoding="latin-1", errors="ignore") as f:
        for line in track(f, description="Cargando..."):
            pw = line.strip()
            if pw:
                passwords.add(pw)
    console.print(f"[green][i]Wordlist cargada: {len(passwords)} contraseñas únicas[/i][/green]")
    return passwords

def password_in_wordlist(password, wordlist):
    return password in wordlist

def complexity_score(password):
    score = 0
    reasons = []

    l = len(password)
    if l >= 12:
        score += 3
    elif l >= 8:
        score += 2
    elif l >= 6:
        score += 1
    else:
        reasons.append("Muy corta (<6)")

    if re.search(r"[a-z]", password): score += 1
    else: reasons.append("Sin minúsculas")
    if re.search(r"[A-Z]", password): score += 1
    else: reasons.append("Sin mayúsculas")
    if re.search(r"[0-9]", password): score += 1
    else: reasons.append("Sin números")
    if re.search(r"[^\w\s]", password): score += 1
    else: reasons.append("Sin símbolos")

    if len(set(password)) < 4:
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
    charset = 0
    if re.search(r"[a-z]", password): charset += 26
    if re.search(r"[A-Z]", password): charset += 26
    if re.search(r"[0-9]", password): charset += 10
    if re.search(r"[^\w\s]", password): charset += 32
    if charset == 0: charset = 26
    combinations = charset ** len(password)
    seconds = combinations / TRIES_PER_SECOND
    if seconds < 60: return f"{seconds:.2f} segundos"
    minutes = seconds / 60
    if minutes < 60: return f"{minutes:.2f} minutos"
    hours = minutes / 60
    if hours < 24: return f"{hours:.2f} horas"
    days = hours / 24
    if days < 365: return f"{days:.2f} días"
    years = days / 365
    return f"{years:.2f} años"

def display_result(password, classification, reasons, time_estimate):
    table = Table(title="Resultado de Evaluación de Contraseña", title_style="bold magenta")
    table.add_column("Campo", style="cyan", no_wrap=True)
    table.add_column("Valor", style="yellow")
    
    table.add_row("Contraseña", password)
    
    color_map = {
        "MALÍSIMA": "bold red",
        "MALA": "red",
        "MEDIO BUENA": "orange1",
        "BUENA": "green",
        "EXCELENTE": "bold green"
    }
    
    table.add_row("Clasificación", f"[{color_map.get(classification, 'white')}]{classification}[/{color_map.get(classification, 'white')}]")
    table.add_row("Tiempo estimado crackeo", time_estimate)
    table.add_row("Problemas / advertencias", ", ".join(reasons) if reasons else "Ninguna")
    
    console.print(table)
    console.rule()

def main():
    wordlist = load_wordlist()
    if not wordlist:
        return

    console.print("\n[bold cyan]Bienvenido al Password Tester[/bold cyan]")
    console.print("[green]Escribe 'salir' para terminar la aplicación[/green]\n")

    try:
        while True:
            password = console.input("[bold yellow]Escribe la contraseña a evaluar:[/] ").strip()
            if password.lower() == "salir":
                console.print("[cyan]Saliendo...[/cyan]")
                break
            if not password:
                continue

            in_wordlist = password_in_wordlist(password, wordlist)
            score, reasons = complexity_score(password)
            classification = classify_score(score, in_wordlist)
            time_estimate = estimated_crack_time(password)
            
            display_result(password, classification, reasons, time_estimate)

    except KeyboardInterrupt:
        console.print("\n[cyan]Saliendo...[/cyan]")

if __name__ == "__main__":
    main()
