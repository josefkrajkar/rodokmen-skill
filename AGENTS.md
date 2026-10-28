# Správa repozitáře rodokmen-skill

Přečti `CLAUDE.md` ve stejné složce; pravidla vydávání a aktualizace projektů platí pro oba klienty.

- Udržuj jeden společný skill pro Claude Code i Codex. Projektové instrukce jsou v `skills/rodokmen/template/AGENTS.md`; šablona `CLAUDE.md` na ně odkazuje.
- Při změně generátoru spusť `python3 -m unittest discover -s tests -v`. Existující rodinná data ani uživatelské instrukce se nesmějí přepsat.
- Náhled a build ověřuj na ukázkovém projektu v dočasné složce. Testovací data nepatří do tohoto repozitáře a ověření nevyžaduje zveřejnění webu.
