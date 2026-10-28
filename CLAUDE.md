# Správa repozitáře rodokmen-skill

Vydání nové verze: zvedni číslo ve třech místech najednou – `.claude-plugin/plugin.json` (`version`),
`skills/rodokmen/VERZE` (podle něj asistent u uživatele pozná, že má aktualizovat projekt) a README („Aktuální verze“).
Mění-li se formát mezi `tools/` a `template/web/`, otestuj i aktualizaci projektu založeného předchozí verzí
(`novy_projekt.py` na stejnou složku, `npm install`, `npm run data`, `npm run build`).
